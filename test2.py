import datetime
print(datetime.datetime.fromtimestamp(100,datetime.timezone.utc).strftime('%H:%M:%S'))