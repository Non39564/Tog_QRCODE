
# from PIL import Image
# from pyzbar.pyzbar import decode
# import cv2
import pymysql
import pyqrcode

def getConnection ():
    return pymysql.connect(
        host = 'localhost',
        db = 'qrcode_tog',
        user = 'root',
        password = '',
        charset = 'utf8',
        cursorclass = pymysql.cursors.DictCursor
		)
    
connection = getConnection()
sql = "SELECT * FROM t304072022"
cursor = connection.cursor()
cursor.execute(sql)
em = cursor.fetchall()

user = []

for x in em:
  a =str(x.get('user'))
  user.append(a)

print(len(user))

# id = ["431490","640027","545519","597449","SC0000","ST9999","620263"]
url = "https://a41e-184-82-103-244.ap.ngrok.io"

for i in range(len(user)):
    print(i)
    qr = pyqrcode.create(url+"/home?username="+user[i])
    qr.png(""+user[i]+".png", scale=6)
    
    

