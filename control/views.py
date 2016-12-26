from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,StreamingHttpResponse
from django.template import RequestContext, loader

import logging
import traceback
import hashlib
import datetime

from .models import *
from .data_filter import *

# Create your views here.

logger = logging.getLogger('ms')


def index_view(request):
	ctx = {}

	try:
		logger.info('index_view, started')

		pt_hot = get_platform_hot()
		if pt_hot['result']	!= 'success':
			return HttpResponse('get_platform_hot got error!')

		s_details = []
		logger.info(pt_hot)

		for (k, v) in pt_hot['songs']:
			detail = MusicModel.objects.filter(music_id=k)
			if detail:
				music_name = detail[0].music_name
				artist = detail[0].artist
				album = detail[0].album
				s_details.append({'music_id':k, 'music_name':music_name, 'artist':artist, 'album':album})

		logger.info(s_details)

		ctx['hot_songs'] = s_details

		ctx['user_flag'] = 0
		ctx['user_id'] = 'null'
		ctx['user_name'] = 'null'

		cookie = 'null'

		if 'lxy_cookie' in request.COOKIES:
			user = UserProfileModel.objects.filter(cookie=request.COOKIES['lxy_cookie'])
			if user:
				ctx['user_flag'] = 1
				ctx['user_id'] = user[0].user_id
				ctx['user_name'] = user[0].user_name
				context = RequestContext(request, ctx)
				template = loader.get_template('control/index.html')
				response = HttpResponse(template.render(context))
				return response
			else:
				cookie = datetime.datetime.now().isoformat()
				ctx['user_id'] = hashlib.sha1(cookie.encode('utf-8')).hexdigest()
		else:
			cookie = datetime.datetime.now().isoformat()
			ctx['user_id'] = hashlib.sha1(cookie.encode('utf-8')).hexdigest()

		context = RequestContext(request, ctx)
		template = loader.get_template('control/index.html')
		response = HttpResponse(template.render(context))
		
		if 'lxy_cookie' not in request.COOKIES:
			response.set_cookie('lxy_cookie', cookie)

		return response
	except Exception as e:
		error = traceback.format_exc()
		logger.info(error)
		ctx['err'] = error
		return JsonResponse(ctx)

def play_view(request, music_id):

	ctx = {}
	
	try:
		logger.info('play_view, music_id - %s, started' % music_id)

		if 'lxy_cookie' not in request.COOKIES:
			return HttpResponse('Invalid user, do not have lxy_cookie!')

		cookie = request.COOKIES['lxy_cookie']
		user_id = hashlib.sha1(cookie.encode('utf-8')).hexdigest()

		songs = MusicModel.objects.filter(music_id=music_id)
		if songs:
			ctx['music_name'] = songs[0].music_name
			ctx['artist'] = songs[0].artist
			ctx['album'] = songs[0].album
		else:
			return HttpResponse('Invalid music_id - %s, where do you come from buddy?' % music_id)

		his = UserHistoryModel(music_id=music_id, user_id=user_id)
		his.save()

		context = RequestContext(request, ctx)
		template = loader.get_template('control/play_view.html')
		return HttpResponse(template.render(context))

	except Exception as e:
		error = traceback.format_exc()
		logger.info(error)
		ctx['err'] = error
		return JsonResponse(ctx)


def search_view(request, user_id):

	ctx = {}

	try:
		logger.info('search_view, user_id - %s, started' % user_id)

		ctx['user_id'] = user_id
		context = RequestContext(request, ctx)
		template = loader.get_template('control/search.html')
		return HttpResponse(template.render(context))

	except Exception as e:
		error = traceback.format_exc()
		logger.info(error)
		ctx['err'] = error
		return JsonResponse(ctx)


def search_data(request, keyword):

	ctx = {}

	try:
		logger.info('search_data, keyword - %s, started' % keyword)

		dat = MusicModel.objects.filter()

		ctx['songs'] = []
		ctx['artists'] = []
		ctx['albums'] = []

		art_tmp = []
		alb_tmp = []

		for each in dat:
			detail = {}
			detail['music_id'] = each.music_id
			detail['artist'] = each.artist
			detail['album'] = each.album
			detail['music_name'] = each.music_name

			if keyword in each.music_name:
				ctx['songs'].append(detail)
			if keyword in each.artist:
				if each.artist not in art_tmp:
					ctx['artists'].append(detail)
					art_tmp.append(each.artist)
			if keyword in each.album:
				if each.album not in alb_tmp:
					ctx['albums'].append(detail)
					alb_tmp.append(each.album)

		ctx['result'] = 'success'

		return JsonResponse(ctx)

	except Exception as e:
		error = traceback.format_exc()
		logger.info(error)
		ctx['result'] = 'failed'
		ctx['err'] = error
		return JsonResponse(ctx)

def register_handler(request, user_name, user_pass):

	ctx = {}

	try:
		logger.info('register_handler, user_name - %s, user_pass - %s, started' % (user_name, user_pass))

		users = UserProfileModel.objects.filter(user_name=user_name)

		if users:
			ctx['result'] = 'repeat'
			return JsonResponse(ctx)

		ctx['result'] = 'success'
		response = JsonResponse(ctx)

		if 'lxy_cookie' in request.COOKIES:
			cookie = request.COOKIES['lxy_cookie']
		else:
			now = datetime.datetime.now().isoformat()
			cookie = now
			response.set_cookie('lxy_cookie', cookie)

		user_id = hashlib.sha1(cookie.encode('utf-8')).hexdigest()
		new_user = UserProfileModel(user_name=user_name, cookie=cookie, user_id = user_id, user_pass=user_pass)
		new_user.save()

		return response

	except Exception as e:
		error = traceback.format_exc()
		logger.info(error)
		ctx['result'] = 'failed'
		ctx['err'] = error
		return JsonResponse(ctx)

def register_view(request):

	ctx = {}

	try:
		logger.info('register_view, started')

		context = RequestContext(request, ctx)
		template = loader.get_template('control/register.html')
		return HttpResponse(template.render(context))

	except Exception as e:
		error = traceback.format_exc()
		logger.info(error)
		ctx['result'] = 'failed'
		ctx['err'] = error
		return JsonResponse(ctx)

def history_view(request, user_id):

	ctx = {}

	try:
		logger.info('history_view, user_id - %s, started' % user_id)

		his_songs = []

		his = UserHistoryModel.objects.filter(user_id=user_id).order_by('-time_created')
		for each in his:
			music_id = each.music_id

			detail = MusicModel.objects.filter(music_id=music_id)
			music_name = detail[0].music_name
			artist = detail[0].artist
			album = detail[0].album

			his_songs.append({'music_id':music_id, 'music_name':music_name, 'artist':artist, 'album':album})

		ctx['result']= ' success'
		ctx['his_songs'] = his_songs
		ctx['user_id'] = user_id

		context = RequestContext(request, ctx)
		template = loader.get_template('control/history.html')
		return HttpResponse(template.render(context))

	except Exception as e:
		error = traceback.format_exc()
		logger.info(error)
		ctx['result'] = 'failed'
		ctx['err'] = error
		return JsonResponse(ctx)

def recommend_view(request, user_id):

	ctx = {}

	try:
		logger.info('recommend_view, user_id - %s' % user_id)

		rs = get_recommend(user_id)
		if rs['result'] != 'success':
			ctx['result'] = 'get_recommend got error!'
			return JsonResponse(ctx)

		songs = rs['rec_songs']
		tags = ''
		for each in rs['rec_tags']:
			tags += '"' + each + '" '

		rec_songs = []

		logger.info(songs)
		for i in songs:
			detail = MusicModel.objects.filter(music_id=i)
			music_name = detail[0].music_name
			artist = detail[0].artist
			album = detail[0].album

			rec_songs.append({'music_id':i, 'music_name':music_name, 'artist':artist, 'album':album})

		ctx['result'] = 'success'
		ctx['rec_songs'] = rec_songs
		ctx['rec_tags'] = tags
		ctx['user_id'] = user_id

		ctx['user_flag'] = 0
		ctx['user_name'] = 'null'

		user = UserProfileModel.objects.filter(user_id=user_id)
		if user:
			ctx['user_flag'] = 1
			ctx['user_name'] = user[0].user_name

		context = RequestContext(request, ctx)
		template = loader.get_template('control/recommend.html')
		return HttpResponse(template.render(context))

	except Exception as e:
		error = traceback.format_exc()
		logger.info(error)
		ctx['result'] = 'failed'
		ctx['err'] = error
		return JsonResponse(ctx)
