# -*- coding:utf-8 -*-

import MySQLdb
from wdzj import settings

class SqlUtil:

    def __init__(self):
        # 打开数据库连接
        self.db = MySQLdb.connect(host=settings.MYSQL_HOSTS, user=settings.MYSQL_USER, passwd=settings.MYSQL_PASSWORD,
                                  db=settings.MYSQL_DB, use_unicode=True, charset="utf8")
        # 使用cursor()方法获取操作游标
        self.cursor = self.db.cursor()

    # 插入表数据
    def insert_data(self, table, item):
        sql = "INSERT INTO " + table + " ({fields}) VALUES ({values})"
        fields = ''
        values = ''
        value = []
        for field in item.fields:
            if field in item and item[field]:
                fields += '`' + field +'`, '
                values += '%s, '
                value.append(item[field])
        fields = fields[0:-2]
        values = values[0:-2]
        fdict = {'fields': fields, 'values': values}
        sql = sql.format(**fdict)
        self.cursor.execute(sql, value)
        self.db.commit()

    # 修改表数据
    def update_data(self, table, where, item):
        sql = "UPDATE {table} SET {sets} WHERE {where}"
        sets = ''
        value = []
        for field in item.fields:
            if field in item and item[field]:
                sets += '`' + field + "` = %s, "
                value.append(item[field])
        sets = sets[0:-2]
        fdict = {
            'table': table,
            'sets': sets,
            'where': where
        }
        sql = sql.format(**fdict)
        self.cursor.execute(sql, value)
        self.db.commit()

    # 判断表数据是否存在
    def is_exist(self, table, fields, item):
        sql = "SELECT EXISTS(SELECT 1 FROM {table} WHERE {where})"
        where = ''
        value = []
        for field in fields:
            where += '`' + field+"` = %s AND "
            value.append(item[field])
        where = where[0:-5]
        fdict = {
            'table': table,
            'where': where
        }
        sql = sql.format(**fdict)
        self.cursor.execute(sql, value)
        return self.cursor.fetchall()[0]

    # 处理平台近7日、近30日统计数据
    def deal_platform_data(self, start_time_7days, start_time_30days, end_time):
        # 处理近7日数据
        sql_7days = "UPDATE fanwe_platform_data d JOIN (SELECT plat_id, SUM(trading_volume) AS trading_volume_7days, SUM(investment_nums) AS investment_nums_7days," \
              "SUM(borrow_nums) AS borrow_nums_7days, FORMAT(SUM(reference_rate)/COUNT(id), 2) AS reference_rate_7days, FORMAT(SUM(loan_term)/COUNT(id), 2) AS loan_term_7days, " \
              "FORMAT(SUM(investment_amount)/COUNT(id), 2) AS investment_amount_7days, FORMAT(SUM(borrow_amount)/COUNT(id), 2) AS borrow_amount_7days FROM fanwe_platform_data " \
              "WHERE dateline > '"+start_time_7days+"' GROUP BY plat_id) t ON d.plat_id = t.plat_id SET d.trading_volume_7days = t.trading_volume_7days, d.investment_nums_7days = t.investment_nums_7days, " \
              "d.borrow_nums_7days = t.borrow_nums_7days, d.reference_rate_7days = t.reference_rate_7days, d.loan_term_7days = t.loan_term_7days, d.investment_amount_7days = t.investment_amount_7days, " \
              "d.borrow_amount_7days = t.borrow_amount_7days WHERE d.dateline = '"+end_time+"'"
        self.cursor.execute(sql_7days)
        # 处理近30日数据
        sql_30days = "UPDATE fanwe_platform_data d JOIN (SELECT plat_id, SUM(trading_volume) AS trading_volume_30days, SUM(investment_nums) AS investment_nums_30days," \
                    "SUM(borrow_nums) AS borrow_nums_30days, FORMAT(SUM(reference_rate)/COUNT(id), 2) AS reference_rate_30days, FORMAT(SUM(loan_term)/COUNT(id), 2) AS loan_term_30days, " \
                    "FORMAT(SUM(investment_amount)/COUNT(id), 2) AS investment_amount_30days, FORMAT(SUM(borrow_amount)/COUNT(id), 2) AS borrow_amount_30days FROM fanwe_platform_data " \
                    "WHERE dateline > '" + start_time_30days + "' GROUP BY plat_id) t ON d.plat_id = t.plat_id SET d.trading_volume_30days = t.trading_volume_30days, d.investment_nums_30days = t.investment_nums_30days, " \
                    "d.borrow_nums_30days = t.borrow_nums_30days, d.reference_rate_30days = t.reference_rate_30days, d.loan_term_30days = t.loan_term_30days, d.investment_amount_30days = t.investment_amount_30days, " \
                    "d.borrow_amount_30days = t.borrow_amount_30days WHERE d.dateline = '" + end_time + "'"
        self.cursor.execute(sql_30days)
        self.db.commit()

    # 处理平台主表评级信息
    def deal_platform_score(self, month):
        # 先清空排名
        sql = "UPDATE fanwe_platform SET newest_score = 0, newest_rank = 101, newest_period = '', newest_trend = 0 WHERE newest_rank <= 100"
        self.cursor.execute(sql)
        # 更新主表排名信息
        sql2 = "UPDATE fanwe_platform_score s JOIN fanwe_platform p ON s.plat_id = p.plat_id SET p.newest_score = s.score, p.newest_rank = s.ranking, " \
              "p.newest_period = FROM_UNIXTIME(UNIX_TIMESTAMP(CONCAT(s.period, '-01')), '%y年%c月'), p.newest_trend = s.trend WHERE s.period = '"+month+"' AND p.operation_state = 1"
        print(sql2)
        self.cursor.execute(sql2)
        self.db.commit()

    def update_statis_month(self, period, statis_month):
        # 更新统计截止月份
        sql = "UPDATE fanwe_platform_month_data SET statis_month = '" + statis_month + "' WHERE period = '" + period + "'"
        self.cursor.execute(sql)
        self.db.commit()