from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test,login_required

def is_recruiter(user):
    return user.is_authenticated and user.is_recruiter
    
@login_required
def Home(request):
    return render(request,'jobseeker/layout.html')

@user_passes_test(is_recruiter, login_url='no_permission_page')
def Applications(request):
    return HttpResponse("<h1>view the Candidate's Applications</h1>")

@user_passes_test(is_recruiter, login_url='no_permission_page')
def Jobs(request):
    return HttpResponse("<h1>view or edit Jobs</h1>")

@user_passes_test(is_recruiter, login_url='no_permission_page')
def CreateJob(request):
    return HttpResponse("<h1>CreateJob</h1>")

@user_passes_test(is_recruiter, login_url='no_permission_page')
def Users(request):
    return HttpResponse("<h1>view or edit Users</h1>")

@user_passes_test(is_recruiter, login_url='no_permission_page')
def CreateUser(request):
    return HttpResponse("<h1>CreateUsers</h1>")

@user_passes_test(is_recruiter, login_url='no_permission_page')
def Profile(request):
    return HttpResponse("<h1>view or edit profile</h1>")

@user_passes_test(is_recruiter, login_url='no_permission_page')
def EmployeeLifeCycle(request):
    return HttpResponse("<h1>EmployeeLifeCycle management</h1>")

