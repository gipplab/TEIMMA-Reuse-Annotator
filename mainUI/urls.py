from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

# URLConf
urlpatterns = [
	path('mainUI/', views.say_hello),
	path('sampledoc/', views.sample_document_2),
	path('implJS/', views.sample_document),
	path('api/getJson', views.getJson),
	path('hellow/', views.viewPag),
	path(r'hellow/getCharacterOffsets', views.getCharacterOffsets),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL,
		document_root=settings.MEDIA_ROOT)