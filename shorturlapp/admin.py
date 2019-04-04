from django.contrib import admin
from shorturlapp.models import Info
# Register your models here.

admin.site.site_header = 'ShortUrl后台管理'
admin.site.site_title = 'ShortUrl'
admin.site.index_title = '后台管理'
admin.register(Info)


