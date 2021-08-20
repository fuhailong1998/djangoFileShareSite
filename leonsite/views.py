import os

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from leonsite.models import User, File


def StrOfSize(size):
    '''
    auth: wangshengke@kedacom.com ；科达柯大侠
    递归实现，精确为最大单位值 + 小数点后三位
    '''

    def strofsize(integer, remainder, level):
        if integer >= 1024:
            remainder = integer % 1024
            integer //= 1024
            level += 1
            return strofsize(integer, remainder, level)
        else:
            return integer, remainder, level

    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    integer, remainder, level = strofsize(size, 0, 0)
    if level + 1 > len(units):
        level = -1
    return ('{}.{:>03d} {}'.format(integer, remainder, units[level]))

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
            request.session['login'] = result[0].id
            return redirect('/filelist')


class ExitView(View):
    def get(self, request):
        request.session.clear()
        return redirect('/')


class FileListView(View):
    @isLogin
    def get(self, request, user=None):
        filelist = File.objects.all()
        current_user = request.session['login']
        return render(request, 'filelist.html', {'filelist': filelist, 'current_user': current_user})


class UserCenterView(View):
    @isLogin
    def get(self, request, user=None):
        author = User.objects.get(id=request.session['login'])
        filelist = File.objects.filter(author=author)
        return render(request, 'usercenter.html', {'filelist':filelist})


class UploadView(View):

        def get(self, request):
            return HttpResponse('upload')

        def post(self, request):
            file = request.FILES.get('file', '')

            description = request.POST.get('description', '')

            size = StrOfSize(file.size)

            author = User.objects.get(id=request.session['login'])

            # 入库操作
            File.objects.create(author=author, description=description, file=file, size=size)
            return HttpResponse("上传成功！")



class DownloadView(View):
    def get(self, request, file=None):
        # file = request.GET.get('file', '')

        print(file)

        num = File.objects.get(file=str(file))
        f = File.objects.filter(file=str(file))


        if f.filter(isdelete=True):
            return HttpResponse("文件已删除！")
        elif f.filter(ishide=True):
            return HttpResponse("文件已被发布者隐藏！")
        else:
            f.update(downsum=num.downsum + 1)
            filename = file[file.rindex('/') + 1:]

            with open(os.path.join(os.getcwd(), 'media', file), 'rb') as fr:
                response = HttpResponse(fr.read())
                response['Content-Type'] = 'application/octet-stream'
                response['Content-Disposition'] = 'attachment;filename=' + filename
            return response


class Delete(View):
    def get(self, request):
        file = request.GET.get('file', '')

        File.objects.filter(file=str(file)).update(isdelete=True)

        return JsonResponse({'flag': True})


class ChangePassword(View):
    def get(self, request):
        return render(request, 'changepassword.html')