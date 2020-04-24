from django.contrib import admin
from django.urls import path
import core.views as views

urlpatterns = [
	path('admin/', admin.site.urls),

# ````Callback URL
	path('', views.callback_url),

	# Url to fetch top 10 most recent commits.
	path('get_recent_commits/', views.top_10_recent_commits),

	# Url to fetch most frequently used words.
	path('most_frequent_words/', views.most_frequently_used),

	# Url to fetch most common commit hour.
	path('most_common_hour/', views.time_of_the_hour),

    # path('get_auth_code/', views.get_auth_code),
]
