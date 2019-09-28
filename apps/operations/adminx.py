import xadmin

from apps.operations.models import UserAsk, UserCourse, UserFavourite, UserMessage, CourseComments
from apps.operations.models import Banner


class BannerAdmin(object):
    list_display  = ["title", "image", "url", "index"]
    search_fields = ["title", "image", "url", "index"]
    list_filter   = ["title", "image", "url", "index"]


class UserAskAdmin(object):
    list_display  = ["name", "mobile", "course", "added_time"]
    search_fields = ["name", "mobile", "course"]
    list_filter   = ["name", "mobile", "course", "added_time"]


class UserCourseAdmin(object):
    list_display  = ["user", "course", "added_time"]
    search_fields = ["user", "course"]
    list_filter   = ["user", "course", "added_time"]


class UserMessaageAdmin(object):
    list_display  = ["user", "message", "has_read", "added_time"]
    search_fields = ["user", "message", "has_read"]
    list_filter   = ["user", "message", "has_read", "added_time"]


class CourseCommentsAdmin(object):
    list_display  = ["user", "course", "comments", "added_time"]
    search_fields = ["user", "course", "comments"]
    list_filter   = ["user", "course", "comments", "added_time"]


class UserFavouriteAdmin(object):
    list_display  = ["user", "fav_id", "fav_type", "added_time"]
    search_fields = ["user", "fav_id", "fav_type"]
    list_filter   = ["user", "fav_id", "fav_type", "added_time"]


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
xadmin.site.register(UserMessage, UserMessaageAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserFavourite, UserFavouriteAdmin)