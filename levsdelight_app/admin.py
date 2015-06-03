from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Slideshow
from .models import MonthMap
from .models import Author


admin.site.register(Slideshow)
admin.site.register(MonthMap)
admin.site.register(Author)
