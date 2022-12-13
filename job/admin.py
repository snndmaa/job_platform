from django.contrib import admin
from job.models import Company, Post, Comment, Payment, Field, Qualification, Role, Industry, Discipline, State, Region

# Register your models here.

admin.site.register(Company)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Payment)
admin.site.register(Field)
admin.site.register(Role)
admin.site.register(Industry)
admin.site.register(Discipline)
admin.site.register(State)
admin.site.register(Region)
admin.site.register(Qualification)