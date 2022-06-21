# 字符串模版

tmp1 = '{}, {:.4f} and {}'.format('One', 2, 'Three')
print(tmp1)

tmp1 = '{0}, {1:.2f} and {1}, {2}'.format('One', 2, 'Three')
print(tmp1)

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
            return ','.join(['DecoratorAsClassByParameters', self.__power_name__, self.__power_type__, func(*args, **kwargs)])

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
