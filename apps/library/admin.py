from django.contrib import admin
from .models import LikeDislikePrompt, Model, Parameter, ParameterMapping, Prompt

# Register your models here.
admin.site.register(LikeDislikePrompt)
admin.site.register(Model)
admin.site.register(Parameter)
admin.site.register(ParameterMapping)
admin.site.register(Prompt)
