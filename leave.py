from flask import Flask, request,send_file
from flask_restful import Resource, Api
from sqlalchemy import create_engine, null
from flask_cors import CORS
import pyrebase
from json import dumps,dump
from mail  import *
from documents import *
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from datetime import date,timedelta,datetime
from holidays import getHolidays

config = {
    'apiKey': "AIzaSyBXPWOPBLz87VXW5Hh_DGVSxw8Ak23pgEM",
    'authDomain': "leave-management-840a3.firebaseapp.com",
    'databaseURL': "https://leave-management-840a3.firebaseio.com",
    'projectId': "leave-management-840a3",
    'storageBucket': "leave-management-840a3.appspot.com",
    'messagingSenderId': "116832669800",
    'appId': "1:116832669800:web:19e5f5de80209738ffebdd",
    'measurementId': "G-B2YEJY3CH1"
}

firebase = pyrebase.initialize_app(config)
s = firebase.storage()



e = create_engine('sqlite:///leave2.db')

app = Flask(__name__)
api = Api(app)
result = []
CORS(app)
holidays = getHolidays(str(datetime.now().year))


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
        query = conn.execute('select Name , Fid from Teaching where Teaching.email =' + '\'' + email + '\'' )
        for i in query.cursor.fetchall():
            dict = {
                'name' : i[0],
                'url' : s.child(i[1] + '.jpg').get_url(None)
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
        delta = tdate - fdate
        max_leaves = conn.execute('select max_leaves from LeaveTypes where lid = \'' + lid+'\'').fetchall()[0][0]
        days_between_dates = list(map(lambda x: str(fdate+timedelta(days=x)),range(delta.days+1)))
        available_dates = list(filter(lambda x: True if(x not in holidays) else False,days_between_dates))
        no_of_days = len(available_dates)
        applied_leaves = conn.execute('select sum(nodays) from Leaves where lid = \'' +lid+'\'' + 'and email = \'' + email + '\'').fetchall()[0][0]
        row_id = conn.execute('select max(id) from Leaves').fetchall()[0][0]
        if(not applied_leaves):
            applied_leaves = 0
        if row_id:
            row_id += 1
        else:
            row_id = 1
        values = "('%d','%s','%s','%s','%s','%s','%s','%d','%s' , '%s')" %(row_id , email , fid,lid , from_date , to_date , reason , no_of_days , contact , '')
        
        if (max_leaves - applied_leaves) >= no_of_days:
            query = conn.execute('insert into Leaves values ' + values)
            return [True,no_of_days,available_dates]
        else:
            return False

class Lecturer_details(Resource):
    def get(self,email):
        result.clear()
        conn = e.connect()
        query = conn.execute('select Name,Fid,Designation,email,Phno from Teaching where Teaching.email !=' + '\'' + email + '\'' )
        for i in query.cursor.fetchall():
            dict = {
                'name' : i[0],
                'fid' : i[1],
                'designation' : i[2],
                'url' : s.child(i[1] + '.jpg').get_url(None),
                'email' : i[3],
                'phone' : i[4]
                 
            }
            result.append(dict)
        return result

class Alternate_Arrangement(Resource):
    def post(self,email,date,sem,sec,sub,time,fac):
        conn = e.connect()
        from_fid = conn.execute('select Fid from Teaching where Teaching.email =' + '\'' + email + '\'').fetchall()[0][0]
        from_name = conn.execute('select name from Teaching where Teaching.email =' + '\'' + email + '\'').fetchall()[0][0]
        to_email = conn.execute('select email from Teaching where Teaching.Name = ' + '\'' + fac + '\'').fetchall()[0][0]
        to_fid = conn.execute('select fid from Teaching where Teaching.Name = ' + '\'' + fac + '\'').fetchall()[0][0]
        mail(from_name,date,sem,sub,time,to_email,sec)
        values = "('%s' , '%s' , '%d' ,'%s' ,'%s', '%s' , '%s'  , '%s' , '%s')" %(email,date,int(sem),sec,sub,time,from_fid,to_email,to_fid)
        query = conn.execute('insert into alternate values ' + values)
        



class Check_Leaves(Resource):
    def get(self,email):
        result.clear()
        conn = e.connect()
        leaves = conn.execute('select from_date,nodays,lid,reason,contact,approved from Leaves where Leaves.email =' + '\'' + email + '\'').fetchall()
        for leave in leaves:
            dict = {
                'from_date':leave[0],
                'nodays':leave[1],
                'leavetype':conn.execute('select description from LeaveTypes where LeaveTypes.lid =' + '\'' + leave[2] + '\'').fetchall()[0][0],
                'reason':leave[3],
                'contact':leave[4],
                'approved' : leave[5]
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

class From_Alt(Resource):
    def get(self,email):
        result.clear()
        conn = e.connect()
        from_alt = conn.execute('select Applied_date , sem,sec,subject,Applied_time , T_email , T.Name from alternate , Teaching T where T.Fid = alternate.T_fid and F_email = ' + '\'' + email + '\'').fetchall()
        for alt in from_alt:
            dict = {
                'date' : alt[0],
                'sem' : alt[1],
                'sec':alt[2],
                'subject' : alt[3],
                'time' : alt[4],
                'email' : alt[5] , 
                'name' : alt[6] 
            }
            result.append(dict)
        return result

class To_Alt(Resource):
    def get(self,email):
        result.clear()
        conn = e.connect()
        from_alt = conn.execute('select Applied_date , sem,sec,subject,Applied_time , F_email  , T.name from alternate , Teaching T where T.Fid = alternate.F_fid and T_email = ' + '\'' + email + '\'').fetchall()
        for alt in from_alt:
            dict = {
                'date' : alt[0],
                'sem' : alt[1],
                'sec' : alt[2],
                'subject' : alt[3],
                'time' : alt[4],
                'email' : alt[5] , 
                'name' : alt[6] 
            }
            result.append(dict)
        return result

class Leaves_Today(Resource):
    def get(self,date):
        result.clear()
        conn = e.connect()
        query = conn.execute('select Teaching.Name , LeaveTypes.description , Leaves.to_date , Leaves.reason , Leaves.approved from Teaching , Leaves , LeaveTypes where Leaves.from_date = ' + '\'' + date + '\'' + ' and 	 Leaves.lid = LeaveTypes.lid and Leaves.email = Teaching.email').fetchall()
        for i in query:
            dict = {
                'name' : i[0],
                'type' : i[1],
                'date' : i[2],
                'reason' : i[3],
                'approved' : i[4],
            }
            result.append(dict)
        return result

class Approve_Leave(Resource):
    def post(self,name,leave_type,from_date):
        conn = e.connect()
        email = conn.execute('select email from Teaching where name = ' + '\'' + name + '\'').fetchall()[0][0]
        lid = conn.execute('select lid from LeaveTypes where description = ' + '\'' + leave_type + '\'').fetchall()[0][0]
        try:
            conn.execute('update Leaves set approved = \'Yes\' where email = ' + '\'' + email + '\'' +  'and from_date = ' + '\'' + from_date + '\'' + 'and lid = ' + '\'' + lid + '\'')
            return True
        except:
            return False

class Download_Acknowledgment(Resource):
    def get(self , email , nodays , from_date):
        conn = e.connect()
        name = conn.execute('select name from Teaching where email = ' + '\'' + email + '\'').fetchall()[0][0]
        to_date = conn.execute('select to_date from Leaves where email = '+'\''+email+'\' and from_date= \''+from_date+'\'').fetchall()[0][0]
        generatedocx(name , nodays , from_date , to_date)
        return send_file('./Leave.docx' , as_attachment = True , attachment_filename = 'Leave.docx' , mimetype = 'application/msword')


api.add_resource(Faculty_details,'/api/Faculty/<string:email>')
api.add_resource(Nav_Page,'/api/nav/<string:email>')
api.add_resource(Leave_Types , '/api/leaveTypes/<string:email>')
api.add_resource(Apply_Leave , '/api/apply/<string:email>/<string:from_date>/<string:to_date>/<string:leave_type>/<string:reason>/<string:contact>')
api.add_resource(Lecturer_details,'/api/Lecturers/<string:email>')
api.add_resource(Alternate_Arrangement , '/api/alternate/<string:email>/<string:date>/<string:sem>/<string:sec>/<string:sub>/<string:time>/<string:fac>')
api.add_resource(Check_Leaves,'/api/check/<string:email>')
api.add_resource(Remaining_leaves,'/api/remainingLeaves/<string:email>')
api.add_resource(From_Alt , '/api/fromAlt/<string:email>')
api.add_resource(To_Alt , '/api/toAlt/<string:email>')
api.add_resource(Leaves_Today , '/api/today/<string:date>')
api.add_resource(Approve_Leave , '/api/approve/<string:name>/<string:leave_type>/<string:from_date>')
api.add_resource(Download_Acknowledgment , '/api/download/<string:email>/<string:nodays>/<string:from_date>')

if __name__ == '__main__':
     app.run(debug=True)


