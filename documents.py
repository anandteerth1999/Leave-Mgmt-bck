from __future__ import print_function
from mailmerge import MailMerge
from datetime import date



def generatedocx(name,nodays,from_date,to_date):
    # Define the templates - assumes they are in the same directory as the code
    template_1 = "Leave_Application.docx"

    # Show a simple example
    document_1 = MailMerge(template_1)
    document_1.merge(
        date='{:%d-%b-%Y}'.format(date.today()),
        Name=name,
        nod=nodays,
        from_date=from_date,
        to_date=to_date)
    document_1.write('Leave.docx')
    

