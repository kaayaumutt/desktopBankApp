from attr import s
import mysql_config
import mysql.connector
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from untitled import Ui_MainWindow
from untitled2 import Ui_MainWindow2
from untitled3 import Ui_MainWindow3
from untitled4 import Ui_MainWindow4
from untitled5 import Ui_MainWindow5
import random
import requests
from bs4 import BeautifulSoup

class myApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(myApp,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.selectedDatabase = mysql_config.selectDatabase(mysql_config.host,mysql_config.user,mysql_config.password,mysql_config.database)
        self.rndIban = random.randint(100000000000,199999999999)
        self.ui.pushButton.clicked.connect(self.signUp)
        self.ui.pushButton_2.clicked.connect(self.registerUser)
        self.newWindow = Ui_MainWindow2()
        self.sendWindow = Ui_MainWindow3()
        self.moneyWindow = Ui_MainWindow4()
        self.customerWindow = Ui_MainWindow5()

    def signUp(self):
        mycursor = self.selectedDatabase.cursor()
        mycursor.execute(f"Select * From {mysql_config.table} Where tcNo ='{self.ui.lineEdit.text()}' and password ='{self.ui.lineEdit_2.text()}' ")
        result = mycursor.fetchall()
        control = True
        for p in result:
            if p[1] == self.ui.lineEdit.text() and p[2] == self.ui.lineEdit_2.text():
                self.signBank(p[0],p[4],p[5],p[6])
                control = False
                break
        
        if control:
            QtWidgets.QMessageBox.about(self,"Giriş","Bilgileriniz hatalı lütfen kontrol ediniz.")

    def registerUser(self):
        mycursor = self.selectedDatabase.cursor()
        mycursor.execute(f"Select * From {mysql_config.table} Where tcNo ='{self.ui.lineEdit_3.text()}' and name ='{self.ui.lineEdit_5.text()}' and surname = '{self.ui.lineEdit_6.text()}' ")
        result = mycursor.fetchall()
        tableControl = True
        for p in result:
            if p[1] == self.ui.lineEdit_3.text() and p[4] == self.ui.lineEdit_5.text() and p[5] == self.ui.lineEdit_6.text():
                tableControl = False
                break

        if tableControl and self.ui.lineEdit_3.text().isdigit() and self.ui.lineEdit_3.text() != "" and self.ui.lineEdit_3.text()[0] != "0" and len(self.ui.lineEdit_3.text()) == 11 and self.ui.lineEdit_4.text() != "" and self.ui.lineEdit_5.text() != "" and self.ui.lineEdit_6.text() != "" and len(self.ui.lineEdit_4.text()) >= 4 and len(self.ui.lineEdit_5.text()) >= 4 and len(self.ui.lineEdit_6.text()) >= 4 and self.ui.lineEdit_5.text().isdigit() == False and self.ui.lineEdit_6.text().isdigit() == False:
            mycursor.execute(f"INSERT INTO {mysql_config.table}(tcNo,password,iban,name,surname,money) VALUES('{self.ui.lineEdit_3.text()}','{self.ui.lineEdit_4.text()}','{str(self.rndIban)}','{self.ui.lineEdit_5.text()}','{self.ui.lineEdit_6.text()}','0')")
            self.selectedDatabase.commit()
            QtWidgets.QMessageBox.about(self,"Kayıt",f"Merhaba {self.ui.lineEdit_5.text()} {self.ui.lineEdit_6.text()} Bankamıza başarıyla kayıt oldunuz.")
            self.ui.lineEdit_3.setText("")
            self.ui.lineEdit_4.setText("")
            self.ui.lineEdit_5.setText("")
            self.ui.lineEdit_6.setText("")
        else:
            QtWidgets.QMessageBox.about(self,"Kayıt","Kayıt olamadınız bilgileri doğru giriniz.")
    
    def signBank(self,id,name,surname,balance):
        print(f"Giriş başarılı::{name} {surname} {balance}")
        self.newWindow.setupUi(self)
        self.newWindow.pushButton.clicked.connect(lambda: self.sendMoneyWindow(id,name, surname, balance))
        self.newWindow.pushButton_2.clicked.connect(lambda: self.moneyOptionWindow(id,name,surname,balance,True))
        self.newWindow.pushButton_3.clicked.connect(lambda: self.moneyOptionWindow(id,name,surname,balance,False))
        self.newWindow.pushButton_4.clicked.connect(self.customersWindow)
        self.newWindow.label_17.setText(str(name).upper())
        self.newWindow.label_18.setText(str(surname).upper())
        self.newWindow.label_19.setText(balance+" TL")
        self.updateExchangeRate()

    def updateExchangeRate(self):
        url = "https://altin.in/"
        html = requests.get(url).content
        soup = BeautifulSoup(html,'html.parser')
        gold = soup.find('div',{"class":"ons"}).find("a").find("h2").text
        dolar = soup.find('div',{"class":"dolar"}).find("a").find("h2").text
        euro = soup.find('div',{"class":"eurost"}).find("a").find("h2").text
        parite = soup.find('div',{"id":"parite"}).find("a").find("h2").text
        sterlin = soup.find('div',{"class":"sterlinsr"}).find("a").find("h2").text
        silver = soup.find('div',{"id":"gumus"}).find("a").find("h2").text
        platin = soup.find('div',{"id":"platin"}).find("a").find("h2").text
        self.newWindow.label_9.setText(gold)
        self.newWindow.label_10.setText(dolar)
        self.newWindow.label_11.setText(euro)
        self.newWindow.label_12.setText(parite)
        self.newWindow.label_13.setText(sterlin)
        self.newWindow.label_14.setText(silver)
        self.newWindow.label_15.setText(platin)

    def sendMoneyWindow(self,id,name,surname,balance):
        self.sendWindow.setupUi(self)
        self.sendWindow.pushButton.clicked.connect(lambda: self.sendMoney(id,name, surname, balance))

    def sendMoney(self,id,name,surname,balance):
        sendTcNo = self.sendWindow.lineEdit.text()
        sendIban = self.sendWindow.lineEdit_2.text()
        sendName = self.sendWindow.lineEdit_3.text()
        sendSurname = self.sendWindow.lineEdit_4.text()
        sendAmount = self.sendWindow.lineEdit_5.text()
        
        mycursor = self.selectedDatabase.cursor()
        mycursor.execute(f"Select * From {mysql_config.table} Where tcNo ='{sendTcNo}' and iban ='{sendIban}' and name ='{sendName}' and surname = '{sendSurname}' ")
        result = mycursor.fetchall()
        for p in result:
            if p[1] == sendTcNo and p[3] == sendIban and p[4] == sendName and p[5] == sendSurname and int(balance) >= int(sendAmount) and p[4] != name and p[5] != surname:
                mycursor.execute(f"UPDATE {mysql_config.table} SET money='{str(int(balance)-int(sendAmount))}' Where id ='{id}'  ")
                mycursor.execute(f"UPDATE {mysql_config.table} SET money='{str(int(p[6])+int(sendAmount))}' Where id ='{p[0]}' ")
                mycursor.execute(f"INSERT INTO {mysql_config.tableLog} VALUES('{id}','{name}','{surname}','{p[0]}','{sendName}','{sendSurname}','{sendAmount}')")
                self.selectedDatabase.commit()
                balance = str(int(balance)-int(sendAmount))
                print("başarılı giriş")
                self.signBank(id,name,surname,balance)
                break
            else:
                QtWidgets.QMessageBox.about(self,"Havale","Hatalı giriş!")
        
    def moneyOptionWindow(self,id,name,surname,balance,control):
        self.moneyWindow.setupUi(self)
        if control:
            self.moneyWindow.label_2.setText("Para Yatırma Ekranı")
        else:
            self.moneyWindow.label_2.setText("Para Çekme Ekranı")
        self.moneyWindow.pushButton.clicked.connect(lambda: self.moneyOption(id,name, surname, balance,control))
    
    def moneyOption(self,id,name,surname,balance,control):
        mycursor = self.selectedDatabase.cursor()
        if control:
            mycursor.execute(f"UPDATE {mysql_config.table} SET money='{str(int(balance)+int(self.moneyWindow.lineEdit.text()))}' Where id ='{id}'  ")
            self.selectedDatabase.commit()
            self.signBank(id,name,surname,str(int(balance)+int(self.moneyWindow.lineEdit.text())))
        else:
            if int(balance) >= int(self.moneyWindow.lineEdit.text()):
                mycursor.execute(f"UPDATE {mysql_config.table} SET money='{str(int(balance)-int(self.moneyWindow.lineEdit.text()))}' Where id ='{id}'  ")
                self.selectedDatabase.commit()
                self.signBank(id,name,surname,str(int(balance)-int(self.moneyWindow.lineEdit.text())))
            else:
                QtWidgets.QMessageBox.about(self,"Para Çekme","Yetersiz Bakiye!")
    
    def customersWindow(self):
        self.customerWindow.setupUi(self)
        mycursor = self.selectedDatabase.cursor()
        mycursor.execute(f"Select * From {mysql_config.table}")
        result = mycursor.fetchall()
        for p in result:
            nameSurname = str(p[4]).upper()+" - "+str(p[5]).upper()
            self.customerWindow.listWidget.addItem(nameSurname)

class Window:
    def __init__(self):
        self.mydb = mysql_config.mydb
        self.mysqlEdited()
        self.selectedDatabase = mysql_config.selectDatabase(mysql_config.host,mysql_config.user,mysql_config.password,mysql_config.database)
        self.appWindow()

    def mysqlEdited(self):
        mycursor = self.mydb.cursor()
        mycursor.execute("SHOW DATABASES")

        databaseControl = True
        for x in mycursor:
            if str(x) == f"('{mysql_config.database}',)":
                databaseControl = False
                print(x)
                break
            else:
                print(x)

        if databaseControl:
            self.mydb.cursor().execute(f"CREATE DATABASE {mysql_config.database}")
            self.mydb.close()
                
            mydb = mysql_config.selectDatabase(mysql_config.host,mysql_config.user,mysql_config.password,mysql_config.database)
            mydb.cursor().execute(f"CREATE TABLE {mysql_config.table} (id INT PRIMARY KEY AUTO_INCREMENT,tcNo VARCHAR(255) NOT NULL,password VARCHAR(255) NOT NULL,iban VARCHAR(255) NOT NULL,name VARCHAR(255) NOT NULL,surname VARCHAR(255) NOT NULL,money VARCHAR(255) NOT NULL)")
            mydb.cursor().execute(f"CREATE TABLE {mysql_config.tableLog} (senderId VARCHAR(255),senderName VARCHAR(255),senderSurname VARCHAR(255),sentId VARCHAR(255),sentName VARCHAR(255),sentSurname VARCHAR(255),sentMoney VARCHAR(255))")
            print(f"{mysql_config.host} adresli sunucunuza {mysql_config.database} adlı databaseyi ve {mysql_config.table} adlı ve {mysql_config.tableLog} adlı tabloyu başarıyla oluşturdunuz.")
        else:
            print(f"{mysql_config.database} adlı database ve {mysql_config.table} adlı ve {mysql_config.tableLog} adlı tablo zaten oluşturulmuş.")

    def appWindow(self):
        app = QtWidgets.QApplication(sys.argv)
        win = myApp()
        win.show()
        sys.exit(app.exec_())

if __name__=="main":
    Window()
else:
    print("desktop_bankApp.py dosyası başka dosyadan çalışıyor.")

#-Settings -> mysql_config.py
