from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
   #declare object definition
    __tablename__ = "users"
    #define column name and its type/constraint
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, unique = True,nullable = False)
    messages = db.relationship('Message', backref='user', lazy=True)

    @staticmethod
    def createUser(username):
        u = User(username = username)
        db.session.add(u)
        db.session.commit()
        return u

    @staticmethod
    def getUserByName(name):
        u = User.query.filter(User.username == name).first()
        return u

    @staticmethod
    def getUserByID(user_id):
        u = User.query.filter(User.id == user_id).first()
        return u
    
    def joinChannel(self, channel_id):
        m = Membership(user_id = self.id, channel_id = channel_id)
        db.session.add(m)
        db.session.commit()

    def createChannel(self, ch_name):
        c = Channel(channel_name = ch_name)
        db.session.add(c)
        db.session.commit()

    def giveMessageToChannel(self, channel_id, message):
        m = Message(user_id = self.id, channel_id = channel_id, text = message)
        db.session.add(m)
        db.session.commit()

class Channel(db.Model):
    __tablename__ = "channels"
    id = db.Column(db.Integer, primary_key = True)
    channel_name = db.Column(db.String, unique = True, nullable = False)
    
    @staticmethod
    def getChannelByID(search_channel_id):
        c = Channel.query.filter(Channel.id == search_channel_id).first()
        return c

    @staticmethod
    def getChannelByName(name):
        c = Channel.query.filter(Channel.channel_name == name).first()
        return c

    def getLastNumberMessages(self, n):
        messages = Message.query.filter(Message.channel_id == self.id).order_by(Message.id.desc()).limit(n).order_by(Message.id.asc())
        return messages


class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key = True)    
    text = db.Column(db.String, nullable = False)
    times = db.Column(db.DateTime, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    channel_id = db.Column(db.Integer, db.ForeignKey("channels.id"), nullable = False)