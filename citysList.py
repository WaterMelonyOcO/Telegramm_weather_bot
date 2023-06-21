import json
from utils import *

class citysList:
    
    def __init__(self) -> None:
        try:
            with open('db.json', 'r') as db:
                if ( db ):
                    return
        except:
            print('[ERR] reas db errror INIT')
            with open('db.json', 'a') as db:
                db.write(json.dumps({}))
    
    def addCity(self, city: str) -> list:
        db = self.readData()
        err = []
        
        if ( len(city) == 0):
            err.append("вы не ввели город")
            return err
  
        cityData = getCityData(city) 
        if ( cityData == None):
            err.append("такого города нету")
            return err
        
        if ( cityData[1] in db):
            err.append("этот город уже добавлен")
            return err

        db[cityData[1]] = {'coord': cityData[0], 'isDefault': False}
        self.writeData(db)
        return err
    
    def delCity(self, city: str) -> list:
        db = self.readData()
        err = []
        
        if ( city not in db ):
            err.append("такого города нету в списке")
            return err
        
        del db[city]
        self.writeData(db)
        return err
        
    
    def setdefault(self, city: str):
        db = self.readData()
        errs = []
        
        if ( city not in db ):
            errs.append("такого города нету у вас в списке")
            return errs
        
        for i in db:
            if ( db[i]['isDefault'] == True ):
                db[i]['isDefault'] = False
        
        db[city]['isDefault'] = True
        self.writeData(db)
        return
    
    def getDefaultCity(self) -> dict:
        db = self.readData()
        for i in db:
            if ( db[i]['isDefault'] == True ):
                return (i, db[i]['coord'])
    
    def getSaveCitys(self) -> list:
        db = self.readData()
        citys = []  
        
        if ( len(db.items()) <= 0):
            return None
        
        for i in db:
            citys.append(i)
        
        return citys
    
    def writeData(self, data):
        with open('db.json', 'w') as db:
            db.write(json.dumps(data))
    
    def readData(self) -> dict:
        with open('db.json', 'r') as db:
            return json.loads(db.read())