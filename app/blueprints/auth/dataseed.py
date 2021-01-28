from app import db
from . import models

# ADD SINGLE USER
if db.engine.dialect.has_table(db.engine, 'user'):
    if db.session.query(models.User).count() == 0:
        user = models.User(username='Jack', email='Jackmckeon@live.co.uk')
        user.set_password('notguest')
        user.roles = [db.session.query(models.Role).get(2), ]
        db.session.add(user)
        db.session.commit()
        print("User Entries: " + str(db.session.query(models.User).count()))
