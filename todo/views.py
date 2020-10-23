from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404,reverse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from . import forms,models
from .forms import AdminSigupForm
from .forms import TodoForm,ContactForm,MyProfileForm,SendMultiMailForm,MyBiodataForm,BiodataPrivacyForm,BiodataHelpForm,RequestsForApprovalForm
from .models import Todo,Contact,MyProfile,SendMultiMail,MyBiodata,BiodataPrivacy,MyBiodataInbox,MyBiodataChatbox,BiodataHelp,RequestsForApproval
from django.utils import timezone
from django.contrib.auth.decorators import login_required,user_passes_test
from django.views.decorators.csrf import csrf_protect
import re,random,datetime
import csv,logging,xlwt,googletrans

from django.http import HttpResponse,JsonResponse
from googletrans import Translator
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms.models import model_to_dict
import json
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from datetime import datetime,timedelta,date
# Create your views here.
logger = logging.getLogger(__name__)
def signupuser(request):
    if request.method == 'GET':
        return render(request,'todo/signupuser.html',{'form':UserCreationForm()})
    else:
        #create a new User
        if request.POST['password1'] == request.POST['password2']:
            if len(request.POST['password1'])<8:
                return render(request,'todo/signupuser.html',{'form':UserCreationForm(),'error':"Passowrd length is too short"})
            elif not re.findall('\d',request.POST['password1']):
                return render(request,'todo/signupuser.html',{'form':UserCreationForm(),'error':"Passowrd must conain atlease 1 digit 0-9"})
            elif not re.findall('[A-Z]',request.POST['password1']):
                return render(request,'todo/signupuser.html',{'form':UserCreationForm(),'error':"Passowrd must conain atlease 1 capital letter"})
            elif not re.findall('[a-z]',request.POST['password1']):
                return render(request,'todo/signupuser.html',{'form':UserCreationForm(),'error':"Passowrd must conain atlease 1 small letter"})
            elif not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]',request.POST['password1']):
                return render(request,'todo/signupuser.html',{'form':UserCreationForm(),'error':"Passowrd must conain atlease 1 special character"})




            else:
                try:
                    user=User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                    user.save()
                    login(request,user)
                    return redirect(currenttodos)
                except IntegrityError:
                    return render(request,'todo/signupuser.html',{'form':UserCreationForm(),'error':"User already exists"})
        else:
            #Tell the user the password didn't match
            #println("Passoword didn't match")
            return render(request,'todo/signupuser.html',{'form':UserCreationForm(),'error':"Passwod didn't match"})
@login_required
def currenttodos(request):
    #todos=Todo.objects.all()
    #we want user specific database objects
    todos = Todo.objects.filter(user=request.user,datecompleted__isnull=True)
    return render(request,'todo/currenttodos.html',{'todos':todos})
@login_required
def completedtodos(request):
    #todos=Todo.objects.all()
    #we want user specific database objects
    todos = Todo.objects.filter(user=request.user,datecompleted__isnull=False).order_by('-datecompleted')
    return render(request,'todo/completedtodos.html',{'todos':todos})

@login_required
def viewtodo(request,todo_pk):
    todo=get_object_or_404(Todo,pk=todo_pk,user=request.user)
    if request.method == 'GET':
        form =  TodoForm(instance=todo)
        return render(request,'todo/viewtodo.html',{'todo':todo,'form':form})
    else:
        try:
            form=TodoForm(request.POST,instance=todo)
            form.save()
            return redirect(currenttodos)
        except ValueError:
            return render(request,'todo/viewtodo.html',{'todo':todo,'form':form,'error':"Bad info passed.Please try again."})

@login_required
def getassociatestatustodo(request,associateusername):
    try:
        get_list_or_404(MyProfile,user=request.user,associate=associateusername,username=request.user.username)
    except:
        currentwork=[]
        completedwork=[]
        return render(request,'todo/getassociatestatustodo.html',{'currentwork':currentwork,'completedwork':completedwork,'error':"Sorry, selected user is not your associate!!"})
    associate=get_object_or_404(User,username=associateusername)
    currentwork=Todo.objects.filter(user=associate,datecompleted__isnull=True)
    completedwork=Todo.objects.filter(user=associate,datecompleted__isnull=False).order_by('-datecompleted')
    return render(request,'todo/getassociatestatustodo.html',{'currentwork':currentwork,'completedwork':completedwork})

@login_required
def exportdatatodo(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}{}.csv"'.format(request.user.username,"_currentwork")
    todos = Todo.objects.filter(user=request.user,datecompleted__isnull=True)
    writer = csv.writer(response)
    writer.writerow(['Title', 'memo', 'Created', 'Datecompleted','Createdby','isImportant'])
    for row in todos:
        writer.writerow([row.title,row.memo,row.created,row.datecompleted,row.user.username,row.important,])
    return response

@login_required
def exportexceldatatodo(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="{}{}.xls"'.format(request.user.username,"_currentwork")
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('CurrentWork')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns=['Title', 'memo', 'isImportant']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    todos = Todo.objects.filter(user=request.user,datecompleted__isnull=True).values_list('title','memo','important')
    for row in todos:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

@login_required
def exportcompledatatodo(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}{}.csv"'.format(request.user.username,"_completedWork")
    todos = Todo.objects.filter(user=request.user,datecompleted__isnull=False)
    writer = csv.writer(response)
    writer.writerow(['Title', 'memo', 'Created', 'Datecompleted','Createdby','isImportant'])
    for row in todos:
        writer.writerow([row.title,row.memo,row.created,row.datecompleted,row.user.username,row.important,])
    return response

@login_required
def exportexcelcompledatatodo(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="{}{}.xls"'.format(request.user.username,"_completedWork")
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('CompletedWork')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns=['Title', 'memo', 'isImportant']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    todos = Todo.objects.filter(user=request.user,datecompleted__isnull=False).values_list('title','memo','important')
    for row in todos:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response






@login_required
def myprofiletodo(request):
    user = request.user
    if request.method == 'GET':
        try:
            myprofiles=get_list_or_404(MyProfile,user=request.user)
            try:
                leadprofiles=get_list_or_404(MyProfile,lead__isnull=False,user=request.user)
            except:
                leadprofiles=[]
            try:
                associateprofiles=get_list_or_404(MyProfile,associate__isnull=False,user=request.user)
            except:
                associateprofiles=[]
        except:
            leadprofiles=[]
            associateprofiles=[]
            myprofiles=[]
        form =  MyProfileForm()
        return  render(request,'todo/myprofiletodo.html',{'myprofiles':myprofiles,'leadprofiles':leadprofiles,'associateprofiles':associateprofiles,'form':form})
    else:
        lead=get_object_or_404(User,pk=request.POST['user'])
        try:
            try:
                get_list_or_404(MyProfile,user=request.user,username=request.user.username,lead=lead.username)
                error="Selected User is already your lead!!"
                notduplicateuser=False
            except:
                notduplicateuser=True
            try:
                #get_list_or_404(MyProfile,user=lead,username=lead.username,associate=request.user.username)
                get_list_or_404(MyProfile,user=request.user,username=request.user.username,associate=lead.username)
                error="Selected user is your associate!!"
                notduplicateuser=False
            except:
                logger.error('do nothing')
            if request.user == lead:
                error="You can't add yourself as a lead!!"
                notduplicateuser=False

            if  not (notduplicateuser):
                form=MyProfileForm(request.POST)
                try:
                    myprofiles=get_list_or_404(MyProfile,user=request.user)
                    try:
                        leadprofiles=get_list_or_404(MyProfile,lead__isnull=False,user=request.user)
                    except:
                        leadprofiles=[]
                    try:
                        associateprofiles=get_list_or_404(MyProfile,associate__isnull=False,user=request.user)
                    except:
                        associateprofiles=[]
                except:
                    myprofiles =[]
                    leadprofiles=[]
                    associateprofiles=[]
                return render(request,'todo/myprofiletodo.html',{'myprofiles':myprofiles,'leadprofiles':leadprofiles,'associateprofiles':associateprofiles,'form':form,'error':error})
            form=MyProfileForm(request.POST)
            form2=MyProfileForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = user
            newtodo.username=user.username
            newtodo.lead=lead.username
            newtodo.save()

            newtodo2 = form2.save(commit=False)
            newtodo2.user = lead
            newtodo2.username=lead.username
            newtodo2.associate=request.user.username
            newtodo2.save()
            try:
                myprofiles=get_list_or_404(MyProfile,user=request.user)
                try:
                    leadprofiles=get_list_or_404(MyProfile,lead__isnull=False,user=request.user)
                except:
                    leadprofiles=[]
                try:
                    associateprofiles=get_list_or_404(MyProfile,associate__isnull=False,user=request.user)
                except:
                    associateprofiles=[]
            except:
                myprofiles =[]
                associateprofiles=[]
                leadprofiles=[]
            return  render(request,'todo/myprofiletodo.html',{'myprofiles':myprofiles,'leadprofiles':leadprofiles,'associateprofiles':associateprofiles,'form':form,'success':"User added successfuly"})
        except ValueError:
            return render(request,'todo/myprofiletodo.html',{'myprofiles':myprofiles,'leadprofiles':leadprofiles,'associateprofiles':associateprofiles,'form':form,'error':"Bad info passed.Please try again."})


@login_required
def removeassociatetodo(request):
    user = request.user
    if request.method == 'GET':
        try:
            myprofiles=get_list_or_404(MyProfile,user=request.user)
            try:
                leadprofiles=get_list_or_404(MyProfile,lead__isnull=False,user=request.user)
            except:
                leadprofiles=[]
            try:
                associateprofiles=get_list_or_404(MyProfile,associate__isnull=False,user=request.user)
            except:
                associateprofiles=[]
        except:
            leadprofiles=[]
            associateprofiles=[]
            myprofiles=[]
        form =  MyProfileForm()
        return  render(request,'todo/myprofiletodo.html',{'myprofiles':myprofiles,'leadprofiles':leadprofiles,'associateprofiles':associateprofiles,'form':form})
    else:
        try:
            associate=get_object_or_404(User,pk=request.POST['user'])
            myprofiles =get_list_or_404(MyProfile,user=request.user,associate=associate.username)
            try:
                form =  MyProfileForm()
                associatedelete=[]
                #associatedelete=get_object_or_404(MyProfile,associate=associate.username,username=request.user.username,user=request.user)
                associatedelete=get_list_or_404(MyProfile,user=request.user,associate=associate.username,username=request.user.username)
                associateleaddelete=get_list_or_404(MyProfile,user=associate,lead=request.user.username,username=associate.username)
                associatedelete[0].delete()
                associateleaddelete[0].delete()
                try:
                    myprofiles=get_list_or_404(MyProfile,user=request.user)
                    try:
                        leadprofiles=get_list_or_404(MyProfile,lead__isnull=False,user=request.user)
                    except:
                        leadprofiles=[]
                    try:
                        associateprofiles=get_list_or_404(MyProfile,associate__isnull=False,user=request.user)
                    except:
                        associateprofiles=[]
                except:
                    myprofiles =[]
                    leadprofiles=[]
                    associateprofiles=[]

                return  render(request,'todo/myprofiletodo.html',{'myprofiles':myprofiles,'leadprofiles':leadprofiles,'associateprofiles':associateprofiles,'form':form,'success':"Associate deleted successfuly"})
            except:
                try:
                    myprofiles=get_list_or_404(MyProfile,user=request.user)
                    try:
                        leadprofiles=get_list_or_404(MyProfile,lead__isnull=False,user=request.user)
                    except:
                        leadprofiles=[]
                    try:
                        associateprofiles=get_list_or_404(MyProfile,associate__isnull=False,user=request.user)
                    except:
                        associateprofiles=[]
                except:
                    myprofiles =[]
                    associateprofiles=[]
                    leadprofiles=[]
                return  render(request,'todo/myprofiletodo.html',{'myprofiles':myprofiles,'leadprofiles':leadprofiles,'associateprofiles':associateprofiles,'form':form,'error':"Some error occoured during delettion !"})
        except:
            try:
                myprofiles=get_list_or_404(MyProfile,user=request.user)
                try:
                    leadprofiles=get_list_or_404(MyProfile,lead__isnull=False,user=request.user)
                except:
                    leadprofiles=[]
                try:
                    associateprofiles=get_list_or_404(MyProfile,associate__isnull=False,user=request.user)
                except:
                    associateprofiles=[]
            except:
                myprofiles =[]
                leadprofiles=[]
                associateprofiles=[]
            form =  MyProfileForm()
            return render(request,'todo/myprofiletodo.html',{'myprofiles':myprofiles,'leadprofiles':leadprofiles,'associateprofiles':associateprofiles,'form':form,'error':"Selected user is not your associate!!"})

@login_required
def exportassociatedatatodo(request):
    user = request.user
    if request.method == 'GET':
        try:
            myprofiles=get_list_or_404(MyProfile,user=request.user)
            try:
                leadprofiles=get_list_or_404(MyProfile,lead__isnull=False,user=request.user)
            except:
                leadprofiles=[]
            try:
                associateprofiles=get_list_or_404(MyProfile,associate__isnull=False,user=request.user)
            except:
                associateprofiles=[]
        except:
            leadprofiles=[]
            associateprofiles=[]
            myprofiles=[]
        form =  MyProfileForm()
        return  render(request,'todo/myprofiletodo.html',{'myprofiles':myprofiles,'leadprofiles':leadprofiles,'associateprofiles':associateprofiles,'form':form})
    else:
        try:
            associate=get_object_or_404(User,pk=request.POST['user'])
            myprofiles =get_list_or_404(MyProfile,user=request.user)
            try:
                form =  MyProfileForm()
                associatedelete=[]
                associatedeletes=get_list_or_404(MyProfile,user=request.user,associate=associate.username,username=request.user.username)
                associatedelete=associatedeletes[0]
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="{}{}.csv"'.format(associatedelete.user.username,"_completedWork")
                todos = Todo.objects.filter(user=associatedelete.user)
                writer = csv.writer(response)
                writer.writerow(['Title', 'memo', 'Created', 'Datecompleted','Createdby','isImportant'])
                for row in todos:
                    writer.writerow([row.title,row.memo,row.created,row.datecompleted,row.user.username,row.important,])
                return response
            except:
                try:
                    myprofiles =myprofiles=get_list_or_404(MyProfile,user=request.user)
                    try:
                        leadprofiles=get_list_or_404(MyProfile,lead__isnull=False,user=request.user)
                    except:
                        leadprofiles=[]
                    try:
                        associateprofiles=get_list_or_404(MyProfile,associate__isnull=False,user=request.user)
                    except:
                        associateprofiles=[]
                except:
                    myprofiles =[]
                return  render(request,'todo/myprofiletodo.html',{'myprofiles':myprofiles,'leadprofiles':leadprofiles,'associateprofiles':associateprofiles,'form':form,'error':"Selected user is not your associate !"})
        except:
            myprofiles =[]
            form =  MyProfileForm()
            return render(request,'todo/myprofiletodo.html',{'myprofiles':myprofiles,'form':form,'error':"Bad info passed or no user mapped .Please try again."})








@login_required
def completetodo(request,todo_pk):
    todo=get_object_or_404(Todo,pk=todo_pk,user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect(currenttodos)

@login_required
def deletetodo(request,todo_pk):
    todo=get_object_or_404(Todo,pk=todo_pk,user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.delete()
        return redirect(currenttodos)

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return render(request,'todo/logout.html')
    else:
        return render(request,'todo/signupuser.html',{'form':UserCreationForm()})


def loginuser(request):
    if request.method == 'GET':
        return render(request,'todo/loginuser.html',{'form':AuthenticationForm()})
    else:
        #authenticate function
        user=authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request,'todo/loginuser.html',{'form':AuthenticationForm(),'error':"Username and Password do not match"})
        else:
            login(request,user)
            return redirect('afterlogin')



def home(request):
    return render(request,'todo/home.html')




def sendmailtodo(request):
    if request.method == 'GET':
        form = SendMultiMailForm()
        return render(request,'todo/sendmailtodo.html',{'form':form})
    else:
        error=None
        msg = MIMEMultipart()
        if bool(request.POST['pass']!='') & bool(request.POST['from'] != ''):
            passw=request.POST['pass']
            msg['From']=request.POST['from']
        else:
            msg['From']='kushwahasamajshadi@gmail.com'
            passw="Ksamaj@#123"
        msg['Subject']=request.POST['subject']
        body=request.POST['body']
        msg.attach(MIMEText(body, 'plain'))
        tolist=list(request.POST['to'].split(','))
        for to in tolist:
            logger.error(to)
            msg['To'] = to
            message = msg.as_string()
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            try:
                s.login(msg['From'], passw)
            except smtplib.SMTPAuthenticationError:
                return render(request,'todo/sendmailtodo.html',{'error':'Email and password not accepted,Please enter correct details!'})
            try:
                s.sendmail(msg['From'], msg['To'], message)
                msgdict={'sender':msg['From'],'receivers':msg['To'],'subject':msg['Subject'],'body':body}
                form=SendMultiMailForm(data=msgdict)
                form.save()
                logger.error('till not error')
                if form.is_valid():
                    logger.error('saved in db')
                    form.save()
            except smtplib.SMTPRecipientsRefused:
                return render(request,'todo/sendmailtodo.html',{'error':'Receiver mail field is empty!'})
            logger.error("email sent")
            s.quit()
            # open the file to be sent
            # filename = "File_name_with_extension"
            # attachment = open("Path of the file", "rb")
            #
            # # instance of MIMEBase and named as p
            # p = MIMEBase('application', 'octet-stream')
            #
            # # To change the payload into encoded form
            # p.set_payload((attachment).read())
            #
            # # encode into base64
            # encoders.encode_base64(p)
            #
            # p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
            #
            # # attach the instance 'p' to instance 'msg'
            # msg.attach(p)
        return render(request,'todo/sendmailtodo.html',{'success':'success','error':error})



def abouttodo(request):
    logger.error(request.method)
    return render(request,'todo/abouttodo.html')
def portfoliotodo(request):
    return render(request,'todo/portfoliotodo.html')
def contacttodo(request):

    if request.method == 'GET':
        return render(request,'todo/contacttodo.html',{'form':ContactForm()})
    else:
        try:
            form=ContactForm(request.POST)
            form.save()
            todos = Contact.objects.latest('id')
            return render(request,'todo/contacttodo.html',{'form':ContactForm(),'contact':todos})
        except ValueError:
            return render(request,'todo/contacttodo.html',{'form':ContactForm(),'error':"Bad data Passed! Try again."})

    return render(request,'todo/contacttodo.html')

def contacttodos(request):
    #todos=Todo.objects.all()
    #we want user specific database objects
    todos = Contact.objects.latest('id')
    return render(request,'todo/contacttodo.html',{'form':ContactForm(),'contact':todos})


@login_required
def createbiodatatodo(request):
    if request.method == 'GET':
        return render(request,'todo/createbiodatatodo.html',{'form':MyBiodataForm()})
    else:
        form=MyBiodataForm(request.POST, request.FILES)
        newtodo = form.save(commit=False)
        newtodo.user = request.user
        newtodo.username = request.user.username
        try:

            if form.is_valid():
                newtodo.save()
                todos = MyBiodata.objects.filter(user=request.user,deletedrow=False).order_by('-id')
                logger.error(todos[0].id)
                privacymodel=BiodataPrivacy()
                privacymodel.user=request.user
                privacymodel.username=request.user.username
                privacymodel.biodataid=todos[0].id
                privacymodel.save()
                return render(request,'todo/mybiodatatodos.html',{'todos':todos,'msg':'BIODATA Created Successfully.'})
            else:
                return render(request,'todo/createbiodatatodo.html',{'form':MyBiodataForm(),'error':"Bad data Passed!Please Try again."})
        except ValueError:
            return render(request,'todo/createtodo.html',{'form':MyBiodataForm(),'error':"Bad data Passed! Try again."})

@login_required
def mybiodatatodo(request):
    todos = MyBiodata.objects.filter(user=request.user,deletedrow=False).order_by('-id')
    return render(request,'todo/mybiodatatodos.html',{'todos':todos})
@login_required
def viewmybiodatatodo(request,todo_pk):
    todo=get_object_or_404(MyBiodata,pk=todo_pk,user=request.user,deletedrow=False)
    if request.method == 'GET':
        form =  MyBiodataForm(instance=todo)
        return render(request,'todo/viewmybiodatatodo.html',{'todo':todo,'form':form})
    else:
        try:
            form=MyBiodataForm(request.POST,instance=todo)
            form.save()
            todos = MyBiodata.objects.filter(user=request.user).order_by('-id')
            return render(request,'todo/mybiodatatodos.html',{'todos':todos,'msg':'BIODATA updated Successfully.'})
        except ValueError:
            return render(request,'todo/viewmybiodatatodo.html',{'todo':todo,'form':form,'error':"Bad info passed.Please try again."})
@login_required
def mybiodatahometodo(request):
    user_list = MyBiodata.objects.filter(deletedrow=False).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(user_list, 3)
    try:
        todos = paginator.page(page)
    except PageNotAnInteger:
        todos = paginator.page(1)
    except EmptyPage:
        todos = paginator.page(paginator.num_pages)
    return render(request,'todo/mybiodatahometodo.html',{'todos':todos})

@login_required
def mybiodatadeletetodo(request,todo_pk):
    todo=get_object_or_404(MyBiodata,pk=todo_pk,user=request.user,deletedrow=False)
    if request.method == 'GET':
        form =  MyBiodataForm(instance=todo)
        return render(request,'todo/viewmybiodatatodo.html',{'todo':todo,'form':form})
    else:
        try:
            todo.deletedrow=True
            todo.last_updated_at=datetime.datetime.now()
            todo.save()
            todos = MyBiodata.objects.filter(user=request.user,deletedrow=False).order_by('-id')
            return render(request,'todo/mybiodatatodos.html',{'todos':todos,'msg':'Biodata deleted Successfully.'})
        except ValueError:
            return render(request,'todo/viewmybiodatatodo.html',{'todo':todo,'form':form,'error':"Bad info passed.Please try again."})

@login_required
def mybiodataprivacytodo(request):
    if request.method == 'GET':
        return render(request,'todo/mybiodataprivacytodo.html',{'form':BiodataPrivacyForm()})
    else:
        try:
            todo=get_object_or_404(BiodataPrivacy,biodataid=request.POST['biodataid'],user=request.user)
            todo.contact_visibility=request.POST['contact_visibility']
            todo.email_visibility=request.POST['email_visibility']
            todo.education_detail_visibility=request.POST['education_detail_visibility']
            todo.address_detail_visibility=request.POST['address_detail_visibility']
            todo.hide_profile=request.POST['hide_profile']
            todo.save()
            todo1=get_object_or_404(MyBiodata,pk=request.POST['biodataid'],user=request.user)
            todo1.contact_visibility=request.POST['contact_visibility']
            todo1.email_visibility=request.POST['email_visibility']
            todo1.education_detail_visibility=request.POST['education_detail_visibility']
            todo1.address_detail_visibility=request.POST['address_detail_visibility']
            todo1.hide_profile=request.POST['hide_profile']
            todo1.save()
            return render(request,'todo/mybiodataprivacytodo.html',{'form':BiodataPrivacyForm(),'msg':'Privacy updated Successfully.'})
        except :
            return render(request,'todo/mybiodataprivacytodo.html',{'form':BiodataPrivacyForm(),'error':"Incorrect biodataID ! Please try again."})

@login_required
def mybiodatadownloadtodo(request):
    if request.method == 'GET':
        return render(request,'todo/mybiodatadownloadtodo.html',{'msg':'PLEASE ENTER YOUR BIODATA ID'})
    else:
        try:
            todo=get_object_or_404(MyBiodata,pk=request.POST['biodataid'],user=request.user,deletedrow=False)
            logger.error(todo.id)
            return render(request,'todo/mybiodatadownloadtodo.html',{'todo':todo,'found':'found'})
        except :
            return render(request,'todo/mybiodatadownloadtodo.html',{'error':"It's not your biodata ID, Please try again."})


@login_required
def viewcontacttodo(request):
    try:
        requestto=get_object_or_404(MyBiodata,pk=request.POST['biodataid'],deletedrow=False)
        if request.POST['requesttype'] == 'contact':
            todos=get_list_or_404(RequestsForApproval,user=request.user,contact_view_request='yes',requesttobiodataid=requestto.id)
            result="CONTACT NUMBER: {}".format(requestto.contact_number)
        else:
            todos=get_list_or_404(RequestsForApproval,user=request.user,connect_request='yes',requesttobiodataid=requestto.id)
            result="YOU ARE ALREADY CONNECTED TO: {}".format(requestto.user.username)
        return JsonResponse({'msg':result})
    except:
        try:
            if request.POST['requesttype'] == 'contact':
                todo1=get_list_or_404(RequestsForApproval,user=request.user,requesttobiodataid=requestto.id,request_type='contact')
                result="YOU HAVE ALREADY RAISED REQUEST TO : {} ,PLEASE WAIT FOR APPROVAL ".format(requestto.user.username)
            else:
                todo1=get_list_or_404(RequestsForApproval,user=request.user,requesttobiodataid=requestto.id,request_type='connect')
                result="YOU HAVE ALREADY RAISED REQUEST TO : {} ,PLEASE WAIT FOR APPROVAL ".format(requestto.user.username)
            return JsonResponse({'msg':result})
        except:
            logger.error('raise new view req')
        try:
            try:
                requesfrom=get_list_or_404(MyBiodata,user=request.user,deletedrow=False)
                requefrombiodataid=requesfrom[0].id
            except:
                requesfrom=[]
                requefrombiodataid=''
            requestmodel=RequestsForApproval()
            requestmodel.user=request.user
            requestmodel.requestfromusername=request.user.username
            requestmodel.userbiodataid=requefrombiodataid
            requestmodel.requesttousername=requestto.user.username
            requestmodel.requesttoemailid=requestto.email_ID
            requestmodel.requesttobiodataid=requestto.id
            if request.POST['requesttype'] == 'contact':
                requestmodel.request_type='contact'
            else:
                requestmodel.request_type='connect'
            requestmodel.save()
            msg = MIMEMultipart()
            msg['From'] = 'kushwahasamajshadi@gmail.com'
            msg['To'] = requestto.email_ID
            logger.error(requestto.email_ID)
            if request.POST['requesttype'] == 'contact':
                msg['Subject'] = " VIEW CONTACT REQUEST"
                body = " {} : WANTS TO VIEW YOUR CONTACT NUMBER ON KUSHWAHA SAMAJ SHADI WEBSITE,KINDLY CHECK YOUR NOTIFICATIONS AND SHARE DETAILS IF INTERESTED ".format(request.user.username)
            else:
                msg['Subject'] = " CONNECT REQUEST"
                body = " {} : WANTS TO   CONTECT YOU ON KUSHWAHA SAMAJ SHADI WEBSITE,KINDLY CHECK YOUR NOTIFICATIONS AND ACCEPT REQUEST IF INTERESTED ".format(request.user.username)
            msg.attach(MIMEText(body, 'plain'))
            try:
                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.starttls()
                s.login(msg['From'], "Ksamaj@#123")
                text = msg.as_string()
                s.sendmail(msg['From'], msg['To'], text)
                s.quit()
            except:
                result='YOUR VIEW CONTACT REQUEST RAISED  '
            logger.error('not error ttls')
            result='YOUR VIEW CONTACT REQUEST RAISED AND HAVE SENT MAIL TO USER '
        except:
            result='SORRY,SELECTED BIODATA USER HAS NOT UPLOADED EMAIL ID'
        return JsonResponse({'msg':result})



@login_required
def biodatachatstodo(request):
    if request.method == 'GET':
        try:
            logger.error('before inbox')
            inbox=get_list_or_404(MyBiodataInbox,user=request.user)
            logger.error('after inbox')
        except:
            inbox=[]
        try:
            chats=get_list_or_404(MyBiodataChatbox,user=request.user)
        except:
            chats=[]
        try:
            requser=get_list_or_404(MyBiodata,user=request.user)
            logger.error(requser[0].email_ID)
            reqapproval=get_list_or_404(RequestsForApproval,requesttoemailid=requser[0].email_ID)
        except:
            reqapproval=[]
        return render(request,'todo/biodatachatstodo.html',{'inbox':inbox,'chats':chats,'reqapproval':reqapproval})
    else:
        if request.method == 'POST':
            if request.POST['sentboxview'] == 'sentboxview':
                logger.error(' sentbox request')
                try:
                    outbox =get_list_or_404(MyBiodataChatbox,user=request.user)
                except:
                    outbox=[]
                mydict={}
                for row in outbox:
                    localdict={}
                    for row1 in mydict:
                        localdict['msgtousername']=row.msgtousername
                        localdict['subject']=row.subject
                        localdict['msg']=row.msg
                    mydict[row.msgtousername]=localdict
                return JsonResponse({'result':'success','msgs':mydict})

            elif request.POST['sentboxview'] == 'pendingrequests':
                logger.error('Peding requests')
                try:
                    requser=get_list_or_404(MyBiodata,user=request.user)
                    logger.error(requser[0].email_ID)
                    reqapproval=get_list_or_404(RequestsForApproval,requesttoemailid=requser[0].email_ID)
                except:
                    reqapproval=[]
                mydict={}
                for row in reqapproval:
                    localdict={}
                    localdict['request_from']=row.user.username
                    localdict['contact_view_request']=row.contact_view_request
                    localdict['connect_request']=row.connect_request
                    localdict['request_type']=row.request_type
                    localdict['biodataid']=row.userbiodataid
                    localdict['rowid']=row.id
                    mydict[row.id]=localdict
                logger.error(mydict)
                return JsonResponse({'result':'success','msgs':mydict})
            elif request.POST['sentboxview'] == 'getmychatusers':
                try:
                    myusers=get_list_or_404(RequestsForApproval,user=request.user,request_type='connect',connect_request='yes')
                except:
                    myusers=[]
                mydict={}
                for row in myusers:
                    localdict={}
                    localdict['request_from']=row.user.username
                    localdict['requesttousername']=row.requesttousername
                    localdict['requesttobiodataid']=row.requesttobiodataid
                    localdict['requesttoemailid']=row.requesttoemailid
                    localdict['biodataid']=row.userbiodataid
                    localdict['rowid']=row.id
                    mydict[row.requesttousername]=localdict
                logger.error(mydict)
                return JsonResponse({'result':'success','msgs':mydict})
            elif request.POST['sentboxview'] == 'sendmymsg':
                try:
                    myusers=get_list_or_404(RequestsForApproval,user=request.user,request_type='connect',connect_request='yes',requesttobiodataid=request.POST['tobiodataid'])
                    touser = get_object_or_404(MyBiodata,pk=request.POST['tobiodataid'])
                    sentbox=MyBiodataChatbox()
                    sentbox.user=request.user
                    sentbox.msgtousername=touser.user.username
                    sentbox.msg=request.POST['msg']
                    sentbox.save()
                    toinbox=MyBiodataInbox()
                    toinbox.user=touser.user
                    toinbox.mybiodataid=touser.id
                    toinbox.msgfromusername=request.user.username
                    toinbox.msg=request.POST['msg']
                    toinbox.save()
                    return JsonResponse({'result':'MESSAGE HAS BEEN SENT SUCCESSFULLY.'})

                except:
                    return JsonResponse({'result':'SORRY,YOU ARE NOT AUTHORIZED TO SEND MESSAGE TO SELECTED USER'})

                return JsonResponse({'result':'success'})
            elif request.POST['sentboxview'] == 'approvereq':
                logger.error('app requests')
                try:
                    reqapproval=get_object_or_404(RequestsForApproval,pk=request.POST['rowid'])
                    logger.error(request.POST['reqtype'])
                    if request.POST['reqtype'] == 1:
                        reqapproval.contact_view_request='yes'
                    else:
                        reqapproval.connect_request='yes'
                    reqapproval.save()
                    return JsonResponse({'result':'REQUEST APPROVED SUCCESSFULLY'})
                except:
                    return JsonResponse({'result':'BAD DATA PASSED, PLEASE TRY AGAIN!'})
            elif request.POST['sentboxview'] == 'rejectreq':
                logger.error('rej requests')
                try:
                    reqapproval=get_object_or_404(RequestsForApproval,pk=request.POST['rowid'])
                    if request.POST['reqtype'] == 1:
                        reqapproval.contact_view_request='no'
                    else:
                        reqapproval.connect_request='no'
                    reqapproval.save()
                    return JsonResponse({'result':'REQUEST REJECTED FOR NOW!'})
                except:
                    return JsonResponse({'result':'BAD DATA PASSED, PLEASE TRY AGAIN!'})
            elif request.POST['sentboxview'] == 'deletereq':
                logger.error('del requests')
                try:
                    reqapproval=get_object_or_404(RequestsForApproval,pk=request.POST['rowid'])
                    reqapproval.delete()
                    return JsonResponse({'result':'REQUEST DELETED SUCCESSFULLY'})
                except:
                    return JsonResponse({'result':'BAD DATA PASSED, PLEASE TRY AGAIN!'})
            elif request.POST['sentboxview'] == 'unblockreq':
                logger.error('unblock requests')
                try:
                    reqapproval=get_list_or_404(RequestsForApproval,requesttobiodataid=request.POST['biodataid'],requesttousername=request.user.username,requestfromusername=request.POST['msgfromusername'])
                    for row in reqapproval:
                        row.connect_request='yes'
                        row.save()
                    return JsonResponse({'result':'USER HAS BEEN UNBLOCKED'})
                except:
                    return JsonResponse({'result':'BAD DATA PASSED, PLEASE TRY AGAIN!'})
            elif request.POST['sentboxview'] == 'blockreq':
                try:
                    reqapproval=get_list_or_404(RequestsForApproval,requesttobiodataid=request.POST['biodataid'],requesttousername=request.user.username,requestfromusername=request.POST['msgfromusername'])
                    for row in reqapproval:
                        row.connect_request='no'
                        row.save()
                    return JsonResponse({'result':'USER HAS BEEN BLOCKED SUCCESSFULLY'})
                except:
                    return JsonResponse({'result':'BAD DATA PASSED, PLEASE TRY AGAIN!'})
            elif request.POST['sentboxview'] == 'userspecific':
                logger.error('sentbox user specific request')
                try:
                    inbox=get_list_or_404(MyBiodataChatbox,user=request.user,msgtousername=request.POST['msgfromusername'])
                except:
                    inbox=[]
                mydict={}
                for row in inbox:
                    localdict={}
                    localdict['msg']=row.msg
                    localdict['msgfromusername']=row.msgtousername
                    mydict[row.id]=localdict
                logger.error(mydict)
                return JsonResponse({'result':request.POST['msgfromusername'],'msgs':mydict})

            try:
                logger.error('inbox request')
                inbox=get_list_or_404(MyBiodataInbox,user=request.user,msgfromusername=request.POST['msgfromusername'])
            except:
                inbox=[]
            mydict={}
            for row in inbox:
                localdict={}
                localdict['msg']=row.msg
                localdict['msgfromusername']=row.msgfromusername
                mydict[row.id]=localdict
            logger.error(mydict)
            return JsonResponse({'result':request.POST['msgfromusername'],'msgs':mydict})
        try:
            todo=get_object_or_404(MyBiodata,pk=request.POST['biodataid'],user=request.user,deletedrow=False)
            logger.error(todo.id)
            return render(request,'todo/mybiodatadownloadtodo.html',{'todo':todo,'found':'found'})
        except :
            return render(request,'todo/mybiodatadownloadtodo.html',{'error':"It's not your biodata ID, Please try again."})


def biodatahelptodo(request):

    if request.method == 'GET':
        return render(request,'todo/biodatahelptodo.html',{'form':BiodataHelpForm()})
    else:
        try:
            form=BiodataHelpForm(request.POST)
            form.save()
            try:
                msg = MIMEMultipart()
                msg['From'] = 'kushwahasamajshadi@gmail.com'
                msg['To'] = 'rohitkushwah9527@gmail.com'
                msg['Subject'] = request.POST['subject']
                body = "{} & contact number {} & emailid {}".format(request.POST['query'],request.POST['contact_number'],request.POST['email_id'])
                msg.attach(MIMEText(body, 'plain'))
                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.starttls()
                s.login(msg['From'], "Ksamaj@#123")
                text = msg.as_string()
                s.sendmail(msg['From'], msg['To'], text)
                s.quit()

                msg = MIMEMultipart()
                msg['From'] = 'kushwahasamajshadi@gmail.com'
                msg['To'] = request.POST['email_id']
                msg['Subject'] = request.POST['subject']
                body = "You send us this query {}  .We will help you on priority Thanks".format(request.POST['query'])
                msg.attach(MIMEText(body, 'plain'))
                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.starttls()
                s.login(msg['From'], "Ksamaj@#123")
                text = msg.as_string()
                s.sendmail(msg['From'], msg['To'], text)
                s.quit()
            except:
                logger.error('error occured in biodata help')



            todos = BiodataHelp.objects.latest('id')
            return render(request,'todo/biodatahelptodo.html',{'form':BiodataHelpForm(),'contact':todos})
        except ValueError:
            return render(request,'todo/biodatahelptodo.html',{'form':BiodataHelpForm(),'error':"Bad data Passed! Try again."})

    return render(request,'todo/biodatahelptodo.html')

@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request,'todo/createtodo.html',{'form':TodoForm()})
    else:
        try:
            form=TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect(currenttodos)
        except ValueError:
            return render(request,'todo/createtodo.html',{'form':TodoForm(),'error':"Bad data Passed! Try again."})


def translatortodo(request):
    translator = Translator()
    available_langugages=googletrans.LANGUAGES
    if request.method == 'POST':
        return render(request,'todo/translatortodo.html',{'available_langugages':available_langugages})
    else:
        return render(request,'todo/translatortodo.html',{'available_langugages':available_langugages})


@csrf_protect
def translatetodo(request):
    fromlangval = request.POST['fromlangval']
    tolangval = request.POST['tolangval']
    lefttext = request.POST['lefttext']
    righttext = request.POST['righttext']
    resulttype = request.POST['resulttype']
    translator = Translator()
    #result = translator.translate(lefttext,src='en',dest=tolangval)
    langsrc = fromlangval
    langdetected = translator.detect(lefttext)
    if(langdetected.lang != fromlangval):
        langsrc=langdetected.lang
    result = translator.translate(lefttext, src=langsrc, dest=tolangval)

    if(resulttype == 'pronunciation'):
        return JsonResponse({'result':result.pronunciation,'langdetected':langdetected.lang})
    else:
        return JsonResponse({'result':result.text,'langdetected':langdetected.lang})

def passwordgeneratortodo(request):
    thestring=""
    Characters=list('abcdefghijklmnopqrstuvwxyz')
    if request.GET.get("uppercase"):
        Characters.extend(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
    if request.GET.get("special"):
        Characters.extend(list('!@#$%^&*()_+'))
    if request.GET.get("number"):
        Characters.extend(list('1234567890'))

    length=int(request.GET.get("length",8))
    for x in range(length):
        thestring += random.choice(Characters)

    return render(request,'todo/passwordgeneratortodo.html',{"password":thestring})


# hospital services

def crosslogintodo(request):
    if request.user.is_authenticated:
        if is_admin(request.user):
            error="SORRY,YOU ARE ADMIN.YOU DON'T HAVE SUFFICIENT PRIVILEGES"
        elif is_doctor(request.user):
            error="SORRY,YOU ARE DOCTOR.YOU DON'T HAVE SUFFICIENT PRIVILEGES"
        elif is_patient(request.user):
            error="SORRY,YOU ARE PATIENT.YOU DON'T HAVE SUFFICIENT PRIVILEGES"
        else :
            error="SORRY,YOU ARE NORMAL USER.YOU DON'T HAVE SUFFICIENT PRIVILEGES TO ACCESS HOSPITAL SERVICES"
        return render(request,'todo/crossloginuser.html',{"error":error})
    else:
        return HttpResponseRedirect('userlogin')

#for showing signup/login button for admin
def userclick_view(request,todo_pk):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    if todo_pk==1:
        logger.error('inside1')
        form=AdminSigupForm()
        logger.error('outside post')
        if request.method=='POST':
            logger.error('inside post')
            form=AdminSigupForm(request.POST)
            error='INVALID INPUT!'
            logger.error(form.is_valid())
            if form.is_valid():
                user=form.save()
                user.set_password(user.password)
                user.save()
                my_admin_group = Group.objects.get_or_create(name='ADMIN')
                my_admin_group[0].user_set.add(user)
                logger.error('all ok')
                return HttpResponseRedirect('userlogin')
            elif  User.objects.filter(username=request.POST['username']).count():
                error='Username is already used,Please Enter unique value'
            return render(request,'todo/adminsignup.html',{'form':form,'error':error})
        return render(request,'todo/adminsignup.html',{'form':form})
    elif todo_pk==2:
        userForm=forms.DoctorUserForm()
        doctorForm=forms.DoctorForm()
        mydict={'userForm':userForm,'doctorForm':doctorForm}
        if request.method=='POST':
            userForm=forms.DoctorUserForm(request.POST)
            doctorForm=forms.DoctorForm(request.POST,request.FILES)
            if userForm.is_valid() and doctorForm.is_valid():
                user=userForm.save()
                user.set_password(user.password)
                user.save()
                doctor=doctorForm.save(commit=False)
                doctor.user=user
                doctor=doctor.save()
                my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
                my_doctor_group[0].user_set.add(user)
                return HttpResponseRedirect('userlogin')
            elif User.objects.filter(username=request.POST['username']).count():
                error='Username is already Used,Please Enter Unique Value'
                mydict['error']=error
        return render(request,'todo/doctorsignup.html',context=mydict)
    elif todo_pk==3:
        userForm=forms.PatientUserForm()
        patientForm=forms.PatientForm()
        mydict={'userForm':userForm,'patientForm':patientForm}
        if request.method=='POST':
            userForm=forms.PatientUserForm(request.POST)
            patientForm=forms.PatientForm(request.POST,request.FILES)
            if userForm.is_valid() and patientForm.is_valid():
                user=userForm.save()
                user.set_password(user.password)
                user.save()
                patient=patientForm.save(commit=False)
                patient.user=user
                patient.assignedDoctorId=request.POST.get('assignedDoctorId')
                patient=patient.save()
                my_patient_group = Group.objects.get_or_create(name='PATIENT')
                my_patient_group[0].user_set.add(user)
                return HttpResponseRedirect('userlogin')
            elif User.objects.filter(username=request.POST['username']).count():
                error='Username is already Used,Please Enter Unique Value'
                mydict['error']=error
        return render(request,'todo/patientsignup.html',context=mydict)
    return render(request,'todo/userclick.html')

#for checking userType
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()
def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()

def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_doctor(request.user):
        accountapproval=models.Doctor.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('doctor-dashboard')
        else:
            return render(request,'todo/user_wait_for_approval.html')
    elif is_patient(request.user):
        accountapproval=models.Patient.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('patient-dashboard')
        else:
            return render(request,'todo/user_wait_for_approval.html')
    else:
        if request.user.is_authenticated:
            return redirect('crosslogintodo')
        return redirect('home')

@login_required(login_url='loginuser')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    #for both table in admin dashboard
    doctors=models.Doctor.objects.all().order_by('-id')
    patients=models.Patient.objects.all().order_by('-id')
    #for three cards
    doctorcount=models.Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount=models.Doctor.objects.all().filter(status=False).count()

    patientcount=models.Patient.objects.all().filter(status=True).count()
    pendingpatientcount=models.Patient.objects.all().filter(status=False).count()

    appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()
    mydict={
    'doctors':doctors,
    'patients':patients,
    'doctorcount':doctorcount,
    'pendingdoctorcount':pendingdoctorcount,
    'patientcount':patientcount,
    'pendingpatientcount':pendingpatientcount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    }
    return render(request,'todo/admin_dashboard.html',context=mydict)

@login_required(login_url='loginuser')
@user_passes_test(is_admin)
def admin_doctor_view(request):
    return render(request,'todo/admin_doctor.html',{'tempname':'admin-doctor-righthand'})

@login_required(login_url='loginuser')
@user_passes_test(is_admin)
def admin_patient_view(request):
    return render(request,'todo/admin_patient.html',{'tempname':'admin-patient-righthand'})
@login_required(login_url='loginuser')
@user_passes_test(is_admin)
def admin_appointment_view(request):
    return render(request,'todo/admin_appointment.html',{'tempname':'admin-appointment-righthand'})
@login_required(login_url='loginuser')
@user_passes_test(is_admin)
def admin_view_doctor_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'todo/admin_view_doctor.html',{'doctors':doctors})

@login_required(login_url='loginuser')
@user_passes_test(is_admin)
def delete_doctor_from_hospital_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-view-doctor')



@login_required(login_url='loginuser')
@user_passes_test(is_admin)
def update_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)

    userForm=forms.DoctorUserForm(instance=user)
    doctorForm=forms.DoctorForm(request.FILES,instance=doctor)
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST,instance=user)
        doctorForm=forms.DoctorForm(request.POST,request.FILES,instance=doctor)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.status=True
            doctor.save()
            return redirect('admin-view-doctor')
        elif User.objects.filter(username=request.POST['username']).count():
            error='Username is already Used,Please Enter Unique Value'
            mydict['error']=error
    return render(request,'todo/admin_update_doctor.html',context=mydict)

@login_required(login_url='loginuser')
@user_passes_test(is_admin)
def admin_add_doctor_view(request):
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor.status=True
            doctor.save()

            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)
            return HttpResponseRedirect('admin-view-doctor')
        elif User.objects.filter(username=request.POST['username']).count():
            error='Username is already Used,Please Enter Unique Value'
            mydict['error']=error
    return render(request,'todo/admin_add_doctor.html',context=mydict)

@login_required(login_url='loginuser')
@user_passes_test(is_admin)
def admin_approve_doctor_view(request):
    #those whose approval are needed
    doctors=models.Doctor.objects.all().filter(status=False)
    return render(request,'todo/admin_approve_doctor.html',{'doctors':doctors})

@login_required(login_url='loginuser')
@user_passes_test(is_admin)
def approve_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    doctor.status=True
    doctor.save()
    return redirect(reverse('admin-approve-doctor'))


@login_required(login_url='loginuser')
@user_passes_test(is_admin)
def reject_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-approve-doctor')



@login_required(login_url='loginuser')
@user_passes_test(is_admin)
def admin_view_doctor_specialisation_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'todo/admin_view_doctor_specialisation.html',{'doctors':doctors})

@login_required(login_url='loginuser')
@user_passes_test(is_admin)
def admin_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'todo/admin_view_patient.html',{'patients':patients})


@login_required(login_url='loginuser')
@user_passes_test(is_admin)
def delete_patient_from_hospital_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-view-patient')



@login_required(login_url='loginuser')
@user_passes_test(is_admin)
def update_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)

    userForm=forms.PatientUserForm(instance=user)
    patientForm=forms.PatientForm(request.FILES,instance=patient)
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST,instance=user)
        patientForm=forms.PatientForm(request.POST,request.FILES,instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.status=True
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.save()
            return redirect('admin-view-patient')
        elif User.objects.filter(username=request.POST['username']).count():
            error='Username is already Used,Please Enter Unique Value'
            mydict['error']=error
    return render(request,'todo/admin_update_patient.html',context=mydict)

@login_required(login_url='loginuser')
@user_passes_test(is_admin)
def admin_add_patient_view(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            patient=patientForm.save(commit=False)
            patient.user=user
            patient.status=True
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.save()

            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
            return HttpResponseRedirect('admin-view-patient')
        elif User.objects.filter(username=request.POST['username']).count():
            error='Username is already Used,Please Enter Unique Value'
            mydict['error']=error
    return render(request,'todo/admin_add_patient.html',context=mydict)

#------------------FOR APPROVING PATIENT BY ADMIN----------------------
@login_required(login_url='loginuser')
@user_passes_test(is_admin)
def admin_approve_patient_view(request):
    #those whose approval are needed
    patients=models.Patient.objects.all().filter(status=False)
    return render(request,'todo/admin_approve_patient.html',{'patients':patients})



@login_required(login_url='loginuser')
@user_passes_test(is_admin)
def approve_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    patient.status=True
    patient.save()
    return redirect(reverse('admin-approve-patient'))



@login_required(login_url='loginuser')
@user_passes_test(is_admin)
def reject_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-approve-patient')

#--------------------- FOR DISCHARGING PATIENT BY ADMIN START-------------------------
@login_required(login_url='loginuser')
@user_passes_test(is_admin)
def admin_discharge_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'todo/admin_discharge_patient.html',{'patients':patients})



@login_required(login_url='loginuser')
@user_passes_test(is_admin)
def discharge_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    days=(date.today()-patient.admitDate) #2 days, 0:00:00
    assignedDoctor=models.User.objects.all().filter(id=patient.assignedDoctorId)
    d=days.days # only how many day that is 2
    patientDict={
        'patientId':pk,
        'name':patient.get_name,
        'mobile':patient.mobile,
        'address':patient.address,
        'symptoms':patient.symptoms,
        'admitDate':patient.admitDate,
        'todayDate':date.today(),
        'day':d,
        'assignedDoctorName':assignedDoctor[0].first_name,
    }
    if request.method == 'POST':
        try:
            feeDict ={
                'roomCharge':int(request.POST['roomCharge'])*int(d),
                'doctorFee':request.POST['doctorFee'],
                'medicineCost' : request.POST['medicineCost'],
                'OtherCharge' : request.POST['OtherCharge'],
                'total':(int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
            }
        except:
            patientDict['error']='PLEASE ENTER NUMERIC VALUES FOR CHARGES!'
            return render(request,'todo/patient_generate_bill.html',context=patientDict)
        patientDict.update(feeDict)
        #for updating to database patientDischargeDetails (pDD)
        pDD=models.PatientDischargeDetails()
        pDD.patientId=pk
        pDD.patientName=patient.get_name
        pDD.assignedDoctorName=assignedDoctor[0].first_name
        pDD.address=patient.address
        pDD.mobile=patient.mobile
        pDD.symptoms=patient.symptoms
        pDD.admitDate=patient.admitDate
        pDD.releaseDate=date.today()
        pDD.daySpent=int(d)
        pDD.medicineCost=int(request.POST['medicineCost'])
        pDD.roomCharge=int(request.POST['roomCharge'])*int(d)
        pDD.doctorFee=int(request.POST['doctorFee'])
        pDD.OtherCharge=int(request.POST['OtherCharge'])
        pDD.total=(int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        pDD.save()
        return render(request,'todo/patient_final_bill.html',context=patientDict)
    return render(request,'todo/patient_generate_bill.html',context=patientDict)

#--------------for discharge patient bill (pdf) download and printing
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return

def download_pdf_view(request,pk):
    dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=pk).order_by('-id')[:1]
    dict={
        'patientName':dischargeDetails[0].patientName,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':dischargeDetails[0].address,
        'mobile':dischargeDetails[0].mobile,
        'symptoms':dischargeDetails[0].symptoms,
        'admitDate':dischargeDetails[0].admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
    }
    return render_to_pdf('todo/download_bill.html',dict)

@login_required(login_url='loginuser')
@user_passes_test(is_admin)
def admin_view_appointment_view(request):
    appointments=models.Appointment.objects.all().filter(status=True)
    return render(request,'todo/admin_view_appointment.html',{'appointments':appointments})
@login_required(login_url='loginuser')
@user_passes_test(is_admin)
def admin_add_appointment_view(request):
    appointmentForm=forms.AppointmentForm()
    mydict={'appointmentForm':appointmentForm,}
    if request.method=='POST':
        appointmentForm=forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment=appointmentForm.save(commit=False)
            appointment.doctorId=request.POST.get('doctorId')
            appointment.patientId=request.POST.get('patientId')
            appointment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName=models.User.objects.get(id=request.POST.get('patientId')).first_name
            appointment.status=True
            appointment.save()
        return HttpResponseRedirect('admin-view-appointment')
    return render(request,'todo/admin_add_appointment.html',context=mydict)



@login_required(login_url='loginuser')
@user_passes_test(is_admin)
def admin_approve_appointment_view(request):
    #those whose approval are needed
    appointments=models.Appointment.objects.all().filter(status=False)
    return render(request,'todo/admin_approve_appointment.html',{'appointments':appointments})



@login_required(login_url='loginuser')
@user_passes_test(is_admin)
def approve_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.status=True
    appointment.save()
    return redirect(reverse('admin-approve-appointment'))



@login_required(login_url='loginuser')
@user_passes_test(is_admin)
def reject_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('admin-approve-appointment')

@login_required(login_url='loginuser')
@user_passes_test(is_doctor)
def doctor_dashboard_view(request):
    #for three cards
    patientcount=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).count()
    appointmentcount=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).count()
    patientdischarged=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name).count()

    #for  table in doctor dashboard
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).order_by('-id')
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid).order_by('-id')
    appointments=zip(appointments,patients)
    mydict={
    'patientcount':patientcount,
    'appointmentcount':appointmentcount,
    'patientdischarged':patientdischarged,
    'appointments':appointments,
    'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'todo/doctor_dashboard.html',context=mydict)

@login_required(login_url='loginuser')
@user_passes_test(is_doctor)
def doctor_patient_view(request):
    mydict={
    'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'todo/doctor_patient.html',context=mydict)


@login_required(login_url='loginuser')
@user_passes_test(is_doctor)
def doctor_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'todo/doctor_view_patient.html',{'patients':patients,'doctor':doctor})



@login_required(login_url='loginuser')
@user_passes_test(is_doctor)
def doctor_view_discharge_patient_view(request):
    dischargedpatients=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'todo/doctor_view_discharge_patient.html',{'dischargedpatients':dischargedpatients,'doctor':doctor})

@login_required(login_url='loginuser')
@user_passes_test(is_doctor)
def doctor_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'todo/doctor_appointment.html',{'doctor':doctor})



@login_required(login_url='loginuser')
@user_passes_test(is_doctor)
def doctor_view_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'todo/doctor_view_appointment.html',{'appointments':appointments,'doctor':doctor})



@login_required(login_url='loginuser')
@user_passes_test(is_doctor)
def doctor_delete_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'todo/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})



@login_required(login_url='loginuser')
@user_passes_test(is_doctor)
def delete_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'todo/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})

@login_required(login_url='loginuser')
@user_passes_test(is_patient)
def patient_dashboard_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id)
    doctor=models.Doctor.objects.get(user_id=patient.assignedDoctorId)
    mydict={
    'patient':patient,
    'doctorName':doctor.get_name,
    'doctorMobile':doctor.mobile,
    'doctorAddress':doctor.address,
    'symptoms':patient.symptoms,
    'doctorDepartment':doctor.department,
    'admitDate':patient.admitDate,
    }
    return render(request,'todo/patient_dashboard.html',context=mydict)

@login_required(login_url='loginuser')
@user_passes_test(is_patient)
def patient_appointment_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    return render(request,'todo/patient_appointment.html',{'patient':patient})

@login_required(login_url='loginuser')
@user_passes_test(is_patient)
def patient_view_appointment_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    appointments=models.Appointment.objects.all().filter(patientId=request.user.id)
    return render(request,'todo/patient_view_appointment.html',{'appointments':appointments,'patient':patient})

@login_required(login_url='loginuser')
@user_passes_test(is_patient)
def patient_book_appointment_view(request):
    appointmentForm=forms.PatientAppointmentForm()
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    mydict={'appointmentForm':appointmentForm,'patient':patient}
    if request.method=='POST':
        appointmentForm=forms.PatientAppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment=appointmentForm.save(commit=False)
            appointment.doctorId=request.POST.get('doctorId')
            appointment.patientId=request.user.id #----user can choose any patient but only their info will be stored
            appointment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName=request.user.first_name #----user can choose any patient but only their info will be stored
            appointment.status=False
            appointment.save()
        return HttpResponseRedirect('patient-view-appointment')
    return render(request,'todo/patient_book_appointment.html',context=mydict)

@login_required(login_url='loginuser')
@user_passes_test(is_patient)
def patient_discharge_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=patient.id).order_by('-id')[:1]
    patientDict=None
    if dischargeDetails:
        patientDict ={
        'is_discharged':True,
        'patient':patient,
        'patientId':patient.id,
        'patientName':patient.get_name,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':patient.address,
        'mobile':patient.mobile,
        'symptoms':patient.symptoms,
        'admitDate':patient.admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
        }
        print(patientDict)
    else:
        patientDict={
            'is_discharged':False,
            'patient':patient,
            'patientId':request.user.id,
        }
    return render(request,'todo/patient_discharge.html',context=patientDict)
