import os

from flask import Flask, render_template, request, session, jsonify, redirect, url_for
from flask_session import Session
from flask_socketio import SocketIO, emit
from models import *
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

app = Flask(__name__)

#import developer key from .env file into environment variable
#load_dotenv(verbose=True)
#env_path = Path('.') / '.env'
#load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv('DATABASE_URL')

#raise error message if DATABASE_URL cannot be found in environment variable
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

#tell flask sqlAlchemy where that database is
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['DEBUG'] = True
Session(app)

#link the database to flask application
db.init_app(app) 

#point socket io to application
socketio = SocketIO(app)

@app.route("/login")
def login():
    '''
    return login form to visitor
    '''
    return render_template('login.html')

@app.route("/validate_user", methods = ['POST'])
def validateUser():
    '''
    retrieve username from login form and redirect user to channel list if user is validated.
    @username can be mixture of uppercase, lowercase and 
    '''
    #get user name from User model
    username = request.form.get("username")
    user = User.getUserByName(username)
    #if user does not exist in User model
    if not user:
        #create a new user
        user = User.createUser(username)
    #load user information to Flask session
    session["username"] = user.username
    session["user_id"] = user.id
    #redirect user to list of channel
    return redirect(url_for('channelList'))

@app.route("/logout")
def logout():
    '''
    if user logout, remove user's session at Flask file system.
    '''
    session.pop('username', None)
    return render_template('logout.html')

@app.route("/list", methods = ["POST", "GET"])
def channelList():
    '''
    a view that display channels
    '''
    #if user want to create channel
    if request.method == "POST":
        if request.form.get("channel_name"):
            #get user from User model according to username; if user does not login, return error message
            user = User.getUserByName(session["username"])
            if user == None:
                error_message = "user has not login"
                return render_template("error.html", error_message = error_message)
            #if user login, create the channel according to submitted channel name
            channel_name = request.form.get("channel_name")
            user.createChannel(channel_name)
    #setup a list of channels and username for template rendering
    username = session.get("username")
    channels = Channel.query.all()
    return render_template("channel_list.html", username = username, channels = channels)

@app.route("/channel/<string:channel_name>")
def channel(channel_name):
    '''
    show all the messages that are in corresponding channel
    
    need to store channel id in session. Whenever user want to post a message, 
    message will be saved at right channel according to channel id in session
    '''
    channel = Channel.getChannelByName(channel_name)
    session["channel_id"] = channel.id
    return render_template("channel.html", 
                            channel = channel, 
                            username = session["username"])

@app.route("/post", methods = ["POST"])
def post():
    start = int(request.form.get("start"))
    amount = int(request.form.get("amount"))
    channel_id = session['channel_id']
    messages = Message.query.join(User).filter(Message.channel_id == channel_id).order_by(Message.times.desc())[start:start+amount]
    #query a range of message by specifying start and end; return messages
    data = []
    for message in messages:
        message_time = message.times.strftime('%I:%M:%S at %m/%d')
        data.append({
            "message" : message.text, 
            "username" : message.user.username, 
            "times" : message_time
        })

    return jsonify(data)

@socketio.on("send message")
def sendMessage(data):
    #setup information that is relevant to message
    user_id = session["user_id"]
    channel_id = session['channel_id']
    message = data["message"]
    username = session["username"]
    now_time = datetime.now(tz = None)
    
    #write message to database
    m = Message(
            user_id = user_id,
            channel_id = channel_id,
            text = message, 
            times = now_time
        )
    db.session.add(m)
    db.session.commit()
    #prepare format of time in terms of hour:minute:secoond at month/day
    message_time = now_time.strftime('%I:%M:%S at %m/%d')
    
    #broadcast it to all the browsers
    emit(
        "broadcast message",
        {
            "message" : m.text, 
            "username" : m.user.username, 
            "times" : message_time, 
            "is_sent" : True
        },
        broadcast = True
    )


if __name__ == '__main__':
    socketio.run(app)