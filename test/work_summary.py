import json

import pandas as pd
import numpy as np


excel_files = [
    r"E:\Download\DevWorklog_20250122093052(2).xlsx"
]

work_summary_path = r"E:\Download\work_summary_aily.json"

def collect():
    items = []
    req_count = {}
    bug_count = {}
    mp_count = {}
    other_count = {}
    # 分类时间
    type_time = {}
    # 分类个数
    type_count = {}
    # 需求时间
    re_time = {}
    # 需求个数
    re_count = {}
    # 项目时间
    project_time = {}
    # 项目个数
    project_count = {}

    for excel_file in excel_files:
        df_sheet = pd.read_excel(excel_file, sheet_name='Sheet1')
        for value in df_sheet.values:
            item = {
                "duration": value[6],
                "start_time": value[4],
                "end_time": value[5],
                "type": value[11],
                "project_name": value[27],
                "project_id": value[8],
                "customer_name": value[28],
                "dms_id": value[13]
            }
            items.append(item)
            group_type_time_sum(type_time, item['type'], item)
            group_type_time_sum(project_time, item['customer_name'], item)

    # 处理需求个数
    req_count = group_type_count(items, '需求')
    # 处理故障个数
    mq_count = group_type_count(items, '故障')
    # 其他任务个数
    other_count = group_type_count(items, '其他')
    # 处理bug个数
    bug_count = group_type_count(items, 'BUG')

    counter = {
        "需求": req_count,
        "故障": mq_count,
        "BUG": bug_count,
        "其他": other_count,
    }

    timer = {
        "需求": np.ceil(type_time['需求'] * 100) / 100,
        "故障": np.ceil(type_time['故障'] * 100) / 100,
        "BUG": np.ceil(type_time['BUG'] * 100) / 100,
        "其他": np.ceil(type_time['其他'] * 100) / 100,
    }

    project_timer = {}
    customer_timer= {}

    project_dms_counter = {}
    customer_dms_counter = {}

    project_counter = {}
    customer_counter = {}

    std_dms_counter = {}
    std_timer = {}

    for item in items:
        if item['project_name'] not in project_timer:
            project_timer[item['project_name']] = float(item['duration'])
        else:
            project_timer[item['project_name']] += float(item['duration'])

        if item['customer_name'] not in customer_timer:
            customer_timer[item['customer_name']] = float(item['duration'])
        else:
            customer_timer[item['customer_name']] += float(item['duration'])

        if item['project_name'] not in project_dms_counter:
            project_dms_counter[item['project_name']] = {
                item['dms_id']: 1,
            }
        else:
            if item['dms_id'] in project_dms_counter[item['project_name']]:
                project_dms_counter[item['project_name']][item['dms_id']] += 1
            else:
                project_dms_counter[item['project_name']][item['dms_id']] = 1

        if item['customer_name'] not in customer_dms_counter:
            customer_dms_counter[item['customer_name']] = {
                item['dms_id']: 1,
            }
        else:
            if item['dms_id'] in customer_dms_counter[item['customer_name']]:
                customer_dms_counter[item['customer_name']][item['dms_id']] += 1
            else:
                customer_dms_counter[item['customer_name']][item['dms_id']] = 1

    for project_item in project_dms_counter:
        if project_item not in project_dms_counter[project_item]:
            project_counter[project_item] = len(project_dms_counter[project_item].values())

    for project_item in customer_dms_counter:
        if project_item not in customer_dms_counter[project_item]:
            customer_counter[project_item] = len(customer_dms_counter[project_item].values())

    with pd.ExcelWriter(r'E:\Download\work_summary_aily.xlsx') as writer:
        counter_ex = pd.DataFrame(counter.items(), columns=['类型', '数量'])
        counter_ex.to_excel(writer, sheet_name='counter', index=False)

        timer_ex = pd.DataFrame(timer.items(), columns=['类型', '时间'])
        timer_ex.to_excel(writer, sheet_name='timer', index=False)

        project_timer_ex = pd.DataFrame(project_timer.items(), columns=['项目', '时间'])
        project_timer_ex.to_excel(writer, sheet_name='project_timer', index=False)

        customer_timer_ex = pd.DataFrame(customer_timer.items(), columns=['客户', '时间'])
        customer_timer_ex.to_excel(writer, sheet_name='customer_timer', index=False)

        project_counter_ex = pd.DataFrame(project_counter.items(), columns=['项目', '数量'])
        project_counter_ex.to_excel(writer, sheet_name='project_counter', index=False)

        customer_counter_ex = pd.DataFrame(customer_counter.items(), columns=['客户', '数量'])
        customer_counter_ex.to_excel(writer, sheet_name='customer_counter', index=False)

    with open(work_summary_path, "w", encoding="utf-8") as file:
        file.write(json.dumps(items, sort_keys=True, indent=4, ensure_ascii=False))

def group_type_count(items, type_name):
    dit = {}
    count = 0
    dit[type_name] = {}
    for item in items:
        if item['type'] != type_name:
            continue
        dms_id = item['dms_id']
        if dms_id in dit[type_name]:
            dit[type_name][dms_id] += 1
        else:
            dit[type_name][dms_id] = 1

    return len(dit[type_name])

def group_type_time_sum(dic, group, item):
    if group in dic:
        dic[group] += float(item['duration'])
    else:
        dic[group] = float(item['duration'])

def group_department():
    file_path = r"E:\Download\d.xlsx"
    sheet = pd.read_excel(file_path, sheet_name='Sheet1')
    dit ={}
    for value in sheet.values:
        if value[2] not in dit:
            dit[value[2]] = float(value[1])
        else:
            dit[value[2]] += float(value[1])

    with pd.ExcelWriter(file_path) as writer:
        counter = pd.DataFrame(dit.items(), columns=['部门', '工时'])
        counter.to_excel(writer, sheet_name='counter', index=False)

def aliy_std_count():
    json_data= json.load(open(work_summary_path, encoding="utf-8"))
    std_items = filter(lambda x: '产品' in x['project_name'], json_data)
    std_group_items = list(std_items)
    count = 0
    for item in std_group_items:
       count += float(item['duration'])
    return count

print(aliy_std_count())
# collect()
# group()
# group_department()
