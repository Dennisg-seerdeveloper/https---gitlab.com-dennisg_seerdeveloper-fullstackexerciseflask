from bson.objectid import ObjectId

class PostDB:
	def __init__(self, conn):
		self.conn = conn

	def getPosts(self, username):
		return self.conn.find({'username': username})

	def createPost(self, post, username):
		post_id = self.conn.insert({'post':post, 'username': username})
		return post_id

	def deletePost(self, ids):
		self.conn.delete_one({'_id': ObjectId(ids)})
