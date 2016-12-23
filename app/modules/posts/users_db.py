class UserDB:
    def __init__(self, conn):
        self.conn = conn

    def getUser(self, username):
        return self.conn.find({'username':username})

    def getUserWithPassword(self, username, password):
        return self.conn.find({'username':username, 'password': password})

    def createUser(self, username, password):
        self.conn.insert({'username':username, 'password': password})