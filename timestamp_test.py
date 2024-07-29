import pytz
from datetime import datetime
#display the current time in my timezone
print(datetime.now(pytz.timezone('US/Central')))

# print(pytz.all_timezones)
