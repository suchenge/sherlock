import os
import re
import pymysql
import pyperclip3 as pc

mysql_connect = {
    "host": '192.168.100.212',
    "port": 3306,
    "user": 'root',
    "passwd": 'tiger_scm',
    "db": 'ironman_scmcloud'
}

database_connect = pymysql.connect(
    host=mysql_connect["host"],
    user=mysql_connect["user"],
    passwd=mysql_connect["passwd"],
    port=mysql_connect["port"],
    db=mysql_connect['db'])

def batch_edit_field(file_path):
    result = ''
    lines = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        columns = line.split(',')
        colunmObj = {}
        colunmObj["FiledId"] = columns[0]
        colunmObj["FiledName"] = columns[1]
        colunmObj["ModelName"] = columns[2]
        colunmObj["ControlType"] = columns[3]
        colunmObj["ReferenceCode"] = columns[4]

        result += insert_batch_edit_field_sql(colunmObj)

    pc.copy(result)

def insert_batch_edit_field_sql(columns):
    return f'''
INSERT INTO batch_edit_field (FIELD_ID, FIELD_NAME, MODEL_NAME, CONTROL_TYPE, REFERENCE_CODE, IS_ACTIVE)
SELECT '{columns["FiledId"]}', '{columns["FiledName"]}', '{columns["ModelName"]}', '{columns["ControlType"]}', '{columns["ReferenceCode"]}', 1
FROM DUAL
WHERE NOT EXISTS(SELECT 1 FROM batch_edit_field WHERE FIELD_ID = '{columns["FiledId"]}' AND MODEL_NAME = '{columns["ModelName"]}');
''' 

batch_edit_field(r'E:\Download\batcheditfield.txt')

def build_in_param(keys):
    message_array = ["'%s'" % x for x in keys]
    message_param = ','.join(message_array)
    return message_param

def get_database_message_key(sql):
    database_cursor = database_connect.cursor()
    database_cursor.execute(sql)
    database_result = database_cursor.fetchall()

    if len(database_result) <= 0:
        return {}

    result = {}
    for row in database_result:
        result[row[1]] = row[0]

    return result

def find_resource(keys):
    result = []
    in_keys = build_in_param(keys)
    sql = "SELECT view_text, resource_key FROM sys_resource sr WHERE sr.resource_key IN (%s) AND sr.language_type = 'zh-cn';" % in_keys
    resource_result = get_database_message_key(sql)

    for message_info in resource_result:
        key_info = {}
        key_info["key"] = message_info
        key_info["text"] = resource_result[message_info]
        result.append(key_info)
    
    return result

def extract_key(content):
    pattern = re.compile(r'/// ([^<].*)');
    return re.findall(pattern, content)

def appendComment(file_path):
    content = None
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    keys = extract_key(content)
    resources = find_resource(keys)
    for resource in resources:
        content = content.replace('/// %s' % resource["key"], '/// %s' % resource["text"])

    pc.copy(content)
    

appendComment(r'D:\quantum-scm\power-scm\scm.configration\SCM.Configration\SCM.Configration.Service\Modules\Vendor\Response\VendorQueryResponse.cs')

def controlTypeToPrivateCode():
    control_type = '''
Label|标签,
Text|文本,
LongText|长文本,
Number|数字,
NumberWithUnit|单位,
Decimal|小数,
Time|时间,
TimePicker|时间输入框,
DateTime|日期时间,
Checkbox|复选,
Dropdown|下拉菜单,
MultiDropdown|多选菜单,
MuitSelect|快速多选,
QuickSelect|快速选择,
StatusTimeline|流程图,
Address|地址
'''
    sql = '';
    control_types = control_type.strip().split(',')
    for index in range(len(control_types)):
        type_info = control_types[index].strip().split('|')
        sql += f'''INSERT INTO privatesyscode (CodeType, CodeID, CodeName, CodeNameEN, TTID, CreatedBy, CreatedDate, UpdatedBy, UpdatedDate, IS_ACTIVE, SORT_NO) 
SELECT 'ControlType','{type_info[0]}','{type_info[1]}','{type_info[0]}','PUBLIC', 'System', NOW(), 'System', NOW(), 'Y', NULL 
FROM DUAL
WHERE NOT EXISTS(SELECT 1 FROM privatesyscode WHERE CodeType = 'ControlType' AND CodeID = '{type_info[0]}');'''
        sql += '\r\n\r\n'
    pc.copy(sql)

controlTypeToPrivateCode()

def create_event_receiver():
    sql = '';
    for index in range(20):
        line = index + 1;
        sql += f'''INSERT INTO reg_event_receiver (`TYPE_FULL_NAME`,`PROPERTY_NAME`,`PROPERTY_TYPE`,`CUSTOM_TYPE`,`IS_USER`,`IS_EMAIL`,`IS_MOBILE`,`REMARK`,`CREATED_DATE`)
SELECT 'SCM.Message.DTO.OMS.Default.PurchaseOrderEventDTO,SCM.Contract.Message','VendorUdf{line}','EMAIL',NULL,'N','Y','N','自定义{line}',NOW() FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM reg_event_receiver WHERE TYPE_FULL_NAME='SCM.Message.DTO.OMS.Default.PurchaseOrderEventDTO,SCM.Contract.Message' AND PROPERTY_NAME='VendorUdf{line}');'''
        sql += '\n\r'
        pc.copy(sql)


create_event_receiver();



def createMap(modelName, fieldName, length):
    sql = '';
    for index in range(length):
        line = index + 1;
        sortId = line * 10;
        sql += f'''INSERT INTO edit_form_template
(SYS_ID, MODEL_NAME, FIELD_NAME, SORT_ID, CONTROL_TYPE, GROUP_NAME, IS_HIDDEN, 
CAN_HIDDEN, IS_REQUIRED, READ_ONLY, EDIT_READ_ONLY, DEFAULT_VALUE, QUICK_SELECT_COLUMN, QUICK_SELECT_COMPLATE, 
QUICK_SELECT_MODEL, QUICK_SELECT_IS_MATCH, QUICK_SELECT_PAGE_API, QUICK_SELECT_TEXT_API, CHECKED_VALUE, REFER_COLUMN_NAME, DROPDOWN_ALLOW_EMPTY, 
CONVERT_DATA, DROPDOWN_FORMAT, VALIDATE_RULE, MAX_LENGTH, NUMBER_MAX, NUMBER_MIN, IS_DIGITS, 
DECIMAL_DIGITS, PROVINCE_COLUMN_NAME, CITY_COLUMN_NAME, COUNTY_COLUMN_NAME, DATE_FORMAT, DATE_DEFAULT_TIME,
CREATED_BY, CREATED_DATE, UPDATED_BY, UPDATED_DATE, IS_CONVERTIBLE)
SELECT 'OMS', 'CMST{modelName}', '{fieldName}{line}', {sortId}, 'Text', 'General', 0,
		1, 0, 0, 0, '', '', '',
		'', 0, '', '', '', '', 0, 
		'', '', '', 100, 0.000000, 0.000000, 0,
		0, '', '', '', '', '', 
		'DBA', NOW(), 'DBA', NOW(), NULL
FROM DUAL 
WHERE NOT EXISTS(SELECT 1 FROM edit_form_template WHERE SYS_ID = 'OMS' AND MODEL_NAME = 'CMST{modelName}' AND FIELD_NAME = '{fieldName}{line}');'''
        sql += '\n\r'
    pc.copy(sql)
    
createMap('ShippingDetailUdf', 'OSdUdf', 30);

# 集合匹配
tmpList = [
            {"path": "path", "status": "done", "id": 1},
            {"path": "path", "status": "error", "id": 2},
            {"path": "path", "status": "done", "id": 3},
            {"path": "path", "status": "downloading", "id": 4}
]

print(all([item["status"] == "done" for item in tmpList]))
print(any([item["status"] == "downloading" for item in tmpList]))


tmp = list(filter(lambda item: item["status"] == "error", tmpList))
print(tmp)

# 字符串模版

tmp1 = '{}, {:.4f} and {}'.format('One', 2, 'Three')
print(tmp1)

tmp1 = '{0}, {1:.2f} and {1}, {2}'.format('One', 2, 'Three')
print(tmp1)

from itertools import count
from math import pi

tmp1 = '{name} is approximately {value:.2f}'.format(name='数学符号', value=pi)
print(tmp1)

# 迭代索引：值对
for index, tmp in enumerate(tmp1):
    print('{index}:{value}'.format(index=index, value=tmp))


# 以class方式定义的装饰器
class DecoratorAsClass(object):
    def __init__(self, func):
        self.function = func

    def __call__(self, *args, **kwargs):
        result = self.function(*args, **kwargs)
        return '{0}, Hello, {1}'.format('DecoratorAsClass', result)


@DecoratorAsClass
def show_name(name):
    return 'My name is {name}'.format(name=name)


print(show_name('九九'))


# 带参数的以class方式定义的装饰器
class DecoratorAsClassByParameters(object):
    def __init__(self, power_name, power_type):
        self.__power_name__ = power_name
        self.__power_type__ = power_type

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            return ','.join(
                ['DecoratorAsClassByParameters', self.__power_name__, self.__power_type__, func(*args, **kwargs)])

        return wrapper


@DecoratorAsClassByParameters('99', 'Admin')
def show_name(name):
    return 'My name is {name}'.format(name=name)


print(show_name('九九'))


# 带参数的装饰器
def decorator_func(power_name):
    def __decorator_wrapper__(func):
        def __wrapper__(*args, **kwargs):
            return ','.join([power_name, 'Hello', func(*args, **kwargs)])

        return __wrapper__

    return __decorator_wrapper__


@decorator_func('你好')
def show_name(your_name):
    return 'My name is {name}'.format(name=your_name)


print(show_name('九九'))


# 自定义赋值验证装饰器
class Verify(object):
    def __init__(self, length, type) -> None:
        self.__length__ = length
        self.__type__ = type

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            print('调用装饰器Verify')
            value = args[1]

            if not isinstance(value, self.__type__):
                raise AttributeError('Type not is' + str(self.__type__))

            if len(value) > int(self.__length__):
                raise AttributeError('Length > ' + self.__length__)

            func(*args, **kwargs)

        return wrapper


class Person(object):
    def __init__(self) -> None:
        self.__first_name__, self.__last_name__ = None, None

    '''
    def __setattr__(self, attribute_name: str, value: Any) -> None:
        print('调用setattr赋值给%s' % attribute_name)
        if attribute_name in self.__dict__:
            self.__dict__[attribute_name] = value

    def __getattr__(self, attribute_name) -> Any:
        print('调用getattr获取%s的值' % attribute_name)
        return self.__dict__[attribute_name]
    '''

    @property
    def first_name(self):
        return self.__first_name__

    @first_name.setter
    @Verify('10', str)
    def first_name(self, value):
        self.__first_name__ = value

    @property
    def last_name(self):
        return self.__last_name__

    @last_name.setter
    def last_name(self, value):
        self.__last_name__ = value


p = Person()
p.first_name = 'vito'
print('first_name:' + p.first_name)


# 上下文管理器 -with语句
class Release(object):
    def __init__(self, thread_count):
        print('init')
        self.__thread_count__ = thread_count

    def start(self):
        print('start')

    def __enter__(self):
        print('enter')
        # __enter__方法必须有返回值，或返回self
        return self

    def __exit__(self, exc_type, exc_value, trace):
        print('exit')


with Release(5) as release:
    release.start()

# 异步变成，async和await
import time
import asyncio


async def hello(index):
    await asyncio.sleep(index)
    print('index:%s, %s' % (index, time.time()))


loop = asyncio.get_event_loop()
tasks = [hello(i) for i in range(5)]
loop.run_until_complete(asyncio.wait(tasks))


# 多重继承
class BaseClass(object):
    def __init__(self):
        pass

    def show(self):
        print('BaseClass')


class ClassA(BaseClass):
    def show(self):
        super().show()
        print('ClassA')


class ClassB(BaseClass):
    def show(self):
        super().show()
        print('ClassB')


class ClassC(ClassA, ClassB):
    def show(self):
        super().show()
        # super(ClassB, self).show()
        print('ClassC')


ClassC().show()

# 集合的交集、并集、差集
# 并集 union
# 交集 intersection
# 差集 difference
list_1 = {'a', 'b', 'c', 'd'}
list_2 = {'a', 'c', 'e', 'f'}

# 并集 union
union_list = list(list_1.union(list_2))
union_list.sort()
print(union_list)

# ['a', 'b', 'c', 'd', 'e', 'f']

# 交集 intersection
intersection_list = list_1.intersection(list_2)
intersection_list = sorted(intersection_list)
print(intersection_list)
# ['a', 'c']


# 差集 difference
difference_list = list_1.difference(list_2)
print(sorted(difference_list))
# ['b', 'd']

# 格式化输出
orders = [('feeder', 8.2, 2), ('diaper', 0.50, 50), ('cushion', 0.58, 20)]

for item, price, quantity in orders:
    # 字体的关系，中文对其有影响
    # {0:10s},      s表示参数为字符串，10表示输出长度为10位，字符串自动用空格补齐
    # {3: ^5d},     d表示参数为整数, 5表示输出长度为5位, ^表示居中对齐，:后有空格表示长度用空格补齐（数值型默认用0补齐）
    # {1: <10.2f}   f表示参数位浮点型，10表示输出长度位10位，.2表示保留小数点后两位, <表示居左对齐，:后有空格表示长度用空格补齐（数值型默认用0补齐）
    # {2: >7.2f}    f表示参数位浮点型，7表示输出长度位10位，.4表示保留小数点后两位, >表示居左对齐，:后有空格表示长度用空格补齐（数值型默认用0补齐）
    print('{0:10s}{3: ^5d}¥{1: <10.2f}¥{2: >7.4f}'.format(item, price, price * quantity, quantity))

'''
feeder      2  ¥8.20      ¥16.4000
diaper     50  ¥0.50      ¥25.0000
cushion    20  ¥0.58      ¥11.6000
'''

# 自定义序列化和反序列化
# python模块json序列化和反序列化时，不会序列化方法和函数，需要自定义序列化器或反序列化器
import json


class Person(object):
    def __init__(self, first_name, last_name) -> None:
        self.first_name = first_name
        self.last_name = last_name

    def full_name(self) -> str:
        return self.first_name + ' ' + self.last_name


# json 模块只能序列化dict类型的数据，所以对象序列化时，只序列化对象的__dict__内的内容
json_str = json.dumps(Person('Vito', 'Su').__dict__)
print(json_str)

'''
{"first_name": "Vito", "last_name": "Su"}
'''


# 自定义序列化方法
class PersonToJson(json.JSONEncoder):
    def default(self, obj: Person):
        if isinstance(obj, Person):
            return {"first_name": obj.first_name,
                    "last_name": obj.last_name,
                    "full_name": obj.full_name()}


json_str = json.dumps(Person('Vito', 'Su'), cls=PersonToJson)
print(json_str)
'''
{"first_name": "Vito", "last_name": "Su", "full_name": "Vito Su"}
'''


# 自定义反序列化方法
class JsonToPerson(json.JSONDecoder):
    def decode(self, s: str):
        json_object = json.loads(s)
        return Person(json_object['first_name'], json_object['last_name'])


json_str = '{"first_name": "99", "last_name": "Su"}'
person = json.loads(json_str, cls=JsonToPerson)
print(person.full_name())
'''
99 Su
'''

# reduce
from functools import reduce

r = reduce(lambda x, y: x * y, range(1, 11))
print(r)


class TestFactory(object):
    def __init__(self, name):
        print(self.__class__.__name__ + name)


def factory(cls, *args, **kwargs):
    return cls(*args, **kwargs)


factory(TestFactory, 'Vito1')


# staticmethod

class MyClass(object):
    counter = 0

    @staticmethod
    def Count(cls):
        cls.counter += 1
        print(cls.counter)
