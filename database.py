import os

from flask import Flask, render_template, request, session
#from flask_socketio import SocketIO, emit
from models import *

from datetime import datetime, timedelta

from settings import DATABASE_URL

app = Flask(__name__)


#tell flask sqlAlchemy where that database is
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#link the database to flask application
db.init_app(app) 

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config['DEBUG'] = True

#postgres://cylikbqqbipbff:7b413088713156b728df001d7a4157deabab9f922061f80c73b10ccd27283ec2@ec2-174-129-253-146.compute-1.amazonaws.com:5432/d5k1ibv8ga50gh
def mock_datetime():
    d = datetime.now(tz = None)
    for i in range(10):
        #new_d = d - timedelta(days = i)
        new_d = d - timedelta(minutes = i)
        print (new_d)

def create_n_mock_message(n):
    d = datetime.now(tz = None)
    for i in range(1, n + 1):
        print(f"create mock message {i}")
        new_d = d - timedelta(minutes = i)
        m = Message(user_id = 1, channel_id = 1, text = str(i), times = new_d)
        db.session.add(m)
    db.session.commit()

def queryForeignTable():
    #u = Message.query.join(User).filter(Message.channel_id == 1).order_by(Message.id.desc()).limit(10).users
    m = Message.query.join(User).filter(Message.channel_id == 1).all()
    return m

def testQueryForeignTalbe():
    messages = queryForeignTable()
    for m in messages:
        print(m.user.username)
def queryUserToMessage():
    u = User.query.first()
    m = u.messages
    return m
def testQueryUserToMessage():
    messages = queryUserToMessage()
    for m in messages:
        print(m.text)

def queryGivenRange():
    start = 0
    amount = 20
    channel_id = 1
    messages = Message.query.join(User).filter(Message.channel_id == channel_id).order_by(Message.times.desc())[start:start+amount]
    #using sql query a range of message obj by specifying start and end; return messages
    return messages

def testQueryGivenRange():
    messages = queryGivenRange()
    for message in messages:
        print(f"{message.text} at {message.times}, index {message.id}")


def main():
    print("===Testing start===")
    #db.create_all()
    #create_n_mock_message(40)
    #db.create_all()
    #testQueryForeignTalbe()
    #testQueryUserToMessage()
    testQueryGivenRange()
    #mock_datetime() 
    
    print("===Process Finished===")

if __name__ == '__main__':
    with app.app_context():
        main()