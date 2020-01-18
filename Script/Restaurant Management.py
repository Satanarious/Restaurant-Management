from PyQt5 import uic,QtWidgets,QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from datetime import datetime as dt
from tkinter import messagebox,Tk
import mysql.connector
import xlwt,xlrd
from cryptography.fernet import Fernet
import os
import shutil
import requests
import random
class Ui(QtWidgets.QMainWindow):
    def __init__(self,login):
        super().__init__()
        self.mydb=login.mydb
        self.mycursor=login.mycursor
        uic.loadUi('MainUi.ui', self)
        self.tabWidget.tabBar().setVisible(0)
        self.tabs()
        self.background()
        self.reset_buttons()
        self.pushButton_12.clicked.connect(self.add_item)
        self.pushButton_24.clicked.connect(self.reset_additem)
        self.pushButton_13.clicked.connect(self.search)
        self.pushButton_14.clicked.connect(self.delete)
        self.pushButton_15.clicked.connect(self.reset_edititem)
        self.pushButton_17.clicked.connect(self.search_view)
        self.pushButton_23.clicked.connect(self.add_row)
        self.pushButton_25.clicked.connect(self.delete_row)
        self.pushButton_16.clicked.connect(self.handleAddTab)
        self.pushButton_26.clicked.connect(self.reset_order)
        self.pushButton_42.clicked.connect(self.search_customer)
        self.pushButton_43.clicked.connect(self.search_order)
        self.pushButton_27.clicked.connect(self.export_customers)
        self.pushButton_28.clicked.connect(self.export_order)
        self.pushButton_30.clicked.connect(self.export_menu)
        self.pushButton_29.clicked.connect(self.export_log)
        self.pushButton_44.clicked.connect(self.search_log)
        self.pushButton_48.clicked.connect(self.authenticate)
        self.pushButton_49.clicked.connect(self.unauthenticate)
        self.pushButton_50.clicked.connect(self.change_pass)
        self.pushButton_51.clicked.connect(self.change_restaurant_name)
        self.pushButton_31.clicked.connect(self.reset_name)
        self.pushButton_45.clicked.connect(self.search_menu)
        self.pushButton_32.clicked.connect(self.import_items)
        self.pushButton_27.setDisabled(True)
        self.pushButton_28.setDisabled(True)
        self.pushButton_29.setDisabled(True)
        self.pushButton_30.setDisabled(True)
        self.comboBox_8.currentIndexChanged.connect(self.select_menu)
        self.comboBox_8.setCurrentIndex(0)
        self.comboBox_6.currentIndexChanged.connect(self.select_login)
        self.comboBox_6.setCurrentIndex(0)
        self.search_buttons()
        self.radioButton_2.setChecked(True)
        self.dateEdit.dateChanged.connect(lambda:self.dateEdit_2.setMinimumDate(self.dateEdit.date()))
        self.dateEdit_5.dateChanged.connect(lambda:self.dateEdit_6.setMinimumDate(self.dateEdit_5.date()))
        self.spinBox.valueChanged.connect(lambda:self.spinBox_2.setMinimum(self.spinBox.value()))
        self.spinBox_3.valueChanged.connect(lambda:self.spinBox_4.setMinimum(self.spinBox_3.value()))
        self.tabWidget_4.tabCloseRequested.connect(self.removeTab)
        self.treeWidget.selectionModel().selectionChanged.connect(lambda:self.selected(self.treeWidget.currentIndex().data(Qt.DisplayRole).split(')')))
        self.selected(['1.1','Read Home Page'])
        self.verticalSlider.valueChanged[int].connect(self.change_size)
        self.treeWidget.expandAll()
        self.reset1()
        self.reset2()
        self.reset3()
        self.reset4()
        self.reset5()
        self.tables_served()
        self.edit_buttons()
        self.toggle_edit(False)
        self.set_theme()
        self.login_datetime()
        self.earning()
        self.tables_today()
        self.favourite()
        self.login_details()
        self.unauthenticate()
        self.show()
        self.fields=['Serial','Item Id','Item Name','Half Rate','Full Rate']
        self.restaurant_name()
        self.reset_name()
        self.label_72.setStyleSheet("color:#b4b4b4;")
    def change_size(self):
        size=self.verticalSlider.value()
        cursor = self.textEdit.textCursor()
        self.textEdit.selectAll()
        self.textEdit.setFontPointSize(size)
        self.textEdit.setTextCursor( cursor )
    def selected(self,select):
        if(len(select[0])>1 and select[0]!='4.1' and select[0]!='4.2'):
            f=open("Assets/help/"+select[0]+".txt",'r')
            data='\n'.join(f.readlines())
            f.close()
            self.label_73.setText(select[1].strip())
            self.textEdit.setText(data)
            movie1=QMovie("Assets/help/"+select[0]+".gif")
            self.label_74.setMovie(movie1)
            movie1.start()
    def import_items(self):
        self.dialog=Import(self)
    def reset_name(self):
        a=open('Assets//preference.txt','r')
        data=eval(a.read())
        self.lineEdit_35.setText(data['name'])
        self.spinBox_5.setValue(data['size'])
        index = self.fontComboBox.findText(data['family'], QtCore.Qt.MatchFixedString)
        self.fontComboBox.setCurrentIndex(index)
    def change_restaurant_name(self):
        name=self.lineEdit_35.text()
        size=self.spinBox_5.value()
        family=self.fontComboBox.currentText()
        if(name==''):
            Tk().wm_withdraw()
            messagebox.showerror('Error Name','No Restaurant Name Entered')
            return
        a=open('Assets//preference.txt','r')
        data=eval(a.read())
        a.close()
        a=open('Assets//preference.txt','w')
        data['name']=name
        data['size']=size
        data['family']=family
        a.write(str(data))
        a.close()
        self.restaurant_name()        
    def restaurant_name(self):
        a=open('Assets//preference.txt','r')
        data=eval(a.read())
        self.label_2.setText(data['name'])
        self.label_2.setStyleSheet("font-family:{};font-size:{}px;".format(data['family'],str(data['size']*2)))
        a.close()
    def logout_details(self):
        self.dt=dt.now()
        date=str(self.dt.year)+'-'+str(self.dt.month)+'-'+str(self.dt.day)
        time=str(self.dt.hour)+':'+str(self.dt.minute)+':'+str(self.dt.second)
        tables=self.label_9.text()
        if(self.label_11.text()=='None'):
            earning=None
        else:
            earning=float(self.label_11.text())
        if(self.label_12.text()=='None'):
            favourite=None
        else:
            favourite=self.label_12.text()
        sql='insert into logout (Date,Time,Tables_Served,Earning,Favourite) values (%s,%s,%s,%s,%s)'
        val=(date,time,tables,earning,favourite)
        self.mycursor.execute(sql,val)
        self.mydb.commit()
    def closeEvent(self, event):
        Tk().wm_withdraw()
        result =messagebox.askyesno("Exit Prompt","Would you like to Logout?")
        if(result):
            self.logout_details()
            event.accept()
        else:
            event.ignore()
    def search_menu(self):
        by=self.comboBox_7.currentText()
        if(by=='All'):
            val='`all`'
        elif(by=='Starters'):
            val='starters'
        elif(by=='Main Course'):
            val='maincourse'
        elif(by=='Desserts'):
            val='desserts'
        else:
            val='drinks'
        by=self.comboBox_8.currentText()
        if(by=='None'):
            src=''
        elif(by=='Half Price'):
            src='Half_Rate'
        else:
            src='Full_Rate'
        if(by=='None'):
            sql='select * from '+val
            self.mycursor.execute(sql)
            table=self.mycursor.fetchall()
            self.tableWidget_10.setRowCount(0)
            if(len(table)>0):
                self.pushButton_30.setEnabled(True)
                for i in range(len(table)):
                    rowPosition = self.tableWidget_10.rowCount()
                    self.tableWidget_10.insertRow(rowPosition)
                    self.tableWidget_10.setItem(rowPosition , 0,QtWidgets.QTableWidgetItem(str(table[i][0])))
                    self.tableWidget_10.setItem(rowPosition , 1,QtWidgets.QTableWidgetItem(str(table[i][1])))
                    self.tableWidget_10.setItem(rowPosition , 2,QtWidgets.QTableWidgetItem(str(table[i][2])))
                    self.tableWidget_10.setItem(rowPosition , 3,QtWidgets.QTableWidgetItem(str(table[i][3])))
            else:
                self.pushButton_30.setDisabled(True)
            return
        elif(not(self.groupBox_20.isChecked()) and not(self.groupBox_19.isChecked())):
            self.tableWidget_10.setRowCount(0)
            Tk().wm_withdraw()
            messagebox.showerror('Error price','No price field Checked')
            return
        elif(self.groupBox_20.isChecked() and self.groupBox_19.isChecked()):
            sql='select * from '+val+' where '+src+' between %s and %s'
            val=(self.lineEdit_25.text(),self.lineEdit_24.text())
        elif(self.groupBox_20.isChecked()):
            sql='select * from '+val+' where '+src+'>%s'
            val=(self.lineEdit_25.text(),)
        elif(self.groupBox_19.isChecked()):
            sql='select * from '+val+' where '+src+'<%s'
            val=(self.lineEdit_24.text(),)
        self.tableWidget_10.setRowCount(0)
        self.mycursor.execute(sql,val)
        table=self.mycursor.fetchall()
        if(len(table)>0):
            self.pushButton_30.setEnabled(True)
            for i in range(len(table)):
                rowPosition = self.tableWidget_10.rowCount()
                self.tableWidget_10.insertRow(rowPosition)
                self.tableWidget_10.setItem(rowPosition , 0,QtWidgets.QTableWidgetItem(str(table[i][0])))
                self.tableWidget_10.setItem(rowPosition , 1,QtWidgets.QTableWidgetItem(str(table[i][1])))
                self.tableWidget_10.setItem(rowPosition , 2,QtWidgets.QTableWidgetItem(str(table[i][2])))
                self.tableWidget_10.setItem(rowPosition , 3,QtWidgets.QTableWidgetItem(str(table[i][3])))
        else:
            self.pushButton_30.setDisabled(True)
    def select_menu(self):
        by=self.comboBox_8.currentText()
        if(by=='None'):
            self.frame_6.setDisabled(True)
        else:
            self.frame_6.setEnabled(True)
    def change_pass(self):
        key=b'fHfSDj6YKvajRYNo595SwBgPvRky3FLAW3ArpPKn-sA='
        fernet = Fernet(key)
        f=open("Assets//resource.txt",'r')
        data=eval(f.read())
        data=fernet.decrypt(data).decode("utf-8")
        f.close()
        if(self.lineEdit_32.text()=='' or self.lineEdit_33.text()=='' or self.lineEdit_34.text()==''):
            Tk().wm_withdraw()
            messagebox.showerror('Error password','Password field empty')
            return
        elif(self.lineEdit_33.text()!=self.lineEdit_34.text()):
            Tk().wm_withdraw()
            messagebox.showerror('Error New password','New password and retyped passwords don\'t match')
            return
        elif(self.lineEdit_32.text()==data):
            f=open("Assets//resource.txt",'w')
            data=fernet.encrypt(self.lineEdit_33.text().encode())
            f.write(str(data))
            f.close()
            Tk().wm_withdraw()
            messagebox.showinfo('Success','Password Changed Successfully')
            self.lineEdit_32.setText('')
            self.lineEdit_33.setText('')
            self.lineEdit_34.setText('')
        else:
            Tk().wm_withdraw()
            messagebox.showerror('Error Old password','Old password incorrect')
            return
    def unauthenticate(self):
        for i in range(1,5):
            self.tabWidget_5.setTabEnabled(i,False)
        self.label_96.setText('Access Denied  !')
        self.lineEdit_31.setText('')
    def authenticate(self):
        key=b'fHfSDj6YKvajRYNo595SwBgPvRky3FLAW3ArpPKn-sA='
        fernet = Fernet(key)
        f=open("Assets//resource.txt",'r')
        data=eval(f.read())
        data=fernet.decrypt(data).decode("utf-8")
        f.close()
        if(self.lineEdit_31.text()==''):
            Tk().wm_withdraw()
            messagebox.showerror('Error password','No password entered')
            return
        elif(self.lineEdit_31.text()==data):
            for i in range(1,5):
                self.tabWidget_5.setTabEnabled(i,True)
            self.label_96.setText('Access Granted  !')
            self.lineEdit_31.setText('')
    def search_log(self):
        by=self.comboBox_6.currentText()
        typ=self.comboBox_9.currentText().lower()
        if(by=='Date' and not(self.groupBox_9.isChecked()) and not(self.groupBox_13.isChecked())):
            Tk().wm_withdraw()
            messagebox.showerror('Error Date','No Date Type Checked')
            self.tableWidget_9.setRowCount(0)
            self.pushButton_29.setDisabled(True)
            return
        elif(by=='Tables' and not(self.groupBox_16.isChecked()) and not(self.groupBox_15.isChecked())):
            Tk().wm_withdraw()
            messagebox.showerror('Error Table(s)','No Table Type Checked')
            self.tableWidget_9.setRowCount(0)
            self.pushButton_29.setDisabled(True)
            return
        elif(by=='Favourite' and self.lineEdit_21.text()==''):
            Tk().wm_withdraw()
            messagebox.showerror('Error Favourite','No Favourite Entered')
            self.tableWidget_9.setRowCount(0)
            self.pushButton_29.setDisabled(True)
            return
        elif(by=='Earning' and not(self.groupBox_18.isChecked()) and not(self.groupBox_17.isChecked())):
            Tk().wm_withdraw()
            messagebox.showerror('Error Earning','No Earning Type Checked')
            self.tableWidget_9.setRowCount(0)
            self.pushButton_29.setDisabled(True)
            return
        if(by!='Date' or self.radioButton_2.isChecked()):
            self.tableWidget_9.setHorizontalHeaderItem(0,QTableWidgetItem("Date"))
            self.tableWidget_9.setHorizontalHeaderItem(1,QTableWidgetItem("Table(s)"))
            self.tableWidget_9.setHorizontalHeaderItem(2,QTableWidgetItem("Favourite"))
            self.tableWidget_9.setHorizontalHeaderItem(3,QTableWidgetItem("Earning"))
        if(by=='Date'):
            if(self.radioButton_2.isChecked()):
                self.selected='summary'
                if(self.groupBox_9.isChecked() and self.groupBox_13.isChecked()):
                    sql='select * from (select date,max(tables_served) as Tables,max(favourite) as Favourite,max(earning) as Earning from '+typ+' group by date) as t where date between %s and %s'
                    val=(self.dateEdit_5.date().toPyDate(),self.dateEdit_6.date().toPyDate())
                elif(self.groupBox_9.isChecked()):
                    sql='select * from (select date,max(tables_served) as Tables,max(favourite) as Favourite,max(earning) as Earning from '+typ+' group by date) as t where date>=%s'
                    val=(self.dateEdit_5.date().toPyDate(),)
                elif(self.groupBox_13.isChecked()):
                    sql='select * from (select date,max(tables_served) as Tables,max(favourite) as Favourite,max(earning) as Earning from '+typ+' group by date) as t where date<=%s'
                    val=(self.dateEdit_6.date().toPyDate(),)
            else:
                self.selected='full'
                self.tableWidget_9.setHorizontalHeaderItem(0,QTableWidgetItem("Date"))
                self.tableWidget_9.setHorizontalHeaderItem(1,QTableWidgetItem("Time"))
                self.tableWidget_9.setHorizontalHeaderItem(2,QTableWidgetItem("Tables Served"))
                self.tableWidget_9.setHorizontalHeaderItem(3,QTableWidgetItem("Earning"))
                if(self.groupBox_9.isChecked() and self.groupBox_13.isChecked()):
                    sql='select *  from '+typ+' where date between %s and %s'
                    val=(self.dateEdit_5.date().toPyDate(),self.dateEdit_6.date().toPyDate())
                elif(self.groupBox_9.isChecked()):
                    sql='select * from '+typ+' where date>=%s'
                    val=(self.dateEdit_5.date().toPyDate(),)
                elif(self.groupBox_13.isChecked()):
                    sql='select * from '+typ+' where date<=%s'
                    val=(self.dateEdit_6.date().toPyDate(),)
        elif(by=='Tables'):
            if(self.groupBox_16.isChecked() and self.groupBox_15.isChecked()):
                sql='select * from (select date,max(tables_served) as Tables,max(favourite) as Favourite,max(earning) as Earning from '+typ+' group by date) as t where tables between %s and %s'
                val=(self.dateEdit_5.date().toPyDate(),self.dateEdit_6.date().toPyDate())
            elif(self.groupBox_16.isChecked()):
                sql='select * from (select date,max(tables_served) as Tables,max(favourite) as Favourite,max(earning) as Earning from '+typ+' group by date) as t where tables>=%s'
                val=(self.spinBox_3.value(),)
            elif(self.groupBox_15.isChecked()):
                sql='select * from (select date,max(tables_served) as Tables,max(favourite) as Favourite,max(earning) as Earning from '+typ+' group by date) as t where tables<=%s'
                val=(self.spinBox_4.value(),)
        elif(by=='Favourite'):
            sql='select * from (select date,max(tables_served) as Tables,max(favourite) as Favourite,max(earning) as Earning from '+typ+' group by date) as t where favourite like %s'
            val=('%'+self.lineEdit_21.text()+'%',)
        else:
            if(self.groupBox_18.isChecked() and self.groupBox_17.isChecked()):
                sql='select * from (select date,max(tables_served) as Tables,max(favourite) as Favourite,max(earning) as Earning from '+typ+' group by date) as t where earning between %s and %s'
                val=(self.dateEdit_5.date().toPyDate(),self.dateEdit_6.date().toPyDate())
            elif(self.groupBox_18.isChecked()):
                sql='select * from (select date,max(tables_served) as Tables,max(favourite) as Favourite,max(earning) as Earning from '+typ+' group by date) as t where earning>=%s'
                val=(self.spinBox_3.value(),)
            elif(self.groupBox_17.isChecked()):
                sql='select * from (select date,max(tables_served) as Tables,max(favourite) as Favourite,max(earning) as Earning from '+typ+' group by date) as t where earning<=%s'
                val=(self.spinBox_4.value(),)
        self.mycursor.execute(sql,val)
        table=self.mycursor.fetchall()
        self.tableWidget_9.setRowCount(0)
        if(len(table)>0):
            self.pushButton_29.setEnabled(True)
            for i in range(len(table)):
                rowPosition = self.tableWidget_9.rowCount()
                self.tableWidget_9.insertRow(rowPosition)
                self.tableWidget_9.setItem(rowPosition , 0,QtWidgets.QTableWidgetItem(str(table[i][0])))
                self.tableWidget_9.setItem(rowPosition , 1,QtWidgets.QTableWidgetItem(str(table[i][1])))
                self.tableWidget_9.setItem(rowPosition , 2,QtWidgets.QTableWidgetItem(str(table[i][2])))
                self.tableWidget_9.setItem(rowPosition , 3,QtWidgets.QTableWidgetItem(str(table[i][3])))
        else:
            self.pushButton_29.setDisabled(True)
    def select_login(self):
        by=self.comboBox_6.currentText()
        if(by=='Date'):
            self.frame.show()
            self.frame_2.hide()
            self.frame_3.hide()
            self.frame_4.hide()
        elif(by=='Tables'):
            self.frame.hide()
            self.frame_2.show()
            self.frame_3.hide()
            self.frame_4.hide()
        elif(by=='Favourite'):
            self.frame.hide()
            self.frame_2.hide()
            self.frame_3.show()
            self.frame_4.hide()
        else:
            self.frame.hide()
            self.frame_2.hide()
            self.frame_3.hide()
            self.frame_4.show()
    def login_details(self):
        date=str(self.dt.year)+'-'+str(self.dt.month)+'-'+str(self.dt.day)
        time=str(self.dt.hour)+':'+str(self.dt.minute)+':'+str(self.dt.second)
        tables=self.label_9.text()
        if(self.label_11.text()=='None'):
            earning=None
        else:
            earning=float(self.label_11.text())
        if(self.label_12.text()=='None'):
            favourite=None
        else:
            favourite=self.label_12.text()
        sql='insert into login (Date,Time,Tables_Served,Earning,Favourite) values (%s,%s,%s,%s,%s)'
        val=(date,time,tables,earning,favourite)
        self.mycursor.execute(sql,val)
        self.mydb.commit()
    def favourite(self):
        sql='create or replace view `fav` as select * from (SELECT Item_Id,sum(Half_Quantity)+sum(Full_Quantity) as Quantity FROM orders left join customers on orders.Customer_Id=customers.Customer_Id where customers.Date=%s group by orders.Item_Id) as T order by Quantity DESC LIMIT 0, 1;'
        val=(str(self.dt.year)+'-'+str(self.dt.month)+'-'+str(self.dt.day),)
        self.mycursor.execute(sql,val)
        self.mydb.commit()
        self.mycursor.execute('select * from `fav`')
        fav=self.mycursor.fetchall()
        if(len(fav)>0):
            fav=fav[0][0]
            self.mycursor.execute('select Item_Name from `all` where Item_Id=%s',(fav,))
            fav=self.mycursor.fetchall()
            fav=fav[0][0]
            self.label_12.setText(fav)            
    def tables_today(self):
        self.mycursor.execute('select count(*) from customers where Date=%s',(str(self.dt.year)+'-'+str(self.dt.month)+'-'+str(self.dt.day),))
        amount=self.mycursor.fetchall()
        self.label_9.setText(str(amount[0][0]))
    def earning(self):
        self.mycursor.execute('select sum(Amount) from customers where Date=%s',(str(self.dt.year)+'-'+str(self.dt.month)+'-'+str(self.dt.day),))
        amount=self.mycursor.fetchall()
        self.label_11.setText(str(amount[0][0]))
    def tables_served(self):
        self.mycursor.execute('select count(*) from customers')
        self.tablestillnow=self.mycursor.fetchall()
        if(len(self.tablestillnow)>0):
            self.label_10.setText(str(self.tablestillnow[0][0]))
    def check_customer(self):
        var=self.lineEdit_8.text()
        if(var==''):
            Tk().wm_withdraw()
            messagebox.showerror('Error Name','Customer Name not entered !')
            return(False)
        if(self.tableWidget_7.rowCount()==0 or self.tableWidget_7.itemAt(0, 0)==None):
            Tk().wm_withdraw()
            messagebox.showerror('Error Items','No Initial Order !')
            return(False)
        return(True)
    def export_menu(self):
        allRows = self.tableWidget_10.rowCount()
        self.dialog=Export()
        self.dialog.setModal(True)
        self.dialog.exec_()
        try:
            path=self.dialog.path
            file=self.dialog.file
        except:
            pass
        self.wb = xlwt.Workbook()
        style = xlwt.easyxf('font: bold 1')
        sheet1 = self.wb.add_sheet('Sheet 1')
        sheet1.write(0, 0, 'Item Id',style);sheet1.write(0, 1, 'Item Name',style);sheet1.write(0, 2, 'Half Rate',style);sheet1.write(0, 3, 'Full Rate',style)
        for i in range(allRows):
            c=[]
            c.append(self.tableWidget_10.item(i,0).text())
            c.append(self.tableWidget_10.item(i,1).text())
            c.append(self.tableWidget_10.item(i,2))
            c.append(self.tableWidget_10.item(i,3).text())
            if(c[2]==None):
                c[2]='None'
            else:
                c[2]=c[2].text()
            sheet1.write(i+1,0,c[0]);sheet1.write(i+1,1,c[1]);sheet1.write(i+1,2,c[2]);sheet1.write(i+1,3,c[3])
        try:
            self.wb.save(path+'/'+file)
            Tk().wm_withdraw()
            messagebox.showinfo('Write Successfull','Data written to excel file !')
        except:
            Tk().wm_withdraw()
            messagebox.showerror('Error','Path or Filename Error')
            return
    def export_log(self):
        allRows = self.tableWidget_9.rowCount()
        self.dialog=Export()
        self.dialog.setModal(True)
        self.dialog.exec_()
        try:
            path=self.dialog.path
            file=self.dialog.file
        except:
            pass
        self.wb = xlwt.Workbook()
        style = xlwt.easyxf('font: bold 1')
        sheet1 = self.wb.add_sheet('Sheet 1')
        sheet1.write(0, 0, 'Date',style);sheet1.write(0, 3, 'Earning',style)
        if(self.selected=='full'):
            sheet1.write(0, 1, 'Time',style);sheet1.write(0, 2, 'Tables Served',style)
        else:
            sheet1.write(0, 1, 'Tables(s)',style);sheet1.write(0, 2, 'Favourite',style)
        for i in range(allRows):
            c=[]
            c.append(self.tableWidget_9.item(i,0).text())
            c.append(self.tableWidget_9.item(i,1).text())
            c.append(self.tableWidget_9.item(i,2))
            c.append(self.tableWidget_9.item(i,3))
            if(c[2]==None):
                c[2]='None'
            else:
                c[2]=c[2].text()
            if(c[3]==None):
                c[3]='None'
            else:
                c[3]=c[3].text()
            sheet1.write(i+1,0,c[0]);sheet1.write(i+1,1,c[1]);sheet1.write(i+1,2,c[2]);sheet1.write(i+1,3,c[3])
        try:
            self.wb.save(path+'/'+file)
            Tk().wm_withdraw()
            messagebox.showinfo('Write Successfull','Data written to excel file !')
        except:
            Tk().wm_withdraw()
            messagebox.showerror('Error','Path or Filename Error')
            return
    def export_order(self):
        allRows = self.tableWidget_15.rowCount()
        a=[]
        a.append(self.label_56.text())
        a.append(self.label_57.text())
        a.append(self.label_47.text())
        a.append(self.label_48.text())
        self.dialog=Export()
        self.dialog.setModal(True)
        self.dialog.exec_()
        try:
            path=self.dialog.path
            file=self.dialog.file
        except:
            pass
        self.wb = xlwt.Workbook()
        style = xlwt.easyxf('font: bold 1')
        sheet1 = self.wb.add_sheet('Sheet 1')
        sheet1.write(0, 0, 'Date',style);sheet1.write(1, 0, 'Time',style);sheet1.write(2, 0, 'Customer Name',style);sheet1.write(3, 0, 'Order Type',style)
        sheet1.write(0, 1, a[0]);sheet1.write(1, 1, a[1]);sheet1.write(2, 1, a[2]);sheet1.write(3, 1, a[3])
        sheet1.write(4, 0, 'Item Name',style);sheet1.write(4, 1, 'Half Quantity',style);sheet1.write(4, 2, 'Full Quantity',style);sheet1.write(4, 3, 'Amount',style)
        for i in range(allRows):
            c=[]
            c.append(self.tableWidget_15.item(i,0).text())
            c.append(self.tableWidget_15.item(i,1))
            c.append(self.tableWidget_15.item(i,2))
            c.append(self.tableWidget_15.item(i,3).text())
            if(c[1]==None):
                c[4]='None'
            else:
                c[1]=c[1].text()
            if(c[2]==None):
                c[2]='None'
            else:
                c[2]=c[2].text()
            sheet1.write(i+5,0,c[0]);sheet1.write(i+5,1,c[1]);sheet1.write(i+5,2,c[2]);sheet1.write(i+5,3,c[3])
        try:
            self.wb.save(path+'/'+file)
            Tk().wm_withdraw()
            messagebox.showinfo('Write Successfull','Data written to excel file !')
        except:
            Tk().wm_withdraw()
            messagebox.showerror('Error','Path or Filename Error')
            return
    def export_customers(self):
        allRows = self.tableWidget_14.rowCount()
        self.dialog=Export()
        self.dialog.setModal(True)
        self.dialog.exec_()
        try:
            path=self.dialog.path
            file=self.dialog.file
        except:
            pass
        self.wb = xlwt.Workbook()
        style = xlwt.easyxf('font: bold 1')
        sheet1 = self.wb.add_sheet('Sheet 1')
        sheet1.write(0, 0, 'Date',style);sheet1.write(0, 1, 'Time',style);sheet1.write(0, 2, 'Id',style);sheet1.write(0, 3, 'Type',style);sheet1.write(0, 4, 'Table Number',style)
        sheet1.write(0, 5, 'Name',style);sheet1.write(0, 6, 'Amount',style)
        for i in range(allRows):
            c=[]
            c.append(self.tableWidget_14.item(i,0).text())
            c.append(self.tableWidget_14.item(i,1).text())
            c.append(self.tableWidget_14.item(i,2).text())
            c.append(self.tableWidget_14.item(i,3).text())
            c.append(self.tableWidget_14.item(i,4))
            c.append(self.tableWidget_14.item(i,5).text())
            c.append(self.tableWidget_14.item(i,6).text())
            if(c[4]==None):
                c[4]='None'
            else:
                c[4]=c[4].text()
            sheet1.write(i+1,0,c[0]);sheet1.write(i+1,1,c[1]);sheet1.write(i+1,2,c[2]);sheet1.write(i+1,3,c[3]);sheet1.write(i+1,4,c[4]);sheet1.write(i+1,5,c[5]);sheet1.write(i+1,6,c[6])
        try:
            self.wb.save(path+'/'+file)
            Tk().wm_withdraw()
            messagebox.showinfo('Write Successfull','Data written to excel file !')
        except:
            Tk().wm_withdraw()
            messagebox.showerror('Error','Path or Filename Error')
            return
    def reset_order(self):
        self.comboBox_4.setCurrentIndex(0)
        self.lineEdit_8.setText('')
        self.lineEdit_26.setText('')
        self.lineEdit_7.setText('')
        self.tableWidget_7.setRowCount(0)
        self.tableWidget_8.setRowCount(0)
    def removeTab(self, index):
        widget = self.tabWidget_4.widget(index)
        if widget != None and index!=0:
            widget.deleteLater()
            self.tabWidget_4.removeTab(index)
    def handleAddTab(self):
        if(self.check_customer()):
            p=new_order(self)
    def delete_row(self):
        rowPosition = self.tableWidget_7.rowCount()
        self.tableWidget_7.setRowCount(rowPosition-1)
    def add_row(self):
        rowPosition = self.tableWidget_7.rowCount()
        self.tableWidget_7.insertRow(rowPosition)
    def search_order(self):
        val=self.lineEdit_20.text()
        if(val==''):
            Tk().wm_withdraw()
            messagebox.showerror('Error Id','Customer Id not entered !')
            self.pushButton_28.setDisabled(True)
            self.tableWidget_15.setRowCount(0)
            self.label_47.setText('Unknown')
            self.label_48.setText('Unknown')
            self.label_49.setText('0')
            self.label_56.setText('Unknown')
            self.label_57.setText('Unknown')
            return
        sql='select Item_Id,Half_Quantity,Full_Quantity,Total from orders where Customer_Id=%s'
        self.mycursor.execute(sql,(val,))
        table=self.mycursor.fetchall()
        self.tableWidget_15.setRowCount(0)
        if(len(table)>0):
            self.pushButton_28.setEnabled(True)
            for i in range(len(table)):
                rowPosition = self.tableWidget_15.rowCount()
                self.mycursor.execute('select Item_Name from `all` where Item_Id=%s',(table[i][0],))
                name=self.mycursor.fetchall()[0][0]
                self.tableWidget_15.insertRow(rowPosition)
                self.tableWidget_15.setItem(rowPosition , 0,QtWidgets.QTableWidgetItem(name))
                self.tableWidget_15.setItem(rowPosition , 1,QtWidgets.QTableWidgetItem(str(table[i][1])))
                self.tableWidget_15.setItem(rowPosition , 2,QtWidgets.QTableWidgetItem(str(table[i][2])))
                self.tableWidget_15.setItem(rowPosition , 3,QtWidgets.QTableWidgetItem(str(table[i][3])))
        self.mycursor.execute('select * from customers where Customer_Id=%s',(val,))
        table=self.mycursor.fetchall()
        if(len(table)>0):
            self.label_47.setText(table[0][5])
            self.label_48.setText(table[0][3])
            self.label_49.setText(str(table[0][6]))
            self.label_56.setText(str(table[0][0]))
            self.label_57.setText(str(table[0][1]))
        else:
            self.label_47.setText('Unknown')
            self.label_48.setText('Unknown')
            self.label_49.setText('0')
            self.label_56.setText('Unknown')
            self.label_57.setText('Unknown')
    def search_view(self):
        val=self.lineEdit_7.text()
        sql='select * from `all` where Item_Name like %s'
        self.mycursor.execute(sql,('%'+val+'%',))
        table=self.mycursor.fetchall()
        self.tableWidget_8.setRowCount(0)
        if(len(table)>0):
            for i in range(len(table)):
                rowPosition = self.tableWidget_8.rowCount()
                self.tableWidget_8.insertRow(rowPosition)
                self.tableWidget_8.setItem(rowPosition , 0,QtWidgets.QTableWidgetItem(str(table[i][0])))
                self.tableWidget_8.setItem(rowPosition , 1,QtWidgets.QTableWidgetItem(str(table[i][1])))
                self.tableWidget_8.setItem(rowPosition , 2,QtWidgets.QTableWidgetItem(str(table[i][2])))
                self.tableWidget_8.setItem(rowPosition , 3,QtWidgets.QTableWidgetItem(str(table[i][3])))
    def search_buttons(self):
        self.pushButton_33.clicked.connect(self.search_all)
        self.pushButton_35.clicked.connect(self.search_starters)
        self.pushButton_37.clicked.connect(self.search_main)
        self.pushButton_39.clicked.connect(self.search_desserts)
        self.pushButton_41.clicked.connect(self.search_drinks)
    def search_all(self):
        text=self.lineEdit_6.text()
        if(text==''):
            return
        sql='select * from `all` where Item_Name like %s'
        self.mycursor.execute(sql,('%'+text+'%',))
        table=self.mycursor.fetchall()
        self.tableWidget.setRowCount(0)
        if(len(table)>0):
            self.toggle_edit(True)
            for i in range(len(table)):
                rowPosition = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowPosition)
                self.tableWidget.setItem(rowPosition , 0,QtWidgets.QTableWidgetItem(str(table[i][0])))
                self.tableWidget.setItem(rowPosition , 1,QtWidgets.QTableWidgetItem(str(table[i][1])))
                self.tableWidget.setItem(rowPosition , 2,QtWidgets.QTableWidgetItem(str(table[i][2])))
                self.tableWidget.setItem(rowPosition , 3,QtWidgets.QTableWidgetItem(str(table[i][3])))
    def search_starters(self):
        text=self.lineEdit_9.text()
        if(text==''):
            return
        sql='select * from starters where Item_Name like %s'
        self.mycursor.execute(sql,('%'+text+'%',))
        table=self.mycursor.fetchall()
        self.tableWidget_2.setRowCount(0)
        if(len(table)>0):
            self.toggle_edit(True)
            for i in range(len(table)):
                rowPosition = self.tableWidget_2.rowCount()
                self.tableWidget_2.insertRow(rowPosition)
                self.tableWidget_2.setItem(rowPosition , 0,QtWidgets.QTableWidgetItem(str(table[i][0])))
                self.tableWidget_2.setItem(rowPosition , 1,QtWidgets.QTableWidgetItem(str(table[i][1])))
                self.tableWidget_2.setItem(rowPosition , 2,QtWidgets.QTableWidgetItem(str(table[i][2])))
                self.tableWidget_2.setItem(rowPosition , 3,QtWidgets.QTableWidgetItem(str(table[i][3])))
    def search_main(self):
        text=self.lineEdit_10.text()
        if(text==''):
            return
        sql='select * from maincourse where Item_Name like %s'
        self.mycursor.execute(sql,('%'+text+'%',))
        table=self.mycursor.fetchall()
        self.tableWidget_3.setRowCount(0)
        if(len(table)>0):
            self.toggle_edit(True)
            for i in range(len(table)):
                rowPosition = self.tableWidget_3.rowCount()
                self.tableWidget_3.insertRow(rowPosition)
                self.tableWidget_3.setItem(rowPosition , 0,QtWidgets.QTableWidgetItem(str(table[i][0])))
                self.tableWidget_3.setItem(rowPosition , 1,QtWidgets.QTableWidgetItem(str(table[i][1])))
                self.tableWidget_3.setItem(rowPosition , 2,QtWidgets.QTableWidgetItem(str(table[i][2])))
                self.tableWidget_3.setItem(rowPosition , 3,QtWidgets.QTableWidgetItem(str(table[i][3])))
    def search_desserts(self):
        text=self.lineEdit_15.text()
        if(text==''):
            return
        sql='select * from desserts where Item_Name like %s'
        self.mycursor.execute(sql,('%'+text+'%',))
        table=self.mycursor.fetchall()
        self.tableWidget_4.setRowCount(0)
        if(len(table)>0):
            self.toggle_edit(True)
            for i in range(len(table)):
                rowPosition = self.tableWidget_4.rowCount()
                self.tableWidget_4.insertRow(rowPosition)
                self.tableWidget_4.setItem(rowPosition , 0,QtWidgets.QTableWidgetItem(str(table[i][0])))
                self.tableWidget_4.setItem(rowPosition , 1,QtWidgets.QTableWidgetItem(str(table[i][1])))
                self.tableWidget_4.setItem(rowPosition , 2,QtWidgets.QTableWidgetItem(str(table[i][2])))
                self.tableWidget_4.setItem(rowPosition , 3,QtWidgets.QTableWidgetItem(str(table[i][3])))
    def search_drinks(self):
        text=self.lineEdit_16.text()
        if(text==''):
            return
        sql='select * from drinks where Item_Name like %s'
        self.mycursor.execute(sql,('%'+text+'%',))
        table=self.mycursor.fetchall()
        self.tableWidget_5.setRowCount(0)
        if(len(table)>0):
            self.toggle_edit(True)
            for i in range(len(table)):
                rowPosition = self.tableWidget_5.rowCount()
                self.tableWidget_5.insertRow(rowPosition)
                self.tableWidget_5.setItem(rowPosition , 0,QtWidgets.QTableWidgetItem(str(table[i][0])))
                self.tableWidget_5.setItem(rowPosition , 1,QtWidgets.QTableWidgetItem(str(table[i][1])))
                self.tableWidget_5.setItem(rowPosition , 2,QtWidgets.QTableWidgetItem(str(table[i][2])))
                self.tableWidget_5.setItem(rowPosition , 3,QtWidgets.QTableWidgetItem(str(table[i][3])))
    def search(self):
        self.select_type = str(self.comboBox_2.currentText())
        self.select_id=self.lineEdit_5.text()
        if(self.select_id==''):
            self.tableWidget_6.setRowCount(0)
            self.toggle_edit(False)
            return
        if(self.select_type=='Starters'):
            sql='select * from starters where Item_Id=%s'
        elif(self.select_type=='Main Course'):
            sql='select * from maincourse where Item_Id=%s'
        elif(self.select_type=='Desserts'):
            sql='select * from desserts where Item_Id=%s'
        elif(self.select_type=='Drinks'):
            sql='select * from drinks where Item_Id=%s'
        self.mycursor.execute(sql,(self.select_id,))
        table=self.mycursor.fetchall()
        self.tableWidget_6.setRowCount(0)
        if(len(table)>0):
            self.toggle_edit(True)
            for i in range(len(table)):
                rowPosition = self.tableWidget_6.rowCount()
                self.tableWidget_6.insertRow(rowPosition)
                self.tableWidget_6.setItem(rowPosition , 0,QtWidgets.QTableWidgetItem(str(table[i][0])))
                self.tableWidget_6.setItem(rowPosition , 1,QtWidgets.QTableWidgetItem(str(table[i][1])))
                self.tableWidget_6.setItem(rowPosition , 2,QtWidgets.QTableWidgetItem(str(table[i][2])))
                self.tableWidget_6.setItem(rowPosition , 3,QtWidgets.QTableWidgetItem(str(table[i][3])))
        else:
            self.toggle_edit(False)
    def change_type(self):
        val=str(self.comboBox_2.currentText())
        if(val==self.select_type):
            return
        if(val=='Starters'):
            val='starters'
        elif(val=='Main Course'):
            val='maincourse'
        elif(val=='Desserts'):
            val='desserts'
        elif(val=='Drinks'):
            val='drinks'  
        if(self.select_type=='Starters'):
            self.mycursor.execute('insert into '+val+' select * from starters where Item_Id=%s',(self.select_id,))
        elif(self.select_type=='Main Course'):
            self.mycursor.execute('insert into '+val+' select * from maincourse where Item_Id=%s',(self.select_id,))
        elif(self.select_type=='Desserts'):
            self.mycursor.execute('insert into '+val+' select * from desserts where Item_Id=%s',(self.select_id,))
        elif(self.select_type=='Drinks'):
            self.mycursor.execute('insert into '+val+' select * from drinks where Item_Id=%s',(self.select_id,))
        self.mydb.commit()
        if(self.select_type=='Starters'):
            sql='delete from starters where Item_Id=%s'
        elif(self.select_type=='Main Course'):
            sql='delete from maincourse where Item_Id=%s'
        elif(self.select_type=='Desserts'):
            sql='delete from desserts where Item_Id=%s'
        elif(self.select_type=='Drinks'):
            sql='delete from drinks where Item_Id=%s'
        self.mycursor.execute(sql,(self.select_id,))
        self.mydb.commit()
        Tk().wm_withdraw()
        messagebox.showinfo('Success','Item Type changed successfully !')
    def change_id(self):
        val=str(self.comboBox_2.currentText())
        if(val=='Starters'):
            val='starters'
        elif(val=='Main Course'):
            val='maincourse'
        elif(val=='Desserts'):
            val='desserts'
        elif(val=='Drinks'):
            val='drinks'
        value=self.lineEdit_12.text()
        sql='update '+val+' set Item_Id=%s where Item_Id=%s'
        self.mycursor.execute(sql,(value,self.select_id))
        self.mydb.commit()
        Tk().wm_withdraw()
        messagebox.showinfo('Success','Item ID changed successfully !')
    def change_name(self):
        val=str(self.comboBox_2.currentText())
        if(val=='Starters'):
            val='starters'
        elif(val=='Main Course'):
            val='maincourse'
        elif(val=='Desserts'):
            val='desserts'
        elif(val=='Drinks'):
            val='drinks'
        value=self.lineEdit_13.text()
        sql='update '+val+' set Item_Name=%s where Item_Id=%s'
        self.mycursor.execute(sql,(value,self.select_id))
        self.mydb.commit()
        Tk().wm_withdraw()
        messagebox.showinfo('Success','Item Name changed successfully !')
    def change_halfrate(self):
        val=str(self.comboBox_2.currentText())
        if(val=='Starters'):
            val='starters'
        elif(val=='Main Course'):
            val='maincourse'
        elif(val=='Desserts'):
            val='desserts'
        elif(val=='Drinks'):
            val='drinks'
        value=self.lineEdit_14.text()
        sql='update '+val+' set Half_Rate=%s where Item_Id=%s'
        self.mycursor.execute(sql,(value,self.select_id))
        self.mydb.commit()
        Tk().wm_withdraw()
        messagebox.showinfo('Success','Half Rate changed successfully !')
    def change_fullrate(self):
        val=str(self.comboBox_2.currentText())
        if(val=='Starters'):
            val='starters'
        elif(val=='Main Course'):
            val='maincourse'
        elif(val=='Desserts'):
            val='desserts'
        elif(val=='Drinks'):
            val='drinks'
        value=self.lineEdit_11.text()
        sql='update '+val+' set Full_Rate=%s where Item_Id=%s'
        self.mycursor.execute(sql,(value,self.select_id))
        self.mydb.commit()
        Tk().wm_withdraw()
        messagebox.showinfo('Success','Full Rate changed successfully !')
    def edit_buttons(self):
        self.pushButton_18.clicked.connect(self.change_type)
        self.pushButton_19.clicked.connect(self.change_id)
        self.pushButton_20.clicked.connect(self.change_name)
        self.pushButton_21.clicked.connect(self.change_halfrate)
        self.pushButton_22.clicked.connect(self.change_fullrate)
    def delete(self):
        if(self.select_type=='Starters'):
            sql='delete from starters where Item_Id=%s'
        elif(self.select_type=='Main Course'):
            sql='delete from maincourse where Item_Id=%s'
        elif(self.select_type=='Desserts'):
            sql='delete from desserts where Item_Id=%s'
        elif(self.select_type=='Drinks'):
            sql='delete from drinks where Item_Id=%s'
        Tk().wm_withdraw()
        ans=messagebox.askyesno('Caution','Do you want to delete this food item?')
        if(ans):
            self.mycursor.execute(sql,(self.select_id,))
            self.mydb.commit()
            Tk().wm_withdraw()
            messagebox.showinfo('Success','Menu Item deleted successfully !')
    def toggle_edit(self,toggle):
        if(toggle):
            self.pushButton_14.setEnabled(True)
            self.pushButton_18.setEnabled(True)
            self.pushButton_19.setEnabled(True)
            self.pushButton_20.setEnabled(True)
            self.pushButton_21.setEnabled(True)
            self.pushButton_22.setEnabled(True)
        else:
            self.pushButton_14.setDisabled(True)
            self.pushButton_18.setDisabled(True)
            self.pushButton_19.setDisabled(True)
            self.pushButton_20.setDisabled(True)
            self.pushButton_21.setDisabled(True)
            self.pushButton_22.setDisabled(True)     
    def reset_additem(self):
        self.comboBox.setCurrentIndex(0)
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.lineEdit_3.setText('')
        self.lineEdit_4.setText('')
    def reset_edititem(self):
        self.comboBox_3.setCurrentIndex(0)
        self.lineEdit_11.setText('')
        self.lineEdit_12.setText('')
        self.lineEdit_13.setText('')
        self.lineEdit_14.setText('')
    def check_addition(self):
        var1=self.lineEdit.text()
        var2=self.lineEdit_2.text()
        var3=self.lineEdit_3.text()
        var4=self.lineEdit_4.text()
        Tk().wm_withdraw()
        if(var1==''):
            messagebox.showerror('Error Id','Item Id Empty')
            return(False)
        self.mycursor.execute('select * from `all` where Item_Id=%s',(var1,))
        data=self.mycursor.fetchall()
        if(len(data)>0):
            Tk().wm_withdraw()
            messagebox.showerror('Error Item_Id','Item Id already exists')
            return(False)
        if(var2==''):
            messagebox.showerror('Error Name','Item Name Empty')
            return(False)
        if(var3!=''):
            try:
                float(var3)
            except:
                messagebox.showerror('Error Half Price','Half price Error')
                return(False)
        if(var4==''):
            messagebox.showerror('Error Full Price','Full price Error')
            return(False)
        if(var4!=''):
            try:
                float(var4)
            except:
                messagebox.showerror('Error Full Price','Full price Error')
                return(False)
        return(True)
    def add_item(self):
        if(self.check_addition()):
            text = str(self.comboBox.currentText())
            var1=self.lineEdit.text()
            var2=self.lineEdit_2.text()
            var3=self.lineEdit_3.text()
            var4=self.lineEdit_4.text()
            if(var3==''):
                var3=None
            if(text=='Starters'):
                sql = "INSERT INTO starters (Item_Id,Item_Name,Half_Rate,Full_Rate) VALUES (%s,%s,%s,%s)"
            if(text=='Main Course'):
                sql = "INSERT INTO maincourse (Item_Id,Item_Name,Half_Rate,Full_Rate) VALUES (%s,%s,%s,%s)"
            if(text=='Desserts'):
                sql = "INSERT INTO desserts (Item_Id,Item_Name,Half_Rate,Full_Rate) VALUES (%s,%s,%s,%s)"
            if(text=='Drinks'):
                sql = "INSERT INTO drinks (Item_Id,Item_Name,Half_Rate,Full_Rate) VALUES (%s,%s,%s,%s)"
            val = (var1,var2,var3,var4)
            self.mycursor.execute(sql,val)
            self.mydb.commit()
            Tk().wm_withdraw()
            messagebox.showinfo('Write Successful','Menu Item added to the database')
    def login_datetime(self):
        self.dt=dt.now()
        self.date=str(self.dt.day)+'/'+str(self.dt.month)+'/'+str(self.dt.year)
        if(self.dt.hour>12):
            self.time=str(self.dt.hour-12)+':'+str(self.dt.minute)+':'+str(self.dt.second)+' PM'
        else:
            self.time=str(self.dt.hour)+':'+str(self.dt.minute)+':'+str(self.dt.second)+' AM'
        self.label_8.setText(self.time)
        self.label_13.setText(self.date)
    def reset1(self):
        sql='select * from `all`'
        self.mycursor.execute(sql)
        table=self.mycursor.fetchall()
        self.tableWidget.setRowCount(0)
        if(len(table)>0):
            for i in range(len(table)):
                rowPosition = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowPosition)
                self.tableWidget.setItem(rowPosition , 0,QtWidgets.QTableWidgetItem(str(table[i][0])))
                self.tableWidget.setItem(rowPosition , 1,QtWidgets.QTableWidgetItem(str(table[i][1])))
                self.tableWidget.setItem(rowPosition , 2,QtWidgets.QTableWidgetItem(str(table[i][2])))
                self.tableWidget.setItem(rowPosition , 3,QtWidgets.QTableWidgetItem(str(table[i][3])))
    def reset2(self):
        sql='select * from starters'
        self.mycursor.execute(sql)
        table=self.mycursor.fetchall()
        self.tableWidget_2.setRowCount(0)
        if(len(table)>0):
            for i in range(len(table)):
                rowPosition = self.tableWidget_2.rowCount()
                self.tableWidget_2.insertRow(rowPosition)
                self.tableWidget_2.setItem(rowPosition , 0,QtWidgets.QTableWidgetItem(str(table[i][0])))
                self.tableWidget_2.setItem(rowPosition , 1,QtWidgets.QTableWidgetItem(str(table[i][1])))
                self.tableWidget_2.setItem(rowPosition , 2,QtWidgets.QTableWidgetItem(str(table[i][2])))
                self.tableWidget_2.setItem(rowPosition , 3,QtWidgets.QTableWidgetItem(str(table[i][3])))
    def reset3(self):
        sql='select * from maincourse'
        self.mycursor.execute(sql)
        table=self.mycursor.fetchall()
        self.tableWidget_3.setRowCount(0)
        if(len(table)>0):
            for i in range(len(table)):
                rowPosition = self.tableWidget_3.rowCount()
                self.tableWidget_3.insertRow(rowPosition)
                self.tableWidget_3.setItem(rowPosition , 0,QtWidgets.QTableWidgetItem(str(table[i][0])))
                self.tableWidget_3.setItem(rowPosition , 1,QtWidgets.QTableWidgetItem(str(table[i][1])))
                self.tableWidget_3.setItem(rowPosition , 2,QtWidgets.QTableWidgetItem(str(table[i][2])))
                self.tableWidget_3.setItem(rowPosition , 3,QtWidgets.QTableWidgetItem(str(table[i][3])))
    def reset4(self):
        sql='select * from desserts'
        self.mycursor.execute(sql)
        table=self.mycursor.fetchall()
        self.tableWidget_4.setRowCount(0)
        if(len(table)>0):
            for i in range(len(table)):
                rowPosition = self.tableWidget_4.rowCount()
                self.tableWidget_4.insertRow(rowPosition)
                self.tableWidget_4.setItem(rowPosition , 0,QtWidgets.QTableWidgetItem(str(table[i][0])))
                self.tableWidget_4.setItem(rowPosition , 1,QtWidgets.QTableWidgetItem(str(table[i][1])))
                self.tableWidget_4.setItem(rowPosition , 2,QtWidgets.QTableWidgetItem(str(table[i][2])))
                self.tableWidget_4.setItem(rowPosition , 3,QtWidgets.QTableWidgetItem(str(table[i][3])))
    def reset5(self):
        sql='select * from drinks'
        self.mycursor.execute(sql)
        table=self.mycursor.fetchall()
        self.tableWidget_5.setRowCount(0)
        if(len(table)>0):
            for i in range(len(table)):
                rowPosition = self.tableWidget_5.rowCount()
                self.tableWidget_5.insertRow(rowPosition)
                self.tableWidget_5.setItem(rowPosition , 0,QtWidgets.QTableWidgetItem(str(table[i][0])))
                self.tableWidget_5.setItem(rowPosition , 1,QtWidgets.QTableWidgetItem(str(table[i][1])))
                self.tableWidget_5.setItem(rowPosition , 2,QtWidgets.QTableWidgetItem(str(table[i][2])))
                self.tableWidget_5.setItem(rowPosition , 3,QtWidgets.QTableWidgetItem(str(table[i][3])))
    def background(self):
        movie=QMovie("Assets//back.gif")
        self.label.setMovie(movie)
        movie.start()
        movie1=QMovie("Assets//table.gif")
        self.label_21.setMovie(movie1)
        movie1.start()
        movie2=QMovie("Assets//ex.gif")
        self.label_64.setMovie(movie2)
        movie2.start()
        movie3=QMovie("Assets//people.gif")
        self.label_70.setMovie(movie3)
        movie3.start()
    def reset_buttons(self):
        self.pushButton_7.clicked.connect(self.reset1)
        self.pushButton_8.clicked.connect(self.reset2)
        self.pushButton_9.clicked.connect(self.reset3)
        self.pushButton_10.clicked.connect(self.reset4)
        self.pushButton_11.clicked.connect(self.reset5)
    def tabs(self):
        self.pushButton.clicked.connect(lambda: self.tabWidget.setCurrentIndex(0))
        self.pushButton_5.clicked.connect(lambda : self.tabWidget.setCurrentIndex(1))
        self.pushButton_2.clicked.connect(lambda : self.tabWidget.setCurrentIndex(2))
        self.pushButton_3.clicked.connect(lambda : self.tabWidget.setCurrentIndex(3))
        self.pushButton_4.clicked.connect(lambda : self.tabWidget.setCurrentIndex(4))
        self.pushButton_6.clicked.connect(lambda : self.tabWidget.setCurrentIndex(5))
        self.pushButton_52.clicked.connect(lambda : self.tabWidget.setCurrentIndex(6))
    def set_theme(self):
        file = QFile("Assets//DarkOrange.qss")
        file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(file)
        self.setStyleSheet(stream.readAll())
    def search_customer(self):
        self.tableWidget_14.setRowCount(0)
        a=[]
        fields={0:'(Date',1:'(Time',2:'(Table_Number',3:'(Customer_Name',4:'(Order_type',5:'(Amount'}
        a.append(self.groupBox_6.isChecked());a.append(self.groupBox_7.isChecked());a.append(self.groupBox_10.isChecked())
        a.append(self.groupBox_11.isChecked());a.append(self.groupBox_12.isChecked());a.append(self.groupBox_14.isChecked())
        c=[]
        b=self.dateEdit.date().toPyDate();c.append(b)
        b=self.dateEdit_2.date().toPyDate();c.append(b)
        b=self.timeEdit.time().toString();c.append(b)
        b=self.timeEdit_2.time().toString();c.append(b)
        b=self.spinBox.value();c.append(b)
        b=self.spinBox_2.value();c.append(b)
        b=self.lineEdit_17.text()
        if(b=='' and a[3]):
            Tk().wm_withdraw()
            messagebox.showerror('Customer Name','Customer Name blank')
            self.pushButton_27.setDisabled(True)
            return
        else:
            c.append(b)
        b=self.comboBox_5.currentText();c.append(b)
        b=self.lineEdit_18.text()
        if(b=='' and a[5]):
            Tk().wm_withdraw()
            messagebox.showerror('Amount','From value blank')
            self.pushButton_27.setDisabled(True)
            return
        else:
            c.append(b)
        b=self.lineEdit_19.text()
        if(b=='' and a[5]):
            Tk().wm_withdraw()
            messagebox.showerror('Amount','To value blank')
            self.pushButton_27.setDisabled(True)
            return
        else:
            c.append(b)
        d={0:[c[0],c[1]],1:[c[2],c[3]],2:[c[4],c[5]],3:'%'+c[6]+'%',4:c[7],5:[c[8],c[9]]}
        self.tableWidget_14.setRowCount(0)
        try:
            pos=a.index(True)
        except:
            Tk().wm_withdraw()
            messagebox.showerror('Search Parameters','No search parameters Checked')
            self.pushButton_27.setDisabled(True)
            return
        sql='select * from customers where '
        val=[]
        btw=' between %s and %s) '
        eq=' =%s) '
        like=' like %s) '
        for i in range(len(a)):
            if(a[i]):
                if(type(d[i])==list):
                    val.extend(d[i])
                else:
                    val.append(d[i])
                if(i==pos and i in [0,1,2,5]):
                    sql+=fields[i]+btw
                elif(i==pos and i==3):
                    sql+=fields[i]+like
                elif(i==pos and i==4):
                    sql+=fields[i]+eq
                elif(a[i] and i in [0,1,2,5]):
                    sql+='and '+fields[i]+btw
                elif(a[i] and i==3):
                    sql+='and '+fields[i]+like
                elif(a[i] and i==4):
                    sql+='and '+fields[i]+eq
        self.mycursor.execute(sql,val)
        table=self.mycursor.fetchall()
        if(len(table)>0):
            for i in range(len(table)):
                rowPosition = self.tableWidget_14.rowCount()
                self.tableWidget_14.insertRow(rowPosition)
                self.tableWidget_14.setItem(rowPosition , 0,QtWidgets.QTableWidgetItem(str(table[i][0])))
                self.tableWidget_14.setItem(rowPosition , 1,QtWidgets.QTableWidgetItem(str(table[i][1])))
                self.tableWidget_14.setItem(rowPosition , 2,QtWidgets.QTableWidgetItem(str(table[i][2])))
                self.tableWidget_14.setItem(rowPosition , 3,QtWidgets.QTableWidgetItem(str(table[i][3])))
                self.tableWidget_14.setItem(rowPosition , 4,QtWidgets.QTableWidgetItem(str(table[i][4])))
                self.tableWidget_14.setItem(rowPosition , 5,QtWidgets.QTableWidgetItem(str(table[i][5])))
                self.tableWidget_14.setItem(rowPosition , 6,QtWidgets.QTableWidgetItem(str(table[i][6])))
            self.label_43.setText(str(rowPosition+1))
            self.pushButton_27.setEnabled(True)
        else:
            self.label_43.setText('0')
            self.pushButton_27.setDisabled(True)
class new_order():
            def __init__(self,ui_var):
                self.obj=ui_var
                self.number=self.obj.lineEdit_26.text()
                now=dt.now()
                self.order_time=str(now.hour)+':'+str(now.minute)+':'+str(now.second)
                self.order_date=str(now.year)+'-'+str(now.month)+'-'+str(now.day)
                self.contents = QtWidgets.QWidget(self.obj.tabWidget_4)
                self.layout = QtWidgets.QVBoxLayout(self.contents)
                font = QFont("Segoe UI", 14) 
                self.grid = QGridLayout()
                self.l1 = QLabel();self.l1.setFont(font);self.l1.setText("Order Type:")
                self.l4 = QLabel();self.l4.setFont(font);self.l4.setText(str(self.obj.comboBox_4.currentText()))
                self.l2 = QLabel();self.l2.setFont(font);self.l2.setText("Customer Name:")
                self.l5 = QLabel();self.l5.setFont(font);self.l5.setText(str(self.obj.lineEdit_8.text()))
                self.grid.addWidget(self.l1,0,0)
                self.grid.addWidget(self.l2,1,0)
                self.grid.addWidget(self.l4,0,2)
                self.grid.addWidget(self.l5,1,2)
                if(str(self.obj.comboBox_4.currentText())=='Dine In'):
                    self.l3 = QLabel();self.l3.setFont(font);self.l3.setText("Table number:")
                    self.line = QLineEdit();self.line.setFont(font);self.line.setFixedWidth(40)
                    self.grid.addWidget(self.l3,3,0)
                    self.grid.addWidget(self.line,3,2)
                self.g1 = QGroupBox();self.g1.setTitle("Search Item:");self.g1.setFont(font)
                self.grid2 = QGridLayout()
                self.line1 = QLineEdit();self.line1.setFont(font);self.line1.setFixedWidth(500)
                self.grid2.addWidget(self.line1,0,0)
                self.b1 = QPushButton('Search');self.b1.setFont(font);self.b1.clicked.connect(self.search_view)
                self.grid2.addWidget(self.b1,0,1)
                self.t1= QTableWidget();self.t1.setColumnCount(4);self.t1.setHorizontalHeaderLabels(['Item ID', 'Item Name', 'Half Price', 'Full Price'])
                self.grid2.addWidget(self.t1,1,0,1,3)
                self.g1.setLayout(self.grid2)
                self.grid.addWidget(self.g1,4,0,1,3)
                self.g2 = QGroupBox();self.g2.setTitle("Order Details:");self.g2.setFont(font)
                self.grid3 = QGridLayout()
                self.t2= QTableWidget();self.t2.setColumnCount(3);self.t2.setHorizontalHeaderLabels(['Item ID','Half Quantity', 'Full Quantity'])
                allRows = self.obj.tableWidget_7.rowCount()
                for i in range(allRows):
                    c1 = self.obj.tableWidget_7.item(i,0)
                    c2 = self.obj.tableWidget_7.item(i,1)
                    c3 = self.obj.tableWidget_7.item(i,2)
                    if(c1!=None):
                        c1=c1.text()
                    if(c2!=None):
                        c2=c2.text()
                    if(c3!=None):
                        c3=c3.text()
                    self.t2.insertRow(i)
                    self.t2.setItem(i , 0,QtWidgets.QTableWidgetItem(c1))
                    self.t2.setItem(i , 1,QtWidgets.QTableWidgetItem(c2))
                    self.t2.setItem(i , 2,QtWidgets.QTableWidgetItem(c3))
                self.grid3.addWidget(self.t2,0,0)
                self.b2 = QPushButton('+');self.b2.setFont(font);self.b2.clicked.connect(lambda:self.t2.setRowCount(self.t2.rowCount()+1))
                self.b3 = QPushButton('-');self.b3.setFont(font);self.b3.clicked.connect(lambda:self.t2.setRowCount(self.t2.rowCount()-1))
                self.grid3.addWidget(self.b2,0,1)
                self.b4 = QPushButton('Order Completed');self.b4.setFont(font);self.b4.clicked.connect(self.order_complete)
                self.grid3.addWidget(self.b4,1,0)
                self.grid3.addWidget(self.b3,1,1)
                self.g2.setLayout(self.grid3)
                self.grid.addWidget(self.g2,5,0,1,3)
                self.layout.addLayout(self.grid)
                self.obj.tabWidget_4.addTab(self.contents, str(self.obj.lineEdit_8.text()))
            def sendPostRequest(reqUrl,phoneNo, senderId, textMessage):
                req_params = {
                'apikey':'LX9TDKCJZEK2PYX1FV820Z5JL57N058H',
                'secret': '3RTY9O4N1I8LJMJF',
                'usetype':'stage',
                'phone': phoneNo,
                'message':textMessage,
                'senderid':senderId}
                return requests.post('https://www.sms4india.com/api/v1/sendCampaign', req_params)
            def order_complete(self):
                if(self.order_check()):
                    typ=self.l4.text()
                    amount=0
                    for i in self.full_order:
                        amount+=i[3]
                    typ=self.l4.text()
                    if(typ=='Dine In'):
                        sql='insert into customers(Date,Time,Order_Type,Table_Number,Customer_Name,Amount) values(%s,%s,%s,%s,%s,%s)'
                        val=(self.order_date,self.order_time,typ,self.line.text(),self.l5.text(),amount)
                    else:
                        sql='insert into customers(Date,Time,Order_Type,Customer_Name,Amount) values(%s,%s,%s,%s,%s)'
                        val=(self.order_date,self.order_time,typ,self.l5.text(),amount)
                    self.obj.mycursor.execute(sql,val)
                    self.obj.mydb.commit()
                    self.obj.mycursor.execute('select Customer_Id from customers where time=%s',(self.order_time,))
                    Id=self.obj.mycursor.fetchall()[0][0]
                    string='Date:\t\t\t{}\nTime:\t\t\t{}\nCustomer Name:\t\t{}\nOrder Type:\t\t{}\n\nItem Id\t   Half Quantity\t   Full Quantiy\tPrice\n\n'.format(self.order_date,self.order_time,self.l5.text(),typ)
                    for i in self.full_order:
                        string+=i[0]+"\t\t"+str(i[1])+"\t\t"+str(i[2])+"\t"+str(i[3])+"\n"
                        sql='insert into orders(Customer_Id,Item_Id,Half_Quantity,Full_Quantity,Total) values(%s,%s,%s,%s,%s)'
                        val=(Id,i[0],i[1],i[2],i[3])
                        self.obj.mycursor.execute(sql,val)
                        self.obj.mydb.commit()
                    string+="\nTotal=\t"+str(amount)
                    self.obj.earning()
                    self.obj.tables_today()
                    self.obj.tables_served()
                    self.obj.favourite()
                    Tk().wm_withdraw()
                    messagebox.showinfo('Order Receipt',string)
                    index=self.obj.tabWidget_4.currentIndex()
                    self.obj.tabWidget_4.removeTab(index)
                    f=open("Assets/preference.txt",'r')
                    name=eval(f.readline())['name']
                    f.close()
                    if(len(self.number)==10):
                        try:
                            int(self.number)
                            response = self.sendPostRequest(self.number, name, 'Thank you for choosing \''+name+'\'. Your total bill was '+str(amount)+'. Hope to see you soon.' )   
                        except:
                            pass                            
            def order_check(self):
                typ=self.l4.text()
                self.full_order=[]
                if(typ=='Dine In' and (self.line.text()==None or self.line.text()=='')):
                    Tk().wm_withdraw()
                    messagebox.showerror('Error Table Number','No Table Number')
                    return(False)                        
                allRows = self.t2.rowCount()
                if(allRows==0):
                    Tk().wm_withdraw()
                    messagebox.showerror('Error Order','No order Items added')
                    return(False)
                for i in range(allRows):
                    total=0
                    c1 = self.t2.item(i,0)
                    c2 = self.t2.item(i,1)
                    c3 = self.t2.item(i,2)
                    if(c1!=None):
                        if(not(c1.text())):
                            Tk().wm_withdraw()
                            messagebox.showerror('Error Item Id','Item Id Empty\nRow='+str(i+1)+'\nColumn=Item ID')
                            return(False)
                        c1=c1.text()
                    else:
                        Tk().wm_withdraw()
                        messagebox.showerror('Error Item Id','Item Id Empty\nRow='+str(i+1)+'\nColumn=Item ID')
                        return(False)
                    if(c2==None):
                        if(c3==None):
                            Tk().wm_withdraw()
                            messagebox.showerror('Error Quantity','No quantity entered\nRow='+str(i+1)+'\nColumn=Half Quantity or Full Quantity')
                            return(False)          
                    elif(c2.text()):
                        c2=c2.text()
                        try:
                            c2=float(c2)
                        except:
                            Tk().wm_withdraw()
                            messagebox.showerror('Error Half Quantity','Half Quatity not a number\nRow='+str(i+1)+'\nColumn=Half Quantity')
                            return(False)
                    elif(c3!=None):
                        c2=0
                        if not(c3.text()):
                            Tk().wm_withdraw()
                            messagebox.showerror('Error Quantity','No quantity entered\nRow='+str(i+1)+'\nColumn=Half Quantity or Full Quantity')
                            return(False)
                    if(c3==None):
                        pass
                    elif(c3.text()):
                        c3=c3.text()
                        try:
                            c3=float(c3)
                        except:
                            Tk().wm_withdraw()
                            messagebox.showerror('Error Full Quantity','Full Quantity not a number\nRow='+str(i+1)+'\nColumn=Full Quantity')
                            return(False)
                    else:
                        Tk().wm_withdraw()
                        messagebox.showerror('Error Full Quantity','Full Quantity not a number\nRow='+str(i+1)+'\nColumn=Full Quantity')
                        return(False)
                    sql='select Half_Rate,Full_Rate from `all` where Item_Id=%s'
                    self.obj.mycursor.execute(sql,(c1,))
                    item=self.obj.mycursor.fetchall()
                    if(len(item)==0):
                        Tk().wm_withdraw()
                        messagebox.showerror('Error Item Name','Item not found\nRow='+str(i+1))
                        return(False)
                    else:
                        if(c2==None):
                            c2=0
                        if(c3==None):
                            c3=0
                        if(item[0][0]==None):
                            hp=0
                        else:
                            hp=item[0][0]
                        fp=item[0][1]
                        total=(c2*hp)+(c3*fp)
                        self.full_order.append([c1,c2,c3,total])
                return(True)
            def search_view(self):
                val=self.line1.text()
                sql='select * from `all` where Item_Name like %s'
                self.obj.mycursor.execute(sql,('%'+val+'%',))
                table=self.obj.mycursor.fetchall()
                self.t1.setRowCount(0)
                if(len(table)>0):
                    for i in range(len(table)):
                        rowPosition = self.t1.rowCount()
                        self.t1.insertRow(rowPosition)
                        self.t1.setItem(rowPosition , 0,QtWidgets.QTableWidgetItem(str(table[i][0])))
                        self.t1.setItem(rowPosition , 1,QtWidgets.QTableWidgetItem(str(table[i][1])))
                        self.t1.setItem(rowPosition , 2,QtWidgets.QTableWidgetItem(str(table[i][2])))
                        self.t1.setItem(rowPosition , 3,QtWidgets.QTableWidgetItem(str(table[i][3])))
class Import(QtWidgets.QDialog):
    def __init__(self,obj):
        super().__init__()
        self.obj=obj
        uic.loadUi('Import.ui',self)
        file = QFile("Assets//DarkOrange.qss")
        file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(file)
        self.setStyleSheet(stream.readAll())
        screen_center = lambda widget: QApplication.desktop().screen().rect().center()- widget.rect().center()
        self.move(screen_center(self))
        self.pushButton_3.clicked.connect(self.open_file)
        self.pushButton.clicked.connect(self.create_file)
        self.pushButton_2.clicked.connect(self.upload_file)
        self.setModal(True)
        self.anim()
        self.show()
    def create_file(self):
        source="Assets/Import.xlsx"
        destination=os.environ['USERPROFILE']+"\desktop\Import.xlsx"
        shutil.copyfile(source, destination)
        Tk().wm_withdraw()
        messagebox.showinfo('Import File','File Created Successfully on the DESKTOP')

    def open_file(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Spreadsheet (*.xlsx)", options=options)
        if fileName:
            self.lineEdit.setText(fileName)
    def upload_file(self):
        path=self.lineEdit.text()
        wb = xlrd.open_workbook(path)
        sheet = wb.sheet_by_index(0)
        def check():
            for i in range(1,sheet.nrows):
                if(sheet.cell_value(i, 0).lower() not in ['starters','main course','desserts','drinks']):
                    Tk().wm_withdraw()
                    messagebox.showerror('Error',f'Error detected at\nRow={i}\nColumn=A')
                    return(False)
                if(type(sheet.cell_value(i, 3))==str):
                    if(sheet.cell_value(i, 3)!=''):
                        Tk().wm_withdraw()
                        messagebox.showerror('Error',f'Error detected at\nRow={i}\nColumn=D')
                        return(False)
                if(type(sheet.cell_value(i, 4))==str):
                    if(sheet.cell_value(i, 4)!=''):
                        Tk().wm_withdraw()
                        messagebox.showerror('Error',f'Error detected at\nRow={i}\nColumn=E')
                        return(False)
            return(True)
        if(check()):
            for i in range(1,sheet.nrows):
                _type=sheet.cell_value(i, 0).lower()
                if(_type=='starters'):
                    sql = "INSERT INTO starters (Item_Id,Item_Name,Half_Rate,Full_Rate) VALUES (%s,%s,%s,%s)"
                if(_type=='main course'):
                    sql = "INSERT INTO maincourse (Item_Id,Item_Name,Half_Rate,Full_Rate) VALUES (%s,%s,%s,%s)"
                if(_type=='desserts'):
                    sql = "INSERT INTO desserts (Item_Id,Item_Name,Half_Rate,Full_Rate) VALUES (%s,%s,%s,%s)"
                if(_type=='drinks'):
                    sql = "INSERT INTO drinks (Item_Id,Item_Name,Half_Rate,Full_Rate) VALUES (%s,%s,%s,%s)"
                val = (sheet.cell_value(i, 1),sheet.cell_value(i, 2),None if(sheet.cell_value(i, 3))=='' else float(sheet.cell_value(i, 3)),None if(sheet.cell_value(i, 4))=='' else float(sheet.cell_value(i, 4)))
                self.obj.mycursor.execute(sql,val)
                self.obj.mydb.commit()
        Tk().wm_withdraw()
        messagebox.showinfo('Write Succesfull','File Successfully imported into the database.')   

    def anim(self):
        movie1=QMovie("Assets//xls.gif")
        self.label_3.setMovie(movie1)
        movie1.start()
class Export(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('Export.ui', self)
        file = QFile("Assets//DarkOrange.qss")
        file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(file)
        self.setStyleSheet(stream.readAll())
        screen_center = lambda widget: QApplication.desktop().screen().rect().center()- widget.rect().center()
        self.move(screen_center(self))
        self.pushButton.clicked.connect(self.select_path)
        self.pushButton_2.clicked.connect(self.save)
        self.anim()
        self.show()
    def anim(self):
        movie1=QMovie("Assets//xls.gif")
        self.label_3.setMovie(movie1)
        movie1.start()
    def select_path(self):
        fileName = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if fileName:
            self.lineEdit_2.setText(fileName)
    def check(self):
        if(self.lineEdit.text()=='' or self.lineEdit_2.text()==''):
            Tk().wm_withdraw()
            messagebox.showerror('Error','Field(s) empty')
            return(False)
        else:
            return(True)
    def save(self):
        if(self.check()):
            self.path=self.lineEdit_2.text()
            self.file=self.lineEdit.text()+'.xls'
            self.close()
            return
class Login(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('login.ui', self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        screen_center = lambda widget: QApplication.desktop().screen().rect().center()- widget.rect().center()
        self.move(screen_center(self))
        self.set_theme()
        self.show()
        self.show=QPixmap("Assets//show.png")
        self.hide=QPixmap("Assets//hide.png")
        self.pushButton_3.setIcon(QIcon(self.show))
        self.pushButton_3.setStyleSheet("background:transparent;border: 0px;")
        self.echo=False
        self.pushButton_3.clicked.connect(self.pass_visibility)
        self.pushButton.clicked.connect(self.check_pass)
        self.pushButton_2.clicked.connect(self.close)
        self.lineEdit_2.setFocus()
        global mydb,mycursor
    def set_theme(self):
                file = QFile("Assets//DarkOrange.qss")
                file.open(QFile.ReadOnly | QFile.Text)
                stream = QTextStream(file)
                self.setStyleSheet(stream.readAll())
    def pass_visibility(self):
        if(self.echo==True):
            self.lineEdit.setEchoMode(QLineEdit.Password)
            self.echo=False
            self.pushButton_3.setIcon(QIcon(self.show))
        else:
            self.lineEdit.setEchoMode(QLineEdit.Normal)
            self.echo=True
            self.pushButton_3.setIcon(QIcon(self.hide))
            
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.check_pass()
    def check_pass(self):
        var1=self.lineEdit_2.text()
        var2=self.lineEdit.text()
        if(var1=='' or var2==''):
            return
        c=True
        try:
            self.mydb = mysql.connector.connect(host="localhost",user=var1,passwd=var2)
        except:
            c=False
        if(c):
            self.mycursor = self.mydb.cursor()
            self.mycursor.execute('create database if not exists restaurant')
            self.mycursor.execute('use restaurant')
            self.mycursor.execute('create table if not exists starters(Item_Id VARCHAR(45) PRIMARY KEY,Item_Name VARCHAR(60),Half_Rate FLOAT,Full_Rate FLOAT)')
            self.mycursor.execute('create table if not exists maincourse(Item_Id VARCHAR(45) PRIMARY KEY,Item_Name VARCHAR(60),Half_Rate FLOAT,Full_Rate FLOAT)')
            self.mycursor.execute('create table if not exists desserts(Item_Id VARCHAR(45) PRIMARY KEY,Item_Name VARCHAR(60),Half_Rate FLOAT,Full_Rate FLOAT)')
            self.mycursor.execute('create table if not exists drinks(Item_Id VARCHAR(45) PRIMARY KEY,Item_Name VARCHAR(60),Half_Rate FLOAT,Full_Rate FLOAT)')
            self.mycursor.execute('create or replace view `all` as select * from starters union select * from maincourse union select * from desserts union select * from drinks')
            self.mycursor.execute('create table if not exists customers(Date DATE,Time TIME,Customer_Id INT AUTO_INCREMENT PRIMARY KEY,Order_Type VARCHAR(15),Table_Number INT,Customer_Name VARCHAR(60),Amount FLOAT)')
            self.mycursor.execute('create table if not exists orders(Customer_Id INT,Item_Id VARCHAR(30),Half_Quantity INT,Full_Quantity INT,Total FLOAT)')
            self.mycursor.execute('create table if not exists login(Date DATE,Time TIME,Tables_Served INT,Earning INT,Favourite VARCHAR(60))')
            self.mycursor.execute('create table if not exists logout(Date DATE,Time TIME,Tables_Served INT,Earning INT,Favourite VARCHAR(60))')
            self.close()
            self.Main()
        else:
            print("Error")
    def Main(self):
        self.main=Ui(self)
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Login()
    sys.exit(app.exec_())






