# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from locator import models
import time


# Create your views here.


def index(request):
    """
    系统启动入口
    :param request: 
    :return: 进入登录页面
    """
    return render(request, 'login.html', )


def login(request):
    """
    登录验证方法，若通过验证则进入主页，否则返回登录页面并显示提示信息
    :param request: 
    :return: 
    """
    # if authority(request) == False:
    #    return HttpResponseRedirect('/locator/lock')
    validate = {}
    v1 = ""
    v2 = ""
    flag = True
    validatepassword = ""
    username = ""
    password = ""

    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    try:
        validatepassword = models.User.objects.get(username=username)
        if validatepassword.password != password:
            v2 = "Incorrect password！"
            flag = False
        print validatepassword
    except Exception, e:
        print e
        v2 = "Incorrect password！"
        flag = False

    if username == "":
        v1 = "Username cannot be empty！"
        flag = False
    if password == "":
        v2 = "Password cannot be empty！"
        flag = False
    validate = {"v1": v1, "v2": v2}
    testclass=100

    if flag:
        request.session["username"] = username
        request.session["password"] = password
        request.session['email'] = validatepassword.email
        request.session['userid'] = validatepassword.id
        request.session['isadmin'] = validatepassword.isadmin
        request.session['avatarloc'] = validatepassword.avatarloc
        if validatepassword.isadmin == 'yes':
            return render(request, 'admin/index_admin.html')
        else:
            members = []
            try:
                productobj = models.ProUser.objects.get(user_id=validatepassword.id)
                productId = int(productobj.product_id)
                userids = models.ProUser.objects.filter(product_id=productId)
                for userid in userids:
                    member = models.User.objects.get(id=userid.user_id)
                    members.append(member)
            except Exception, e:
                print e
            return render(request, 'index.html', {'members': members})
    else:
        return render(request, 'login.html', {"validate": validate, "testclass":testclass})


def logout(request):
    """
    退出方法，删除当前用户的session并返回登录页面
    :param request: 
    :return: 登录页面
    """
    del request.session['username']  # 删除session
    del request.session['password']
    return HttpResponseRedirect('/locator/index/')


def profile(request):
    """
    进入个人信息页面
    :param request: 
    :return: 个人信息页面
    """
    if request.session['isadmin'] == 'yes':
        return render(request, 'admin/profile_admin.html')
    else:
        return render(request, 'profile.html')


def main(request):
    """
    由于login方法中涉及session操作，重复调用会导致错误，
    因此用这个方法作为系统内部进入主页的接口
    :param request: 
    :return: 进入主页
    """
    # if authority(request) == False:
    #    return HttpResponseRedirect('/locator/lock')
    if request.session['isadmin'] == 'yes':
        return render(request, 'admin/index_admin.html')
    else:
        members = []
        try:
            productobj = models.ProUser.objects.get(user_id=request.session['userid'])
            productId = int(productobj.product_id)
            userids = models.ProUser.objects.filter(product_id=productId)
            for userid in userids:
                member = models.User.objects.get(id=userid.user_id)
                members.append(member)
        except Exception, e:
            print e
        return render(request, 'index.html', {'members': members})


def edit(request):
    """
    进入编辑新密码页面
    :param request: 
    :return: 
    """
    # if authority(request) == False:
    #    return HttpResponseRedirect('/locator/lock')

    return render(request, 'editprofile.html')


def confirm(request):
    """
    修改密码
    :param request: 
    :return: 
    """
    # if authority(request) == False:
    #    return HttpResponseRedirect('/locator/lock')
    flag = True
    infomation = ""
    username = request.session['username']
    inputPassword = request.POST.get('password', None)
    inputPassword2 = request.POST.get('password2', None)
    if inputPassword == "":
        flag = False
        infomation = "Password cannot be empty！"
    if inputPassword2 == "":
        flag = False
        infomation = "Confirm cannot be empty！"
    if inputPassword != inputPassword2:
        flag = False
        infomation = "Password and confirm password must be consistent!"
    if flag:
        user = models.User.objects.get(username=username)  # 查询该条记录
        user.password = inputPassword  # 修改
        user.save()
        return render(request, 'profile.html', {'success': 'Success！'})
    else:
        return render(request, 'editprofile.html', {'infomation': infomation})


def lock(request):
    """
    锁定页面
    :param request: 
    :return: 
    """
    request.session['lock'] = 'lock'
    return render(request, 'lock_screen.html')


def unlock(request):
    """
    解锁页面
    :param request: 
    :return: 
    """
    request.session['lock'] = 'unlock'
    password = request.POST.get('password', None)
    realpassword = request.session['password']
    if password == realpassword:
        return HttpResponseRedirect('/locator/main/')
    else:
        return render(request, 'lock_screen.html')


def newreport(request):
    """
    跳转到提交报告页面
    :param request: 
    :return: 
    """
    # authority(request)

    current = request.session['username']
    finalusers = []
    finalproducts = []
    products = models.Product.objects.all()
    for p in products:
        finalproducts.append(p.name)

    users = models.User.objects.all()
    for u in users:
        if u.username != current:
            finalusers.append(u.username)

    return render(request, 'newreport.html', {'products': finalproducts, 'users': finalusers})


def savereport(request):
    """
    存储新的缺陷报告
    status 参数 ：open代表未分配，unfix代表未修复，fixed代表已修复
    :param request: 
    :return: 
    """
    # authority(request)
    summary = request.POST.get('summary')
    description = request.POST.get('description')
    reporter = request.session['userid']
    assignee = request.POST.get('assignee')
    productid = request.POST.get('product')
    status = 'open'
    opendate = time.strftime("%Y-%d-%m")
    component = request.POST.get('component')
    version = request.POST.get('version')
    platform = request.POST.get('platform')
    os = request.POST.get('os')
    priority = request.POST.get('priority')
    severity = request.POST.get('severity')
    # print summary
    # print description
    # print reporter
    # print assignee
    # print status
    # print opendate
    # print component
    # print version
    # print platform
    # print os
    # print priority
    # print severity
    # print productid

    models.Report.objects.create(summary=summary, description=description, reporter=reporter,
                                 assignee=assignee, status=status, opendate=opendate,
                                 component=component, version=version, platform=platform, os=os,
                                 priority=priority, severity=severity, productid=productid)
    return HttpResponseRedirect('/locator/main')


def authority(request):
    username = ""
    lock = request.session['lock']
    if lock == 'lock':
        return False
    else:
        return True


def unfixed(request):
    # 待修复页面
    current_name = request.session['username']
    current_isadmin = request.session['isadmin']
    reports = models.Report.objects.all()
    disContent = []

    if current_isadmin == 'yes':
        for report in reports:
            if report.status == 'unfixed':
                tmpContent = (report.bugid, report.summary, report.reporter, time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(float(report.opendate))), report.assignee)
                disContent.append(tmpContent)
        return render(request, 'admin/defects_not_resolved_admin.html', {'contents': disContent})
    else:
        for report in reports:
            if report.assignee == current_name and report.status == 'unfixed':
                tmpContent = (report.bugid, report.summary, report.reporter, time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(float(report.opendate))))
                disContent.append(tmpContent)
        return render(request, 'defects_not_resolved.html', {'contents': disContent})


def fixed(request):
    # 已修复页面
    current_name = request.session['username']
    current_isadmin = request.session['isadmin']
    reports = models.Report.objects.all()
    disContent = []

    if current_isadmin == 'yes':
        for report in reports:
            if report.status == 'fixed':
                tmpContent = (report.bugid, report.summary, report.reporter, time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(float(report.opendate))), report.fixdate)
                disContent.append(tmpContent)
        return render(request, 'admin/defects_resolved_admin.html', {'contents': disContent})
    else:
        for report in reports:
            if report.assignee == current_name and report.status == 'fixed':
                tmpContent = (report.bugid, report.summary, report.reporter, time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(float(report.opendate))), report.fixdate)
                disContent.append(tmpContent)
        return render(request, 'defects_resolved.html', {'contents': disContent})


def not_assigned(request):
    reports = models.Report.objects.all()
    disContent = []

    for report in reports:
        if report.status == 'open':
            tmpContent = (report.bugid, report.summary, report.reporter, time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(float(report.opendate))))
            disContent.append(tmpContent)
    return render(request, 'admin/defects_not_assigned_admin.html', {'contents': disContent})
