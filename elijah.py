import mysql.connector
import uuid
import random
from datetime import date
import webview
mydb = mysql.connector.connect(host='localhost',user='root',passwd='2005',db='project')
if mydb.is_connected()==True:
    print('Database Established')
    print()
mycursor = mydb.cursor()
    
'''
mycursor.execute('CREATE TABLE QUIZ(QN int,QUESTION varchar(100),OPTA varchar(30),OPTB varchar(30),OPTC varchar(30),OPTD varchar(30),CORRECT varchar(30),CHOSEN char(1))')
mydb.commit()
mycursor.execute("INSERT INTO QUIZ VALUES(1,'What is the tallest mountain in the world?','K2','Everest','Kilimanjaro','Mauna Kea','Everest','N')")
mydb.commit()
mycursor.execute("INSERT INTO QUIZ VALUES(2,'What company was initially known as Blue Ribbon Sports?','Nike','Puma','Reebok','Adidas','Nike','N')")
mydb.commit()
mycursor.execute("INSERT INTO QUIZ VALUES(3,'Which is the only planet in our solar system not named after a Roman or Greek god?','Mercury','Neptune','Earth','Jupiter','Earth','N')")
mydb.commit()
mycursor.execute("INSERT INTO QUIZ VALUES(4,'On what date is Bastille Day celebrated in France?','July 14','March 25','July 4','August 21','July 14','N')")
mydb.commit()
mycursor.execute("INSERT INTO QUIZ VALUES(5,'How many rings is the Olympic symbol made up of?','3','4','5','6','5','N')")
mydb.commit()
mycursor.execute("INSERT INTO QUIZ VALUES(6,'What was the first movie released in the Marvel Cinematic Universe?','Spiderman','Iron Man','Deadpool','Thor','Iron Man','N')")
mydb.commit()
mycursor.execute("INSERT INTO QUIZ VALUES(7,'What is the most streamed song on Spotify?','Shape of You - Ed Sheeran','Blinding Lights - The Weeknd','Dance Monkey - Tones and I','Sunflower - Post Malone','Shape of You - Ed Sheeran','N')")
mydb.commit()
mycursor.execute("INSERT INTO QUIZ VALUES(8,'What is the capital of Iceland?','Helsinki','Reykjavik','Bern','Stockholm','Reykjavik','N')")
mydb.commit()
mycursor.execute("INSERT INTO QUIZ VALUES(9,'How many elements are there in the periodic table?','101','116','121','118','118','N')")
mydb.commit()
mycursor.execute("INSERT INTO QUIZ VALUES(10,'How many time zones are there in Russia?','9','10','11','12','11','N')")
mydb.commit()'''

#mycursor.execute("CREATE TABLE LEADERBOARD(Name varchar(50), Score int, Date date, ID varchar(50) primary key)")

class api():
    global mydb,mycursor,roundc,scorec,pname,cc,colors
    pname=""
    roundc=1
    scorec=0
    colors = ["#E83737","#31CF1B","#3780E8","#B2CA06","#E837E7","#E83737"]
    cc=0

    def connect(self):
        return None

    def play(self,name):
        print("generating question")
        global mydb,mycursor,roundc,cc,colors,pname,scorec
        pname=name
        q=self.question_select()
        roundc=1
        scorec=0
        if q is None: 
            self.resetquestions()
            return{"type": "won","s": scorec}
        else:
            return {"type":"q","q":q,"r":roundc,"c":colors[cc]}

    def question_select(self):
        global mydb,mycursor,roundc,scorec
        mycursor.execute('SELECT QN FROM QUIZ WHERE CHOSEN="N"')
        x = mycursor.fetchall()
        print(x)
        if x ==[]:
            return None
        else:
            l = []
            for i in x:
                l+=list(i)
            r=random.choice(l)
            mycursor.execute('SELECT QN,QUESTION,OPTA,OPTB,OPTC,OPTD,CORRECT FROM QUIZ WHERE QN={}'.format(r))
            y = mycursor.fetchone()
            return y

    def verify(self,ans,c,n):
        try:
            print(c,ans)
            global mydb,mycursor,roundc,scorec,colors,cc
            if ans==c:
                roundc+=1
                print("generating question")
                mycursor.execute("UPDATE QUIZ SET CHOSEN='Y' WHERE QN={}".format(n))
                mydb.commit()
                q=self.question_select()
                if q is None:
                    print("Won") 
                    scorec +=((roundc)*5-5)
                    self.savetoleaderboard(pname,scorec,date.today())
                    self.resetquestions()
                    return{"type": "won","s": scorec}   
                else: 
                    if cc!= len(colors)-1:
                        cc+=1
                    else:
                        cc=0
                    print(q)
                    return {"type":"q","q":q,"r":roundc,"c":colors[cc]}
            else:
                print("Lost")
                scorec +=((roundc)*5-5)
                self.savetoleaderboard(pname,scorec,date.today())
                self.resetquestions()
                return {"type":"wa","s": scorec}
        except Exception as e:
            print(e)


    

    def savetoleaderboard(self,name,score,date):
        global pname,scorec
        try:
            print("Saving")
            id = uuid.uuid4()
            print(id)
            mycursor.execute('INSERT INTO LEADERBOARD VALUES("{}",{},"{}","{}")'.format(pname,scorec,date,id))
            mydb.commit()
        except Exception as e:
            print(e)

    def resetquestions(self):
        mycursor.execute('UPDATE QUIZ SET CHOSEN="N"')
        mydb.commit()
        
    def leaderboard(self):
        mycursor.execute('SELECT * FROM LEADERBOARD ORDER BY SCORE DESC')
        html=""
        x = mycursor.fetchall()
        for i in x:
            html+='''
            
                            
                <li class="lrow">
                    <div>{}</div>
                    <div>{}</div>
                    <div>{}</div>
                </li>

            '''.format(i[0],i[2],i[1])
        return html
                        
    def addaquestion(self,q,a,b,c,d,can):
        print("adding")
        mycursor.execute("select count(*) from quiz")
        qn = mycursor.fetchone()
        qno=int(qn[0])+1
        mycursor.execute('INSERT INTO QUIZ VALUES({},"{}","{}","{}","{}","{}","{}","{}")'.format(qno,q,a,b,c,d,can,'N'))
        mydb.commit()
        print('Data Successfully Added')
            


    def disp_managequestion(self):
        mycursor.execute('SELECT * FROM QUIZ')
        selectedq = mycursor.fetchall()
        html =""
        for i in selectedq:
            html+='''
                    
                    <li class="lrow">
                            
                    <div>{}</div>
                    <div id="q-{}" contenteditable="true">{}</div>
                    <div id="a-{}" contenteditable="true">{}</div>
                    <div id="b-{}" contenteditable="true">{}</div>
                    <div id="c-{}" contenteditable="true">{}</div>
                    <div id="d-{}" contenteditable="true">{}</div>
                    <div id="ca-{}" contenteditable="true">{}</div>
                    <div><button id="{}" onclick="update_q(this.id)"><i class="fi-rr-upload"></i></button><br><button onclick="deleteq(this.id)" id="{}"><i class="fi-rr-trash"></i></button></div>
                    
                    </li>
                        
                '''.format(i[0],i[0],i[1],i[0],i[2],i[0],i[3],i[0],i[4],i[0],i[5],i[0],i[6],i[0],i[0])
        print(html)

        return html

                
    def updatequestion(self,qn,q,a,b,c,d,co):
        try:
            print("Updating")
            mycursor.execute("UPDATE Quiz set QUESTION='{}',OPTA='{}',OPTB='{}',OPTC='{}',OPTD='{}',CORRECT='{}' WHERE QN={}".format(q,a,b,c,d,co,qn))
            mydb.commit()
            mycursor.execute('SELECT * FROM QUIZ')
            selectedq = mycursor.fetchall()
            html =""
            for i in selectedq:
                html+='''
                    
                    <li class="lrow">
                            
                    <div>{}</div>
                    <div id="q-{}" contenteditable="true">{}</div>
                    <div id="a-{}" contenteditable="true">{}</div>
                    <div id="b-{}" contenteditable="true">{}</div>
                    <div id="c-{}" contenteditable="true">{}</div>
                    <div id="d-{}" contenteditable="true">{}</div>
                    <div id="ca-{}" contenteditable="true">{}</div>
                    <div><button id="{}" onclick="update_q(this.id)"><i class="fi-rr-upload"></i></button><br><button onclick="deleteq(this.id)" id="{}"><i class="fi-rr-trash"></i></button></div>
                    </li>
                        
                '''.format(i[0],i[0],i[1],i[0],i[2],i[0],i[3],i[0],i[4],i[0],i[5],i[0],i[6],i[0],i[0])
            print(html)

            return html
        except Exception as e:
            print(e)
            
    def deletequestion(self,qn):
        try:
            mycursor.execute("delete from quiz where qn='{}'".format(qn))
            mydb.commit()
            html = self.disp_managequestion()
            return html
        except Exception as e:
            print(e)
    
    def searchquestion(self,q):
        try:
            print("search")
            mycursor.execute("SELECT * FROM QUIZ WHERE QUESTION LIKE'{}%'".format(q))
            selectedq = mycursor.fetchall()
            print(q)
            html =""
            for i in selectedq:
                html+='''
                    
                    <li class="lrow">
                            
                    <div>{}</div>
                    <div id="q-{}" contenteditable="true">{}</div>
                    <div id="a-{}" contenteditable="true">{}</div>
                    <div id="b-{}" contenteditable="true">{}</div>
                    <div id="c-{}" contenteditable="true">{}</div>
                    <div id="d-{}" contenteditable="true">{}</div>
                    <div id="ca-{}" contenteditable="true">{}</div>
                    <div><button id="{}" onclick="update_q(this.id)"><i class="fi-rr-upload"></i></button><br><button onclick="deleteq(this.id)" id="{}"><i class="fi-rr-trash"></i></button></div>
                    </li>
                        
                '''.format(i[0],i[0],i[1],i[0],i[2],i[0],i[3],i[0],i[4],i[0],i[5],i[0],i[6],i[0],i[0])
            print(html)

            return html
        
        except Exception as e:
            print(e)

    def disp_managelead(self):
        mycursor.execute('SELECT * FROM LEADERBOARD')
        selectedq = mycursor.fetchall()
        html =""
        for i in selectedq:
            html+='''
                    
                    <li class="lrow">
                            
                    <div>{}</div>
                    <div>{}</div>
                    <div id="sc-{}" contenteditable="true">{}</div>
                    <div><button id="{}" onclick="update_l(this.id)"><i class="fi-rr-upload"></i></button><br><button onclick="deletel(this.id)" id="{}"><i class="fi-rr-trash"></i></button></div>
                    </li>
                        
                '''.format(i[0],i[2],i[3],i[1],i[3],i[3])
        print(html)

        return html

    def updatescore(self,id,s):
        try:
            print(s)
            mycursor.execute("UPDATE LEADERBOARD set Score='{}' WHERE id='{}'".format(s,id))
            mydb.commit()
            mycursor.execute('SELECT * FROM LEADERBOARD')
            selectedq = mycursor.fetchall()
            html =""
            for i in selectedq:
                html+='''
                    
                    <li class="lrow">
                            
                    <div>{}</div>
                    <div>{}</div>
                    <div id="sc-{}" contenteditable="true">{}</div>
                    <div><button id="{}" onclick="update_l(this.id)"><i class="fi-rr-upload"></i></button><br><button onclick="deletel(this.id)" id="{}"><i class="fi-rr-trash"></i></button></div>
                    </li>
                        
                '''.format(i[0],i[2],i[3],i[1],i[3],i[3])
            print(html)

            return html
        except Exception as e:
            print(e)
            
    def deletescore(self,id):
        try:
            print(id)
            mycursor.execute("delete from LEADERBOARD where id='{}'".format(id))
            mydb.commit()
            html = self.disp_managelead()
            return html
        except Exception as e:
            print(e)
    
    def searchscore(self,n):
        try:
            print("search")
            mycursor.execute("SELECT * FROM LEADERBOARD WHERE NAME LIKE'{}%'".format(n))
            selectedq = mycursor.fetchall()
            html =""
            for i in selectedq:
                html+='''
                    
                    <li class="lrow">
                            
                    <div>{}</div>
                    <div>{}</div>
                    <div id="sc-{}" contenteditable="true">{}</div>
                    <div><button id="{}" onclick="update_l(this.id)"><i class="fi-rr-upload"></i></button><br><button onclick="deletel(this.id)" id="{}"><i class="fi-rr-trash"></i></button></div>
                    
                    </li>
                        
                '''.format(i[0],i[2],i[3],i[1],i[3],i[3])
            print(html)

            return html
        
        except Exception as e:
            print(e)
      

   
            

api = api()
ht = ''
with open('elijah.html', 'r') as f:
    ht = str(f.read())
    window = webview.create_window('Computer Project', html=ht, js_api=api)
    webview.start(debug=True)
