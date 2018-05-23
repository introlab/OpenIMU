import time
import datetime

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print("%s function took %0.3f ms" % (f.__name__, (time2-time1)*1000.0))
        return ret
    return wrap


def datetime_from_dotnet_ticks(ticks):
    return datetime.datetime(1, 1, 1) + datetime.timedelta(microseconds=ticks/10)