import json
import time
import redis
from datetime import datetime, timedelta
from functools import partial, wraps
from pytz import timezone
from uuid import uuid4
from redis.exceptions import WatchError

g_redis_db = redis.Redis()

success = 0
TZ = "Asia/Shanghai"


def cache_with_lock(func=None, *, lock_name=None, dft=None,
                    conn=None, acquire_timeout=10, lock_timeout=10):
    if func is None:
        return partial(cache_with_lock,
                       dft=dft,
                       lock_name=lock_name,
                       conn=conn,
                       acquire_timeout=acquire_timeout,
                       lock_timeout=lock_timeout)
    conn = conn or g_redis_db

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        key = lock_name or str(args) + json.dumps(kwargs)
        locked = redis_acquire_lock(
            conn=conn,
            key=key,
            acquire_timeout=acquire_timeout,
            lock_timeout=lock_timeout)
        if not locked:
            print('already locked')
            return dft
        try:
            return func(self, *args, **kwargs)
        finally:
            redis_release_lock(conn, key, locked)
    return wrapper


def redis_acquire_lock(conn, key, acquire_timeout=100, lock_timeout=100):
    identifier = str(uuid4())
    lock_name = key + '.lock'
    end = time.time() + acquire_timeout
    while time.time() < end:
        if conn.set(lock_name, identifier, ex=lock_timeout, nx=True):
            return identifier
        elif not conn.ttl(lock_name):
            conn.expire(lock_name, lock_timeout)
        time.sleep(.001)
    return False


def redis_release_lock(conn, key, identifier):
    lock_name = key + '.lock'
    pipe = conn.pipeline()
    while True:
        try:
            pipe.watch(lock_name)
            data = pipe.get(lock_name)
            if data.decode() == identifier:
                pipe.multi()
                pipe.delete(lock_name)
                pipe.execute()
                return True
            pipe.unwatch()
            break
        except (WatchError, AttributeError):
            return False
    return False


def last_dayoftheweek_zero_dt(day='Sun', tz=TZ, hour=0, minute=0, second=0, microsecond=0):
    """上一个周几（默认零点）的时间
    :param day:                 周几，英文前缀或者全拼，大小写不敏感
    :param tz:                  时区，默认东三区
    :param hour:                小时更换
    :param minute:              分钟更换
    :param second:              秒数更换
    :param microsecond:         微妙更换
    :return:                    datetime.datetime
    """
    today_dt, day_idx, today_weekday = _dayofweek_dt_weekday(
        day=day,
        tz=tz,
        hour=hour,
        minute=minute,
        second=second,
        microsecond=microsecond)

    timedelta_days = today_weekday - day_idx
    if timedelta_days < 0:
        one_weekdays = 7
        timedelta_days += one_weekdays

    last_zero_dt = today_dt - timedelta(days=timedelta_days)
    return last_zero_dt


def this_dayoftheweek_zero_dt(day='Sun', tz=TZ, hour=0, minute=0, second=0, microsecond=0):
    """下一个周几（默认零点）的时间
    :param day:                 周几，英文前缀或者全拼，大小写不敏感
    :param tz:                  时区，默认东三区
    :param hour:                小时更换
    :param minute:              分钟更换
    :param second:              秒数更换
    :param microsecond:         微妙更换
    :return:                    datetime.datetime
    """

    today_dt, day_idx, today_weekday = _dayofweek_dt_weekday(
        day=day,
        tz=tz,
        hour=hour,
        minute=minute,
        second=second,
        microsecond=microsecond)

    timedelta_days = day_idx - today_weekday
    if timedelta_days <= 0:
        one_weekdays = 7
        timedelta_days += one_weekdays
    this_zero_dt = today_dt + timedelta(days=timedelta_days)

    return this_zero_dt


def _dayofweek_dt_weekday(day, tz=TZ, hour=0, minute=0, second=0, microsecond=0):
    if isinstance(day, str):
        day = day.capitalize()
    day_idx = _dayoftheweek_index_m()[day]
    now_t = datetime.now(tz=timezone(tz))
    today_weekday = now_t.weekday()
    now_t_zero = now_t.replace(
        hour=hour,
        minute=minute,
        second=second,
        microsecond=microsecond)

    return now_t_zero, day_idx, today_weekday


def _dayoftheweek_index_m():
    mon_idx, tue_idx, wed_idx, thu_idx, fri_idx, sat_idx, sun_idx = range(7)
    return {
        'Mon': mon_idx,
        'Tue': tue_idx,
        'Wed': wed_idx,
        'Thu': thu_idx,
        'Fri': fri_idx,
        'Sat': sat_idx,
        'Sun': sun_idx,
        'Monday': mon_idx,
        'Tuesday': tue_idx,
        'Wednesday': wed_idx,
        'Thursday': thu_idx,
        'Friday': fri_idx,
        'Saturday': sat_idx,
        'Sunday': sun_idx,
    }


if __name__ == '__main__':
    pass
