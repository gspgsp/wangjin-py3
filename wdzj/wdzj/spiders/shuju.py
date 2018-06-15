#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import scrapy
import datetime
import time
from bs4 import BeautifulSoup
from scrapy.http import Request
from wdzj.items import DataItem
from wdzj.sqlutil import SqlUtil

reload(sys)
sys.setdefaultencoding('utf-8')

class Myspider(scrapy.Spider):
    name = 'shuju'
    allowed_domains = ['wdzj.com']
    bash_url = 'https://shuju.wdzj.com'

    def start_requests(self):
        yield Request(self.bash_url, self.parse)

    def parse(self, response):
        trs = BeautifulSoup(response.text, 'lxml').find('div', class_='shuju-table').find('table', class_='normal-table-two').find('tbody', class_='tb-body').find_all('tr')
        bashurl = str(response.url)
        # for index in range(1, 2):
        for index in range(len(trs)):
            plat_id = trs[index].attrs['data-platid']
            if plat_id != '0':
                url = bashurl + '/plat-info-' + plat_id + '.html'
                yield Request(url, callback=self.get_data, meta={'plat_id': plat_id})

    def closed(self, reason):
        # 处理近7天和近30天数据统计
        sqlutil = SqlUtil()
        new_date = datetime.datetime.today() + datetime.timedelta(-7)
        start_time_7days = time.strftime('%Y-%m-%d', new_date.timetuple())
        new_date = datetime.datetime.today() + datetime.timedelta(-30)
        start_time_30days = time.strftime('%Y-%m-%d', new_date.timetuple())
        end_time = time.strftime('%Y-%m-%d')
        sqlutil.deal_platform_data(start_time_7days, start_time_30days, end_time)

    # 获取平台数据
    def get_data(self, response):
        item = DataItem()
        soup = BeautifulSoup(response.text, 'lxml')
        # 平台主表部分信息
        item['plat_one_month_vol'] = self.self_strip(soup.find('div', class_="pt-30xq").find_all('li')[0].find('div', class_='cen').get_text())
        boxes = soup.find_all('div', class_="pt-info")[1].find_all('div', class_="lbor")
        for index in range(len(boxes)):
            text = self.self_strip(boxes[index].find('b').get_text())
            if index == 0:
                item['plat_reference_rate'] = text
            elif index == 1:
                item['plat_investment_horizon'] = text

        item['plat_id'] = response.meta['plat_id']
        item['dateline'] = self.self_strip(soup.find('div', class_='detail-tit').find('em').get_text())[-10:]
        # 第一行数据
        lis = soup.find_all('ul', class_='xlist')[0].find_all('li')
        for index in range(len(lis)):
            rate_data = self.self_strip(lis[index].find('div', class_='rate-data').get_text()).replace(',', '')
            rate_rank = self.deal_data_rank(lis[index].find('div', class_='rate-data').find('span').attrs['class'])
            if index == 0:
                item['trading_volume'] = rate_data
                item['trading_volume_rank'] = rate_rank
            elif index == 1:
                item['capital_inflow'] = rate_data
                item['capital_inflow_rank'] = rate_rank
            elif index == 2:
                item['not_repay'] = rate_data
                item['not_repay_rank'] = rate_rank
            elif index == 3:
                item['reference_rate'] = rate_data
                item['reference_rate_rank'] = rate_rank
            elif index == 4:
                item['loan_term'] = rate_data
                item['loan_term_rank'] = rate_rank
        # 第二行数据
        lis = soup.find_all('ul', class_='xlist')[1].find_all('li')
        for index in range(len(lis)):
            rate_data = self.self_strip(lis[index].find('div', class_='rate-data').get_text()).replace(',', '')
            rate_rank = self.deal_data_rank(lis[index].find('div', class_='rate-data').find('span').attrs['class'])
            if index == 0:
                item['investment_nums'] = rate_data
                item['investment_nums_rank'] = rate_rank
            elif index == 1:
                item['investment_amount'] = rate_data
                item['investment_amount_rank'] = rate_rank
            elif index == 2:
                item['duein_investment_nums'] = rate_data
                item['duein_investment_nums_rank'] = rate_rank
            elif index == 3:
                item['borrow_nums'] = rate_data
                item['borrow_nums_rank'] = rate_rank
            elif index == 4:
                item['borrow_amount'] = rate_data
                item['borrow_amount_rank'] = rate_rank
        # 第三行数据
        lis = soup.find_all('ul', class_='xlist')[2].find_all('li')
        for index in range(len(lis)):
            rate_data = self.self_strip(lis[index].find('div', class_='rate-data').get_text()).replace(',', '')
            rate_rank = self.deal_data_rank(lis[index].find('div', class_='rate-data').find('span').attrs['class'])
            if index == 0:
                item['bid_nums'] = rate_data
                item['bid_nums_rank'] = rate_rank
            elif index == 1:
                item['duein_borrow_nums'] = rate_data
                item['duein_borrow_nums_rank'] = rate_rank
        yield item

    # 处理数据排名
    def deal_data_rank(self, cls):
        rank = 0
        for cl in cls:
            if cl == 'arrow-down':
                rank = -1
                break
            elif cl == 'arrow-up':
                rank = 1
                break
        return rank

    # 自定义字符串去除空格函数
    def self_strip(self, str):
        str = str.strip()
        if str == '-':
            str = ''
        return str