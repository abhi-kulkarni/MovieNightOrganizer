from app import db
import datetime
import json
import decimal

class Friend(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    firstname=db.Column(db.String(100),nullable=False)
    lastname=db.Column(db.String(100),nullable=False)
    children = db.relationship('MovieList', backref='parent', passive_deletes=True)

    def to_dict(self):
        fields = {}
        for field in [x for x in dir(self) if not x.startswith("_") and x != 'metadata']:
            data = self.__getattribute__(field)
            if type(data) is datetime.datetime:
                data = data.strftime('%Y-%m-%dT%H:%M:%SZ')
            if type(data) is datetime.date:
                data = data.strftime('%Y-%m-%d')
            if not hasattr(data, '__call__'):
                try:
                    json.dumps(data)
                    if field[-4:] == "List" and type(data) is not list:
                        fields[field] = [x for x in data.split(",") if x.strip() != ""]
                    else:
                        fields[field] = data
                except TypeError:
                    if type(data) is decimal.Decimal:
                        fields[field] = float(data)
                    else:
                        fields[field] = None
        return fields


class MovieList(db.Model):

    id=db.Column(db.Integer,primary_key=True)
    friendid = db.Column(db.Integer, db.ForeignKey('friend.id', ondelete='CASCADE'))
    movie1 = db.Column(db.String(100),nullable=True)
    movie2 = db.Column(db.String(100),nullable=True)
    movie3 = db.Column(db.String(100),nullable=True)
    movie4 = db.Column(db.String(100),nullable=True)
    movie5 = db.Column(db.String(100),nullable=True)
    movie6 = db.Column(db.String(100),nullable=True)
    movie7 = db.Column(db.String(100),nullable=True)
    movie8 = db.Column(db.String(100),nullable=True)
    movie9 = db.Column(db.String(100),nullable=True)
    movie10 = db.Column(db.String(100),nullable=True)

    def to_dict(self):
        fields = {}
        for field in [x for x in dir(self) if not x.startswith("_") and x != 'metadata']:
            data = self.__getattribute__(field)
            if type(data) is datetime.datetime:
                data = data.strftime('%Y-%m-%dT%H:%M:%SZ')
            if type(data) is datetime.date:
                data = data.strftime('%Y-%m-%d')
            if not hasattr(data, '__call__'):
                try:
                    json.dumps(data)
                    if field[-4:] == "List" and type(data) is not list:
                        fields[field] = [x for x in data.split(",") if x.strip() != ""]
                    else:
                        fields[field] = data
                except TypeError:
                    if type(data) is decimal.Decimal:
                        fields[field] = float(data)
                    else:
                        fields[field] = None
        return fields