from .models import *

import traceback

import logging
logger = logging.getLogger('ms')

PLAT_HOT_NUM = 10
RECOMMEND_NUM = 10

def get_platform_hot():

	ctx = {}

	try:
		logger.info('get_platform_hot, started')

		songs = UserHistoryModel.objects.filter()

		records = {}
		for each in songs:
			music_id = each.music_id
			if music_id not in records:
				records[music_id] = 1
			else:
				records[music_id] += 1
			
		sort_rd = sorted(records.items(), key=lambda item:item[1], reverse=True)
		
		songs = sort_rd
		if len(sort_rd) > PLAT_HOT_NUM:
			songs = sort_rd[0:PLAT_HOT_NUM-1]

		ctx['result'] = 'success'
		ctx['songs'] = songs
		return ctx

	except Exception as e:
		err = traceback.format_exc()
		logger.info(err)
		ctx['result'] = 'failed'
		ctx['err'] = err
		return ctx

def top_played(in_tag, x):

	ctx = {}

	try:
		logger.info('top_played, in_tag - %s, x - %s, started' % (in_tag, x))

		top_songs = []
		records = {}

		if in_tag == 'platform':
			his = UserHistoryModel.objects.filter()

			for each in his:
				music_id = each.music_id
				if music_id not in records:
					records[music_id] = 1
				else:
					records[music_id] += 1
		else:
			t_songs = MusicTagModel.objects.filter(tag=in_tag)
			
			for each in t_songs:
				music_id = each.music_id
				t_his = UserHistoryModel.objects.filter(music_id=music_id).count()
				if music_id not in records:
					records[music_id] = 1
				else:
					records[music_id] += t_his

		sort_rd = sorted(records.items(), key=lambda item:item[1], reverse=True)
		tmp = sort_rd
		if len(sort_rd) > x:
			tmp = sort_rd[0:x-1]

		for (k, v) in tmp:
			top_songs.append(k)

		ctx['result'] = 'success'
		ctx['top_songs'] = top_songs
		return ctx

	except Exception as e:
		err = traceback.format_exc()
		logger.info(err)
		ctx['result'] = 'failed'
		ctx['err'] = err
		return ctx

def newest_release(date_range, x):

	ctx = {}

	try:
		logger.info('newest_release, date_range - %s, x - %s, start' % (date_range, x))

		news = []
		songs = MusicModel.objects.filter().order_by('-date')

		for each in songs:
			news.append(each.music_id)

		ctx['result'] = 'success'
		ctx['new_songs'] = news
		
		if len(news) > x:
			ctx['new_songs'] = news[0:x-1]

		return ctx

	except Exception as e:
		err = traceback.format_exc()
		logger.info(err)
		ctx['result'] = 'failed'
		ctx['err'] = err
		return ctx

def top_tag(user_id, x):
	try:
		logger.info('top_tag, user_id - %s, started' % user_id)

		his = UserHistoryModel.objects.filter(user_id=user_id)

		records = {}

		for each in his:
			music_id = each.music_id
			tags = MusicTagModel.objects.filter(music_id=music_id)
			logger.info(tags.count())
			for i in tags:
				tag = i.tag
				if tag not in records:
					records[tag] = 1
				else:
					records[tag] += 1
		
		logger.info(records)

		sort_rd = sorted(records.items(), key=lambda item:item[1], reverse=True)
		tags = []
		for (k, v) in sort_rd:
			tags.append(k)

		if x == 1:
			return tags[0]
		else:
			if len(tags) > x:
				return tags[0:x-1]
			else:
				return tags

	except Exception as e:
		err = traceback.format_exc()
		logger.info(err)
		ctx = {}
		ctx['result'] = 'failed'
		ctx['err'] = err
		return ctx

def get_recommend(user_id):

	ctx = {}

	try:
		logger.info('get_recommend, user_id - %s' % user_id)

		his_count = UserHistoryModel.objects.filter(user_id=user_id).count()

		rec_songs = []
		rec_tags = []

		if his_count == 0:
			rec_songs.extend(top_played('platform', RECOMMEND_NUM / 2)['top_songs'])
			rec_songs.extend(newest_release(30, RECOMMEND_NUM / 2)['new_songs'])
			rec_tags.append('最新')
			rec_tags.append('最热')
		elif his_count <= 5:
			tag = top_tag(user_id, 1)
			rec_songs.extend(top_played(tag, RECOMMEND_NUM)['top_songs'])
			rec_tags.append(tag)
		else:
			tags = top_tag(user_id, 3)
			for each in tags:
				rec_songs.extend(top_played(each, 4)['top_songs'])
			rec_tags.extend(tags)

		ctx['result'] = 'success'
		ctx['rec_songs'] = rec_songs
		ctx['rec_tags'] = rec_tags
		return ctx

	except Exception as e:
		err = traceback.format_exc()
		logger.info(err)
		ctx['result'] = 'failed'
		ctx['err'] = err
		return ctx
