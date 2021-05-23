import sys
import imaplib
import getpass
import email
import datetime
import mailparser
from bs4 import BeautifulSoup
import re
import csv
import io

    
def email_parser(username,email_id,password):
    csv_file=open(username+".csv","w",newline='',encoding="utf-8")
    writer=csv.writer(csv_file)
    writer.writerow(['FROM','SUBJECT','LINK'])
    mails=imaplib.IMAP4_SSL('imap.gmail.com')
    try:
        mails.login(email_id,password)
    except imaplib.IMAP4.error:
        return "LOGIN FAILED...!!ENTER CORRECT DETAILS"
    rv,mailboxes=mails.list()
    rv,data=mails.select("inbox")
    if rv=='OK':#ok
        rv,data2=mails.search(None,'(UNSEEN)')
        if rv!='OK':
            return
        for num in data2[0].split():
            rv,data1=mails.fetch(num,'(RFC822)')
            if rv!='OK':
                return
            raw_email=data1[0][1]
            mail2=mailparser.parse_from_bytes(raw_email)
            html1=mail2.body
            soup=BeautifulSoup(html1,'html.parser')
            links_with_text=[]
            for a in soup.find_all('a',attrs={'href': re.compile("^http://")}):
                links=(a.get('href'))
                if links not in links_with_text:
                    links_with_text.append(links)
            if len(links_with_text)!=0:
                sub=mail2.subject
                sender=mail2.from_
                for i in links_with_text:
                    writer.writerow([sender[0][1],sub,i])
        # process_mailbox(mails,writer)
        mails.close()
        csv_file.close()
    mails.logout()
    return 'scrapping completed'
        
    
if __name__ == '__main__':
    username=''
    email_id=''
    password=''
    email_parser(username,email_id,password)