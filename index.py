from flask import Flask, render_template, url_for

app = Flask(__name__)

class User:
    def __init__(self):
        self.nric = 99999
        self.name = "james"
        self.birth = "1/1/1998"
        self.sex = "Male"
        self.country = "Singapore"
        self.nationality = "Singaporean"
    
    def getNRIC(self):
        return self.nric 

    def getName(self):
        return self.name

    def getDateofBirth(self):
        return self.birth

    def getSex(self):
        return self.sex

    def getCountryOfBirth(self):
        return self.country

    def getNationality(self):
        return self.nationality

@app.route('/')
def getMain():
    user = User()
    return render_template('index.html',
                        nric = user.getNRIC(),
                        name = user.getName(),
                        birth = user.getDateofBirth(),
                        sex = user.getSex(),
                        country = user.getCountryOfBirth(),
                        nationality = user.getNationality())
