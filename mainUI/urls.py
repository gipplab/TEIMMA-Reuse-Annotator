from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

# URLConf
urlpatterns = [
	path('mainUI/', views.say_hello),
	path('feedbackAnno/', views.feednackanno),
	path('sampledoc/', views.sample_document_2),
	path('download/', views.download_file, name='download_file'),
	path('about/', views.sample_document),
	path('api/getJson', views.getJson),
	path(r'hellow/getCharacterOffsets', views.getCharacterOffsets),
	path('pair-detail/<str:file_name1>/<str:file_name2>/', views.pair_detail_view, name='pair_detail'),
	path('save_pair/', views.save_pair, name='save_pair'),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL,
		document_root=settings.MEDIA_ROOT)