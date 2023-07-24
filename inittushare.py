import numpy as np
import pandas as pd
import tushare as ts
from sqlalchemy import create_engine
import datetime
import tqdm
import os
import json
import baostock as bs

#初始化


def init_engine(database):
    engine = create_engine('mysql+pymysql://root:zbiao@localhost/%s?charset=utf8' % database)
    return engine


def init_ts(ts, token):
    ts.set_token(token)
    pro = ts.pro_api()
    return pro
#获得日期


def get_date(engine):
    startdate = pd.read_sql("select distinct trade_date from dayk order by trade_date desc limit 1;", engine)
    if startdate.empty:
        with open("init_ts.log", "w"):
            startdate = "2000-01-01"
    else:
        if os.path.exists("init_ts.log"):
            with open("init_ts.log", "r") as rf:
                errordate = rf.read()
                errordate = errordate.replace("下载数据错误日期：", "")
                errordate = errordate.split("\n")
            name_num = 1
            while os.path.exists("init_ts%s.log" % name_num):
                name_num += 1
            os.rename("init_ts.log", "init_ts%s.log" % name_num)
            with open("init_ts.log", "w"):
                pass
        else:
            with open("init_ts.log", "w"):
                pass
        startdate = startdate.iloc[0][0].strftime("%Y-%m-%d")
    lg = bs.login()
    rs = bs.query_history_k_data_plus("sh.000001","date,code,open,high,low,close,preclose,volume,amount,pctChg",start_date='%s' % startdate, end_date='', frequency="d")
    rsdata = rs.get_data()
    date_list = rsdata["date"].values
    date_list = np.append(date_list, errordate[:-1])
    return date_list


def from_ts_to_mysql(pro, engine, datestr: str):
    try:
        df = pro.daily(**{"ts_code": "", "trade_date": datestr, "start_date": "", "end_date": "", "offset": "","limit": ""}, fields=["ts_code", "trade_date", "open", "high", "low", "close", "vol", "amount"])
        df.to_sql("dayk", engine, if_exists="append", index=None)
    except:
        with open("init_ts.log", "a") as af:
            af.write("下载数据错误日期：%s\n" % datestr)


def main():
    engine = init_engine("tushare")
    date_list = get_date(engine)
    pro = init_ts(ts, "a1a821dfab3a1110e4c9f7e99ed4ca4484f00ea3bb76cc5bbb5419f0")
    for datestr in tqdm.tqdm(date_list):
        datestr = datestr.replace("-", "")
        from_ts_to_mysql(pro, engine, datestr)


if __name__ == "__main__":
    main()
