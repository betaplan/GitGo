import requests
import pandas as pd
import time
import json
import os
import csv
import numpy as np

file = r'D:\eastmoney\stock_data.csv'  # 生成文件路径
filename = r'D:\eastmoney'


def get_json(url):  # 获取JSON
    try:
        r = requests.get(url)  # 抓取网页返回json信息
        r.raise_for_status()
        r.encoding = 'utf-8'
        # print(r.json())
        # with open(r"C:\Users\xxp\.spyder-py3\testcode\tmp.txt", "w") as fp:
        # fp.write(json.dumps(r.json(),indent=4,ensure_ascii=False)) # txt测试是否成功获取网页
        return r.json()
    except:
        return 'false'


def get_stock_info(result):  # 获取某个股票的信息 result 为dict类型
    items_all = []
    items_finish = []
    # "序号	代码	名称	相关链接	最新价	涨跌幅	涨跌额	成交量(手)	成交额	振幅	最高	最低	今开	昨收	量比	换手率	市盈率(动态)	市净率\n"
    all_name = result.get("data").get("diff")  # list类型
    for i in range(0, len(all_name) - 1):  # 数组长度限定30交易日内数据
        item = all_name[i]  # 获取数据 dict类型
        items_all += [item['f12'], item['f14']]

    for i in range(0, len(items_all), 2):  # 转成二维数组
        items_finish.append(items_all[i:i + 2])
        # print(items_finish[1])
    # 下述注释部分为方法二 也可以取得数据 方法主要是为了后续我做数据库存写操作方便些
    # if os.path.exists(filename):#文件路径检测
    #     #print("path exists")
    #     df=pd.DataFrame(data=all_name,columns=['f12','f14'])
    #     df['f12'] = '#' + df['f12'] #防止0在保存时候被去除
    #     df.to_csv(file,index=False,encoding='utf_8_sig')
    #     print ('文件创建成功')
    # else:
    #     os.makedirs(filename)
    #     print('create path success')
    # return ''
    if os.path.exists(filename):  # 文件路径检测
        # print("path exists")
        df = pd.DataFrame(data=items_finish, columns=['code', 'name'])
        df['code'] = '#' + df['code']  # 防止0在保存时候被去除
        df.to_csv(file, index=False, encoding='utf_8_sig')
        print('文件创建成功')
    else:
        os.makedirs(filename)
        print('create path success')
    return ''


def main():
    url = 'http://31.push2.eastmoney.com/api/qt/clist/get?pn=1&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152'  # 1591683995 为时间戳
    # 此部分url删减了部分不需要的内容
    stock_info = get_json(url)  # 获取json数据
    # print(stock_info)
    get_stock_info(stock_info)  # 对数据进行处理


if __name__ == '__main__':  # 在其他文件import这个py文件时,不会自动运行主函数
    main()