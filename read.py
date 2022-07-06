import pymysql



def getConnection ():
    return pymysql.connect(
        host = 'localhost',
        db = 'qrcode',
        user = 'root',
        password = '',
        charset = 'utf8',
        cursorclass = pymysql.cursors.DictCursor
		)
    
connection = getConnection()
sql = "SELECT * FROM employee"
cursor = connection.cursor()
cursor.execute(sql)
em = cursor.fetchall()

for x in em:
  print(x)