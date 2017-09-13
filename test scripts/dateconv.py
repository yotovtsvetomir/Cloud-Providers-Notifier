from datetime import datetime, timedelta
import pytz
from dateutil.tz import tzutc, tzlocal




#def toUTC(d,tz):
#    return tz.normalize(tz.localize(d)).astimezone(pytz.utc)

s = '7/7'

clean = datetime.strptime(s, '%m/%d')
print clean




#print clean

#eastern = pytz.timezone("US/Eastern")
#loc_dt = eastern.localize(clean)
#utc = toUTC(clean, eastern)
#print toUTC(clean, eastern)
#print loc_dt.strftime(fmt)

#for tmz in pytz.all_timezones:
#    print tmz

#west = pytz.timezone("US/Pacific")
#loc_dt1 = west.localize(clean)
#print toUTC(clean,west)


#local = utc.astimezone(tzlocal())
#print('Local: ' + str(local))
