from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
import pymysql


#admin,trainer,trainee can login using username&password

def loginform(request):
    data=""
    con=pymysql.connect("localhost","root","","employeedb")
    c=con.cursor()
    if(request.POST):
        username=request.POST.get("username")
        password=request.POST.get("password")
        #d="select r_id from login_table where username='"+str(username)+"' and password='"+str(password)+"'"
        c.execute("select r_id,l_id from login_tab where username='"+str(username)+"' and l_password='"+str(password)+"'")
        data=c.fetchone()
        print(data[0])
        c.execute("select role from role_tab where r_id='"+str(data[0])+"'")
        data1=c.fetchone()
        print(data1[0])

        request.session["loginid"]=data[1]

        if(str(data1[0])=="admin"):
            return HttpResponseRedirect("adminview")
        elif(str(data1[0])=="trainer"):
            return HttpResponseRedirect("trainerview")
        elif(str(data1[0])=="trainee"):
            return HttpResponseRedirect("traineeview")
    return render(request,"loginform.html",{"data":data})
#admin can add trainee & trainer ,assign password and username
def addtrainer(request):
    data=""
    con=pymysql.connect("localhost","root","","employeedb")
    c=con.cursor()
    trainername = request.POST.get("trname")
    location = request.POST.get("location")
    specialization = request.POST.get("spec")
    contactno = request.POST.get("cno")
    username = request.POST.get("uname")
    password = request.POST.get("pwd")
    if(request.POST):
     c.execute("insert into login_tab(username,l_password,r_id) values('"+str(username)+"','"+str(password)+"','"+str(2)+"')")
     con.commit()

     c.execute("select l_id from login_tab WHERE username='"+str(username)+"' AND l_password='"+str(password)+"'")
     data = c.fetchone()
     print(data)
     c.execute("insert into trainer_tab(tr_name,location, contactno, specialization, r_id, l_id )values('"+str(trainername)+"','"+str(location)+"','"+str(contactno)+"','"+str(specialization)+"','"+str(2)+"','"+str(data[0])+"')")
     con.commit()
    return render(request,"addtrainer.html",{"data":data})

def addtrainee(request):
    data=""
    con=pymysql.connect("localhost","root","","employeedb")
    c=con.cursor()
    c.execute("select * from trainer_tab")
    data=c.fetchall()
    
    if(request.POST):
         traineename = request.POST.get("tname")
         location = request.POST.get("location")
         qualification = request.POST.get("qual")
         department = request.POST.get("dept")
         trainername = request.POST.get("trainername")
         username = request.POST.get("uname")
         password = request.POST.get("pwd")
       
         c.execute("insert into login_tab(username,l_password,r_id) values('"+str(username)+"','"+str(password)+"','"+str(3)+"')")
         con.commit()

         c.execute("select l_id from login_tab WHERE username='"+str(username)+"' AND l_password='"+str(password)+"'")
         data1 = c.fetchone()

         c.execute("insert into trainee_tab(t_name,location, qualification, department, tr_id, r_id, l_id  )values('"+str(traineename)+"','"+str(location)+"','"+str(qualification)+"','"+str(department)+"', '"+str(trainername)+"','"+str(3)+"','"+str(data1[0])+"')")
         con.commit()

    return render(request,"addtrainee.html",{"data":data})

def trainerview(request):
    data=""
    con=pymysql.connect("localhost","root","","employeedb")
    c=con.cursor()

    loginid=request.session.get("loginid")  #loginid passed through session from login
    
    c.execute("select tr_id from trainer_tab where l_id='"+str(loginid)+"'") #using the loginid the trainerid is fetched
    data=c.fetchone()
    c.execute("select * from trainee_tab where tr_id='"+str(data[0])+"'") #the trainerid is used to get the datas from trainee table.
    data1=c.fetchall()

    request.session["trainerid"]=data[0]

    return render(request,"trainerview.html",{"data1":data1})
#trainer can add,project,mark,date to the trainee
def feedback(request):
    con=pymysql.connect("localhost","root","","employeedb")
    c=con.cursor()
    trainerid=request.session.get("trainerid") #trainerid fetched using session
    traineeid = request.GET.get("id") #from the feedback.html id is passed here
    if(request.POST):
        project = request.POST.get("project")
        marks = request.POST.get("mark")
        date = request.POST.get("date")
        c.execute("insert into feeback_tab(project,marks,f_date,tr_id,t_id)values('"+str(project)+"','"+str(marks)+"','"+str(date)+"','"+str(trainerid)+"','"+str(traineeid)+"')")
        con.commit()
    return render(request,"feedback.html")
#admin can view trainee name,location,qual,dept,trainer name,
def adminview(request):
    data=""
    con=pymysql.connect("localhost","root","","employeedb")
    c=con.cursor()
    c.execute("select t.t_id,t.t_name,t.location,t.qualification,t.department,tr.tr_name,tr.specialization from trainee_tab t inner join trainer_tab tr on t.tr_id=tr.tr_id")
    data=c.fetchall()
    return render(request,"adminview.html",{"data":data})

def viewfeedback(request):
    data=""
    con=pymysql.connect("localhost","root","","employeedb")
    c=con.cursor()
    traineeid=request.GET.get("id")
    c.execute("select * from feeback_tab where t_id='"+str(traineeid)+"'")
    data=c.fetchall()
    return render(request,"viewfeedback.html",{"data":data})

def traineeview(request):
    data1=""
    con=pymysql.connect("localhost","root","","employeedb")
    c=con.cursor()
    loginid=request.session.get("loginid")
    c.execute("select t_id from trainee_tab where l_id='"+str(loginid)+"'")
    data=c.fetchone()
    c.execute("select * from feeback_tab where t_id='"+str(data[0])+"'")
    data1=c.fetchall()
    return render(request,"traineeview.html",{"data1":data1})
