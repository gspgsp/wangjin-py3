#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import scrapy
import json
import re
import time
from bs4 import BeautifulSoup
from scrapy.http import Request
from wdzj.items import IndustryDataItem
from wdzj.items import StatisticalDataItem
from wdzj.items import MonthDataItem
from wdzj.sqlutil import SqlUtil

reload(sys)
sys.setdefaultencoding('utf-8')

class Myspider(scrapy.Spider):
    name = 'industry'
    allowed_domains = ['wdzj.com']
    bash_url = [
        'https://m.wdzj.com/shuju/interfaceWapIndustry',
        'https://m.wdzj.com/shuju/platformTypeData',
        'https://m.wdzj.com/shuju/areaData'
    ]
    statis_month = ''

    def start_requests(self):
        for url in self.bash_url:
            if url.find('Industry') != -1:    # 行业数据
                yield Request(url, self.get_industry_data)
            elif url.find('Type') != -1:      # 类型分布
                yield Request(url, self.get_statistical_data, meta={'type': 1})
            elif url.find('area') != -1:      # 区域分布
                yield Request(url, self.get_statistical_data, meta={'type': 2})

    def closed(self, reason):
        # 更新统计截止月份
        sqlutil = SqlUtil()
        sqlutil.update_statis_month(time.strftime('%Y-%m'), self.statis_month)

    # 行业数据
    def get_industry_data(self, response):
        data = json.loads(response.text)['data']
        for type in range(1, 4):
            # 成交指数
            # industryItem = IndustryDataItem()
            # industryItem['period'] = period_day
            # industryItem['type'] = type
            # if type == 1:
            #     industryItem['index'] = data['volume'].pop()
            # elif type == 2:
            #     industryItem['index'] = data['interestRate'].pop()
            # elif type == 3:
            #     industryItem['index'] = data['popularity'].pop()
            # yield industryItem
            for index in range(len(data['date'])):
                # 成交指数
                industryItem = IndustryDataItem()
                industryItem['period'] = data['date'][index]
                industryItem['type'] = type
                if type == 1:
                    industryItem['index'] = data['volume'][index]
                elif type == 2:
                    industryItem['index'] = data['interestRate'][index]
                elif type == 3:
                    industryItem['index'] = data['popularity'][index]
                yield industryItem
        period_day = data['date'].pop()

        for type in range(4, 10):
            # 参考收益率指数
            # industryItem = IndustryDataItem()
            # industryItem['period'] = period_month
            # industryItem['type'] = type
            # if type == 4:
            #     industryItem['index'] = data['problemNum'].pop()
            # elif type == 5:
            #     industryItem['index'] = data['problemPercent'].pop()
            # elif type == 6:
            #     industryItem['index'] = data['y1'].pop()
            # elif type == 7:
            #     industryItem['index'] = data['y3'].pop()
            # elif type == 8:
            #     industryItem['index'] = data['y5'].pop()
            # elif type == 9:
            #     industryItem['index'] = data['y4'].pop()
            # yield industryItem
            for index in range(len(data['x'])):
                # 参考收益率指数
                industryItem = IndustryDataItem()
                industryItem['period'] = data['x'][index]
                industryItem['type'] = type
                if type == 4:
                    industryItem['index'] = data['problemNum'][index]
                elif type == 5:
                    industryItem['index'] = data['problemPercent'][index]
                elif type == 6:
                    industryItem['index'] = data['y1'][index]
                elif type == 7:
                    industryItem['index'] = data['y3'][index]
                elif type == 8:
                    industryItem['index'] = data['y5'][index]
                elif type == 9:
                    industryItem['index'] = data['y4'][index]
                yield industryItem
        period_month = data['x'].pop()

        # 月度数据
        monthItem = MonthDataItem()
        monthItem['period'] = time.strftime('%Y-%m')
        monthItem['end_day'] = period_day
        monthItem['end_month'] = period_month
        percent = data['percent']
        monthItem['amount_index'] = percent['day_amount_index']
        monthItem['amount_index_trend'] = percent['day_amount_index_percent']
        monthItem['popularity_index'] = percent['day_popularity_index']
        monthItem['popularity_index_trend'] = percent['day_popularity_index_percent']
        monthItem['new_problem_plat_num'] = percent['new_problem_plat_num_percent']
        yield monthItem

    # 统计数据
    def get_statistical_data(self, response):
        period = str(self.self_strip(BeautifulSoup(response.text, 'lxml').find('section', class_='tabledesc').find('div', class_='date').get_text())[0:-1]).replace('年', '-')
        self.statis_month = period
        data = json.loads(re.search(r"var lists = (.*);", response.text, re.M | re.I).group(1))
        for rec in data:
            item = StatisticalDataItem()
            item['type'] = response.meta['type']
            item['period'] = period
            # 指数名称
            item['index'] = rec['province']
            # 成交量(亿元)
            item['amount'] = rec['amount']
            # 综合参考收益率(%)
            item['income_rate'] = rec['incomeRate']
            # 运营平台数量
            item['operate_plat_num'] = rec['operatePlatNumber']
            # 问题平台数量
            item['problem_plat_num'] = rec['problemPlatNumber']
            # 投资人数(万)
            item['bidder_num'] = rec['bidderNum']
            # 借款人数(万)
            item['borrower_num'] = rec['borrowerNum']
            # 待收余额(亿元)
            item['balance_loans'] = rec['balanceLoans']
            # 平均借款期限(月)
            item['loan_period'] = rec['loanPeriod']
            yield item

    # 自定义字符串去除空格函数
    def self_strip(self, str):
        str = str.strip()
        if str == '-':
            str = ''
        return str

