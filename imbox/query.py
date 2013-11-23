def build_search_query(unread=False, sent_from=False, sent_to=False,
                       date__gt=False, date__lt=False, **kwargs):
	"""
	todo: make sure no other arguments
	      are ever haphazardly passed into build_search_query
	      and remove **kwargs

	"""
	query = "(ALL)"

	if unread != False:
		query = "(UNSEEN)"

	if sent_from:
		query = '{0} (FROM "{1}")'.format(query, sent_from)

	if sent_to:
		query = '{0} (TO "{1}")'.format(query, sent_to)

	if date__gt:
		query = '{0} (SINCE "{1}")'.format(query, date__gt)

	if date__lt:
		query = '{0} (BEFORE "{1}")'.format(query, date__lt)

	return str(query)
