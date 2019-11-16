from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from flask_cors import CORS
from json import dumps,dump



e = create_engine('sqlite:///leave2.db')

app = Flask(__name__)
api = Api(app)
result = []
CORS(app)

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
    def get(self,slno,nod,from1,to,reason,caddr,type1):
        print(slno)
        caddr = caddr.replace("*","/")
        caddr = caddr.replace("'","\"")
        conn = e.connect()
        values = "('%s','%s','%s','%s','%s','%s','%s')" %(slno,type1,nod,from1,to,reason,caddr)
        query = conn.execute("insert into apply values"+values)



api.add_resource(Faculty_details,'/Faculty')
api.add_resource(HodLeave,'/HOD_Leave')
api.add_resource(apply_Leave,'/applied/<string:slno>/<string:type1>/<string:nod>/<string:from1>/<string:to>/<string:reason>/<string:caddr>')

if __name__ == '__main__':
     app.run()


