
from itertools import count
from flask import Flask,Blueprint,render_template,request,url_for,redirect,session,flash
from database import*
import smtplib
from email.mime.text import MIMEText
from flask_mail import Mail

import random 


user=Blueprint('user',__name__)



@user.route('/user_home')
def user_home():

	return render_template('user_home.html')

@user.route('/user_managecreditcard',methods=['post','get'])
def user_managecreditcard():

	data={}
	uid=session['user_id']
	q="select * from creditcard inner join user using (user_id) where user_id='%s'"%(uid)
	res=select(q)
	data['cre']=res

	if "action" in request.args:
		action=request.args['action']
		cid=request.args['cid']


	else:
		action=None


	if action=='delete':
		q="delete from creditcard where creditcard_id='%s'"%(cid)
		delete(q)
		flash(' successfully')
		return redirect(url_for('user.user_managecreditcard'))

	if action=='update':
		q="select * from creditcard where creditcard_id='%s'"%(cid)
		res=select(q)
		data['cred']=res


	if "update" in request.form:
		c=request.form['card']
		m=request.form['month']
		p=request.form['pin_no']
		i=request.form['ifsc']
		b=request.form['bank']
		q="update creditcard set cardnum='%s',month='%s',pin_no='%s',ifsc_code='%s',acc_no='%s',status='pending' where creditcard_id='%s'"%(c,m,p,i,b,cid)
		update(q)
		flash(' successfully')
		return redirect(url_for('user.user_managecreditcard'))



	if "credit" in request.form:
		uid=session['user_id']
		c=request.form['card']
		m=request.form['month']
		cvv=request.form['cvv']
		p=request.form['pin_no']
		i=request.form['ifsc']
		b=request.form['bank']

		q="insert into creditcard values(null,'%s','%s','%s','%s',curdate(),'30000','%s','%s','%s','pending')"%(uid,c,m,p,i,b,cvv)
		insert(q)
		flash(' successfully')
		return redirect(url_for('user.user_managecreditcard'))
	return render_template('user_managecreditcard.html',data=data)


@user.route('/user_requestacc',methods=['post','get'])
def user_requestacc():
	data={}
	uid=session['user_id']

	q="select * from request inner join user using (user_id) where user_id='%s'"%(uid)
	res=select(q)
	data['req']=res

	if "request" in request.form:
			uid=session['user_id']
			d=request.form['det']
			q="insert into request values(null,'%s','%s',curdate(),'pending')"%(uid,d)
			insert(q)
			flash(' successfully')
			return redirect(url_for('user.user_requestacc'))				
	
	return render_template('user_requestacc.html',data=data)

@user.route('/user_viewtransaction')	
def user_viewtransaction():
	data={}
	q="select * from transaction"
	res=select(q)
	data['tra']=res
	return render_template('user_viewtransaction.html',data=data)

@user.route('/user_managedeposit',methods=['post','get'])
def user_managedeposit():
	data={}
	uid=session['user_id']
	q="select * from creditcard inner join user using (user_id) where user_id='%s'"%(uid)
	res=select(q)
	data['acc']=res

	if "acc" in request.form:
		crid=request.args['crid']
		b=request.form['bal']
		q="update creditcard set balance=balance+'%s' where creditcard_id='%s'"%(b,crid)
		update(q)

		q="insert into transaction values(null,'%s','','%s',curdate(),'credit')"%(crid,b)
		insert(q)
		flash(' successfully')
		return redirect(url_for('user.user_managecreditcard'))
		

	return render_template('user_managedeposit.html',data=data)

@user.route('/user_transfer',methods=['post','get'])
def user_transfer():
	data={}
	uid=session['user_id']

	q="select * from request where status='accept'  and user_id='%s'"%(uid)
	ress=select(q)
	print(ress)
	print(q)
	if  ress:
		q="select * from account where user_id='%s'"%(uid)
		res=select(q)
		acc=res[0]['accountnumber']
		data['acco']=acc

		amt=res[0]['balance']
		data['amo']=amt



	if "transfer" in request.form:
		f=request.form['facc']
		t=request.form['toacc']
		a=request.form['amo']

		q="SELECT *,request.status as st FROM `request` inner join account using(user_id) WHERE user_id!='%s' AND `accountnumber`='%s' AND request.`status`='accept'"%(uid,t)
		res1=select(q)

		if res1:
			session['f']=f
			session['t']=t
			session['a']=a
			return redirect(url_for('user.user_account_verification'))
		else:
			flash("the account is not accepted")
			return redirect(url_for('user.user_transfer'))



		# if int(amt)>=int(a):
			
		# 	q="select * from account where accountnumber='%s'"%(t)
		# 	res=select(q)
		# 	if res:
		# 		return redirect(url_for('user.user_makepayment',f=f,t=t,a=a))
		# 	else:
		# 		flash("invalid")

		# else:
		# 	flash('enter less amount')		

		
	return render_template('user_transfer.html',data=data)	


@user.route('user_otp',methods=['post','get'])	
def user_otp():
	otp=request.args['n']

	if "otp" in request.form:
		o=request.form['number']
		uid=session['user_id']
		f=session['f']
		t=session['t']
		a=session['a']


		if o==otp:
			q="insert into transaction values(null,'%s','%s',curdate(),'debit')"%(f,a)
			insert(q)
			q="insert into transaction values(null,'%s','%s',curdate(),'credit')"%(t,a)
			insert(q)
			
			q="update account set balance=balance-'%s'  where accountnumber='%s'"%(a,f)
			update(q)
			q="update account set balance=balance+'%s'  where accountnumber='%s'"%(a,t)
			update(q)
			flash(' successfully')
			return redirect(url_for('user.user_transfer'))
	return render_template('user_otp.html')

@user.route('/user_account_verification',methods=['get','post'])
def user_account_verification():
	data={}

	n=random.randint(1000,9999)
	n1=str(n)
	print(n)
	data['row']=n
	session['i']=data['row']
	if "credit" in request.form:
		uid=session['user_id']
		card=request.form['card']
		cvv=request.form['cvv']
		month=request.form['month']
		pin_no=request.form['pin_no']
		ifsc=request.form['ifsc']
		bank=request.form['bank']

		q="SELECT * FROM `creditcard` WHERE `cardnum`='%s' AND `month`='%s' AND `pin_no`='%s' AND `ifsc_code`='%s' AND`acc_no`='%s' and cvv='%s' and user_id='%s' "%(card,month,pin_no,ifsc,bank,cvv,uid)
		print(q)
		res=select(q)
		if res:
			q="SELECT COUNT(`detect_id`) AS counts FROM detect WHERE user_id='%s'"%(uid)
			res1=select(q)
			if res1:
				
				q="delete from detect where user_id='%s'"%(uid)
				delete(q)
				
							
				q="select * from creditcard inner join user using(user_id) where user_id='%s'"%(uid)
				res=select(q)
				if res:
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



				

					return redirect(url_for('user.user_otp',n=n))

				

		else:
			q="insert into detect values(null,'%s','pending')"%(uid)
			insert(q)

			q="SELECT COUNT(`detect_id`) AS counts FROM detect WHERE user_id='%s'"%(uid)
			res1=select(q)
			if res1:
				counts=res1[0]['counts']
				if int (counts) > 3:
					q="UPDATE `creditcard` SET `status`='blocked' WHERE user_id='%s'"%(uid)
					update(q)
					flash('your account is blocked')

			flash('invalid account details')
		return redirect(url_for('user.user_account_verification'))
	

	return render_template('user_account_verification.html')





			

	
			