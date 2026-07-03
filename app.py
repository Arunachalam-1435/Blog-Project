from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import select
from flask_migrate import Migrate
from models import db, Posts
from dotenv import load_dotenv
from datetime import timezone
from zoneinfo import ZoneInfo
import os

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')
load_dotenv('config.env')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

# custom filter for timezone conversion
@app.template_filter('local_timezone')
def local_timezone(dt, tz_name='Asia/Kolkata'):
    if not dt:
        return ''
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    local_dt = dt.astimezone(ZoneInfo(tz_name))
    return local_dt.strftime('%Y-%m-%d %H:%M')

@app.route('/')
def main():
    all_posts = db.session.execute(select(Posts)).scalars().all()
    if not all_posts:
        all_posts = ""
    return render_template('index.html', heading="Welcome all!", all_posts=all_posts)

@app.route('/post', methods=['GET', 'POST', 'DELETE'])
def post():
    if request.method == "POST":
        topic = request.form.get('topic')
        content = request.form.get('body')
        new_post = Posts(title = topic, body = content)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('main', msg='Post created Successfully'))
    elif request.method == "DELETE":
        row = db.session.get(Posts, 1)
        db.session.delete(row)
        db.session.commit()
        return "Post deleted successfully"
    return render_template('post.html', heading='Create a Post')

if __name__ == "__main__":
    app.run()