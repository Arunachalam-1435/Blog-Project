# importing libraries
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from sqlalchemy import select
from flask_migrate import Migrate
from models import db, Posts
from dotenv import load_dotenv
from datetime import timezone
from zoneinfo import ZoneInfo
import os, markdown, textwrap

# initialising necessary components
load_dotenv('config.env')
app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')
app.secret_key = os.environ.get('SECRET_KEY')
PASSWORD_HASH = os.environ.get('PASSWORD_HASH')
if not app.secret_key or not PASSWORD_HASH:
    raise RuntimeError("SECRET_KEY and PASSWORD_HASH must be set in config.env")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False
db.init_app(app)
migrate = Migrate(app, db)
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=[]
)

# custom filter for timezone conversion
@app.template_filter('local_timezone')
def local_timezone(dt, tz_name='Asia/Kolkata'):
    if not dt:
        return ''
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    local_dt = dt.astimezone(ZoneInfo(tz_name))
    return local_dt.strftime('%Y-%m-%d %H:%M')

# custom filter for markdown to html conversion
@app.template_filter('markdown')
def markdown_to_html(md):
    md_html = textwrap.dedent(md).strip()
    md_html = markdown.markdown(md_html)
    return md_html

@app.route('/')
def main():
    all_posts = db.session.execute(select(Posts)).scalars().all()
    return render_template('index.html', heading="Welcome all!", all_posts=all_posts)

@app.route('/post', methods=['GET', 'POST'])
def post():
    if not session.get('logged_in'):
        return redirect(url_for('main'))
    if request.method == "POST":
        topic = request.form.get('topic')
        content = request.form.get('body')
        new_post = Posts(title = topic, body = content)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('main', msg='Post created Successfully'))
    return render_template('create_post.html', heading='Create a Post')

@app.route('/post/<int:id>')
def show_post(id):
    post_content = db.session.get(Posts, id)
    if post_content:
        return render_template('post.html', post_content=post_content)
    else:
        return redirect(url_for('main', msg="Post doesn't exist"))

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("3 per hour", methods=['POST'], deduct_when=lambda res: res.status_code != 302)
def login():
    if request.method == 'GET':
        if session.get('logged_in'):
            return redirect(url_for('post'))
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and check_password_hash(PASSWORD_HASH, password):
            session.clear()
            session['logged_in'] = True
            session['username'] = 'Admin'
            return redirect(url_for('post'))
        return render_template('login.html', error="Invalid credentials"), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('main'))

if __name__ == "__main__":
    app.run(debug=True)