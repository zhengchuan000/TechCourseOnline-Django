from django.views.generic import View
from django.http import JsonResponse
from django.shortcuts import render
from apps.operations.models import UserFavourite, CourseComments
from apps.operations.forms import UserFavForm, CommentsForm
from apps.organizations.models import CourseOrg, Teacher
from apps.courses.models import Course
from apps.operations.models import Banner


class IndexView(View):
    def get(self, request, *args, **kwargs):

        banners = Banner.objects.all().order_by("index")
        courses = Course.objects.filter(is_banner=False)[:6]
        banners_courses = Course.objects.filter(is_banner=True)
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, "index.html", {
            "banners": banners,
            "courses": courses,
            "banners_courses": banners_courses,
            "course_orgs": course_orgs
        })


class CommentView(View):
    def post(self, request, *args, **kwargs):
        """
        用户收藏， 用户取消收藏
        """

        #如果用户未登录，那么直接跳转到登录页面
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": "fail",
                "msg": "用户未登录"
            })

        comment_form = CommentsForm(request.POST)
        if comment_form.is_valid():
            course = comment_form.cleaned_data["course"]
            comments = comment_form.cleaned_data["comments"]

            comment = CourseComments()
            comment.user = request.user
            comment.comments = comments
            comment.course = course
            comment.save()

            return JsonResponse({
                "status": "success",
            })

        else:
            return JsonResponse({
                "status": "fail",
                "msg": "参数错误"
            })


class AddFavView(View):
    def post(self, request, *args, **kwargs):
        """
        用户收藏， 用户取消收藏
        """

        #如果用户未登录，那么直接跳转到登录页面
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": "fail",
                "msg": "用户未登录"
            })

        user_fav_form = UserFavForm(request.POST)
        if user_fav_form.is_valid():
            fav_id = user_fav_form.cleaned_data["fav_id"]
            fav_type = user_fav_form.cleaned_data["fav_type"]

            #是否已经收藏
            existed_records = UserFavourite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)

            if existed_records:
                existed_records.delete()

                if fav_id == 1:
                    course = Course.objects.get(id=fav_id)
                    course.fav_nums -= 1
                    course.save()
                elif fav_id == 2:
                    course_org = CourseOrg.objects.get(id=fav_id)
                    course_org.fav_nums -= 1
                    course_org.save()
                elif fav_id == 3:
                    teacher = Teacher.objects.get(id=fav_id)
                    teacher.fav_nums -= 1
                    teacher.save()
                return JsonResponse({
                    "status": "success",
                    "msg": "收藏"
                })

            else:
                user_fav = UserFavourite()
                user_fav.fav_id = fav_id
                user_fav.user = request.user
                user_fav.save()
                return JsonResponse({
                    "status": "success",
                    "msg": "已收藏"
                })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "参数错误"
            })