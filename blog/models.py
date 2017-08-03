from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.
class Article(models.Model):
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=500)
	content = models.TextField(null=False)
	date_created = models.DateTimeField(auto_now_add=True)
	slug = models.SlugField(null=True, default="")
	comments = models.IntegerField(default=0)

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.name)

		super(Article, self).save(*args, **kwargs)

	def likes_count(self):
		return self.likes.count()
	likes_count.short_description = 'Likes'

	def get_absolute_url(self):
		return reverse('blog:article', kwargs={'article_slug': self.slug})

class Images(models.Model):
	article = models.ForeignKey(Article, related_name='images')
	picture = models.ImageField(upload_to="blog_images", null=False)

	def __str__(self):
		return self.article.name

	class Meta:
		verbose_name_plural = "Images"


class Comment(models.Model):
	poster = models.ForeignKey(User)
	article = models.ForeignKey(Article)
	time = models.DateTimeField(auto_now_add=True)
	comment = models.CharField(max_length=124)

	def __str__(self):
		return self.poster.username

class Like(models.Model):
    user = models.ForeignKey(User)
    article = models.ForeignKey(Article, related_name='likes')
    created = models.DateTimeField(auto_now_add=True)
