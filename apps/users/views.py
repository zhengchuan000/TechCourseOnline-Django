from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.users.form import LoginForm, UploadImageForm, UserInfoForm, ChangePwdForm
from apps.operations.models import UserFavourite, UserMessage, Banner
from apps.organizations.models import CourseOrg, Teacher
from apps.courses.models import Course
from pure_pagination import Paginator, PageNotAnInteger


def message_nums(request):
    if request.user.is_authenticated:
        return {'unread_nums': request.user.usermessage_set.filter(has_read=False).count()}
    else:
        return {}


class MyMessageView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        messages = UserMessage.objects.filter(user=request.user)
        current_page = "message"
        for message in messages:
            message.has_read = True
            message.save()
        # 对讲师列表进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(messages, per_page=1, request=request)
        messages = p.page(page)

        return render(request, "usercenter-message.html", {
            "messages": messages,
            "current_page": current_page
        })


class MyFavCourseView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        current_page = "myfav_course"
        course_list = []
        fav_courses = UserFavourite.objects.filter(user=request.user, fav_type=3)
        for fav_course in fav_courses:
            try:
                course = Teacher.objects.get(id=fav_course.fav_id)
                course_list.append(course)
            except Course.DoesNotExist as e:
                pass

        return render(request, "usercenter-fav-course.html", {
            "course_list": course_list,
            "current_page": current_page
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        current_page = "myfav_teacher"
        teacher_list = []
        fav_teachers = UserFavourite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher = Teacher.objects.get(id=fav_teacher.fav_id)
            teacher_list.append(teacher)
        return render(request, "usercenter-fav-teacher.html", {
            "teacher_list": teacher_list,
            "current_page": current_page
        })


class MyFavOrgView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        current_page = "myfavorg"
        org_list = []
        fav_orgs = UserFavourite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org = CourseOrg.objects.get(id=fav_org.fav_id)
            org_list.append(org)
        return render(request, "usercenter-fav-org.html", {
            "org_list": org_list,
            "current_page": current_page
        })



class MyCourseView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        current_page = "mycourse"
        # my_course = UserCourse.objects.filter(user=request.user)
        return render(request, "usercenter-mycourse.html", {
            # "my_course": my_course,
            "current_page": current_page
        })


class ChangePwdView(View):
    login_url = "/login/"

    def post(self, request, *args, **kwargs):
        pwd_form = ChangePwdForm(request.POST)
        if pwd_form.is_valid():
            # pwd1 = request.POST.get("password1", "")
            # pwd2 = request.POST.get("password2", "")
            #
            # if pwd1 != pwd2:
            #     return JsonResponse({
            #         "status": "fail",
            #         "msg": "密码不一致"
            #     })
            pwd1 = request.POST.get("password1", "")
            user = request.user
            user.set_password(pwd1)
            user.save()
            #login(request, user)

            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse(pwd_form.errors)


class UploadImageView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, *args, **kwargs):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse({
                "status": "fail"
            })


class UserInfoView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        current_page = "info"
        return render(request, 'usercenter-info.html', {
            "current_page": current_page
        })

    def post(self, request, *args, **kwargs):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse(user_info_form.errors)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse("login"))


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))

        banners = Banner.objects.all()[:3]

        return render(request,"login.html", {
            "banners": banners
        })

    def post(self, request, *args, **kwargs):
        login_form = LoginForm(request.POST)

        banners = Banner.objects.all()[:3]

        if login_form.is_valid():
            user_name = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(username=user_name, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, 'login.html', {"msg": "用户名或密码错误", "login_form": login_form, "banners":banners})
        else:
            return render(request, "login.html", {"login_form": login_form, "banners":banners})
# Create your views here.
