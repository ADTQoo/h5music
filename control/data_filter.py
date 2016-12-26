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

def 
