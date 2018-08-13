"""
Created on 2018/8/13
@Author: Jeff Yang
"""

import requests
import json
import uuid


def get_json(url, form_data):
    """获取页面源码"""
    cookie = "JSESSIONID=" + str(uuid.uuid4()) + ";user_trace_token=" + str(uuid.uuid4()) + "; LGUID=" + str(
        uuid.uuid4()) + "; index_location_city=%E6%88%90%E9%83%BD;SEARCH_ID=" + str(
        uuid.uuid4()) + '; _gid=GA1.2.717841549.1514043316;_ga=GA1.2.952298646.1514043316;LGSID=' + str(
        uuid.uuid4()) + ";LGRID=" + str(uuid.uuid4()) + "; "
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0.3',
        'Connection': 'keep-alive',
        'Content-Length': '23',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': cookie,
        'Host': 'www.lagou.com',
        'Origin': 'https://www.lagou.com',
        'Referer': 'https://www.lagou.com/jobs/list_iot?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput=',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'X-Anit-Forge-Code': '0',
        'X-Anit-Forge-Token': 'None',
        'X-Requested-With': 'XMLHttpRequest',
    }
    response = requests.post(url, data=form_data, headers=headers)
    if response.status_code == 200:
        return response.json()
    return


def get_info(data):
    """获取职位及公司信息"""
    items = data['content']['positionResult']['result']
    result = {}
    for item in items:
        # 职位名称
        result['position_name'] = item['positionName']
        # 薪资
        result['salary'] = item['salary']
        # 城市
        result['city'] = item['city']
        # 发布时间
        result['create_time'] = item['createTime']
        # 公司名称
        result['company_name'] = item['companyFullName']
        # 公司性质
        result['finance_stage'] = item['financeStage']
        # 公司规模
        result['company_size'] = item['companySize']
        # 公司业务范围
        result['industry_field'] = item['industryField']
        yield result


if __name__ == '__main__':
    url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
    with open('job_info.json', 'a', encoding='UTF-8') as f:
        for page in range(1, 40):
            form_data = {
                'first': 'false',
                'pn': page,
                'kd': 'iot'
            }
            data = get_json(url, form_data)
            for item in get_info(data):
                print('saving:', item['company_name'])
                json.dump(item, f, ensure_ascii=False)
                f.write('\n')
            print(' === Page', page, 'done! ===')
