from flask import Flask
from flask import g

from modules import default
from modules import posts
from modules import util

from pymongo import MongoClient

app = Flask(__name__)

app.session_interface = util.MongoSessionInterface(db='sessions')

def get_main_db():
    client = MongoClient('mongodb://localhost:27017/')
    maindb = client.postsdb
    return maindb

@app.before_request
def before_request():
    mainDb = get_main_db()
    g.usersdb = posts.UserDB(conn=mainDb.users)
    g.postsdb = posts.PostDB(conn=mainDb.posts)
    g.emoticonsdb = posts.EmoticonDB(conn=mainDb.emoticons)


@app.teardown_request
def teardown_request(exception):
    postdb = getattr(g, 'postdb', None)
    if postdb is not None:
        postdb.close()
    userdb = getattr(g, 'userdb', None)
    if userdb is not None:
        userdb.close()
    emoticondb = getattr(g, 'emoticondb', None)
    if emoticondb is not None:
        emoticondb.close()

app.register_blueprint(default.mod)
app.register_blueprint(posts.mod, url_prefix="/posts")