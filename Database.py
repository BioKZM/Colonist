
class Database():

   def __init__(self, remote=True):
        self.remote = remote
        self.__connectDatabase()
        locale.setlocale(locale.LC_ALL, '')
    
    def __connectDatabase(self):
        """
            Veri Tabanı bağlantısını yapmamızı sağlar.
        """
        if self.remote:
            self.connect = pymysql.connect(host="89.252.183....",user="",passwd="",database="" )
        else:
            self.connect = sqlite3.connect(os.getcwd() + "\\mirket.db") # sqlLite3 ile db dosyamızı seçmemizi sağlar
        self.cursor = self.connect.cursor()
        self.connect.commit()

    # warning set user just one time 
    def _setUser(self, dcId:int, point:int, guide:str):
        guide = guide.replace("'","''")
        self.cursor.execute(f"INSERT INTO users (dcId,point, guide) VALUES('{dcId}', '{point}', '{guide}')")
        self.connect.commit()
    
    def addUser(self, dcId:int, point:int, guide:str):
        if not self.isUserExist(dcId):
            guide = guide.replace("'","''")
            self.cursor.execute(f"INSERT INTO users (dcId,point, guide) VALUES('{dcId}', '{point}', '{guide}')")
            self.connect.commit()
        else:
            print("Kullanıcı zaten eklendi")
    
    def isUserExist(self, dcId:int):
        self.cursor.execute(f"SELECT EXISTS(SELECT * FROM users WHERE dcId='{dcId}')")
        return self.cursor.fetchone()[0]
            
        
    def deleteUser(self, dcId:int):
        self.cursor.execute(f"DELETE FROM users WHERE dcId={dcId}")
        self.connect.commit()
    
    def updateGuide(self, dcId:int, guide:str):
        self.cursor.execute("UPDATE users SET guide=? WHERE dcId=?", (guide,dcId))
        self.connect.commit()

    def updatePoint(self, dcId:int, point:int):
        self.cursor.execute(f"UPDATE users SET point = {point}  WHERE dcId={dcId}")
        self.connect.commit()

    def showUser(self, dcId:int):
        if self.isUserExist(dcId):
            self.cursor.execute(f"SELECT dcId, point, guide, activeChallengeName, challenges, notification FROM users WHERE dcId='{dcId}'")
            users = self.cursor.fetchall()
            self.connect.commit()
            return users[0]

    def showAll(self):
        self.cursor.execute(f"SELECT * FROM users")
        users = self.cursor.fetchall()
        self.connect.commit()
        return users

    def showAllPoints(self):
        self.cursor.execute(f"SELECT point,dcId FROM users")
        points = self.cursor.fetchall()
        self.connect.commit()
        return points

    def showAllGuides(self):
        self.cursor.execute(f"SELECT dcId,guide FROM users")
        guides = self.cursor.fetchall()
        self.connect.commit()
        return guides
    