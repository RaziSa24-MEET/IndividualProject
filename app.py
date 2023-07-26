from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  'apiKey': "AIzaSyAffFgoB-Wk84ExHBGVHmSYJPTYi7s8G-I",
  'authDomain': "lastlabs-b49bc.firebaseapp.com",
  'databaseURL': "https://lastlabs-b49bc-default-rtdb.firebaseio.com",
  'projectId': "lastlabs-b49bc",
  'storageBucket': "lastlabs-b49bc.appspot.com",
  'messagingSenderId': "648347968330",
  'appId': "1:648347968330:web:c31cd94e06233641dc97b3",
  'measurementId': "G-LFKYFJMW7B",
  "databaseURL":"https://lastlabs-b49bc-default-rtdb.firebaseio.com/"
}


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        fullname = request.form['fullname']
        bio = request.form['bio']
        username = request.form['username']
        user = {"email":email ,"password":password ,"fullname":fullname ,"bio":bio ,"username":username}
    
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            uid = login_session['user']['localId']
            db.child("Users").child(uid).set(user)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
            print(error)
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method =="POST":
        title = request.form["Title"]
        text = request.form["Text"]
        Tweet = {'Title':title ,"Text":text ,"UID":login_session['user']['localId']}
        try:
            db.child('Tweet').push(Tweet)
        except:
            print('error')

    return render_template("add_tweet.html")

@app.route("/all_tweets")
def all_tweets():
    tweets = db.child('Tweet').get().val()
    return render_template("tweets.html" ,tweets = tweets)



if __name__ == '__main__':
    app.run(debug=True)