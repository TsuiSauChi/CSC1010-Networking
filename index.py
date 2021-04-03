from flask import Flask, render_template, url_for, redirect, request
from login import ContactForm
from dbcommunicate import db
import fileclient

app = Flask(__name__)
app.config["SECRET_KEY"] = "123456789"

class User:
    def __init__(self, name):
        print(name)
        self.r = db.search(name)
    
    def getNRIC(self):
        return self.r['id']

    def getName(self):
        return self.r['name']

    def getDateofBirth(self):
        return self.r['dob']

    def getNationality(self):
        return self.r['nationality']

@app.route('/login', methods=["GET", "POST"])
def login():
    form = ContactForm()
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        fileclient.download() # TO RETRIEVE DB FILE
        if db.checkpass(username, password) == True:
            return redirect(url_for("identity", username = username))
        else:
            return redirect(url_for("error"))
    else:
        return render_template(
            "contact.jinja2",
            form=form
        )

@app.route('/identity')
def identity():
    user = User(request.args['username'])
    return render_template('index.html',
                        nric = user.getNRIC(),
                        name = user.getName(),
                        birth = user.getDateofBirth(),
                        nationality = user.getNationality())

@app.route('/error')
def error():
    return render_template('error.html')

