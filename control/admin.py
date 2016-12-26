from django.contrib import admin

from .models import *

# Register your models here.

class MusicAdmin(admin.ModelAdmin):
	list_display = ('music_id', 'music_name', 'artist', 'album', 'file_url')

class MusicTagAdmin(admin.ModelAdmin):
	list_display = ('music_id', 'tag')

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user_id', 'cookie', 'user_name')

class UserHistoryAdmin(admin.ModelAdmin):
	list_display = ('user_id', 'time_created', 'music_id')

admin.site.register(MusicModel, MusicAdmin)
admin.site.register(MusicTagModel, MusicTagAdmin)
admin.site.register(UserProfileModel, UserProfileAdmin)
admin.site.register(UserHistoryModel, UserHistoryAdmin)
