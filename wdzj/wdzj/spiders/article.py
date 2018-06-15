# -*- coding: utf-8 -*-
import re
import sys
import time
import json
import scrapy
import urllib2
import random
from bs4 import BeautifulSoup
from scrapy.http import Request
from wdzj.wdzj.items import ArticleItem
from qiniu import Auth, put_file, etag, urlsafe_base64_encode


class ArticleSpider(scrapy.Spider):
    name = 'article'

    allowed_domains = ['wdzj.com']
    bash_url = 'https://www.wdzj.com/news/'


    def start_requests(self):
        yield Request(self.bash_url, self.parse)

    def parse(self, response):
        tabs = [0,1,2,3]
        for i in tabs:
            tab = BeautifulSoup(response.text, 'lxml').find('div', class_='tab-cont').find_all('div', class_="tab-list")[i]
            imgs = tab.find_all('div', class_="img")
            for im in imgs:
                icon = im.find('img').attrs['data-original']
                infourl = 'https:'+im.find('a').attrs['href']
                yield Request(infourl, callback=self.get_news_info, meta={'tab_id': i, 'icon': icon})

    # 获取资讯详情页
    def get_news_info(self, response):
        item = ArticleItem()
        tab_id = response.meta['tab_id']
        soup = BeautifulSoup(response.text, 'lxml')
        title = soup.find('h1', class_="s-title").get_text()
        icon = 'https://www.wdzj.com'+ response.meta['icon']
        # zy = self.self_strip(soup.find('div', class_="s-zy").find('span').get_text())
        start = response.url.rfind('/') + 1
        end = response.url.rfind('.html')
        original_id = response.url[start:end]

        cate_id = self.get_cate_id(tab_id)
        content = soup.find('div', class_="c-cen").prettify().replace('网贷之家', '网金之家')
        content = re.sub("<a\s+[^<>]+>(?P<aContent>[^<>]+?)</a>", "\g<aContent>", content)

        index = original_id.find('-')
        s_lenth = len(soup.find('div', class_="show-box").find('div', class_="s-bq").find_all('span'))
        if index == -1 and s_lenth >= 2:
            zy = soup.find('div', class_="s-zy").find('span')
            if zy:
                zy = self.self_strip(zy.get_text())

            bf = soup.find('div', class_="show-box").find('div', class_="s-bq").find_all('span')[1]
            source = '网金之家'
            if bf:
                bf = self.self_strip(bf.get_text())
                source = re.sub('网贷之家', '网金之家', bf)

            im_start = response.meta['icon'].rfind('/') + 1
            file_name = response.meta['icon'][im_start:]
            self.urllib_download(icon, file_name)

            self.upload_image(file_name)

            img_url = 'http://pa95ogwp4.bkt.clouddn.com/' + file_name
            click_count = random.randint(500,2000)

            item['title'] = title
            item['click_count'] = click_count
            item['icon'] = img_url
            item['content'] = content
            item['cate_id'] = cate_id
            item['original_id'] = original_id
            item['create_time'] = time.time()
            item['brief'] = zy
            item['art_source'] = source.replace('来源：', '')
            yield item

    def get_cate_id(self, tab_id):
        switcher = {
            0: 1,
            1: 2,
            2: 3,
            3: 4,
        }
        return switcher.get(tab_id)

    def upload_image(self,file_name):
        access_key = 'Wlzx_o-SAmn38Hp43BgOrw1YGrci8oNIo7GHGIzK'
        secret_key = 'SmA6FsaIhKf0q3_4ZrLu-2vqpfFcqbxlcYq-RU95'

        q = Auth(access_key, secret_key)

        bucket_name = 'wangjin-images-public'

        key = file_name

        policy ={
            'scope': bucket_name+':'+ key
        }

        token = q.upload_token(bucket_name, key, 3600, policy)

        localfile = './images/' + file_name
        info = put_file(token, key, localfile)

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
        with open('./images/' + file_name, "wb") as f:
            f.write(response.read())

    # 自定义字符串去除空格函数
    def self_strip(self, str):
        str = str.strip()
        if str == '-':
            str = ''
        return str





