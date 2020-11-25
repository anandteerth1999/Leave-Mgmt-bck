import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
def alternate(from_name,date1,sem,sub,time,to_email,sec):
    mail_content = '''Alternate Arrangement Was made to you
    On:'''+date1+'''
    From:'''+from_name+'''
    Sem:'''+sem+'''
    Section:'''+sec+'''
    Subject: '''+sub+'''
    Time:'''+time+'''
    Thank You'''
    #The mail addresses and password
    sender_address = 'simple12161015@gmail.com'
    sender_pass = 'akand@1015'
    receiver_address = to_email
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Alterante Leave arrangement Assigned'   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()

def mail(email,name):
    mail_content = '''Leave was successfully applied we have informed HOD. Waiting for the approval from the HOD
    Please check your email for further updates'''
    sender_address = 'simple12161015@gmail.com'
    sender_pass = 'akand@1015'
    receiver_address = email
    hod_mail_address = 'abhishekbn87@gmail.com'
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Leave applied successfully'   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()

    mail_content = name+''' has applied leave today please logon to Leave-Sys to approve this leave
    Thank you'''
    sender_address = 'simple12161015@gmail.com'
    sender_pass = 'akand@1015'
    receiver_address = hod_mail_address
    #Setup the MIME
    message1 = MIMEMultipart()
    message1['From'] = sender_address
    message1['To'] = receiver_address
    message1['Subject'] = 'Leave applied successfully'   #The subject line
    #The body and the attachments for the mail
    message1.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session1 = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session1.starttls() #enable security
    session1.login(sender_address, sender_pass) #login with mail_id and password
    text1 = message1.as_string()
    session1.sendmail(sender_address, receiver_address, text1)
    session1.quit()


def approve(name,email):
    mail_content = '''Your Recently applied Leave has been approved by the HOD. Please download the approval from the Leave-Sys Website'''
    #The mail addresses and password
    sender_address = 'simple12161015@gmail.com'
    sender_pass = 'akand@1015'
    receiver_address = email
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Leave Approved'   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
