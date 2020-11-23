import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
def mail(from_name,date1,sem,sub,time,to_email,sec):
    mail_content = '''Alternate Arrangement Was made to you
    On:'''+date1+'''
    From:'''+from_name+'''
    Sem:'''+sem+'''
    Section:'''+sec+'''
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
    print('Mail Sent')