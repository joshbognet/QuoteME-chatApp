import os
import time
from flask import Flask, render_template, request, url_for, redirect,flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from forms import RegistrationForm, LoginForm
from passlib.hash import pbkdf2_sha256
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from flask_socketio import SocketIO, join_room, leave_room, send, emit


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

app.config['SECRET_KEY']= '28c1521753f8826032a89da21c5720cd'

db=SQLAlchemy(app)
socketio = SocketIO(app)
# Predefined rooms for chat
ROOMS = ["lounge", "news", "games", "coding"]

login = LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    
    
    def __repr__(self):
        return f'<student {self.username}>'

# @app.route('/')
# @app.route('/home')
# def index():
#     return render_template('home.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    reg_form = RegistrationForm()
   
    #update database if if validation passess
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        email = reg_form.email.data
        password =reg_form.password.data
        
        # hash password
        hash_pswd = pbkdf2_sha256.hash(password)
        
        #Add user to Db
        new_user = User(username=username,email=email, password=hash_pswd) 
        db.session.add(new_user)
        db.session.commit()
        flash('Registered Successfully. Please Login!', 'success')
        return redirect(url_for('Login'))  
    
    return render_template('register.html',form=reg_form)

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def Login():
    
    # instanciate login
    login_form=LoginForm()
    
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for("chat"))
    return render_template('login.html', form=login_form)

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if not current_user.is_authenticated:
        flash('Please login.', 'danger')
        return redirect(url_for("Login"))
    return render_template('chat.html', username=current_user.username, rooms=ROOMS)

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash('You have logged out successfully!', 'success')
    return redirect(url_for("Login"))



# @socketio.on('incoming-msg')
# def on_message(data):
#     """Broadcast messages"""

#     msg = data["msg"]
#     username = data["username"]
#     room = data["room"]
#     # Set timestamp
#     time_stamp = time.strftime('%b-%d %I:%M%p', time.localtime())
#     send({"username": username, "msg": msg, "time_stamp": time_stamp}, room=room)
    
    

# @socketio.on('join')
# def on_join(data):
#     """User joins a room"""

#     username = data["username"]
#     room = data["room"]
#     join_room(room)

#     # Broadcast that new user has joined
#     send({"msg": username + " has joined the " + room + " room."}, room=room)
    
    
# @socketio.on('leave')
# def on_leave(data):
#     """User leaves a room"""

#     username = data['username']
#     room = data['room']
#     leave_room(room)
#     send({"msg": username + " has left the room"}, room=room)



@socketio.on('message')
def message(data):
    print(f'\n\n{data}\n\n')
    send({'msg': data['msg'], "username": data['username'], 
        "time_stamp": time.strftime('%b-%d %I:%M%p', time.localtime())}, room=data["room"])
   

@socketio.on('join')
def on_join(data):
    """User joins a room"""
    
    join_room(data["room"])
    
    # Broadcast that new user has joined
    send({'msg': data['username'] + " has joined the " + data["room"] + " room." }, room=data["room"])
    
@socketio.on('leave')
def on_leave(data):
    """User leaves a room"""

    leave_room(data["room"])
    send({'msg': data['username'] + " has left the room" + data["room"] + " room." }, room=data["room"])

if __name__ =="__main__":
    socketio.run(app, debug=True)