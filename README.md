website: https://message-board-jack.herokuapp.com/login

# Message Board

# Introduction
In modern days, socializing event can be hold not only in reality but also through internet. Message board is a place where people create their anonymous identity, build their own chat channel, and share their thoughts without exposing their real life.

# Description
1. A user can register with a username.
2. After login, user is able to establish chat channel, view a list of channels that has been established by others.
3. Users can enter every channel and leave the message they want. Also, message in history will be loaded as soon as user click in the channel.
4. To incorporate socket.io in Flask in development mode, input "python run.py" at command line.

# Package
see requirements.txt for more details

All developer keys is imported from environment variable by dotenv package. Keys in .env will first be imported to os by dotenv package and ultimately to application.

# Feature
## User
1. At login, a form requires user to enter their username. If the username has been registered before, username will not be created since duplicate username should not exist in the database.
3.	After login, user will be directed channel list. Here, user can build channel with whatever the name they desire. At channel form, user can submit their channel name to backend, where channel name will be registered in database.

## Message
1. At channel, users submit messages to Flask backend. Then messages will be broadcasted to everyone in the channel by socket. Socket is a engine that enable fast and realtime communication between users on the same application. User in one end will receive new messages right after messages are sent from the other end, and application does not have to worry about competing messages.
5. Ajax is used to optimize user's experiences. we don't want to reload user's browser everytime user only asks for minimal changes in page while every other content remains the same. With Ajax, user's browser sends a request to server behind the scene and update its content when browser receives response from server. This way, user's experiences will not be interrupted by constant reloading.
9. User can type in new mesage at the top of the page. When a user types in a message, that message will be inserted at the front row in the page. The messages in the channel are sorted by time in the descending order. By adding message at the front, user can see immediate feedback at the front row without scrolling to the bottom.
10. Behind the scene, new message will be inserted into Heroku's Postgre database. To display chat history, application queries from database messages that correspond to particular channel. However, loading large amount of history will slow down if not even crash our application. To address this issue, a infinite scroll feature is introduced. Infinite scrolling enables our application to load past message when it is necessary to do so.
6. Infinite scroll is achieved by javascript. javascript will measure the edge of page and how much user scrolls. With both parameters, javascript will reload the pages as user has scrolled the page beyond its edge.
7. Card component from bootstrap styles a list of messages in one channel. With card components from bootstrap, user is able to read username, content of message, and time clearly. Moreover, margin is added so that cards that are close to one another will not pressure user's perception
8. Message form is fixed on top of the page when page is scrolled by user. User can type in new message while viewing messages in the past with ease.


## Database and Models
1. Heroku Postgres is used as database. All usernames, channel, messages be will saved here. All the database manipulation is done by SQLAlchemy.
2. Three Models are defined in database: Message, User, Channel
  - messages can be created by many users.
  - messages can be in many channels.
  - message has the fields of user, time of message creation, and content of messages.
  - channel can be created by users.
  - channel has the fields of name
  - user has the fields of name

# Demo
[video demo](https://www.youtube.com/watch?v=UWFfCOb_I-4&feature=youtu.be)

![login](/demo/login.jpg)
![channel list](/demo/channel-list.jpg)
![channel before prepend](/demo/channel-before-prepend.jpg)
![channel before prepend](/demo/channel-after-prepend.jpg)
![logout](/demo/logout.jpg)

