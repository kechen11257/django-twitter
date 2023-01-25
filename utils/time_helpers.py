from datetime import datetime
# pythontimezone
import pytz


def utc_now():
    #就是讲datetime.now()的时间replace为utc的时间
    return datetime.now().replace(tzinfo=pytz.utc)