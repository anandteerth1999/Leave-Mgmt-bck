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
from datetime import date,timedelta



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

class Lecturer_details(Resource):
    def get(self,email):
        result.clear()
        conn = e.connect()
        query = conn.execute('select Name from Teaching where Teaching.email !=' + '\'' + email + '\'' )
        for i in query.cursor.fetchall():
            dict = {
                'name' : i[0]
            }
            result.append(dict)
        return result

class Alternate_Arrangement(Resource):
    def post(self,email,date,sem,sub,time,fac):
        conn = e.connect()
        from_fid = conn.execute('select Fid from Teaching where Teaching.email =' + '\'' + email + '\'').fetchall()[0][0]
        to_email = conn.execute('select email from Teaching where Teaching.name = ' + '\'' + fac + '\'').fetchall()[0][0]
        to_fid = conn.execute('select fid from Teaching where Teaching.name = ' + '\'' + fac + '\'').fetchall()[0][0]
        values = "('%s' , '%s' , '%d' ,'%s' , '%s' , '%s'  , '%s' , '%s')" %(email,date,int(sem),sub,time,from_fid,to_email,to_fid)
        query = conn.execute('insert into alternate values ' + values)        

class Check_Leaves(Resource):
    def get(self,email):
        result.clear()
        conn = e.connect()
        leaves = conn.execute('select from_date,nodays,lid,reason,contact from Leaves where Leaves.email =' + '\'' + email + '\'').fetchall()
        for leave in leaves:
            dict = {
                'from_date':leave[0],
                'nodays':leave[1],
                'leavetype':conn.execute('select description from LeaveTypes where LeaveTypes.lid =' + '\'' + leave[2] + '\'').fetchall()[0][0],
                'reason':leave[3],
                'contact':leave[4]
            }
            result.append(dict)
        return result
class Remaining_leaves(Resource):
    def get(self,email):
        result.clear()
        conn = e.connect()
        remaining_leaves = conn.execute('select LeaveTypes.lid, LeaveTypes.description , max_leaves, applied.email, case when max_leaves - applied.total_days is NULL then max_leaves else max_leaves - applied.total_days end as remaining from LeaveTypes left join applied on LeaveTypes.lid = applied.lid where applied.email ='+ '\'' + email + '\'UNION select LeaveTypes.lid , LeaveTypes.description , LeaveTypes.max_leaves , \'not applied\' , max_leaves as remaining from LeaveTypes where lid not in (select lid from applied where email = \''+email+'\')').fetchall()
        for i in remaining_leaves:
            dict = {
                'description':i[1],
                'max_leaves':i[2],
                'remaining_leaves':i[4]

            }
            result.append(dict)
        return result





api.add_resource(Faculty_details,'/api/Faculty/<string:email>')
api.add_resource(Nav_Page,'/api/nav/<string:email>')
api.add_resource(Leave_Types , '/api/leaveTypes/<string:email>')
api.add_resource(Apply_Leave , '/api/apply/<string:email>/<string:from_date>/<string:to_date>/<string:leave_type>/<string:reason>/<string:contact>')
api.add_resource(Lecturer_details,'/api/Lecturers/<string:email>')
api.add_resource(Alternate_Arrangement , '/api/alternate/<string:email>/<string:date>/<string:sem>/<string:sub>/<string:time>/<string:fac>')
api.add_resource(Check_Leaves,'/api/check/<string:email>')
api.add_resource(Remaining_leaves,'/api/remaining/<string:email>')

if __name__ == '__main__':
     app.run(debug=True)


