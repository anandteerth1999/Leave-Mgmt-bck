from flask import Flask, send_file
from flask.globals import request
import json
from flask_restful import Resource, Api
from sqlalchemy import create_engine, null
from flask_cors import CORS
import pyrebase
from json import dumps, dump
from mail import *
from documents import *
from datetime import date, timedelta, datetime


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
a = firebase.auth()


e = create_engine('sqlite:///leave2.db')

app = Flask(__name__)
api = Api(app)
result = []
dict = {}
CORS(app)
holidays = ['2020-01-05', '2020-01-12', '2020-01-15', '2020-01-19', '2020-01-26', '2020-02-02', '2020-02-09', '2020-02-16', '2020-02-21', '2020-02-23', '2020-03-01', '2020-03-08', '2020-03-15', '2020-03-22', '2020-03-25', '2020-03-29', '2020-04-01', '2020-04-05', '2020-04-06', '2020-04-10', '2020-04-12', '2020-04-14', '2020-04-19', '2020-04-26', '2020-05-01', '2020-05-03', '2020-05-10', '2020-05-17', '2020-05-24', '2020-05-25', '2020-05-31', '2020-06-07', '2020-06-14', '2020-06-21', '2020-06-28', '2020-07-05',
            '2020-07-12', '2020-07-19', '2020-07-26', '2020-08-01', '2020-08-02', '2020-08-09', '2020-08-15', '2020-08-16', '2020-08-22', '2020-08-23', '2020-08-30', '2020-09-06', '2020-09-13', '2020-09-17', '2020-09-20', '2020-09-27', '2020-10-02', '2020-10-04', '2020-10-11', '2020-10-18', '2020-10-25', '2020-10-26', '2020-10-30', '2020-10-31', '2020-11-01', '2020-11-08', '2020-11-14', '2020-11-15', '2020-11-16', '2020-11-22', '2020-11-29', '2020-12-03', '2020-12-06', '2020-12-13', '2020-12-20', '2020-12-25', '2020-12-27']



class Faculty_details(Resource):
    def get(self, email):
        result.clear()
        conn = e.connect()
        flag = Check_Teaching().get(email)
        if flag:
            result.clear()
            query = conn.execute(
                'select Name,Fid,Designation from Teaching where Teaching.email =' + '\'' + email + '\'')
            for i in query.cursor.fetchall():
                dict = {
                    'name': i[0],
                    'fid': i[1],
                    'designation': i[2],
                    'url': s.child(i[1] + '.jpg').get_url(None)
                }
                result.append(dict)
        else:
            result.clear()
            query = conn.execute(
                'select Name,Fid,Designation from Non_Teaching where Non_Teaching.email =' + '\'' + email + '\'')
            for i in query.cursor.fetchall():
                dict = {
                    'name': i[0],
                    'fid': i[1],
                    'designation': i[2],
                    'url': s.child(i[1] + '.jpg').get_url(None)
                }
                result.append(dict)
        return result


class Nav_Page(Resource):
    def get(self, email):
        result.clear()
        conn = e.connect()
        flag = Check_Teaching().get(email)
        if flag:
            result.clear()
            query = conn.execute(
                'select Name , Fid from Teaching where Teaching.email =' + '\'' + email + '\'')
            for i in query.cursor.fetchall():
                dict = {
                    'name': i[0],
                    'url': s.child(i[1] + '.jpg').get_url(None)
                }
                result.append(dict)
        else:
            result.clear()
            query = conn.execute(
                'select Name , Fid from Non_Teaching where Non_Teaching.email =' + '\'' + email + '\'')
            for i in query.cursor.fetchall():
                dict = {
                    'name': i[0],
                    'url': s.child(i[1] + '.jpg').get_url(None)
                }
                result.append(dict)

        return result


class Leave_Types(Resource):
    def get(self, email):
        result.clear()
        conn = e.connect()
        flag = Check_Teaching().get(email)
        if flag:
            gender = conn.execute(
                'select sex from Teaching where Teaching.email =' + '\'' + email + '\'').fetchall()[0][0]
            if gender == 'F':
                query = conn.execute('select description,lid from LeaveTypes')
                for i in query.cursor.fetchall():
                    dict = {
                        'description': i[0],
                        'lid': i[1]
                    }
                    result.append(dict)
            else:
                query = conn.execute(
                    'select description,lid from LeaveTypes where lid != \'ml\'')
                for i in query.cursor.fetchall():
                    dict = {
                        'description': i[0],
                        'lid': i[1]
                    }
                    result.append(dict)
        else:
            gender = conn.execute('select sex from Non_Teaching where Non_Teaching.email =' + '\'' + email + '\'').fetchall()[0][0]
            if gender == 'F':
                query = conn.execute('select description,lid from Non_Teaching_LeaveTypes')
                for i in query.cursor.fetchall():
                    dict = {
                        'description': i[0],
                        'lid': i[1]
                        }
                    result.append(dict)
            else:
                query = conn.execute('select description,lid from Non_Teaching_LeaveTypes where lid != \'ml\'')
                for i in query.cursor.fetchall():
                    dict = {
                        'description': i[0],
                        'lid': i[1]
                        }
                    result.append(dict)
        return result


class Apply_Leave(Resource):
    def post(self, email, from_date,to_date,leave_type,reason,contact,halfDay):
        row_id = 0
        fid='',
        name=''
        lid=''
        max_leaves = 0
        available_dates = []
        no_of_days = float(0)
        conn = e.connect()
        if Check_Teaching().get(email):
            fid = conn.execute(
                'select fid from Teaching where Teaching.email =' + '\'' + email + '\'').fetchall()[0][0]
            name = conn.execute(
                'select name from Teaching where Teaching.email =' + '\'' + email + '\'').fetchall()[0][0]
            if not Check_HOD().get(email):
                lid = conn.execute(
                    'select lid from LeaveTypes where description = '+'\''+leave_type+'\'').fetchall()[0][0]
                max_leaves = conn.execute(
                    'select max_leaves from LeaveTypes where lid = \'' + lid+'\'').fetchall()[0][0]
            else:
                lid = conn.execute(
                    'select lid from HOD_LeaveTypes where description = '+'\''+leave_type+'\'').fetchall()[0][0]
                max_leaves = conn.execute(
                    'select max_leaves from HOD_LeaveTypes where lid = \'' + lid+'\'').fetchall()[0][0]
        else:
            fid = conn.execute(
                'select fid from Non_Teaching where Non_Teaching.email =' + '\'' + email + '\'').fetchall()[0][0]
            name = conn.execute(
                'select name from Non_Teaching where Non_Teaching.email =' + '\'' + email + '\'').fetchall()[0][0]
            lid = conn.execute(
                'select lid from Non_Teaching_LeaveTypes where description = '+'\''+leave_type+'\'').fetchall()[0][0]
            max_leaves = conn.execute(
                'select max_leaves from Non_Teaching_LeaveTypes where lid = \'' + lid+'\'').fetchall()[0][0]
        fdate = [int(i) for i in from_date.split('-')]
        fdate = date(fdate[0], fdate[1], fdate[2])
        tdate = [int(i) for i in to_date.split('-')]
        tdate = date(tdate[0], tdate[1], tdate[2])
        if halfDay == 'false':
            delta = tdate - fdate
            days_between_dates = list(
                map(lambda x: str(fdate+timedelta(days=x)), range(delta.days+1)))
            available_dates = list(filter(lambda x: True if(
                x not in holidays) else False, days_between_dates))
            no_of_days = float(len(available_dates))
        else:
            no_of_days = 0.5
            available_dates = [str(fdate+timedelta(days=0))]
        applied_leaves = conn.execute('select sum(nodays) from Leaves where lid = \'' + \
                                      lid+'\'' + 'and email = \'' + email + '\'').fetchall()[0][0]
        row_id = conn.execute('select max(id) from Leaves').fetchall()[0][0]
        if(not applied_leaves):
            applied_leaves = 0
        if row_id:
            row_id += 1
        else:
            row_id = 1
        values = "('%d','%s','%s','%s','%s','%s','%s','%f','%s' , '%s')" % (row_id , email , fid, lid , from_date , to_date , reason , no_of_days , contact , '')

        if (max_leaves - applied_leaves) >= no_of_days:
            query = conn.execute('insert into Leaves values ' + values)
            mail(email, name)
            return [True, no_of_days, available_dates]
        else:
            return False


class Lecturer_details(Resource):
    def get(self, email):
        result.clear()
        flag = Check_Teaching().get(email)
        print(flag)
        conn = e.connect()
        if flag == True:
            query = conn.execute(
                'select Name,Fid,Designation,email,Phno from Teaching where Teaching.email !=' + '\'' + email + '\'')
            for i in query.cursor.fetchall():
                dict = {
                    'name': i[0],
                    'fid': i[1],
                    'designation': i[2],
                    'url': s.child(i[1] + '.jpg').get_url(None),
                    'email': i[3],
                    'phone': i[4]

                }
                result.append(dict)
        else:
            query = conn.execute(
                'select Name,Fid,Designation,email,Phno from Non_Teaching where Non_Teaching.email !=' + '\'' + email + '\'')
            for i in query.cursor.fetchall():
                dict = {
                    'name': i[0],
                    'fid': i[1],
                    'designation': i[2],
                    'url': s.child(i[1] + '.jpg').get_url(None),
                    'email': i[3],
                    'phone': i[4]

                }
                result.append(dict)

        return result


class Alternate_Arrangement(Resource):
    def post(self, email, date,sem,sec,sub,time,fac):
        conn = e.connect()
        from_fid = conn.execute(
            'select Fid from Teaching where Teaching.email =' + '\'' + email + '\'').fetchall()[0][0]
        from_name = conn.execute(
            'select name from Teaching where Teaching.email =' + '\'' + email + '\'').fetchall()[0][0]
        to_email = conn.execute(
            'select email from Teaching where Teaching.Name = ' + '\'' + fac + '\'').fetchall()[0][0]
        to_fid = conn.execute(
            'select fid from Teaching where Teaching.Name = ' + '\'' + fac + '\'').fetchall()[0][0]
        alternate(from_name, date, sem,sub,time,to_email,sec)
        values = "('%s' , '%s' , '%d' ,'%s' ,'%s', '%s' , '%s'  , '%s' , '%s')" % (email, date,int(sem),sec,sub,time,from_fid,to_email,to_fid)
        query = conn.execute('insert into alternate values ' + values)


class Check_Leaves(Resource):
    def get(self, email):
        result.clear()
        conn = e.connect()
        flag = Check_Teaching().get(email)
        leaves = conn.execute(
            'select from_date,nodays,lid,reason,contact,approved from Leaves where Leaves.email =' + '\'' + email + '\'').fetchall()
        for leave in leaves:
            dict = {
                'from_date': leave[0],
                'nodays': leave[1],
                'leavetype': conn.execute('select description from LeaveTypes where LeaveTypes.lid =' + '\'' + leave[2] + '\'').fetchall()[0][0] if(flag) else conn.execute('select description from Non_Teaching_LeaveTypes where Non_Teaching_LeaveTypes.lid =' + '\'' + leave[2] + '\'').fetchall()[0][0],
                'reason': leave[3],
                'contact': leave[4],
                'approved': leave[5]
            }
            result.append(dict)
        return result


class Remaining_leaves(Resource):
    def get(self, email):
        result.clear()
        conn = e.connect()
        flag = Check_Teaching().get(email)
        isHOD = Check_HOD().get(email)
        if isHOD:
            remaining_leaves = conn.execute('select HOD_LeaveTypes.lid, HOD_LeaveTypes.description , max_leaves, applied.email, case when max_leaves - applied.total_days is NULL then max_leaves else max_leaves - applied.total_days end as remaining from HOD_LeaveTypes left join applied on HOD_LeaveTypes.lid = applied.lid where applied.email =' + \
                                            '\'' + email + '\'UNION select HOD_LeaveTypes.lid , HOD_LeaveTypes.description , HOD_LeaveTypes.max_leaves , \'not applied\' , max_leaves as remaining from HOD_LeaveTypes where lid not in (select lid from applied where email = \''+email+'\')').fetchall()
        elif flag:
            remaining_leaves = conn.execute('select LeaveTypes.lid, LeaveTypes.description , max_leaves, applied.email, case when max_leaves - applied.total_days is NULL then max_leaves else max_leaves - applied.total_days end as remaining from LeaveTypes left join applied on LeaveTypes.lid = applied.lid where applied.email =' + \
                                            '\'' + email + '\'UNION select LeaveTypes.lid , LeaveTypes.description , LeaveTypes.max_leaves , \'not applied\' , max_leaves as remaining from LeaveTypes where lid not in (select lid from applied where email = \''+email+'\')').fetchall()
        else:
            remaining_leaves = conn.execute('select Non_Teaching_LeaveTypes.lid, Non_Teaching_LeaveTypes.description , max_leaves, applied.email, case when max_leaves - applied.total_days is NULL then max_leaves else max_leaves - applied.total_days end as remaining from Non_Teaching_LeaveTypes left join applied on Non_Teaching_LeaveTypes.lid = applied.lid where applied.email =' + \
                                            '\'' + email + '\'UNION select Non_Teaching_LeaveTypes.lid , Non_Teaching_LeaveTypes.description , Non_Teaching_LeaveTypes.max_leaves , \'not applied\' , max_leaves as remaining from Non_Teaching_LeaveTypes where lid not in (select lid from applied where email = \''+email+'\')').fetchall()
        for i in remaining_leaves:
            dict = {
                'description': i[1],
                'max_leaves': i[2],
                'remaining_leaves': i[4]

            }
            result.append(dict)
        return result


class From_Alt(Resource):
    def get(self, email):
        flag = Check_Teaching().get(email)
        result.clear()
        conn = e.connect()
        if flag :
            from_alt = conn.execute(
                'select Applied_date , sem,sec,subject,Applied_time , T_email , T.Name from alternate , Teaching T where T.Fid = alternate.T_fid and F_email = ' + '\'' + email + '\'').fetchall()
            for alt in from_alt:
                dict = {
                    'date': alt[0],
                    'sem': alt[1],
                    'sec': alt[2],
                    'subject': alt[3],
                    'time': alt[4],
                    'email': alt[5] ,
                    'name': alt[6]
                }
                result.append(dict)
        else:
            from_alt = conn.execute(
                'select Applied_date , Applied_time , T_email , T.Name from Non_Teaching_alternate , Non_Teaching T where T.Fid = Non_Teaching_alternate.T_fid and F_email = ' + '\'' + email + '\'').fetchall()
            for alt in from_alt:
                dict = {
                    'date': alt[0],
                    'time': alt[1],
                    'email': alt[2] ,
                    'name': alt[3]
                }
                result.append(dict)

        return result


class To_Alt(Resource):
    def get(self, email):
        flag = Check_Teaching().get(email)
        result.clear()
        conn = e.connect()
        if flag:
            from_alt = conn.execute(
                'select Applied_date , sem,sec,subject,Applied_time , F_email  , T.name from alternate , Teaching T where T.Fid = alternate.F_fid and T_email = ' + '\'' + email + '\'').fetchall()
            for alt in from_alt:
                dict = {
                    'date': alt[0],
                    'sem': alt[1],
                    'sec': alt[2],
                    'subject': alt[3],
                    'time': alt[4],
                    'email': alt[5] ,
                    'name': alt[6]
                }
                result.append(dict)
        else:
            from_alt = conn.execute(
                'select Applied_date , Applied_time , F_email , T.Name from Non_Teaching_alternate , Non_Teaching T where T.Fid = Non_Teaching_alternate.F_fid and T_email = ' + '\'' + email + '\'').fetchall()
            for alt in from_alt:
                dict = {
                    'date': alt[0],
                    'time': alt[1],
                    'email': alt[2],
                    'name': alt[3]
                }
                result.append(dict)


        return result


class Leaves_Today(Resource):
    def get(self, date):
        result.clear()
        conn = e.connect()
        query = conn.execute('select Teaching.Name , LeaveTypes.description , Leaves.to_date , Leaves.reason , Leaves.approved from Teaching , Leaves , LeaveTypes where Leaves.from_date = ' + \
                             '\'' + date + '\'' + ' and 	 Leaves.lid = LeaveTypes.lid and Leaves.email = Teaching.email').fetchall()
        for i in query:
            dict = {
                'name': i[0],
                'type': i[1],
                'date': i[2],
                'reason': i[3],
                'approved': i[4],
            }
            result.append(dict)
        return result


class Approve_Leave(Resource):
    def post(self, name, leave_type,from_date):
        conn = e.connect()
        email = conn.execute(
            'select email from Teaching where name = ' + '\'' + name + '\'').fetchall()[0][0]
        lid = conn.execute('select lid from LeaveTypes where description = ' + \
                           '\'' + leave_type + '\'').fetchall()[0][0]
        try:
            conn.execute('update Leaves set approved = \'Yes\' where email = ' + '\'' + email + \
                         '\'' + 'and from_date = ' + '\'' + from_date + '\'' + 'and lid = ' + '\'' + lid + '\'')
            approve(name, email)
            return True
        except:
            return False


class Download_Acknowledgment(Resource):
    def get(self, email, nodays , from_date):
        conn = e.connect()
        name = conn.execute(
            'select name from Teaching where email = ' + '\'' + email + '\'').fetchall()[0][0]
        to_date = conn.execute('select to_date from Leaves where email = '+ \
                               '\''+email+'\' and from_date= \''+from_date+'\'').fetchall()[0][0]
        generatedocx(name, nodays, from_date , to_date)
        return send_file('./Leave.docx', as_attachment = True, attachment_filename = 'Leave.docx' , mimetype = 'application/msword')


class Subjects(Resource):
    def get(self, sem):
        result.clear()
        conn = e.connect()
        query = conn.execute(
            'select Subjectcode , Subject from Subjects where Sem = ' + sem).fetchall()
        for i in query:
            dict = {
                'subjectCode': i[0],
                'subject': i[1]
            }
            result.append(dict)
        return result


class Check_Teaching(Resource):
    def get(self, email):
        result.clear()
        conn = e.connect()
        query = conn.execute(
            'select \'True\' from Teaching where Teaching.email = ' + '\'' + email + '\'').fetchall()
        if query:
            return True
        else:
            return False


class Non_Teaching_Faculty(Resource):
    def get(self, email):
        result.clear()
        conn = e.connect()
        query = conn.execute(
            'select Name,Fid,Designation from Non_Teaching where Non_Teaching.email =' + '\'' + email + '\'')
        for i in query.cursor.fetchall():
            dict = {
                'name': i[0],
                'fid': i[1],
                'designation': i[2],
                'url': s.child(i[1] + '.jpg').get_url(None)
            }
            result.append(dict)
        return result


class Check_HOD(Resource):
    def get(self, email):
        result.clear()
        conn = e.connect()
        query = conn.execute(
            'select \'True\' from Teaching where Teaching.email = ' + '\'' + email + '\'' + 'and Teaching.Designation = \'Prof & Head\'').fetchall()
        for i in query:
            dict = {
                'flag': i[0]
            }
            result.append(dict)
        return result

class SignUp_User(Resource):
    def post(self,email,password):
        try:
            user = a.create_user_with_email_and_password(email, password)
            print('Sign Up Succesful')
            return user
        except e:
            return e

class Check_User(Resource):
    def get(self):
        result.clear()
        dict = {}
        conn = e.connect()
        query = conn.execute('select Fid from Teaching union all select Fid from Non_Teaching')
        dict['fid'] = []
        for i in query:
            dict['fid'].append(i[0])
        result.append(dict)
        return result

class Register_User(Resource):
    def post(self):
        data = request.get_json(silent = True)
        values = "('%s','%s','%s','%s','%s','%s','%s')" % (data.get('name'), data.get('fid'),data.get('designation'),data.get('phone'),data.get('email'),data.get('address'),data.get('sex'))
        conn = e.connect()
        if data.get('type') == 'teaching':
            try:
                conn.execute('insert into Teaching values' + values)
                return True
            except:
                return False
        else:
            try:
                conn.execute('insert into Non_Teaching values' + values)
                return True
            except:
                return False


class Upload_File(Resource):
    def post(self,fid):
        file = request.files['file']
        file.save('test.jpg')
        s.child(fid + '.jpg').put('test.jpg')
        print('Upload successful')
        print(file)
        return "Done"

class Non_Teaching_Alternate(Resource):
    def post(self,email,date,time,faculty):
        conn = e.connect()
        from_fid = conn.execute(
            'select Fid from Non_Teaching where Non_Teaching.email =' + '\'' + email + '\'').fetchall()[0][0]
        from_name = conn.execute(
            'select name from Non_Teaching where Non_Teaching.email =' + '\'' + email + '\'').fetchall()[0][0]
        to_email = conn.execute(
            'select email from Non_Teaching where Non_Teaching.Name = ' + '\'' + faculty + '\'').fetchall()[0][0]
        to_fid = conn.execute(
            'select fid from Non_Teaching where Non_Teaching.Name = ' + '\'' + faculty + '\'').fetchall()[0][0]
        # alternate(from_name, date, sem, sub, time, to_email, sec)
        values = "('%s' , '%s' , '%s' ,'%s', '%s' , '%s')" % (
            email, date,  time, from_fid, to_email, to_fid)
        query = conn.execute('insert into Non_Teaching_alternate values ' + values)

 

api.add_resource(Register_User , '/api/register')
api.add_resource(Faculty_details, '/api/Faculty/<string:email>')
api.add_resource(Nav_Page, '/api/nav/<string:email>')
api.add_resource(Leave_Types, '/api/leaveTypes/<string:email>')
api.add_resource(Apply_Leave, '/api/apply/<string:email>/<string:from_date>/<string:to_date>/<string:leave_type>/<string:reason>/<string:contact>/<string:halfDay>')
api.add_resource(Lecturer_details, '/api/Lecturers/<string:email>')
api.add_resource(Alternate_Arrangement,
                 '/api/alternate/<string:email>/<string:date>/<string:sem>/<string:sec>/<string:sub>/<string:time>/<string:fac>')
api.add_resource(Check_Leaves, '/api/check/<string:email>')
api.add_resource(Remaining_leaves, '/api/remainingLeaves/<string:email>')
api.add_resource(From_Alt, '/api/fromAlt/<string:email>')
api.add_resource(To_Alt, '/api/toAlt/<string:email>')
api.add_resource(Leaves_Today, '/api/today/<string:date>')
api.add_resource(
    Approve_Leave, '/api/approve/<string:name>/<string:leave_type>/<string:from_date>')
api.add_resource(Download_Acknowledgment,
                 '/api/download/<string:email>/<string:nodays>/<string:from_date>')
api.add_resource(Subjects, '/api/subjects/<string:sem>')
api.add_resource(Check_Teaching, '/api/checkTeaching/<string:email>')
api.add_resource(Non_Teaching_Faculty, '/api/NonTeaching/<string:email>')
api.add_resource(Check_HOD, '/api/checkHOD/<string:email>')
api.add_resource(SignUp_User , '/api/signUp/<string:email>/<string:password>')
api.add_resource(Check_User , '/api/getFIDs')
api.add_resource(Upload_File , '/api/upload/<string:fid>')
api.add_resource(Non_Teaching_Alternate , '/api/nonTeachingAlternate/<string:email>/<string:date>/<string:time>/<string:faculty>')

if __name__ == '__main__':
    app.run(debug=True)
