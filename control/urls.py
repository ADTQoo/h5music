from django.conf.urls import include, url
from .views import *

urlpatterns = [
	url(r'^play/(?P<music_id>[\w\W]+)$', play_view),
	url(r'^search/view/(?P<user_id>[\w\W]+)$', search_view),
	url(r'^search/data/(?P<keyword>[\w\W]+)$', search_data),
	url(r'^user/register/(?P<user_name>[\w\W]+)/(?P<user_pass>[\w\W]+)$', register_handler),
	url(r'^user/regview/', register_view),
	url(r'^history/view/(?P<user_id>[\w\W]+)$', history_view),
	url(r'^recommend/view/(?P<user_id>[\w\W]+)$', recommend_view),
]
