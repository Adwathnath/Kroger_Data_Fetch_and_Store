from datetime import datetime
from DBworks import *


#to store deleted time of json
def del_info():
    times = datetime.now()
    time_str = times.strftime("%Y-%m-%d %I:%M:%S %p")
    msg = 'File deleted on'
    query = "insert into delete_info values(%s,%s)"
    val = (msg,time_str)
    iud(query,val)