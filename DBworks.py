import pymysql


#to get sql connection and data insertion
def iud(qry,value):
    con=pymysql.connect(host="localhost",user="root",password="1234",port=3306,database="KrogerData")
    cmd=con.cursor()
    cmd.execute(qry,value)
    id=cmd.lastrowid
    con.commit()
    con.close()
    return id