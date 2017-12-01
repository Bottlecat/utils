#coding:utf-8
import calendar, datetime
from functools import wraps
isleap = calendar.isleap


def datetimeFormat(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        fromtime = args[0]
        #格式化字符串
        datetime_format = '%Y%m%d'
        if isinstance(fromtime,basestring):
            fromtime = datetime.datetime.strptime(fromtime,datetime_format)
        else:
            fromtime = False
        kwargs.update({'transferTime':fromtime})
        return func(*args,**kwargs)
    return wrap


@datetimeFormat
def day_period(enddate,period,**kwargs):
    if kwargs.get('transferTime'):
        enddate = kwargs.get('transferTime')
    return enddate - datetime.timedelta(days=period)


@datetimeFormat
def month_period(enddate,period,**kwargs):
    if kwargs.get('transferTime'):
        enddate = kwargs.get('transferTime')
    year = enddate.year
    month = enddate.month
    day = enddate.day

    yeardelta,monthdelta = divmod(period,12)
    year -= yeardelta
    if month > monthdelta:
        month -= monthdelta
    else:
        year -= 1
        month = month + 12 - monthdelta
    if month in (4, 6, 9, 11):
        day = min(30, day)
    if month == 2:
        if isleap(year):
            day = min(29, day)
        else:
            day = min(28, day)
    return datetime.datetime(year, month, day)

@datetimeFormat
def year_period(enddate,period,**kwargs):
    if kwargs.get('transferTime'):
        enddate = kwargs.get('transferTime')
    year = enddate.year
    month = enddate.month
    day = enddate.day

    year -= period
    if month == 2:
        if isleap(year):
            day = min(29, day)
        else:
            day = min(28, day)
    return datetime.datetime(year, month, day)
   
@datetimeFormat
def seasonRange(fromtime, n, **kwargs):
    '''根据指定日期获取前n季度的开始和结束日期'''
    if kwargs.get('transferTime'):
        fromtime = kwargs.get('transferTime')
   
    year = fromtime.year
    season = (fromtime.month - 1) / 3

    # 最近一季度结束时间
    if season == 0:
        e_date = datetime.datetime(year, 1, 1) - datetime.timedelta(1)
    else:
        e_date = datetime.datetime(year, season*3+1, 1) - datetime.timedelta(1)
    #最近一季度开始时间
    s_date = datetime.datetime(e_date.year, e_date.month - 2, 1)

    #按往前n季度计算，获取开始、结束时间
    start_date = month_period(s_date, 3*(n-1))
    end_date = month_period(e_date+datetime.timedelta(1), 3*(n-1)) - datetime.timedelta(1)

    return start_date, end_date

@datetimeFormat
def yearRange(fromtime, n ,**kwargs):
    if kwargs.get('transferTime'):
        fromtime = kwargs.get('transferTime')

    year = fromtime.year - n
    s_date = datetime.datetime(year, 1, 1)
    e_date = datetime.datetime(year, 12, 31)
    return s_date, e_date


if __name__ == '__main__':
    #输入datetime类型
    now = datetime.date.today()
    #输入字符串类型
    fromtime = '20160104'

    print day_period(fromtime,4)
    print day_period(now,4)

    print month_period(fromtime,1)
    print month_period(now,1)

    print year_period(fromtime,1)
    print year_period(now,1)

   
    print yearRange(fromtime,2)
    print yearRange(now,2)

    print seasonRange(fromtime,1)
    print seasonRange(now,1)
