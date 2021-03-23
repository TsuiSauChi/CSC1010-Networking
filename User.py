class User():
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