# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy.http import Request
from bs4 import BeautifulSoup
from wdzj.items import ScoreItem
from wdzj.sqlutil import SqlUtil


class Myspider(scrapy.Spider):
    name = "pingji"
    allowed_domains = ["wdzj.com"]
    base_domain = 'https://www.wdzj.com'
    bash_url = 'https://www.wdzj.com/pingji.html'
    login_url = 'https://passport.wdzj.com/userInterface/login'
    month = ''
    user_info = {
        'username': '17321331175',
        'password': '1qaz2wsx',
        'auto_login': 1
    }

    def start_requests(self):
        login_url = self.login_url
        for field in self.user_info:
            if field == 'username':
                login_url += '?'+field+'='+self.user_info[field]
            else:
                login_url += '&' + field + '=' + str(self.user_info[field])
        yield Request(login_url, callback=self.parse_login)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        rdiv = soup.find('div', class_='rate-plat').find('div', class_='plat-ranking')
        self.month = self.self_strip(rdiv.find('div', class_='ranking-y').get_text()) + '-' + self.self_strip(rdiv.find('div', class_='ranking-m').get_text())
        trs = soup.find('div', class_='mod-tablelists').find('tbody', id='tbody_all').find_all('tr')
        for tr in trs:
            plat_id = tr.attrs['data-platid']
            trend = self.deal_score_trend(tr.find_all('td')[2].find('span'))
            infourl = self.base_domain + tr.find_all('td')[1].find_all('a')[0].attrs['href']
            yield Request(infourl, callback=self.get_score, meta={'plat_id': plat_id, 'trend': trend})

    def closed(self, reason):
        # 处理近7天和近30天数据统计
        sqlutil = SqlUtil()
        sqlutil.deal_platform_score(self.month)

    def parse_login(self, response):
        data = json.loads(response.text)
        print(data['msg'])
        if data['error_code'] == '0':
            yield Request(self.bash_url, callback=self.parse)
        # yield super(Myspider, self).start_requests()

    # 获取平台评级
    def get_score(self, response):
        item = ScoreItem()
        soup = BeautifulSoup(response.text, 'lxml')
        item['plat_id'] = response.meta['plat_id']
        item['trend'] = response.meta['trend']
        period = self.self_strip(soup.find('div', class_='detail-tit').get_text())[0:7]
        item['period'] = period.replace('年', '-')
        item['score'] = self.self_strip(soup.find('div', class_='detail-tit').find_all('span')[0].get_text())
        item['ranking'] = self.self_strip(soup.find('div', class_='detail-tit').find_all('span')[1].get_text())
        # 第一行数据
        lis = soup.find_all('ul', class_='xlist')[0].find_all('li')
        for index in range(len(lis)):
            rate_rank = self.deal_score_rank(lis[index].find('div', class_='rate-data').find('span'))
            if rate_rank != 0:
                data, rank = lis[index].find('div', class_='rate-data').stripped_strings
                rate_data = self.self_strip(data).replace(',', '')
            else:
                rate_data = self.self_strip(lis[index].find('div', class_='rate-data').get_text()).replace(',', '')
            if index == 0:
                item['turnover_score'] = rate_data
                item['turnover_rank'] = rate_rank
            elif index == 1:
                item['borrowers_score'] = rate_data
                item['borrowers_rank'] = rate_rank
            elif index == 3:
                item['compliance_score'] = rate_data
                item['compliance_rank'] = rate_rank
        # 第二行数据
        lis = soup.find_all('ul', class_='xlist')[1].find_all('li')
        for index in range(len(lis)):
            rate_rank = self.deal_score_rank(lis[index].find('div', class_='rate-data').find('span'))
            if rate_rank != 0:
                data, rank = lis[index].find('div', class_='rate-data').stripped_strings
                rate_data = self.self_strip(data).replace(',', '')
            else:
                rate_data = self.self_strip(lis[index].find('div', class_='rate-data').get_text()).replace(',', '')
            if index == 1:
                item['transparency_score'] = rate_data
                item['transparency_rank'] = rate_rank
            elif index == 3:
                item['recovery_score'] = rate_data
                item['recovery_rank'] = rate_rank
        yield item

    # 处理评级排名
    def deal_score_trend(self, span):
        cls = span.attrs['class'][0]
        if cls == 'arrow-none':
            trend = 0
        else:
            prex = ''
            if cls == 'arrow-down':
                prex = '-'
            trend = int(prex + self.self_strip(span.get_text()))
        return trend

    # 处理评级排名
    def deal_score_rank(self, span):
        if span:
            cls = span.attrs['class']
            prex = ''
            for cl in cls:
                if cl == 'arrow-down':
                    prex = '-'
                    break
            rank = int(prex + self.self_strip(span.get_text()))
        else:
            rank = 0
        return rank

    # 自定义字符串去除空格函数
    def self_strip(self, str):
        str = str.strip()
        if str == '-':
            str = ''
        return str