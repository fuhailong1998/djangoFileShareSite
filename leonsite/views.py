from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from leonsite.models import User


def isLogin(func):
    def wrapper(UserInfoView, request, *args, **kwargs):
        try:
            user = request.session['login']
        except KeyError:
            return redirect('/')
        res = func(UserInfoView, request, user, *args, **kwargs)
        return res

    return wrapper


class IndexView(View):
    def get(self, request):
        try:
            _ = request.session['login']
            return redirect('/filelist')
        except KeyError:
            return render(request, 'index.html')


    def post(self, request):
        name = request.POST.get('name', '')
        password = request.POST.get('password', '')
        result = User.objects.filter(name=name, password=password)
        if result.count() == 0:
            return HttpResponse('Password Error!')
        else:
            request.session['login'] = name
            return render(request, 'filelist.html')


class ExitView(View):
    def get(self, request):
        request.session.clear()
        return redirect('/')


class FileListView(View):
    @isLogin
    def get(self, request, user=None):
        return HttpResponse('fdgd')


class UserCenterView(View):
    @isLogin
    def get(self, request, user=None):
        return render(request, 'usercenter.html')