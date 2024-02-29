from flask import Flask,render_template,request,redirect,url_for,session
import ibm_db
import ibm_db_dbi as db2
import re
import configparser
import ssl
ssl._create_default_https_context=ssl._create_unverified_context
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app=Flask(__name__)
app.secret_key='a'
con=db2.connect("DATABASE=bludb;HOSTNAME=b1bc1829-6f45-4cd4-bef4-10cf081900bf.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32304;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=ggt91193;PWD=tL4Jy1DoL5XU6d3E",'','')
cur=con.cursor()
conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=b1bc1829-6f45-4cd4-bef4-10cf081900bf.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32304;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=ggt91193;PWD=tL4Jy1DoL5XU6d3E",'','')
@app.route("/")
def welcome():
    return render_template("frontpage.html")
@app.route("/userlogin")
def userlogin():
    return render_template("userloginpage.html")
@app.route("/agentlogin")
def agentlogin():
    return render_template("agentloginpage.html")
@app.route("/adminlogin")
def adminlogin():
    return render_template("adminloginpage.html")
@app.route("/register")
def register():
    return render_template("register.html")
@app.route("/registeration",methods=['GET','POST'])
def registeration():
    global userid
    msg=''
    if request.method=='POST':
        fname=request.form['firstname']
        lname=request.form['lastname']
        email=request.form['email']
        pwd=request.form['password']
        gender=request.form['gender']
        age=request.form['age']
       
        sql="SELECT * FROM REGIS WHERE email=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        acc=ibm_db.fetch_assoc(stmt)
        if acc:
            msg='Account already exists!'
            return redirect(url_for('register',msg=msg))
        else:
            insert_sql="INSERT INTO REGIS VALUES(?,?,?,?,?,?)"
            prep_stmt=ibm_db.prepare(conn,insert_sql)
            ibm_db.bind_param(prep_stmt,1,fname)
            ibm_db.bind_param(prep_stmt,2,lname)
            ibm_db.bind_param(prep_stmt,3,email)
            ibm_db.bind_param(prep_stmt,4,pwd)
            ibm_db.bind_param(prep_stmt,5,gender)
            ibm_db.bind_param(prep_stmt,6,age)
            ibm_db.execute(prep_stmt)
            msg='Registered successfully!'
            return render_template("userloginpage.html",msg=msg)
    else:
        msg='Registration Unsuccessful! Please try again later!'
        return redirect(url_for('register',msg=msg))
@app.route('/login',methods=['GET','POST'])
def login():
    global userid
    msg=''
    if request.method=='POST':
        username=request.form['uname']
        pwd=request.form['pwd']
        sql="SELECT * FROM REGIS WHERE EMAIL=? AND PWD=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,pwd)
        ibm_db.execute(stmt)
        acc=ibm_db.fetch_assoc(stmt)
        if acc:
            msg='Login successful!'
            return render_template("homepage.html")
        else:
            msg="Invalid username/password!"
            return render_template("userloginpage.html")
@app.route('/aglogin',methods=['GET','POST'])
def aglogin():
    global userid
    msg=''
    if request.method=='POST':
        username=request.form['uname']
        pwd=request.form['pwd']
        sql="SELECT * FROM REGIS WHERE EMAIL=? AND PWD=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,pwd)
        ibm_db.execute(stmt)
        acc=ibm_db.fetch_assoc(stmt)
        if acc:
            msg='Login successful!'
            return render_template("agenthomepage.html")
        else:
            msg="Invalid username/password!"
            return render_template("agentloginpage.html")
@app.route('/adlogin',methods=['GET','POST'])
def adlogin():
    global userid
    msg=''
    if request.method=='POST':
        username=request.form['uname']
        pwd=request.form['pwd']
        sql="SELECT * FROM REGIS WHERE EMAIL=? AND PWD=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,pwd)
        ibm_db.execute(stmt)
        acc=ibm_db.fetch_assoc(stmt)
        if acc:
            msg='Login successful!'
            return render_template("adminhomepage.html")
        else:
            msg="Invalid username/password!"
            return render_template("adminloginpage.html")
@app.route('/home')
def home():
    return render_template("homepage.html")
@app.route('/status')
def status():
    cur.execute("SELECT * FROM AGSTAT WHERE EMAIL='shrijaas@gmail.com'")
    account = cur.fetchall()
    return render_template("status.html",account=account)
@app.route('/ticket')
def ticket():
    return render_template("ticket.html")
@app.route('/feedback')
def feedback():
    return render_template("feedback.html")
@app.route('/feed',methods=['GET','POST'])
def feed():
    msg=''
    if request.method=='POST':
        view=request.form['my-reply']
        rate=request.form['feed']
        insert_sql="INSERT INTO FEEDBACK VALUES(?,?)"
        prep_stmt=ibm_db.prepare(conn,insert_sql)
        ibm_db.bind_param(prep_stmt,1,view)
        ibm_db.bind_param(prep_stmt,2,rate)
        ibm_db.execute(prep_stmt)
        msg='Thanks for your valuable feedback!'
        return render_template('homepage.html',msg=msg)
    else:
        msg='Feedback unsuccessful!'
        return render_template('feedback.html',msg=msg)
@app.route('/query',methods=['GET','POST'])
def query():
    msg=''
    if request.method=='POST':
        username=request.form['username']
        email=request.form['email']
        query=request.form['query']
        insert_sql="INSERT INTO TICKET VALUES(?,?,?)"
        prep_stmt=ibm_db.prepare(conn,insert_sql)
        ibm_db.bind_param(prep_stmt,1,username)
        ibm_db.bind_param(prep_stmt,2,email)
        ibm_db.bind_param(prep_stmt,3,query)
        ibm_db.execute(prep_stmt)
        msg='Ticket is raised successfully!'
        return render_template('homepage.html',msg=msg)
    else:
        msg='Query submission Unsuccessful! Please try again later!'
        return render_template('ticket.html',msg=msg)
@app.route('/updatestatus')
def updatestatus():
    return render_template('updatestatus.html')
@app.route('/interaction')
def interaction():
    return render_template('interaction.html')

@app.route('/viewad')
def viewad():
    cur.execute("SELECT * FROM GGT91193.TICKET")
    account = cur.fetchall()
    cur.execute("SELECT AGENTID FROM GGT91193.AGENT")
    account1 = cur.fetchall()
    return render_template('adminhomepage.html',account=account,acc1=account1)
@app.route('/viewag')
def viewag():
    cur.execute("SELECT * FROM GGT91193.AGASS WHERE AGENT='AGENT2'")
    account = cur.fetchall()
    return render_template('agenthomepage.html',account=account)
@app.route('/sendmail')
def sendmail():
    config=configparser.ConfigParser()
    config.read("config.ini")
    def mail(API,from_email,to_email,subject,html_content):
        if API!=None and from_email!=None and len(to_email)>0:
            message=Mail(from_email,to_email,subject,html_content)
            try:
                sg = SendGridAPIClient(API)
                response = sg.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print(e.message)
    try:
        settings=config["SETTINGS"]
    except:
        settings={}
    API=settings.get("APIKEY",None)
    from_email=settings.get("FROM",None)
    to_email=settings.get("TO","")
    subject="AGENT ASSIGNED!"
    html_content="Dear Customer , Your ticket has been viewed and an agent has been alloted for your ticket. Kindly check your account for further details"
    mail(API,from_email,to_email,subject,html_content)
    return render_template('adminloginpage.html')
@app.route('/assign',methods=['GET','POST'])
def assign():
    return render_template('response.html')
@app.route('/queryres',methods=['GET','POST'])
def queryres():
    msg=''
    if request.method=='POST':
        username=request.form['username']
        email=request.form['email']
        res=request.form['queries']
        insert_sql="INSERT INTO RESPONSE VALUES(?,?,?)"
        prep_stmt=ibm_db.prepare(conn,insert_sql)
        ibm_db.bind_param(prep_stmt,1,username)
        ibm_db.bind_param(prep_stmt,2,email)
        ibm_db.bind_param(prep_stmt,3,res)
        ibm_db.execute(prep_stmt)
        msg='Ticket is raised successfully!'
        return render_template('homepage.html',msg=msg)
    else:
        msg='Query submission Unsuccessful! Please try again later!'
        return render_template('ticket.html',msg=msg)
@app.route('/assignag',methods=['GET','POST'])
def assignag():
    msg=''
    if request.method=='POST':
        email=request.form['id']
        query=request.form['id1']
        agent=request.form['agent']
        insert_sql="INSERT INTO AGASS VALUES(?,?,?)"
        prep_stmt=ibm_db.prepare(conn,insert_sql)
        ibm_db.bind_param(prep_stmt,1,email)
        ibm_db.bind_param(prep_stmt,2,agent)
        ibm_db.bind_param(prep_stmt,3,query)
        ibm_db.execute(prep_stmt)
        return render_template('adminhomepage.html')
    else:
        return render_template('frontpage.html')
@app.route('/statusupdate',methods=['GET','POST'])
def statusupdate():
    msg=''
    if request.method=='POST':
        email=request.form['id']
        status=request.form['status']
        insert_sql="INSERT INTO AGSTAT VALUES(?,?)"
        prep_stmt=ibm_db.prepare(conn,insert_sql)
        ibm_db.bind_param(prep_stmt,1,email)
        ibm_db.bind_param(prep_stmt,2,status)
        ibm_db.execute(prep_stmt)
        return render_template('adminhomepage.html')
    else:
        return render_template('frontpage.html')
if __name__=='__main__':
    app.run(host="0.0.0.0",debug=True)