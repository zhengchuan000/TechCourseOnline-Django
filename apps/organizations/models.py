from django.db import models

from apps.users.models import BaseModel


class City(BaseModel):
    class Meta:
        verbose_name = "城市"
        verbose_name_plural = verbose_name

    name = models.CharField(max_length=20, verbose_name="城市名")
    desc = models.CharField(max_length=200, verbose_name="描述")

    def __str__(self):
        return self.name


class CourseOrg(BaseModel):
    class Meta:
        verbose_name = "课程机构"
        verbose_name_plural = verbose_name

    name = models.CharField(verbose_name="机构名称", max_length=50)
    desc = models.TextField(verbose_name="描述")
    tag = models.CharField(max_length=100, default="全国知名", verbose_name="机构名称")
    category = models.CharField(default="pxjg", max_length=4, verbose_name="机构类别", choices=(('pxjg',"培训机构"), ("gr", "个人"), ("gx","高校")))
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
    image = models.ImageField(upload_to="org/%Y/%m", verbose_name="logo", max_length=100)
    address = models.CharField(max_length=150, verbose_name="机构地址")
    students = models.IntegerField(default=0, verbose_name="学习人数")
    course_nums = models.IntegerField(default=0, verbose_name="课程数")
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="所在城市")
    is_auth = models.BooleanField(default=False, verbose_name="是否认证")
    is_gold = models.BooleanField(default=False, verbose_name="是否金牌")

    def get_courses(self):
        courses = self.course_set.filter(is_classic=True)[:3]
        return courses

    def __str__(self):
        return self.name


class Teacher(BaseModel):
    class Meta:
        verbose_name = "讲师"
        verbose_name_plural = verbose_name

    org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name="课程机构")
    name = models.CharField(verbose_name="教师姓名", max_length=50)
    work_years = models.IntegerField(default=0, verbose_name="工作年限")
    work_company = models.CharField(max_length=150, verbose_name="就职公司")
    work_position = models.CharField(max_length=50, verbose_name="公司职位")
    points = models.CharField(max_length=50, verbose_name="教学特点")
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
    age = models.IntegerField(default=18, verbose_name="年龄")
    image = models.ImageField(upload_to="teacher/%Y/%m", verbose_name="头像", max_length=100)

    def __str__(self):
        return self.name

    def course_nums(self):
        return self.course_set.all().count()

