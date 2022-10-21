from django.contrib import admin
from .models import Annotations
from .models import PlainText
from .models import Math
from .models import HTMLFiles

# Register your models here.

admin.site.register(Annotations)
admin.site.register(PlainText)
admin.site.register(Math)
admin.site.register(HTMLFiles)