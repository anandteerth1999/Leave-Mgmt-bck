from __future__ import print_function
from mailmerge import MailMerge
from datetime import date
from docx import Document
from docx.shared import Inches
import base64
from PIL import Image
from io import BytesIO


def generatedocx(name, nodays, from_date, to_date):
    # Define the templates - assumes they are in the same directory as the code
    template_1 = "Leave_Application.docx"
    from_date = from_date.split('-')
    to_date = to_date.split('-')
    print(from_date)

    # Show a simple example
    document_1 = MailMerge(template_1)
    document_1.merge(
        date='{:%d-%b-%Y}'.format(date.today()),
        Name=name,
        nod=nodays,
        from_date=from_date[2] + '-' + from_date[1] + '-' + from_date[0],
        to_date=to_date[2] + '-' + to_date[1] + '-' + to_date[0])
    document_1.write('Leave.docx')


def generate_alternate_approval(from_name, to_name, applied_date, time, url):
    print(len(url) % 4)
    template = 'format.docx'
    document_merge = MailMerge(template)
    document_merge.merge(
        from_name=from_name,
        to_name=to_name,
        date=applied_date,
        time=time
    )
    document_merge.write('Approval.docx')
    document_docx = Document('Approval.docx')
    with open("sign.png", "wb") as fh:
        fh.write(base64.decodebytes(bytes(url.split(',')[1], 'utf-8') + b'=='))
    document_docx.add_picture('sign.png', width=Inches(2.5))
    document_docx.save('Approval.docx')
