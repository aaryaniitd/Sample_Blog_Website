from flask import Flask, render_template,request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail
import json
import os
from werkzeug.utils import secure_filename
from slugify import slugify

local_server = True

with open('C:\\Flask Practice\\templates\\config.json', 'r') as c:
	params = json.load(c)["params"]

app = Flask(__name__)
app.secret_key = "super-secret-key"
app.config.update()

if (local_server):
	app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
	app.config['SQLALCHEMY_DATABASE_URI']= params["prod_uri"]   


db = SQLAlchemy(app)

class Contacts(db.Model):    
	name = db.Column(db.String(80),nullable=False)
	email = db.Column(db.String(20),nullable=False)
	phone_num = db.Column(db.String(12),nullable=False)
	message = db.Column(db.String(200),nullable=False)
	date = db.Column(db.String(12),nullable=True)
	sno = db.Column(db.Integer,primary_key=True)

class Posts(db.Model):
	content = db.Column(db.String(500),nullable=False)
	date = db.Column(db.String(12),nullable=True)
	writer = db.Column(db.String(80),nullable=False)
	email = db.Column(db.String(20),nullable=False)
	title = db.Column(db.String(80),nullable=False)
	tagline = db.Column(db.String(80),nullable=False)
	sno = db.Column(db.Integer,primary_key=True)
	slug = db.Column(db.String(20), nullable=False)
	img_file = db.Column(db.String(20), nullable=False)


@app.route("/")
def home():
	posts = Posts.query.filter_by().all()
	if len(posts) <= 5:
		posts = Posts.query.filter_by().all()
	else:	
		posts = Posts.query.filter_by().all()[0:params['no_of_posts']]
	return render_template('index.html',params = params, posts = posts )
   

@app.route("/about")
def about():
	return render_template('about.html',params = params)

@app.route("/contact", methods = ['GET', 'POST'])
def contact():
	if request.method == 'POST':
		'''Add entry to database'''
		name = request.form.get('name')
		phone = request.form.get('phone')
		email = request.form.get('email')
		mes = request.form.get('message')
		entry = Contacts(name = name, email = email, phone_num = phone, message = mes, date = datetime.now())
		db.session.add(entry)
		db.session.commit()
	return render_template('contact.html',params = params)

@app.route("/post/<string:post_slug>", methods = ['GET'])
def post_route(post_slug):
	post = Posts.query.filter_by(slug = post_slug).first()
	return render_template('post.html',params = params, post = post)

@app.route("/login", methods = ['GET', 'POST'])
def login():
	if 'user' in session and session['user'] == params['admin_username']:
		posts = Posts.query.all()
		return render_template('dashboard.html', params = params, posts = posts)

	elif request.method == 'POST':
		username = request.form.get('uname')
		userpass = request.form.get('pass')
		if username == params['admin_username'] and userpass == params['admin_password']:
			#set a session variable
			session['user']= username
			posts = Posts.query.all()
			return render_template('dashboard.html', params = params, posts = posts)
	else:
		return render_template('login.html',params = params)

app.run(debug = True, port = 3000)
