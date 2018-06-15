# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# 平台信息
class PlatformItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 平台id
    plat_id = scrapy.Field()
    # 平台名称
    name = scrapy.Field()
    # 平台图标
    icon = scrapy.Field()
    # 平台标识
    sign = scrapy.Field()
    # 平台名称首字母
    initial = scrapy.Field()
    # 平台名称所有首字母
    all_initial = scrapy.Field()
    # 关注人数
    focus_nums = scrapy.Field()
    # 运营状态
    operation_state = scrapy.Field()
    # 平台背景
    background = scrapy.Field()
    # 热门方案
    hot_solution = scrapy.Field()
    # 参考利率
    reference_rate = scrapy.Field()
    # 投资期限
    investment_horizon = scrapy.Field()
    # 最新排名
    newest_rank = scrapy.Field()
    # 昨日成交量
    yesterday_vol = scrapy.Field()
    # 昨日待还余额
    yesterday_tbp = scrapy.Field()
    # 近30天成交量
    one_month_vol = scrapy.Field()
    # 债券转让类型
    transfer_type = scrapy.Field()
    # 保障模式
    security_mode = scrapy.Field()
    # 自动投标
    auto_bid = scrapy.Field()
    # 上线时间
    online_time = scrapy.Field()
    # 停业(问题)时间
    problem_time = scrapy.Field()
    # 问题类型
    problem_type = scrapy.Field()
    # 所在省份
    registered_place = scrapy.Field()
    # 所在城市
    registered_city = scrapy.Field()
    # 注册资金
    registered_amount = scrapy.Field()
    # 平台简介
    description = scrapy.Field()
    # 银行存管
    bank_deposit = scrapy.Field()
    # 融资记录
    financing_records = scrapy.Field()
    # 监管协会
    supervise_association = scrapy.Field()
    # 投标保障
    bid_security = scrapy.Field()
    # 官方网站
    official_website = scrapy.Field()
    # 公司地址
    company_address = scrapy.Field()
    # 400电话
    contact_number = scrapy.Field()
    # 公司电话
    company_tel = scrapy.Field()
    # 公司传真
    company_fax = scrapy.Field()
    # QQ群
    company_qq_group = scrapy.Field()
    # 服务邮箱
    service_email = scrapy.Field()
    # 客服QQ
    service_qq = scrapy.Field()
    # 充值费
    recharge_cost = scrapy.Field()
    # 提现费
    withdraw_cost = scrapy.Field()
    # 管理费
    manage_cost = scrapy.Field()
    # VIP费用
    vip_cost = scrapy.Field()
    # 转让费用
    transfer_cost = scrapy.Field()
    # 支付方式
    payment_type = scrapy.Field()

# 平台高管信息
class ManagersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 高管id
    id = scrapy.Field()
    # 平台id
    plat_id = scrapy.Field()
    # 高管名称
    name = scrapy.Field()
    # 高管头像
    picture = scrapy.Field()
    # 高管职位
    position = scrapy.Field()
    # 高管简介
    description = scrapy.Field()

# 平台图片信息
class PhotosItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 平台id
    plat_id = scrapy.Field()
    # 图片名称
    name = scrapy.Field()
    # 图片分类
    category = scrapy.Field()
    # 图片地址
    url = scrapy.Field()

# 平台工商信息
class IcbcItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 平台id
    plat_id = scrapy.Field()
    # 企业名称
    company_name = scrapy.Field()
    # 企业法人
    company_legal_person = scrapy.Field()
    # 公司类型
    company_type = scrapy.Field()
    # 股东结构
    company_structure = scrapy.Field()
    # 注册资本
    registered_capital = scrapy.Field()
    # 实缴资本
    contributed_capital = scrapy.Field()
    # 注册地址
    registered_address = scrapy.Field()
    # 开业日期
    start_date = scrapy.Field()
    # 核准日期
    approved_date = scrapy.Field()
    # 登记机关
    registration_authority = scrapy.Field()
    # 营业执照
    business_license = scrapy.Field()
    # 备案域名
    filing_domain = scrapy.Field()
    # 域名备案时间
    filling_date = scrapy.Field()
    # 备案单位性质
    filling_unit_properties = scrapy.Field()
    # 备案单位名称
    filling_unit_name = scrapy.Field()
    # ICP备案号
    icp_filling_no = scrapy.Field()
    # ICP许可证编号
    icp_license_no = scrapy.Field()

# 平台昨日核心数据
class DataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 平台id
    plat_id = scrapy.Field()
    # 日期
    dateline = scrapy.Field()
    # 成交量
    trading_volume = scrapy.Field()
    # 成交量排名
    trading_volume_rank = scrapy.Field()
    # 资金净流入
    capital_inflow = scrapy.Field()
    # 资金净流入排名
    capital_inflow_rank = scrapy.Field()
    # 待还余额
    not_repay = scrapy.Field()
    # 待还余额排名
    not_repay_rank = scrapy.Field()
    # 参考收益率
    reference_rate = scrapy.Field()
    # 参考收益率排名
    reference_rate_rank = scrapy.Field()
    # 平均借款期限
    loan_term = scrapy.Field()
    # 平均借款期限排名
    loan_term_rank = scrapy.Field()
    # 投资人数
    investment_nums = scrapy.Field()
    # 投资人数排名
    investment_nums_rank = scrapy.Field()
    # 人均投资金额
    investment_amount = scrapy.Field()
    # 人均投资金额排名
    investment_amount_rank = scrapy.Field()
    # 待收投资人数
    duein_investment_nums = scrapy.Field()
    # 待收投资人数排名
    duein_investment_nums_rank = scrapy.Field()
    # 借款人数
    borrow_nums = scrapy.Field()
    # 借款人数排名
    borrow_nums_rank = scrapy.Field()
    # 人均借款金额
    borrow_amount = scrapy.Field()
    # 人均借款金额排名
    borrow_amount_rank = scrapy.Field()
    # 借款标数
    bid_nums = scrapy.Field()
    # 借款标数排名
    bid_nums_rank = scrapy.Field()
    # 待还借款人数
    duein_borrow_nums = scrapy.Field()
    # 待还借款人数排名
    duein_borrow_nums_rank = scrapy.Field()
    # 参考利率
    plat_reference_rate = scrapy.Field()
    # 投资期限
    plat_investment_horizon = scrapy.Field()
    # 近30天成交量
    plat_one_month_vol = scrapy.Field()

# 平台评级信息
class ScoreItem(scrapy.Item):
    # 平台id
    plat_id = scrapy.Field()
    # 时间段
    period = scrapy.Field()
    # 评分
    score = scrapy.Field()
    # 排名
    ranking = scrapy.Field()
    # 排名上涨趋势
    trend = scrapy.Field()
    # 成交量评分
    turnover_score = scrapy.Field()
    # 成交量排名
    turnover_rank = scrapy.Field()
    # 借款人数评分
    borrowers_score = scrapy.Field()
    # 借款人数排名
    borrowers_rank = scrapy.Field()
    # 回本速度评分
    recovery_score = scrapy.Field()
    # 回本速度排名
    recovery_rank = scrapy.Field()
    # 信息透明度评分
    transparency_score = scrapy.Field()
    # 信息透明度排名
    transparency_rank = scrapy.Field()
    # 合规程度评分
    compliance_score = scrapy.Field()
    # 合规程度排名
    compliance_rank = scrapy.Field()

# 平台新闻资讯
class ArticleItem(scrapy.Item):
    # # 标题
    # title = scrapy.Field()
    # # 分类id
    # cate_id = scrapy.Field()
    # # 平台id
    # plat_id = scrapy.Field()
    # # 原文章id
    # original_id = scrapy.Field()
    # # 摘要
    # brief = scrapy.Field()
    # # 内容
    # content = scrapy.Field()
    # # 发布时间
    # create_time = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 缩略图
    icon = scrapy.Field()
    # 内容
    content = scrapy.Field()
    # 分类id
    cate_id = scrapy.Field()
    # 源文章id
    original_id = scrapy.Field()
    # 发布时间
    create_time = scrapy.Field()
    # 摘要
    brief = scrapy.Field()
    # 来源
    art_source = scrapy.Field()
    # 点击数
    click_count = scrapy.Field()

# 平台行业数据
class IndustryDataItem(scrapy.Item):
    # 时间区间
    period = scrapy.Field()
    # 指数类型
    type = scrapy.Field()
    # 指数
    index = scrapy.Field()

# 平台统计数据
class StatisticalDataItem(scrapy.Item):
    # 时间区间
    period = scrapy.Field()
    # 数据类型
    type = scrapy.Field()
    # 指数名称
    index = scrapy.Field()
    # 成交量(亿元)
    amount = scrapy.Field()
    # 综合参考收益率(%)
    income_rate = scrapy.Field()
    # 运营平台数量
    operate_plat_num = scrapy.Field()
    # 问题平台数量
    problem_plat_num = scrapy.Field()
    # 投资人数(万)
    bidder_num = scrapy.Field()
    # 借款人数(万)
    borrower_num = scrapy.Field()
    # 待收余额(亿元)
    balance_loans = scrapy.Field()
    # 平均借款期限(月)
    loan_period = scrapy.Field()

# 平台月度数据
class MonthDataItem(scrapy.Item):
    # 时间区间
    period = scrapy.Field()
    # 每日统计截止日期
    end_day = scrapy.Field()
    # 每月统计截止月份
    end_month = scrapy.Field()
    # 统计数据截止月份
    statis_month = scrapy.Field()
    # 成交指数
    amount_index = scrapy.Field()
    # 成交指数趋势
    amount_index_trend = scrapy.Field()
    # 人气指数
    popularity_index = scrapy.Field()
    # 人气指数趋势
    popularity_index_trend = scrapy.Field()
    # 新增停业问题平台数
    new_problem_plat_num = scrapy.Field()