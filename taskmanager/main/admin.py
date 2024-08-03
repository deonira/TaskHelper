from django.contrib import admin
from .models import Project, Profile, User, Task, Comment
admin.site.register(Project)
admin.site.register(Profile)
admin.site.register(Task)
admin.site.register(Comment)
# Register your models here.
