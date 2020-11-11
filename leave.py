from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine, null
from flask_cors import CORS
from json import dumps,dump
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# Python code to illustrate Sending mail from  
# your Gmail account  
import smtplib
from datetime import date



e = create_engine('sqlite:///leave2.db')

app = Flask(__name__)
api = Api(app)
result = []
CORS(app)


class Faculty_details(Resource):
    def get(self,email):
        result.clear()
        conn = e.connect()
        query = conn.execute('select Name,Fid,Designation from Teaching where Teaching.email =' + '\'' + email + '\'' )
        for i in query.cursor.fetchall():
            dict = {
                'name' : i[0],
                'fid' : i[1],
                'designation' : i[2]
            }
            result.append(dict)
        return result

class Nav_Page(Resource):
    def get(self,email):
        result.clear()
        conn = e.connect()
        query = conn.execute('select Name from Teaching where Teaching.email =' + '\'' + email + '\'' )
        for i in query.cursor.fetchall():
            dict = {
                'name' : i[0]
            }
            result.append(dict)
        return result

class Leave_Types(Resource):
    def get(self,email):
        result.clear()
        conn = e.connect()
        gender = conn.execute('select sex from Teaching where Teaching.email =' + '\'' + email + '\'').fetchall()[0][0]
        if gender == 'F':
            query = conn.execute('select description,lid from LeaveTypes')
            for i in query.cursor.fetchall():
                dict = {
                    'description' : i[0],
                    'lid' : i[1]
                }
                result.append(dict)
        else:
            query = conn.execute('select description,lid from LeaveTypes where lid != \'ml\'')
            for i in query.cursor.fetchall():
                dict = {
                    'description' : i[0],
                    'lid' : i[1]
                }
                result.append(dict)
        return result

class Apply_Leave(Resource):
    def post(self,email,from_date,to_date,leave_type,reason,contact):
        row_id = 0
        conn = e.connect()
        fid = conn.execute('select fid from Teaching where Teaching.email =' + '\'' + email + '\'').fetchall()[0][0]
        lid = conn.execute('select lid from LeaveTypes where description = '+'\''+leave_type+'\'').fetchall()[0][0]
        fdate = [int(i) for i in from_date.split('-')]
        tdate = [int(i) for i in to_date.split('-')]
        fdate = date(fdate[0], fdate[1], fdate[2])
        tdate = date(tdate[0], tdate[1], tdate[2])
        max_leaves = conn.execute('select max_leaves from LeaveTypes where lid = \'' + lid+'\'').fetchall()[0][0]
        no_of_days = (tdate - fdate).days + 1
        applied_leaves = conn.execute('select sum(nodays) from Leaves where lid = \'' +lid+'\'' + 'and email = \'' + email + '\'').fetchall()[0][0]
        row_id = conn.execute('select max(id) from Leaves').fetchall()[0][0]
        if(not applied_leaves):
            applied_leaves = 0
        if row_id:
            row_id += 1
        else:
            row_id = 1
        values = "('%d','%s','%s','%s','%s','%s','%s','%d','%s')" %(row_id , email , fid,lid , from_date , to_date , reason , no_of_days , contact)
        
        if (max_leaves - applied_leaves) >= no_of_days:
            query = conn.execute('insert into Leaves values ' + values)
            return [True,no_of_days]
        else:
            return False
        
        







api.add_resource(Faculty_details,'/api/Faculty/<string:email>')
api.add_resource(Nav_Page,'/api/nav/<string:email>')
api.add_resource(Leave_Types , '/api/leaveTypes/<string:email>')
api.add_resource(Apply_Leave , '/api/apply/<string:email>/<string:from_date>/<string:to_date>/<string:leave_type>/<string:reason>/<string:contact>')

if __name__ == '__main__':
     app.run(debug=True)


