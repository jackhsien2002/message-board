import os

from flask import Flask, render_template, request, session, jsonify
from flask_session import Session
from flask_socketio import SocketIO, emit
from models import *
from datetime import datetime

#postgres://cylikbqqbipbff:7b413088713156b728df001d7a4157deabab9f922061f80c73b10ccd27283ec2@ec2-174-129-253-146.compute-1.amazonaws.com:5432/d5k1ibv8ga50gh



app = Flask(__name__)
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

#tell flask sqlAlchemy where that database is
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#link the database to flask application
db.init_app(app) 

#app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config['DEBUG'] = True

socketio = SocketIO(app)

temp_messages = []

@app.route("/")
def index():
    return render_template("name.html")

@app.route("/test")
def testPage():
    return render_template("test.html")

@app.route("/list", methods = ["POST", "GET"])
def channelList():
    if request.method == "POST":
        if request.form.get("channel_name"):
            channel_name = request.form.get("channel_name")
            user = User.getUserByName(session["username"])
            if user == None:
                error_message = "user has not enter name"
                return render_template("error.html", error_message = error_message)
            user.createChannel(channel_name)            
        if request.form.get("username"):
            username = request.form.get("username")
            user = User.getUserByName(username)
            if not user:
                user = User.createUser(username)
            session["username"] = user.username
            session["user_id"] = user.id

    username = session.get("username")
    channels = Channel.query.all()
    return render_template("channel_list.html", username = username, channels = channels)

@app.route("/channel/<string:channel_name>")
def channel(channel_name):
    #user = User.getUserByName(session["username"])
    #display last 5 messages
    channel = Channel.getChannelByName(channel_name)
    messages = Message.query.join(User).filter(Message.channel_id == channel.id).order_by(Message.id.desc()).limit(10)
    session["channel_id"] = channel.id
    #messages = channel.getLastThreeMessages()
    return render_template("channel.html", 
                            channel = channel, 
                            username = session["username"])

@app.route("/post", methods = ["POST"])
def post():
    start = int(request.form.get("start")) - 1
    amount = int(request.form.get("amount"))
    channel_id = int(request.form.get("channel_id"))
    messages = Message.query.join(User).filter(Message.channel_id == channel_id).offset(start).limit(amount)
    #using sql query a range of message obj by specifying start and end; return messages
    data = []
    for message in messages:
        message_time = message.times.strftime('%M:%S at %m/%d')
        data.append({"message" : message.text, "username" : message.user.username, "times" : message_time})
    return jsonify(data)

@socketio.on("send message")
def sendMessage(data):
    user_id = session["user_id"]
    channel_id = session['channel_id']
    message = data["message"]
    username = session["username"]
    now_time = datetime.now(tz = None)

    m = Message(
            user_id = user_id,
            channel_id = channel_id,
            text = message, 
            times = now_time
        )

    db.session.add(m)
    db.session.commit()

    #do something with database
    #broadcast it to all the browsers
    message_time = datetime.now(tz = None).strftime('%M:%S at %m/%d')
    print(m.user.username, m.text, message_time)
    emit("broadcast message",
        {"message" : m.text, "username" : m.user.username, "times" : message_time},
        broadcast = True)


if __name__ == '__main__':
    socketio.run(app)