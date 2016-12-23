class EmoticonDB:
	def __init__(self, conn):
		self.conn = conn

	def getEmoticons(self, post_id):
		return self.conn.find_one({'post_id': post_id})

	def createEmoticon(self, emoticon, post_id):
		self.conn.insert({'emoticon':emoticon, 'post_id': post_id})

	def updateEmoticon(self, emoticon, post_id):
		self.conn.update_one({'post_id': post_id}, { "$set": {'emoticon':emoticon}})

	def deleteEmoticon(self, ids):
		self.conn.delete_one({'post_id': ids})
