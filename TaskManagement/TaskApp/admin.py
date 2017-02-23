from django.contrib import admin

# Register your models here.
from .models import *

class page_list(admin.ModelAdmin):
	list_per_page = 1000

admin.site.register(Project)
admin.site.register(Task)