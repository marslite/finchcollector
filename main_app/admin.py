from django.contrib import admin

# Register your models here.
from .models import Finch, Feeding
admin.site.register(Finch)
admin.site.register(Feeding)
