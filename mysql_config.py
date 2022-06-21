import mysql.connector

host = "192.168.56.106"
user = "root"
password = "maxmi33"
database = "bankDatabase"
table = "customers"
tableLog = "log"

try:
    mydb = mysql.connector.connect(
            host = host,
            user = user,
            password = password
    )
except:
    print("Hata sunucunu ve bilgilerini kontrol et!")

def selectDatabase(host, user, password, database):
    try:
        selectdb = mysql.connector.connect(
            host = host,
            user = user,
            password = password,
            database = database
        )
    except:
        print("Hata sunucunu ve bilgilerini kontrol et!")
    return selectdb

