from django.contrib import admin
from blog.models import Article, Comment, Images
# Register your models here.

class CommentInline(admin.TabularInline):
	model = Comment

class ImagesInline(admin.TabularInline):

	'''
		Tabular Inline View for Images
	'''
	model = Images

class ArticleAdmin(admin.ModelAdmin):
	'''
		Admin View for Article
	'''
	inlines = [
		ImagesInline, CommentInline
	]
	list_display = ('name', 'date_created', 'likes_count', 'comments')

admin.site.register(Article, ArticleAdmin)