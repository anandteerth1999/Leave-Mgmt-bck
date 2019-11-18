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
    def get(self,email,type1,from1,to,reason,caddr):

        caddr = caddr.replace("*","/")
        caddr = caddr.replace("'","\"")
        conn = e.connect()
        cquery = conn.execute("select slno from Teaching where Teaching.email = email")
        slno = cquery.cursor.fetchall()[0][0]

        values = "('%d','%s','%s','%s','%s','%s','%s','%d')" %(int(slno),type1,null,from1,to,reason,caddr, row_id)
        row_id
        query = conn.execute("insert into apply values"+values)



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
    def get(self):
        j=0
        result.clear()
        conn = e.connect()
        query = conn.execute("select apply.slno,apply.lid,count(apply.lid),sum(apply.no_of_days),leave.no_of_days from leave,apply WHERE apply.lid=leave.lid group by(apply.lid)")
        for i in query.cursor.fetchall():
            llid = int(i[4])-int(i[3])
            dict = {
                'slno':i[0],
                'lid':i[1],
                'nod_applied':i[3],
                'nod_remaining':llid
            }
            result.append(dict)
            j = j+1
        return result


class Alternate(Resource):
    def get(self):
        result.clear()
        conn = e.connect()
        query =  conn.execute("select no_of_days from apply where row_id = max(row_id) ")
        dict = {'no_of_days':query.cursor.fetchall()[0][0]}
        result.append(dict)
        return result



api.add_resource(Faculty_details,'/Faculty')
api.add_resource(HodLeave,'/HOD_Leave')
api.add_resource(apply_Leave,'/applied/<string:email>/<string:type1>/<string:from1>/<string:to>/<string:reason>/<string:caddr>')
api.add_resource(regs_Details,'/regs/<string:Name>/<string:Fid>/<string:Desig>/<string:Ph>/<string:email>/<string:doj>/<string:aadh>/<string:pan>/<string:dob>/<string:addr>/<string:sal>/<string:sex>')
api.add_resource(Leave_Details,'/leaved')
api.add_resource(Alternate,'/alternate')

if __name__ == '__main__':
     app.run()


