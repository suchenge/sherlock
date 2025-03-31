import os

import pyperclip as pc

vue_path = r''
dto_path = r'D:\quantum-scm\power-scm\scm.tms7\SCM.TMS7\SCM.TMS7.OpenSvc\Modules\Order\Response\OrderInfoQueryResponse.cs'

dtoItems = {}
vueItems = []

def get_dto_items2():
    lines = []
    with open(dto_path, 'r', encoding="utf-8") as dto:
        content = dto.read()
        for line in content.split('\n'):
            if '\r' in line: continue
            if '\n' in line: continue
            if '#region' in line: continue
            if '#endregion' in line: continue
            if 'summary' in line: continue
            if '///' in line:
                lines.append(line.replace('///','').strip())
                continue
            if 'JsonPropertyName' in line:
                lines.append(line.replace('[JsonPropertyName("','').replace('")]','').strip())
                continue
            if 'get;' in line or 'set' in line:
                line_contents = [i for i in line.split(' ') if i != '']
                lines.append(line_contents[1])
                continue
    properties = []
    n = 3
    for group in [lines[i:i + n] for i in range(0, len(lines), n)]:
        properties.append({
            'description': group[0],
            'name': group[1],
            'type': group[2],
        })

    return properties


def get_vue_items():
    if os.path.exists(vue_path) is False:
        return

    with open(vue_path, 'r', encoding="utf-8") as vue:
        content = vue.read()
        for line in content.split('\n'):
            if 'field' in line:
                vueItems.append(line.replace('field', '')
                                    .replace(':', '')
                                    .replace(',', '')
                                    .replace('\'', '')
                                    .strip())


def build_vue_items2(items):
    item_content = ''
    for item in items:
        if item['name'] in vueItems: continue
        item_content += '''
  {
    field: '%s',
    title: '%s',
    width: 140,
    visible: false,
    params: {
      query: {
        component: '%s',
      },
    },
  },''' % (item['name'], item['description'], build_component(item['type']))

    pc.copy(item_content)

def build_component(item_type):
    field = item_type.lower()

    if 'date' in field:
        return 'date'
    elif 'int' in field or 'float' in field or 'double' in field or 'decimal' in field:
        return 'number'
    else:
        return 'text'
'''
get_dto_items()
get_vue_items()
build_vue_items()
'''

build_vue_items2(get_dto_items2())

print(dtoItems)
