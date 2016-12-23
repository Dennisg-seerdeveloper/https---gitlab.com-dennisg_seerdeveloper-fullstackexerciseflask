from flask import Blueprint
from flask import render_template
from flask import g
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import session
from bson.objectid import ObjectId

mod = Blueprint('posts', __name__)

@mod.route('/')
def post_list():
    #myfunc = g.emoticonsdb.getEmoticons()
	posts = g.postsdb.getPosts(session['username'])
    #select_emoticons_cpe = g.emoticonsdb.getEmoticons("5859fe2e19468902936724b8")
	complete_cpe = []

	cpe_com = "aaa"
	cpe = {}

	for combine_post_emoticon in posts:
		
		cpe = g.emoticonsdb.getEmoticons(str(combine_post_emoticon["_id"]))

		cpe_com = cpe["emoticon"]

		complete_cpe.append({"_id" : combine_post_emoticon["_id"], 
    						"username" : combine_post_emoticon["username"], 
    						"post" : combine_post_emoticon["post"], 
    						"emoticon" : cpe_com
    						})

    
    	select_emoticons = [{'Name': 'SMILING FACE', 'Code': "&#128512;"},
    					{'Name': 'CRYING FACE', 'Code': '&#128546;'}, 
    					{'Name': 'CONFUSED FACE', 'Code': '&#128533;'}, {'Name': 'SLEEPY FACE', 'Code': '&#128554;'}, {'Name': 'ANGRY FACE', 'Code': '&#128544;'}]

	return render_template('posts/post.html', posts=complete_cpe,
												date='December 21 2016',	
												select_emoticons=select_emoticons)

@mod.route('/', methods=['POST'])
def create_post():
	new_post = request.form['new_post']
	postid = g.postsdb.createPost(new_post, session['username'])
	emoticonparam = ""
	g.emoticonsdb.createEmoticon(emoticonparam, str(postid))

	flash('New post created!', 'create_post_success')
	return redirect(url_for('.post_list'))

@mod.route('/create_emoticon', methods=['POST'])
def create_emoticon():
	emoticon = request.form['post_emoticon']
	post_id = request.form['post_id']
	g.emoticonsdb.updateEmoticon(emoticon, post_id)
	flash('New Emoticon created to the Post.', 'create_emoticon_success')
	return redirect(url_for('.post_list'))

@mod.route('/delete_post', methods=['POST'])
def delete_post():
	post_id = request.form['post_id']

	g.postsdb.deletePost(post_id)
	g.emoticonsdb.deleteEmoticon(post_id)

	flash('Post Deleted.', 'delete_success')
	return redirect(url_for('.post_list'))



