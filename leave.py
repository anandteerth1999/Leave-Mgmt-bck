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
        result.clear
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

api.add_resource(Faculty_details,'/Faculty')

if __name__ == '__main__':
     app.run()
   
