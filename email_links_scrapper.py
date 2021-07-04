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
    save_path='G://python_project/phishing/scanned_data/'+username+".csv"
    csv_file=open(save_path,"w",newline='',encoding="utf-8")
    writer=csv.writer(csv_file)
    writer.writerow(['FROM','SUBJECT','LINK'])
    # ,'qty_dot_url', 'qty_hyphen_url', 'qty_underline_url', 'qty_slash_url', 'qty_questionmark_url', 'qty_equal_url', 'qty_at_url', 'qty_and_url', 'qty_exclamation_url', 'qty_tilde_url', 'qty_comma_url', 'qty_plus_url', 'qty_asterisk_url', 'qty_percent_url', 'qty_tld_url', 'length_url', 'qty_dot_domain', 'qty_hyphen_domain', 'qty_vowels_domain', 'domain_length', 'domain_in_ip', 'qty_dot_directory', 'qty_hyphen_directory', 'qty_underline_directory', 'qty_slash_directory', 'qty_equal_directory', 'qty_at_directory', 'qty_and_directory', 'qty_exclamation_directory', 'qty_space_directory', 'qty_tilde_directory', 'qty_comma_directory', 'qty_plus_directory', 'qty_asterisk_directory', 'qty_hashtag_directory', 'qty_dollar_directory', 'qty_percent_directory', 'directory_length', 'qty_dot_file', 'qty_hyphen_file', 'qty_underline_file', 'qty_questionmark_file', 'qty_equal_file', 'qty_at_file', 'qty_and_file', 'qty_exclamation_file', 'qty_space_file', 'qty_tilde_file', 'qty_comma_file', 'qty_plus_file', 'qty_asterisk_file', 'qty_hashtag_file', 'qty_dollar_file', 'qty_percent_file', 'file_length', 'qty_dot_params', 'qty_hyphen_params', 'qty_underline_params', 'qty_slash_params', 'qty_questionmark_params', 'qty_equal_params', 'qty_at_params', 'qty_and_params', 'qty_exclamation_params', 'qty_space_params', 'qty_tilde_params', 'qty_comma_params', 'qty_plus_params', 'qty_asterisk_params', 'qty_hashtag_params', 'qty_dollar_params', 'qty_percent_params', 'params_length', 'tld_present_params', 'qty_params', 'email_in_url', 'time_response', 'asn_ip', 'time_domain_activation', 'time_domain_expiration', 'qty_ip_resolved', 'qty_nameservers', 'qty_mx_servers', 'ttl_hostname', 'tls_ssl_certificate', 'url_google_index', 'domain_google_index', 'url_shortened', 'phishing'])
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