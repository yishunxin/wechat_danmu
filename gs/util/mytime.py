# -*- coding:utf-8 -*-
import logging
import calendar
import datetime
import time
import types
from datetime import timedelta, date
from time import strftime, localtime
from dateutil.relativedelta import relativedelta

logger = logging.getLogger('performance')
__author__ = 'weijingqi'

DEFAULT_TIME_FORMAT = '%Y-%m-%d %H:%M'
FORMAT_YMDHMS = '%Y-%m-%d %H:%M:%S'
FORMAT_YMDHMS2 = '%Y%m%d%H%M%S'
FORMAT_YMD = '%Y-%m-%d'
FORMAT_YMD2 = '%Y%m%d'
FORMAT_HM = '%H:%M'
FORMAT_MD = '%m%d'

'''
@brief:获取当前时间的秒
'''


def get_now_seconds():
    return int(time.time())


'''
@brief:获取当前时间
'''


def get_now_datetime():
    return datetime.datetime.now()


def get_day_begin(busi_time=None):
    if busi_time is None:
        busi_time = get_now_datetime()
    else:
        busi_time = parse_time(busi_time)
    return datetime.datetime.combine(busi_time, datetime.time.min)


def get_day_end(busi_time=None):
    if busi_time is None:
        busi_time = get_now_datetime()
    else:
        busi_time = parse_time(busi_time)
    return datetime.datetime.combine(busi_time, datetime.time.max)


def get_day(busi_time=None):
    if busi_time is None:
        busi_time = get_now_datetime()
    else:
        busi_time = parse_time(busi_time)
    if isinstance(busi_time, datetime.datetime):
        return datetime.datetime.date(busi_time)
    return busi_time


'''
@brief:格式化时间
'''


def format_time(busi_time, default_format=DEFAULT_TIME_FORMAT):
    if not busi_time:
        return ''
    return busi_time if isinstance(busi_time, types.StringTypes) else busi_time.strftime(default_format)


def format_time_ymd(busi_time):
    return format_time(busi_time, FORMAT_YMD2)


def format_time_ymd2(busi_time):
    return format_time(busi_time, FORMAT_YMD)


def add_delta(busi_time=None, **kwargs):
    if not busi_time:
        busi_time = get_now_datetime()
    return busi_time + datetime.timedelta(**kwargs)


'''
@brief: 解析时间
'''


def parse_time(busi_time, default_format=DEFAULT_TIME_FORMAT):
    if not busi_time:
        return None
    if not isinstance(busi_time, types.StringTypes):
        return busi_time

    try:
        return datetime.datetime.strptime(busi_time, default_format)
    except ValueError:
        try:
            return datetime.datetime.strptime(busi_time, FORMAT_YMD)
        except ValueError:
            try:
                return datetime.datetime.strptime(busi_time, FORMAT_YMDHMS)
            except ValueError:
                try:
                    return datetime.datetime.strptime(busi_time, FORMAT_YMD2)
                except ValueError:
                    try:
                        return datetime.datetime.strptime(busi_time, FORMAT_YMDHMS2)
                    except ValueError:
                        return None


'''
start_time: 2016-05-01
end_time: 2016-05-03
ret: 2016-05-01, 2016-05-02, 2016-05-03
'''


def days_between(start_time, end_time):
    start_time = parse_time(start_time)
    end_time = parse_time(end_time)
    dates = []
    t_start = start_time
    while format_time_ymd(t_start) <= format_time_ymd(end_time):
        dates.append(t_start)
        t_start = add_delta(t_start, days=1)
    return dates


weeks = [u'周一', u'周二', u'周三', u'周四', u'周五', u'周六', u'周日']


def format_week(busi_time):
    if not busi_time:
        return ''
    busi_time = parse_time(busi_time)
    return '%s%s' % (weeks[busi_time.weekday()], format_time(busi_time, '%m%d'))


def get_weekregion(day=None):
    if day is None:
        day = get_now_datetime()
    else:
        day = parse_time(day)
    if not day:
        return None, None
    day = parse_time(format_time_ymd(day))
    wd = day.weekday()
    return add_delta(day, days=0 - wd), add_delta(day, days=6 - wd)


def get_monthregion(day=None):
    if day is None:
        day = get_now_datetime()
    else:
        day = parse_time(day)
    if not day:
        return None, None
    day = parse_time(format_time_ymd(day))
    day = format_time_ymd(day)
    year = int(day[0:4])
    month = int(day[4:6])
    month_range = calendar.monthrange(year, month)
    return datetime.datetime(year, month, 1), datetime.datetime(year, month, month_range[1])


def format_meeting_time(busi_time):
    if not busi_time:
        return ''
    busi_time = parse_time(busi_time)
    return '%s%s' % (weeks[busi_time.weekday()], format_time(busi_time, '%m%d %H:%M'))


def num2datetime(t_num):
    return datetime.datetime.fromtimestamp(float(t_num))


def datetime2num(dt):
    try:
        return time.mktime(dt.timetuple())
    except Exception, e:
        print e
        return 0


def mkday(year, month, day):
    try:
        return datetime.datetime(int(year), int(month), int(day))
    except Exception, e:
        print e
        return None


def format_week2(busi_time):
    if not busi_time:
        return ''
    busi_time = parse_time(busi_time)
    return '%s' % weeks[int(busi_time.strftime('%w'))]


def latest_hour():
    now = get_now_datetime()
    now = add_delta(now, hours=1)
    now = add_delta(now, minutes=-now.minute)
    now = add_delta(now, seconds=-now.second)
    now = add_delta(now, microseconds=-now.microsecond)
    return now


def to_hm(seconds):
    seconds = int(seconds)
    t_str = ''
    h = seconds // 3600
    if h:
        t_str += str(h) + u'时'
    seconds %= 3600
    m = seconds // 60
    if m or h:
        t_str += str(m) + u'分'
    else:
        t_str += u'小于1分'
    return t_str


def to_hm2(seconds):
    seconds = int(seconds)
    h = seconds // 3600
    seconds %= 3600
    m = seconds // 60
    return h, m


year = strftime("%Y", localtime())
mon = strftime("%m", localtime())
day = strftime("%d", localtime())
hour = strftime("%H", localtime())
min = strftime("%M", localtime())
sec = strftime("%S", localtime())


def today():
    '''''
    get today,date format="YYYY-MM-DD"
    '''''
    return date.today()


def get_day_of_day(n=0):
    '''
    if n>=0,date is larger than today
    if n<0,date is less than today
    date format = "YYYY-MM-DD"
    '''
    if (n < 0):
        n = abs(n)
        return date.today() - timedelta(days=n)
    else:
        return date.today() + timedelta(days=n)


def get_days_of_month(year, mon):
    '''''
    get days of month
    '''
    return calendar.monthrange(year, mon)[1]


def get_firstday_of_month(year, mon):
    '''''
    get the first day of month
    date format = "YYYY-MM-DD"
    '''
    days = "01"
    if (int(mon) < 10):
        mon = "0" + str(int(mon))
    arr = (year, mon, days)
    return "-".join("%s" % i for i in arr)


def get_lastday_of_month(year, mon):
    '''''
    get the last day of month
    date format = "YYYY-MM-DD"
    '''
    days = calendar.monthrange(year, mon)[1]
    mon = addzero(mon)
    arr = (year, mon, days)
    return "-".join("%s" % i for i in arr)


def get_firstday_month(n=0):
    '''''
    get the first day of month from today
    n is how many months
    '''
    (y, m, d) = getyearandmonth(n)
    d = "01"
    arr = (y, m, d)
    return "-".join("%s" % i for i in arr)


def get_lastday_month(n=0):
    '''''
    get the last day of month from today
    n is how many months
    '''
    return "-".join("%s" % i for i in getyearandmonth(n))


def getyearandmonth(n=0):
    '''''
    get the year,month,days from today
    befor or after n months
    '''
    thisyear = int(year)
    thismon = int(mon)
    totalmon = thismon + n
    if (n >= 0):
        if (totalmon <= 12):
            days = str(get_days_of_month(thisyear, totalmon))
            totalmon = addzero(totalmon)
            return (year, totalmon, days)
        else:
            i = totalmon / 12
            j = totalmon % 12
            if (j == 0):
                i -= 1
                j = 12
            thisyear += i
            days = str(get_days_of_month(thisyear, j))
            j = addzero(j)
            return (str(thisyear), str(j), days)
    else:
        if ((totalmon > 0) and (totalmon < 12)):
            days = str(get_days_of_month(thisyear, totalmon))
            totalmon = addzero(totalmon)
            return (year, totalmon, days)
        else:
            i = totalmon / 12
            j = totalmon % 12
            if (j == 0):
                i -= 1
                j = 12
            thisyear += i
            days = str(get_days_of_month(thisyear, j))
            j = addzero(j)
            return (str(thisyear), str(j), days)


def addzero(n):
    '''''
    add 0 before 0-9
    return 01-09
    '''
    nabs = abs(int(n))
    if (nabs < 10):
        return "0" + str(nabs)
    else:
        return nabs


def get_today_month(n=0):
    '''''
    获取当前日期前后N月的日期
    date format = "YYYY-MM-DD"
    '''
    t = get_now_datetime()
    # t = mkday(2016, 1, 31)
    return t + relativedelta(months=n)
    # (y, m, d) = getyearandmonth(n)
    # arr = (y, m, d)
    # if (int(day) < int(d)):
    #     arr = (y, m, day)
    # return "-".join("%s" % i for i in arr)


def performance(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        r = func(*args, **kwargs)
        end = time.time()
        logger.info(msg='call %s in %fs' % (func.__name__, (end - start)))
        return r
    wrapper.func_name = func.func_name
    return wrapper
