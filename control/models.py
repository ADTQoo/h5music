from django.db import models

# Create your models here.

class MusicModel(models.Model):

	music_id = models.CharField(max_length=180, default='init')
	music_name = models.CharField(max_length=32, default='init')
	artist = models.CharField(max_length=32, default='init')
	album = models.CharField(max_length=32, default='init')
	file_url = models.CharField(max_length=256, default='init')

class MusicTagModel(models.Model):

	music_id = models.CharField(max_length=180, default='init')
	tag = models.CharField(max_length=32, default='init')


class UserProfileModel(models.Model):

	user_id = models.CharField(max_length=180, default='init')
	cookie = models.CharField(max_length=256, default='init')
	
	user_name = models.CharField(max_length=32, default='init')
	user_pass = models.CharField(max_length=32, default='init')

class UserHistoryModel(models.Model):

	user_id = models.CharField(max_length=180, default='init')
	time_created = models.DateTimeField(null=True, auto_now_add=True)

	music_id = models.CharField(max_length=180, default='init')
