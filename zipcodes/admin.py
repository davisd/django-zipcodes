from django.contrib import admin
from django import forms

from models import Zipcode, ZipcodeUpdate, ZipcodeUpload

admin.site.register(Zipcode)
admin.site.register(ZipcodeUpload)
admin.site.register(ZipcodeUpdate)
