from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  'apiKey': "AIzaSyCFTfTzH9LvizSjlAJNg3u13wb4SZ1hpxM",
  'authDomain': "project-8f3a9.firebaseapp.com",
  'databaseURL': "https://project-8f3a9-default-rtdb.firebaseio.com",
  'projectId': "project-8f3a9",
  'storageBucket': "project-8f3a9.appspot.com",
  'messagingSenderId': "947227924003",
  'appId': "1:947227924003:web:24440249868f28039f8396",
  'measurementId': "G-JKWKYDTNZ7",
  "databaseURL":"https://project-8f3a9-default-rtdb.firebaseio.com/"
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
            return redirect(url_for('add_note'))
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
            return render_template('newnote.html')
        except:
            error = "Authentication failed"
            print(error)
    return render_template("signup.html")


@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if request.method =="POST":
        title = request.form["Title"]
        text = request.form["Text"]
        Note = {'Title':title ,"Text":text ,"UID":login_session['user']['localId']}
        try:
            db.child('Notes').push(Note)
        except:
            print('error')
    return render_template("newnote.html")

@app.route("/all_notes")
def all_notes():
    notes = db.child('Notes').get().val()
    return render_template("notes.html" ,notes = notes)



if __name__ == '__main__':
    app.run(debug=True)