#!/usr/bin/python
# -*- coding:utf-8 -*-
import re
import sys
import time
import json
import scrapy
import os
import urllib2
import urlparse
from bs4 import BeautifulSoup
from scrapy.http import Request
from wdzj.items import PlatformItem
from wdzj.items import ManagersItem
from wdzj.items import PhotosItem
from wdzj.items import IcbcItem
from wdzj.items import ArticleItem

reload(sys)
sys.setdefaultencoding('utf-8')

class Myspider(scrapy.Spider):
    name = 'dangan'
    allowed_domains = ['wdzj.com']
    base_domain = 'https://www.wdzj.com'
    shuju_domain = 'https://shuju.wdzj.com'
    bash_url = base_domain + '/dangan/search?sort=1&filter=e'

    def start_requests(self):
        for num in range(1, 4):
            yield Request(self.bash_url + str(num), self.parse)
        # yield Request(self.bash_url, self.parse)
        # urls = ['https://www.wdzj.com/dangan/lct1/', 'https://www.wdzj.com/dangan/yjcf4/']
        # yield Request(urls[1], callback=self.get_info, meta={'hot_solution': '', 'background': '', 'operation_state': 3})

    def parse(self, response):
        max_num = BeautifulSoup(response.text, 'lxml').find('div', class_='pageList').find_all('a')[-1].attrs['currentnum']
        bashurl = str(response.url)
        for num in range(1, int(max_num) + 1):
        # for num in range(1, 2):
            url = bashurl + '&currentPage=' + str(num)
            yield Request(url, callback=self.get_list)

    # 获取列表页数据
    def get_list(self, response):
        operation_state = self.extract_param(response.url, 'filter')[-1:]
        lis = BeautifulSoup(response.text, 'lxml').find('ul', class_='terraceList').find_all('li', class_='item')
        for li in lis:
            infourl = self.base_domain + li.find('a', class_='look').attrs['href']
            tag = li.find_all('div', class_="itemTitleTag")
            if len(tag) > 0:
                strong = tag[0].find('em').find('strong')
                if strong:
                    start = 1
                    hot_solution = ',1'
                else:
                    start = 0
                    hot_solution = ''
                divs = li.find_all('div', class_="itemTitleTag")
                background = self.deal_plat_background(divs[start].find('em').get_text())
                for index in range(len(divs)):
                    if index > start:
                        text = self.self_strip(divs[index].find('em').get_text())
                        hot_solution = hot_solution + self.deal_hot_solution(text)
            else:
                hot_solution = ''
                background = ''

            yield Request(infourl, callback=self.get_info, meta={'hot_solution': hot_solution, 'background': background, 'operation_state': operation_state})

    # 获取详情页数据
    def get_info(self, response):
        item = PlatformItem()
        soup = BeautifulSoup(response.text, 'lxml')
        plat_id = soup.find(id="platId").attrs['value']
        item['plat_id'] = plat_id
        item['hot_solution'] = response.meta['hot_solution']
        item['background'] = response.meta['background']
        item['operation_state'] = response.meta['operation_state']
        item['name'] = self.self_strip(soup.find('div', class_="title").find('h1').get_text())
        icon_url = 'https:'+soup.find('div', class_="pt-logo").find('img').attrs['src']
        extension = self.file_extension(icon_url)
        file_name = 'plat-'+item['plat_id']+'-icon'+extension
        # self.urllib_download(icon_url, file_name)
        item['icon'] = 'http://p9by7oy7m.bkt.clouddn.com/'+file_name
        item['sign'] = str(self.extract_route(response.url))[8:-1]
        initials = self.multi_get_letter(item['name'])
        ilist = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        if initials[0:1] in ilist:
            item['initial'] = '#'
        else:
            item['initial'] = initials[0:1]
        item['all_initial'] = initials
        online_time = self.self_strip(soup.find_all('div', class_="pt-info")[0].find_all('span')[0].get_text())
        item['online_time'] = str(online_time)[0:10]
        places = self.self_strip(soup.find_all('div', class_="pt-info")[0].find('em').get_text()).split(' · ')
        item['registered_place'] = places[0]
        if len(places) > 1:
            item['registered_city'] = places[1]
        boxes = soup.find_all('div', class_="bq-box")
        if item['operation_state'] != '1' and len(boxes) > 1:
            tags = boxes[0].find_all('span', class_='tag')
            if len(tags) > 0:
                tag = tags[len(tags)-1]
                if tag.find('span'):
                    item['problem_time'] = tag.find('span').get_text()[4:]
                    item['problem_type'] = self.self_strip(tag.get_text()).replace(' ', '')[0:-16]
                    # if item['operation_state'] == '3':
                    #     item['problem_type'] = self.self_strip(tag.get_text()).replace(' ', '')[0:-16]

        item['one_month_vol'] = self.self_strip(soup.find('div', class_="pt-30xq").find_all('li')[0].find('div', class_='cen').get_text())
        b1 = soup.find_all('div', class_="pt-info")[1].find_all('div', class_="box")[0].find('div', class_="b1")
        if b1:
            item['newest_rank'] = self.self_strip(b1.find('span', class_='col').find('b').get_text())
            item['newest_score'] = self.self_strip(b1.find_all('span')[1].get_text())
        boxes = soup.find_all('div', class_="pt-info")[1].find_all('div', class_="lbor")
        for index in range(len(boxes)):
            text = self.self_strip(boxes[index].find('b').get_text())
            if index == 0:
                item['reference_rate'] = text
            elif index == 1:
                item['investment_horizon'] = text
            elif index == 3:
                item['yesterday_vol'] = text
            elif index == 4:
                item['yesterday_tbp'] = text

        atag = soup.find('div', class_="pt-link").find('a', attrs={"class": "nohome"})
        if atag:
            item['official_website'] = ''
        else:
            item['official_website'] = self.extract_domain(soup.find('div', class_="pt-link").find('a').attrs['data-href'])
        item['focus_nums'] = self.self_strip(soup.find('div', class_="pt-bottom").find('div', class_="ty-box").find('em').get_text())
        # 实力资质
        aptitudes = soup.find_all('div', class_="bgbox-bt")[0].find_all('dl')[0]
        dds = aptitudes.find_all('dd')
        if len(dds) == 6:
            start = 1
        else:
            start = 0
        for index in range(len(dds)):
            if index == 0:
                registered_amount = self.self_strip(dds[index].find('div', class_="r").get_text()).replace(' ', '')
                if registered_amount != '':
                    pos = registered_amount.find('（')
                    if self.self_strip(registered_amount[0:pos]) == '':
                        registered_amount = ''
                    else:
                        if pos == -1:
                            registered_amount = registered_amount[0:-2]
                        else:
                            end = pos-3
                            registered_amount = registered_amount[0:end]
                item['registered_amount'] = registered_amount
            if index == 1+start:
                item['bank_deposit'] = self.self_strip(dds[index].find('div', class_="r").get_text())
            elif index == 2+start:
                item['financing_records'] = self.self_strip(dds[index].find('div', class_="r").prettify().replace(' ', ''))
            elif index == 3+start:
                item['supervise_association'] = self.self_strip(dds[index].find('div', class_="r").prettify().replace(' ', ''))

        # 平台服务
        service = soup.find_all('div', class_="bgbox-bt")[0].find_all('dl')[1]
        dds = service.find_all('dd')
        for index in range(len(dds)):
            text = self.self_strip(dds[index].find('div', class_="r").get_text())
            if index == 0:
                item['auto_bid'] = self.deal_auto_bid(text)
            elif index == 1:
                item['transfer_type'] = self.deal_transfer_type(text)
            elif index == 2:
                item['bid_security'] = text
            elif index == 3:
                item['security_mode'] = self.deal_security_mode(text)

        # 平台简介
        gsjj = soup.find('div', class_="da-gsjj")
        if gsjj:
            if item['operation_state'] == '1':
                description = soup.find('div', class_="da-gsjj").find('div', class_='cen-zk').prettify()
                description = re.sub("<a\s+[^<>]+>(?P<aContent>[^<>]+?)</a>", "\g<aContent>", description)
            else:
                description = self.self_strip(soup.find('div', class_="da-gsjj").find('div', class_='cen-zk').get_text())
            item['description'] = description

            # 高管简介
        ggjj = soup.find('div', class_="da-ggjj")
        if ggjj:
            lis = ggjj.find('div', class_='ggnav').find_all('li')
            for index in range(len(lis)):
                mItem = ManagersItem()
                mItem['plat_id'] = plat_id
                mItem['name'] = self.self_strip(lis[index].find('span').get_text())
                mItem['position'] = self.self_strip(lis[index].find('p').get_text())
                ggshow = ggjj.find_all('div', class_='ggshow')[index]
                mItem['picture'] = ggshow.find('img').attrs['src']
                mItem['description'] = self.self_strip(ggshow.find('p').get_text())
                yield mItem

        # 平台费用
        ptfy = soup.find('div', class_="da-ptfy")
        if ptfy:
            dts = soup.find('div', class_="da-ptfy").find_all('dt')
            item['manage_cost'] = self.self_strip(dts[0].find('em').get_text())
            item['withdraw_cost'] = self.self_strip(dts[1].find('em').get_text())
            item['recharge_cost'] = self.self_strip(dts[2].find('em').get_text())
            item['transfer_cost'] = self.self_strip(dts[3].find('em').get_text())
            item['vip_cost'] = self.self_strip(dts[4].find('em').get_text())

        # 现场实拍
        xcsp = soup.find('div', class_="da-xcsp")
        if xcsp:
            boxes = soup.find('div', class_="da-xcsp").find_all('div', class_='imglistbox')
            for index in range(len(boxes)):
                lis = boxes[index].find('div', class_='listimg').find_all('li')
                for li in lis:
                    img_src = li.find('img').attrs['src']
                    if img_src != '<center><h1>413 Request Entity Too Large</h1></center><hr><center>nginx/1.6.0</center>':
                        pItem = PhotosItem()
                        pItem['plat_id'] = plat_id
                        pItem['category'] = index + 1
                        pItem['name'] = li.find('img').attrs['alt']
                        pItem['url'] = 'https:'+img_src
                        yield pItem

        # 联系方式
        lxfs = soup.find('div', class_="da-lxfs")
        if lxfs:
            item['contact_number'] = self.self_strip(lxfs.find_all('dl')[0].find_all('dd')[0].find('div', class_='r').get_text())
            item['contact_number'] = self.self_strip(lxfs.find_all('dl')[0].find_all('dd')[0].find('div', class_='r').get_text())
            item['service_email'] = self.self_strip(lxfs.find_all('dl')[0].find_all('dd')[1].find('div', class_='r').get_text())
            item['company_address'] = self.self_strip(lxfs.find_all('dl')[0].find_all('dd')[2].find('div', class_='r').get_text())
            item['company_tel'] = self.self_strip(lxfs.find_all('dl')[1].find_all('dd')[0].find('div', class_='r').get_text())
            item['company_fax'] = self.self_strip(lxfs.find_all('dl')[1].find_all('dd')[1].find('div', class_='r').get_text())

        yield item

        # 平台工商/备案
        icbcurl = response.url + 'gongshang/'
        yield Request(icbcurl, callback=self.get_icbc, meta={'plat_id': plat_id})

        # 平台资讯
        newsurl = response.url + 'zixun/'
        yield Request(newsurl, callback=self.get_news, meta={'plat_id': plat_id})

        # 平台公告
        noticeurl = response.url + 'dongtai/'
        yield Request(noticeurl, callback=self.get_notice, meta={'plat_id': plat_id})

    # 获取平台工商备案信息
    def get_icbc(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        box = soup.find('div', class_='containerBox')
        if box:
            item = IcbcItem()
            item['plat_id'] = response.meta['plat_id']
            table = box.find('div', class_='gs-box').find('div', class_='left').find('table')
            item['company_name'] = self.self_strip(table.find_all('tr')[0].find_all('td')[1].get_text())
            item['business_license'] = self.self_strip(table.find_all('tr')[0].find_all('td')[3].get_text())
            item['company_legal_person'] = self.self_strip(table.find_all('tr')[1].find_all('td')[1].get_text())
            registered_capital = self.self_strip(table.find_all('tr')[1].find_all('td')[3].get_text())
            if registered_capital:
                item['registered_capital'] = registered_capital[0:-2]
            item['company_type'] = self.self_strip(table.find_all('tr')[2].find_all('td')[1].get_text())
            contributed_capital = self.self_strip(table.find_all('tr')[2].find_all('td')[3].get_text())
            if registered_capital:
                item['contributed_capital'] = contributed_capital[0:-2]
            item['registered_address'] = self.self_strip(table.find_all('tr')[3].find_all('td')[1].get_text())
            item['start_date'] = self.self_strip(table.find_all('tr')[3].find_all('td')[3].get_text())
            item['registration_authority'] = self.self_strip(table.find_all('tr')[5].find_all('td')[1].get_text())
            item['approved_date'] = self.self_strip(table.find_all('tr')[5].find_all('td')[3].get_text())
            item['filing_domain'] = self.self_strip(table.find_all('tr')[6].find_all('td')[1].get_text())
            item['filling_date'] = self.self_strip(table.find_all('tr')[6].find_all('td')[3].get_text())
            item['filling_unit_name'] = self.self_strip(table.find_all('tr')[7].find_all('td')[1].get_text())
            item['filling_unit_properties'] = self.self_strip(table.find_all('tr')[7].find_all('td')[3].get_text())
            item['icp_filling_no'] = self.self_strip(table.find_all('tr')[8].find_all('td')[1].get_text())
            item['icp_license_no'] = self.self_strip(table.find_all('tr')[8].find_all('td')[3].get_text())
            # 股权信息
            tbody = box.find_all('div', class_='gq-box')[0].find('table', class_='table-ic').find('tbody', class_='tbody')
            if tbody:
                trs = tbody.find_all('tr')
                lt = []
                for tr in trs:
                    dt = dict()
                    dt['name'] = self.self_strip(tr.find_all('td')[0].get_text())
                    dt['percent'] = self.self_strip(tr.find_all('td')[1].get_text())
                    dt['amount'] = self.self_strip(tr.find_all('td')[2].get_text())
                    if dt['name'] or dt['percent'] or dt['amount']:
                        lt.append(dt)
                item['company_structure'] = json.dumps(lt)
            yield item

    # 获取平台资讯
    def get_news(self, response):
        cate_id = 5
        plat_id = response.meta['plat_id']
        zllist = BeautifulSoup(response.text, 'lxml').find('ul', class_='zllist')
        if zllist:
            lis = zllist.find_all('li')
            for li in lis:
                infourl = 'https:' + li.find('h3').find('a').attrs['href']
                yield Request(infourl, callback=self.get_news_info, meta={'cate_id': cate_id, 'plat_id': plat_id})

    # 获取平台公告
    def get_notice(self, response):
        cate_id = 6
        plat_id = response.meta['plat_id']
        zxlist = BeautifulSoup(response.text, 'lxml').find('ul', class_='zxlist')
        if zxlist:
            lis = zxlist.find_all('li')
            for li in lis:
                infourl = 'https:' + li.find('a').attrs['href']
                yield Request(infourl, callback=self.get_news_info, meta={'cate_id': cate_id, 'plat_id': plat_id})

    # 获取资讯详情页
    def get_news_info(self, response):
        item = ArticleItem()
        soup = BeautifulSoup(response.text, 'lxml')
        # 文章id
        route = self.extract_route(response.url)
        item['original_id'] = re.search(r"\d+", route).group()
        item['title'] = self.self_strip(soup.find('div', class_='show-box').find('h1', class_='s-title').get_text())
        cate_id = response.meta['cate_id']
        item['cate_id'] = cate_id
        item['plat_id'] = response.meta['plat_id']
        create_time = self.self_strip(soup.find('div', class_='show-box').find('div', class_='s-bq').find('span').get_text())
        if create_time != '':
            if cate_id == 5:
                fstr = '%Y-%m-%d %H:%M:%S'
            elif cate_id == 6:
                fstr = '%Y-%m-%d'
            item['create_time'] = time.mktime(time.strptime(create_time, fstr))
        zy = soup.find('div', class_='show-box').find('div', class_='s-zy')
        if zy:
            item['brief'] = self.self_strip(zy.find('span').get_text())
        content = soup.find('div', class_='show-box').find('div', class_='c-cen').prettify().replace('网贷之家', '网金之家')
        content = re.sub("<a\s+[^<>]+>(?P<aContent>[^<>]+?)</a>", "\g<aContent>", content)
        item['content'] = content
        yield item

    # 处理热门方案字段
    def deal_hot_solution(self, arg):
        # 1-评级百强 2-银行存管 3-加入协会 4-ICP认证 5-之家考察 6-融资平台
        switcher = {
            "评级百强": ",1",
            "银行存管": ",2",
            "加入协会": ",3",
            "融资平台": ",4",
            "ICP认证": ",5",
            "之家考察": ",6",
        }
        return switcher.get(arg.encode('utf-8'), "")

    # 处理自动投标字段
    def deal_auto_bid(self, arg):
        switcher = {
            "不支持": "0",
            "支持": "1",
        }
        return switcher.get(arg.encode('utf-8'), "")

    # 处理平台背景字段
    def deal_plat_background(self, arg):
        # 1-国资控股 2-国资参股 3-上市控股 4-风投系 5-银行系 6-民营系
        switcher = {
            "国资控股": "1",
            "国资参股": "2",
            "上市控股": "3",
            "股权上市": "3",
            "上市参股": "4",
            "风投系": "5",
            "银行系": "6",
            "民营系": "7",
        }
        return switcher.get(arg.encode('utf-8'), "")

    # 处理债权转让字段
    def deal_transfer_type(self, arg):
        # 1-随时转让 2-1月后可转让 3-3月后可转让 4-一年后可转让 5-不可转让
        switcher = {
            "随时转让": "1",
            "1个月": "2",
            "3个月": "3",
            "1年": "4",
            "不可转让": "5",
        }
        return switcher.get(arg.encode('utf-8'), "")

    # 处理保障模式字段
    def deal_security_mode(self, arg):
        # 1-风险准备金 2-小贷公司 3-融资性担保公司 4-非融资性担保公司 5-平台垫付 6-其他
        arr = arg.split('、')
        security_mode = ''
        switcher = {
            "风险准备金": ",1",
            "小贷公司": ",2",
            "融资性担保公司": ",3",
            "非融资性担保公司": ",4",
            "平台垫付": ",5",
        }
        for val in arr:
            security_mode += switcher.get(val.encode('utf-8'), "")

        if security_mode == '':
            security_mode = ',6'
        return security_mode

    # 获取url链接域名信息
    def extract_domain(self, url):
        parsed_uri = urlparse.urlparse(url)
        domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
        return domain

    # 获取url链接路由信息
    def extract_route(self, url):
        parsed_uri = urlparse.urlparse(url)
        route = '{uri.path}'.format(uri=parsed_uri)
        return route

    # 获取url链接参数信息
    def extract_param(self, url, field):
        params = urlparse.parse_qs(urlparse.urlparse(url).query)
        return params[field][0]

    # 自定义字符串去除空格函数
    def self_strip(self, str):
        str = str.strip()
        if str == '-':
            str = ''
        return str

    # 获取中文首字母
    def single_get_first(self, str):
        str = str.encode('gbk')
        try:
            ord(str)
            return str.upper()
        except:
            asc = ord(str[0]) * 256 + ord(str[1]) - 65536
            if asc >= -20319 and asc <= -20284:
                return 'A'
            if asc >= -20283 and asc <= -19776:
                return 'B'
            if asc >= -19775 and asc <= -19219:
                return 'C'
            if asc >= -19218 and asc <= -18711:
                return 'D'
            if asc >= -18710 and asc <= -18527:
                return 'E'
            if asc >= -18526 and asc <= -18240:
                return 'F'
            if asc >= -18239 and asc <= -17923:
                return 'G'
            if asc >= -17922 and asc <= -17418:
                return 'H'
            if asc >= -17417 and asc <= -16475:
                return 'J'
            if asc >= -16474 and asc <= -16213:
                return 'K'
            if asc >= -16212 and asc <= -15641:
                return 'L'
            if asc >= -15640 and asc <= -15166:
                return 'M'
            if asc >= -15165 and asc <= -14923:
                return 'N'
            if asc >= -14922 and asc <= -14915:
                return 'O'
            if asc >= -14914 and asc <= -14631:
                return 'P'
            if asc >= -14630 and asc <= -14150:
                return 'Q'
            if asc >= -14149 and asc <= -14091:
                return 'R'
            if asc >= -14090 and asc <= -13119:
                return 'S'
            if asc >= -13118 and asc <= -12839:
                return 'T'
            if asc >= -12838 and asc <= -12557:
                return 'W'
            if asc >= -12556 and asc <= -11848:
                return 'X'
            if asc >= -11847 and asc <= -11056:
                return 'Y'
            if asc >= -11055 and asc <= -10247:
                return 'Z'
            return ''

    # 获取中文字符串首字母
    def multi_get_letter(self, str):
        letters = ''
        for s in str:
            letters += self.single_get_first(s)
        return letters

    # 获取文件后缀
    def file_extension(self, path):
        return os.path.splitext(path)[1]

    # 图片文件下载
    def urllib_download(self, image_url, file_name):
        # 设置消息头
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/35.0.1916.114 Safari/537.36',
            'Cookie': 'AspxAutoDetectCookieSupport=1'
        }
        request = urllib2.Request(image_url, None, header)
        response = urllib2.urlopen(request)
        with open('./images/'+file_name, "wb") as f:
            f.write(response.read())