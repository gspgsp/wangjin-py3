# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .sqlutil import SqlUtil
from wdzj.items import PlatformItem
from wdzj.items import ManagersItem
from wdzj.items import PhotosItem
from wdzj.items import IcbcItem
from wdzj.items import DataItem
from wdzj.items import ScoreItem
from wdzj.items import ArticleItem
from wdzj.items import IndustryDataItem
from wdzj.items import StatisticalDataItem
from wdzj.items import MonthDataItem

class WdzjPipeline(object):
    def process_item(self, item, spider):
        sqlutil = SqlUtil()
        # 平台信息
        if isinstance(item, PlatformItem):
            ret = sqlutil.is_exist('fanwe_platform', ['plat_id'], item)
            if ret[0] == 1:
                # 更新数据
                sqlutil.update_data('fanwe_platform', 'plat_id = '+item['plat_id'], item)
            else:
                sqlutil.insert_data('fanwe_platform', item)

        # 平台高管
        if isinstance(item, ManagersItem):
            sqlutil.insert_data('fanwe_platform_managers', item)

        # 平台图片
        if isinstance(item, PhotosItem):
            sqlutil.insert_data('fanwe_platform_photos', item)

        # 平台工商备案信息
        if isinstance(item, IcbcItem):
            ret = sqlutil.is_exist('fanwe_platform_icbc', ['plat_id'], item)
            if ret[0] == 1:
                # 更新数据
                sqlutil.update_data('fanwe_platform_icbc', 'plat_id = ' + item['plat_id'], item)
            else:
                sqlutil.insert_data('fanwe_platform_icbc', item)

        # 平台数据
        if isinstance(item, DataItem):
            ret = sqlutil.is_exist('fanwe_platform_data', ['plat_id', 'dateline'], item)
            platItem = PlatformItem()
            platItem['one_month_vol'] = item.pop('plat_one_month_vol')
            platItem['reference_rate'] = item.pop('plat_reference_rate')
            platItem['investment_horizon'] = item.pop('plat_investment_horizon')
            platItem['yesterday_vol'] = item['trading_volume']
            platItem['yesterday_tbp'] = item['not_repay']
            if ret[0] == 1:
                sqlutil.update_data('fanwe_platform_data', 'plat_id = ' + item['plat_id'] + " AND dateline = '" + item['dateline'] + "'", item)
                # print('平台{' + item['plat_id'] + '}' + item['dateline'] + '数据已经存在')
            else:
                # 插入平台数据
                sqlutil.insert_data('fanwe_platform_data', item)
            # 平台信息表数据更新
            sqlutil.update_data('fanwe_platform', 'plat_id = '+item['plat_id'], platItem)

        # 平台评级
        if isinstance(item, ScoreItem):
            ret = sqlutil.is_exist('fanwe_platform_score', ['plat_id', 'period'], item)
            if ret[0] == 1:
                sqlutil.update_data('fanwe_platform_score', 'plat_id = ' + item['plat_id'] + " AND period = '" + item['period'] + "'", item)
                # print('平台{' + item['plat_id'] + '}' + item['period'] + '评级信息已经存在')
            else:
                sqlutil.insert_data('fanwe_platform_score', item)

        # 平台资讯/公告
        # if isinstance(item, ArticleItem):
        #     ret = sqlutil.is_exist('fanwe_article', ['plat_id', 'title'], item)
        #     if ret[0] == 1:
        #         print('资讯{' + item['title'] + '}已经存在')
        #     else:
        #         sqlutil.insert_data('fanwe_article', item)

        # 资讯
        if isinstance(item, ArticleItem):
            ret = sqlutil.is_exist('fanwe_article', ['original_id'], item)
            if ret[0] == 1:
                # 更新数据
                sqlutil.update_data('fanwe_article', 'original_id = ' + item['original_id'], item)
            else:
                sqlutil.insert_data('fanwe_article', item)

        # 平台行业数据
        if isinstance(item, IndustryDataItem):
            ret = sqlutil.is_exist('fanwe_platform_industry_data', ['period', 'type'], item)
            if ret[0] == 1:
                print('{' + item['period'] + '}类型{' + str(item['type']) + '}行业数据已经存在')
            else:
                sqlutil.insert_data('fanwe_platform_industry_data', item)

        # 平台月度数据
        if isinstance(item, MonthDataItem):
            ret = sqlutil.is_exist('fanwe_platform_month_data', ['period'], item)
            if ret[0] == 1:
                sqlutil.update_data('fanwe_platform_month_data', "period = '" + item['period'] + "'", item)
            else:
                sqlutil.insert_data('fanwe_platform_month_data', item)

        # 平台统计数据
        if isinstance(item, StatisticalDataItem):
            ret = sqlutil.is_exist('fanwe_platform_statistical_data', ['period', 'type', 'index'], item)
            if ret[0] == 1:
                period = item.pop('period')
                type = item.pop('type')
                index = item.pop('index')
                sqlutil.update_data('fanwe_platform_statistical_data', "`period` = '" + period + "' AND `type` = " + str(type) + " AND `index` = '" + index + "'", item)
            else:
                sqlutil.insert_data('fanwe_platform_statistical_data', item)

        return item