from flask import *
from database import *

import random 
import uuid
import smtplib
from email.mime.text import MIMEText
from flask_mail import Mail
from sklearn.ensemble import RandomForestClassifier
import sklearn


api=Blueprint('api',__name__)

@api.route('/login',methods=['get','post'])
def login():
	data={}
	
	username = request.args['username']
	password = request.args['password']
	q="SELECT * from login where username='%s' and password='%s'" % (username,password)
	res = select(q)
	if res :
		data['status']  = 'success'
		data['data'] = res
	else:
		data['status']	= 'failed'
	data['method']='login'
	return  str(data)



@api.route('/getaccountdetails',methods=['get','post'])
def getaccountdetails():
	data={}
	lid=request.args['lid']
	q="select * from request where status='accept'  and user_id=(select user_id from user where login_id='%s')"%(lid)
	ress=select(q)
	print(ress)
	print(q)
	if  ress:
		q="select * from account where user_id=(select user_id from user where login_id='%s')"%(lid)
		res=select(q)
		acc=res[0]['accountnumber']
		data['acco']=acc

		amt=res[0]['balance']
		data['amo']=amt
		data['status']  = 'success'
	else:
		data['status']	= 'failed'
	data['method']='getaccountdetails'
	return  str(data)

@api.route('/transctdetails',methods=['get','post'])
def transctdetails():
	data={}
	lid=request.args['lid']
	f=request.args['facc']
	t=request.args['tacc']
	a=request.args['amount']

	q="SELECT *,request.status as st FROM `request` inner join account using(user_id) WHERE user_id!=(select user_id from user where login_id='%s') AND `accountnumber`='%s' AND request.`status`='accept'"%(lid,t)
	res1=select(q)

	if res1:
		data['f']=f
		data['t']=t
		data['a']=a
		data['status']  = 'success'
	else:
		data['status']	= 'failed'
	data['method']='transctdetails'
	return  str(data)

@api.route('/Verifycreditdetails',methods=['get','post'])
def Verifycreditdetails():
	data={}
	card=request.args['cardnum']
	month=request.args['month']
	cvv=request.args['cvv']
	pin_no=request.args['pin']
	ifsc=request.args['ifsc']
	bank=request.args['account']
	lid=request.args['lid']

	q="SELECT * FROM `creditcard` WHERE `cardnum`='%s' AND `month`='%s' AND `pin_no`='%s' AND `ifsc_code`='%s' AND`acc_no`='%s' and cvv='%s' and user_id=(select user_id from user where login_id='%s') "%(card,month,pin_no,ifsc,bank,cvv,lid)
	print(q)
	res=select(q)
	if res:
		q="SELECT COUNT(`detect_id`) AS counts FROM detect WHERE user_id=(select user_id from user where login_id='%s')"%(lid)
		res1=select(q)
		if res1:
			
			q="delete from detect where user_id=(select user_id from user where login_id='%s')"%(lid)
			delete(q)
			
						
			q="select * from creditcard inner join user using(user_id) where user_id=(select user_id from user where login_id='%s')"%(lid)
			res=select(q)
			if res:
				n=random.randint(1000,9999)
				n1=str(n)
				print(n)
				data['otp']=n
				email=res[0]['email']

				
				email=email
				print(email)
				pwd="YOUR OTP :"+n1
				print(pwd)
				try:
					gmail = smtplib.SMTP('smtp.gmail.com', 587)
					gmail.ehlo()
					gmail.starttls()
					gmail.login('hariharan0987pp@gmail.com','rjcbcumvkpqynpep')
				except Exception as e:
					print("Couldn't setup email!!"+str(e))

				pwd = MIMEText(pwd)

				pwd['Subject'] = 'OTP'

				pwd['To'] = email

				pwd['From'] = 'hariharan0987pp@gmail.com'

				try:
					gmail.send_message(pwd)
					print(pwd)
					flash("EMAIL SENED SUCCESFULLY")
						


				except Exception as e:
					print("COULDN'T SEND EMAIL", str(e))
				else:
					flash("Added successfully")

				data['status']  = 'success'
			
	else:
		data['outs']=""
		q="insert into detect values(null,'%s','pending')"%(lid)
		insert(q)

		q="SELECT COUNT(`detect_id`) AS counts FROM detect WHERE user_id='%s'"%(lid)
		res1=select(q)
		if res1:
			counts=res1[0]['counts']
			if int (counts) > 3:
				q="UPDATE `creditcard` SET `status`='blocked' WHERE user_id='%s'"%(lid)
				update(q)
				data['status']  = 'Your are Blocked'
			else:
				data['status']="invalid Data"
		else:
			data['status']="invalid Data"

	data['method']='Verifycreditdetails'
	return  str(data)

@api.route('/transact',methods=['get','post'])
def transact():
	data={}
	f=request.args['f']
	t=request.args['t']

	a=request.args['a']
	lati=request.args['lati']
	longi=request.args['longi']
	q="SELECT *  FROM `transaction` where faccount='%s'" %(f)
	res=select(q)
	print("totalllllllllllllllkkkkkkkkkkkkkkkkkkkkkkkkkkkkk",len(res))
	reslat = []
	reslong = []
	resamount = []
	if len(res)!=0:
		for i in res:
			print("i",i)
			print("f")
			reslat.append(["0", i['latitude'], i['longitude']])
			reslong.append(["0", i['longitude']])
			resamount.append(["0", i['amount']])
			print("hello")
		reslat.append(["0", lati, longi])
		reslong.append(["0", longi])
		print("reslat",reslat)
		# resamount.append(["0", bal])
		# print("location")


		resloc = outlier(reslat)

		print("Amount",resloc)
		# resmt = outlier(resamount)
		resll = resloc[len(resloc) - 1]
		print("resl1",resll)
		if resll != -1:

			q="insert into transaction values(null,'%s','%s','%s','%s','%s',curdate(),'debit')"%(f,t,a,lati,longi)
			insert(q)
			# q="insert into transaction values(null,'%s','%s','%s','%s',curdate(),'credit')"%(t,a,lati,longi)
			# insert(q)
			
			q="update account set balance=balance-'%s'  where accountnumber='%s'"%(a,f)
			update(q)
			q="update account set balance=balance+'%s'  where accountnumber='%s'"%(a,t)
			update(q)

			data['status']	= 'success'
		else:
			data['status']	= 'Fake Detect'
	else:
		q="insert into transaction values(null,'%s','%s','%s','%s','%s',curdate(),'debit')"%(f,t,a,lati,longi)
		insert(q)
		# q="insert into transaction values(null,'%s','%s','%s','%s',curdate(),'credit')"%(t,a,lati,longi)
		# insert(q)
		
		q="update account set balance=balance-'%s'  where accountnumber='%s'"%(a,f)
		update(q)
		q="update account set balance=balance+'%s'  where accountnumber='%s'"%(a,t)
		update(q)
		data['status']	= 'success'

	data['method']='transact'
	return  str(data)

def outlier(res):
    print("outlier")
    ano = []

    print(res)

    model = sklearn.ensemble.IsolationForest(n_estimators=50, max_samples='auto'
                                            , contamination=float(0.1), max_features=1.0)
    model.fit(res)

    ano.append(model.predict(res))
    print(ano)
    anomaly = []
    idvalue = 0
    for ij in ano:
        print(ij)
    res=[]
    for index, value in enumerate(ij, start=1):
        # print(list((index, value)))  # print(k)
        res.append(value)
    print(res)
    return res