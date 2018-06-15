#!/usr/bin/env python
# -*- coding: utf-8 -*-
# def multi_get_letter(str_input):
#   if isinstance(str_input, unicode):
#     unicode_str = str_input
#   else:
#     try:
#       unicode_str = str_input.decode('utf8')
#     except:
#       try:
#         unicode_str = str_input.decode('gbk')
#       except:
#         print 'unknown coding'
#         return
#   return_list = []
#   for one_unicode in unicode_str:
#     return_list.append(single_get_first(one_unicode))
#   return return_list
# def single_get_first(unicode1):
#   str1 = unicode1.encode('gbk')
#   try:
#     ord(str1)
#     return str1
#   except:
#     asc = ord(str1[0]) * 256 + ord(str1[1]) - 65536
#     if asc >= -20319 and asc <= -20284:
#       return 'a'
#     if asc >= -20283 and asc <= -19776:
#       return 'b'
#     if asc >= -19775 and asc <= -19219:
#       return 'c'
#     if asc >= -19218 and asc <= -18711:
#       return 'd'
#     if asc >= -18710 and asc <= -18527:
#       return 'e'
#     if asc >= -18526 and asc <= -18240:
#       return 'f'
#     if asc >= -18239 and asc <= -17923:
#       return 'g'
#     if asc >= -17922 and asc <= -17418:
#       return 'h'
#     if asc >= -17417 and asc <= -16475:
#       return 'j'
#     if asc >= -16474 and asc <= -16213:
#       return 'k'
#     if asc >= -16212 and asc <= -15641:
#       return 'l'
#     if asc >= -15640 and asc <= -15166:
#       return 'm'
#     if asc >= -15165 and asc <= -14923:
#       return 'n'
#     if asc >= -14922 and asc <= -14915:
#       return 'o'
#     if asc >= -14914 and asc <= -14631:
#       return 'p'
#     if asc >= -14630 and asc <= -14150:
#       return 'q'
#     if asc >= -14149 and asc <= -14091:
#       return 'r'
#     if asc >= -14090 and asc <= -13119:
#       return 's'
#     if asc >= -13118 and asc <= -12839:
#       return 't'
#     if asc >= -12838 and asc <= -12557:
#       return 'w'
#     if asc >= -12556 and asc <= -11848:
#       return 'x'
#     if asc >= -11847 and asc <= -11056:
#       return 'y'
#     if asc >= -11055 and asc <= -10247:
#       return 'z'
#     return ''
# def main(str_input):
#   a = multi_get_letter(str_input)
#   b = ''
#   for i in a:
#     b= b+i.upper()
#   print b
# import re
# def main(str_input):
#   b = re.sub("<a\s+[^<>]+>(?P<aContent>[^<>]+?)</a>", "\g<aContent>", str_input)
#   print b
# if __name__ == "__main__":
#   str_input = u'<p>	2018年<a id="neilianxitong" target="_blank" href="http://baike.wdzj.com/doc-view-2205.html">互联网金融监管</a>进入收官阶段，<a id="neilianxitong" target="_blank" href="http://www.wdzj.com/jhzt/171206/P2Pxy_140/">P2P行业</a>“<a id="neilianxitong" target="_blank" href="http://baike.wdzj.com/doc-view-3188.html">资产荒</a>”爆发，各大平台资产收紧，接连出现疯狂<a id="neilianxitong" target="_blank" href="http://baike.wdzj.com/doc-view-3178.html">抢标</a>，甚至无标可投的局面，与2017年年中资产爆棚的情况，有着明显反差，<a id="neilianxitong" target="_blank" href="http://www.wdzj.com/dangan/ppd/">拍拍贷</a>，<a id="neilianxitong" target="_blank" href="http://www.wdzj.com/dangan/wdw/">微贷网</a>，<a id="neilianxitong" target="_blank" href="http://www.wdzj.com/dangan/fhjr/">凤凰金融</a>等标杆企业也频频出现此类状况。相比之下，在垂直领域业务的<a id="neilianxitong" target="_blank" href="http://www.wdzj.com/jhzt/171121/hjpt_140/">互金平台</a>却迎来了春天，像是<a id="neilianxitong" target="_blank" href="http://www.wdzj.com/juhe/170630/cdyw_168/">车贷业务</a>平台<a id="neilianxitong" target="_blank" href="http://www.wdzj.com/dangan/bjd/">百金贷</a>，进入2018年后，平台交易额持续保持高速增长，连续跻身<a id="neilianxitong" target="_blank" href="http://www.wdzj.com/juhe/170630/cdxypm_168/">车贷行业排名</a>前10。这背后究竟隐藏着什么呢？</p>'
#   main(str_input)
import datetime
import time

# new_date =  datetime.datetime.today() + datetime.timedelta(-7)
# print(time.strftime('%Y%m%d', new_date.timetuple()))


# def extract_param(url, field):
#     import urlparse
#     params = urlparse.parse_qs(urlparse.urlparse(url).query)
#     return params[field]
#
# print(extract_param('https://www.wdzj.com/dangan/search?filter=e1&currentPage=2', 'filter'))
# registered_amount = '- （实缴资金：10000万元）'
# if registered_amount != '':
#     pos = registered_amount.find('（')
#     print(registered_amount[0:pos].strip() == '-')
#     if pos == -1:
#         registered_amount = registered_amount[0:-2]
#     else:
#         end = pos - 3
#         registered_amount = registered_amount[0:end]
# print(registered_amount)
# import urlparse
# import re
# url = 'https://www.wdzj.com/dangan/wtcf/dongtai/10425.html'
# parsed_uri = urlparse.urlparse(url)
# route = '{uri.path}'.format(uri=parsed_uri)
# print(re.search(r"\d+", route).group())

import re
str = 'var lists = [{"amount":703.61,"balanceLoans":5170.9,"bidderNum":160.6,"borrowerNum":164.89,"incomeRate":10.51,"loanPeriod":7.85,"operatePlatNumber":1419,"problemPlatNumber":43,"province":"\u6c11\u8425\u7cfb"},{"amount":168.12,"balanceLoans":1769.76,"bidderNum":38.37,"borrowerNum":39.4,"incomeRate":6.63,"loanPeriod":21.82,"operatePlatNumber":15,"problemPlatNumber":0,"province":"\u94f6\u884c\u7cfb"},{"amount":492.75,"balanceLoans":4353.48,"bidderNum":112.47,"borrowerNum":115.48,"incomeRate":7.93,"loanPeriod":14.09,"operatePlatNumber":112,"problemPlatNumber":0,"province":"\u4e0a\u5e02\u7cfb"},{"amount":149.86,"balanceLoans":1277.59,"bidderNum":34.2,"borrowerNum":35.12,"incomeRate":8.79,"loanPeriod":8.67,"operatePlatNumber":224,"problemPlatNumber":0,"province":"\u56fd\u8d44\u7cfb"},{"amount":862.14,"balanceLoans":5519.85,"bidderNum":196.78,"borrowerNum":202.04,"incomeRate":9.09,"loanPeriod":13.63,"operatePlatNumber":155,"problemPlatNumber":0,"province":"\u98ce\u6295\u7cfb"}];' \
      'var datahead = [];var orderKeys = \'amount\';' \
      'require.async([\'statics/js/shuju/listPage\']);'

print(re.search(r"var lists = (.*);var datahead", str, re.M|re.I).group(1))
