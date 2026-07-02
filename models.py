from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
db=SQLAlchemy()

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.Date, nullable=False, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Post {self.id} {self.title}>"
    
