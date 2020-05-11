import json
import time
import redis
from functools import partial, wraps
from uuid import uuid4
from redis.exceptions import WatchError

g_redis_db = redis.Redis()

success = 0


def cache_with_lock(func=None, *, dft=None, conn=None, acquire_timeout=10, lock_timeout=10):
    if func is None:
        return partial(cache_with_lock,
                       dft=dft,
                       conn=conn,
                       acquire_timeout=acquire_timeout,
                       lock_timeout=lock_timeout)
    conn = conn or g_redis_db

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        lock_name = str(args)+json.dumps(kwargs)
        locked = redis_acquire_lock(
            conn=conn,
            key=lock_name,
            acquire_timeout=acquire_timeout,
            lock_timeout=lock_timeout)
        if not locked:
            print('locked')
            return dft
        try:
            return func(self, *args, **kwargs)
        finally:
            redis_release_lock(conn, lock_name, locked)
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
        except WatchError:
            pass
    return False


class A:
    @cache_with_lock
    def b(self, name, age=10):
        print('begin')
        g_redis_db.set('name', name, ex=100)
        g_redis_db.set('age', age, ex=100)
        print(g_redis_db.get('name') + g_redis_db.get('age'))
        global success
        success += 1
        print('end')


if __name__ == '__main__':
    a = A()
    import threading
    t = []
    for i in range(1000):
        tt = threading.Thread(target=a.b, args=('x',), kwargs={'age': 1})
        time.sleep(.002)
        tt.start()
        t.append(tt)
    for ttt in t:
        ttt.join()
        print('done')
    print(success)
