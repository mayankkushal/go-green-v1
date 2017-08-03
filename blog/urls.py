from django.conf.urls import url
from blog import views

app_name = 'blog'
urlpatterns = [
	url(r'^$', views.ArticleListView.as_view(), name='index' ),
	url(r'^article/(?P<article_slug>[\w\-]+)', views.article, name="article"),
	url(r'^add_comment', views.add_comment, name="add_comment"),
	url(r'^like_article', views.like_article, name="like_article"),
	url(r'^check_like', views.check_like, name="check_like"),
]