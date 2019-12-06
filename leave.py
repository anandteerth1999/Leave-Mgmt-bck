from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine, null
from flask_cors import CORS
from json import dumps,dump



e = create_engine('sqlite:///leave2.db')

app = Flask(__name__)
api = Api(app)
result = []
CORS(app)
row_id = 0

class Faculty_details(Resource):
    def get(self):
        result.clear()
        conn = e.connect()
        query = conn.execute('select slno,Name,fid,Designation,Phno,Email,Sex from Teaching')
        for i in query.cursor.fetchall():
            dict = {'slno':i[0],
                    'Name':i[1],
                    'fid':i[2],
                    'Designation':i[3],
                    'Phno':i[4],
                    'Email':i[5],
                    'Sex':i[6]
                    }
            result.append(dict)
        return result


class HodLeave(Resource):
    def get(self):
        result.clear()
        conn = e.connect()
        query = conn.execute('select name from Teaching')
        for i in query.cursor.fetchall():
            dict = {'Name': i[0]}
            result.append(dict)
        return result

class apply_Leave(Resource):
    row_id = 3
    def get(self,email,type1,from1,to,reason,caddr):

        caddr = caddr.replace("*","/")
        caddr = caddr.replace("'","\"")
        conn = e.connect()
        query4 = conn.execute("select row_counter from counters")
        row = query4.cursor.fetchall()[0][0]
        cquery = conn.execute("select slno from Teaching where Teaching.email = email")
        slno = cquery.cursor.fetchall()[0][0]
        query3 = conn.execute("select lid from leave where leave.lid ='"+str(type1)+"'")
        tiff = str(query3.cursor.fetchall()[0][0])
        values = "('%d','%s','%s','%s','%s','%s','%s','%d')" %(int(slno),type1,null,from1,to,reason,caddr,int(row))
        query1 = conn.execute("select CAST((julianday('"+to+"')-julianday('"+from1+"')) as INTEGER)")
        diffd = query1.cursor.fetchall()[0][0]
        query2 = conn.execute("select Remaining_leaves.remaining_days from Remaining_Leaves,Teaching where Teaching.slno = Remaining_leaves.slno and Teaching.email = email and remaining_leaves.lid='"+tiff+"'")
        rem = query2.cursor.fetchall()[0][0]
        #diff = int(rem) - int(diffd)
        if(int(diffd)<=int(rem)):
            query = conn.execute("insert into apply values"+values)
            return True
        else:
            return False


class regs_Details(Resource):
    def get(self,Name,Fid,Desig,Ph,email,doj,aadh,pan,dob,addr,sal,sex):
        addr = addr.replace("*","/")
        addr = addr.replace("'","\"")
        conn = e.connect()
        cquery = conn.execute("select max(slno) from Teaching")
        slno = cquery.cursor.fetchall()[0][0]
        slno = int(slno)+1
        values = "('%d','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(int(slno),Name,Fid,Desig,Ph,email,doj,pan,aadh,dob,addr,sal,sex)
        query = conn.execute("insert into Teaching values"+values)

class Leave_Details(Resource):
    def get(self,email):
        result.clear()
        conn = e.connect()
        query1 = conn.execute("select slno from Teaching where Teaching.email = email")
        slno = query1.cursor.fetchall()[0][0]
        query = conn.execute("select * from remaining_leaves where remaining_leaves.slno = "+str(slno))
        for i in query.cursor.fetchall():
            dict = {
                'slno':i[0],
                'lid':i[1],
                'nod_applied':i[2],
                'nod_remaining':i[3]
            }
            result.append(dict)
        return result



class Alternate(Resource):
    def get(self,email):
        result.clear()
        conn = e.connect()
        query =  conn.execute("select no_of_days from apply where row_id = (select max(row_id) from apply where slno = (select slno from Teaching where Teaching.email = email)) ")
        a = query.cursor.fetchall()[0][0]
        a = int(a)
        return a

class Handel(Resource):
    def get(self):
        result.clear()
        conn = e.connect()
        query = conn.execute("select Name,slno from Teaching")
        for i in query.cursor.fetchall():
            dict = {'Name':i[0],
                    'slno':i[1]
                    }
            result.append(dict)
        return result

class arrange(Resource):
    def get(self,email,date1,class1,section,time,sub,handel):
        conn = e.connect()
        query1 = conn.execute("select slno from Teaching where Teaching.email = email")
        slno = query1.cursor.fetchall()[0][0]
        values = "(%d,'%s','%s','%s','%s','%s',%d)" %(int(slno),date1,class1,section,time,sub,int(handel))
        query = conn.execute("insert into alt_agmt values"+values)

class dateAdd(Resource):
    def get(self,email):
        result.clear()
        conn = e.connect()
        query =  conn.execute("select no_of_days from apply where row_id = (select max(row_id) from apply where slno = (select slno from Teaching where Teaching.email = email)) ")
        a = query.cursor.fetchall()[0][0]
        query =  conn.execute("select from_date from apply where row_id = (select max(row_id) from apply where slno = (select slno from Teaching where Teaching.email = email)) ")
        from1 = query.cursor.fetchall()[0][0]
        result.append(from1)
        a = int(a)
        b = 1
        while(True):
            if(b==a):
                break
            query1 = conn.execute("SELECT date('"+from1+"','"+str(b)+" day')")
            inc = query1.cursor.fetchall()[0][0]
            result.append(inc)
            b = b+1            
        return result

class Mgmtlv(Resource):
    def get(self,Name):
        result.clear()
        conn = e.connect()
        query1 = conn.execute("select slno from Teaching where Teaching.Name = Name")
        slno = query1.cursor.fetchall()[0][0]
        query = conn.execute("select * from remaining_leaves where remaining_leaves.slno = "+str(slno))
        for i in query.cursor.fetchall():
            dict = {
                'slno':i[0],
                'lid':i[1],
                'nod_applied':i[2],
                'nod_remaining':i[3]
            }
            result.append(dict)
        return result

api.add_resource(Faculty_details,'/Faculty')
api.add_resource(HodLeave,'/HOD_Leave')
api.add_resource(apply_Leave,'/applied/<string:email>/<string:type1>/<string:from1>/<string:to>/<string:reason>/<string:caddr>')
api.add_resource(regs_Details,'/regs/<string:Name>/<string:Fid>/<string:Desig>/<string:Ph>/<string:email>/<string:doj>/<string:aadh>/<string:pan>/<string:dob>/<string:addr>/<string:sal>/<string:sex>')
api.add_resource(Leave_Details,'/leaved/<string:email>')
api.add_resource(Alternate,'/alternate/<string:email>')
api.add_resource(Handel,'/handle')
api.add_resource(arrange,'/altinsert/<string:email>/<string:date1>/<string:class1>/<string:section>/<string:time>/<string:sub>/<string:handel>')
api.add_resource(dateAdd,'/dateadd/<string:email>')
api.add_resource(Mgmtlv,'/hodmgt/<string:Name>')

if __name__ == '__main__':
     app.run()


