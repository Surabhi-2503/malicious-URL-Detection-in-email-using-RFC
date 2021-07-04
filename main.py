# IMPORT STATEMENTS
from flask import Flask,render_template,request,session
import secrets
import pandas as pd
import pickle
import urlexpander
from urllib.parse import urlparse
from urllib.request import Request, urlopen, ssl, socket
from sklearn import metrics
from tld import get_tld, get_fld
import os
import re
import requests
from ipwhois import IPWhois
import socket
import datetime
import dns.resolver
import whois
import csv
from csv import reader
from csv import DictReader
# UESER IMPORT
import UrlDivision
import email_links_scrapper
#selenium
from selenium import webdriver   # for webdriver
from selenium.webdriver.support.ui import WebDriverWait  # for implicit and explict waits
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options 
# APP INITIALIZATION
app=Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config["SECRET_KEY"] = "OCML3BRawWEUeaxcuKHLpw"#passing secret key

# IMPORT TRAINED MODEL
model=pickle.load(open('model1.pkl', 'rb'))

# POSSIBLE TINY URL FORMAT
shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
					  r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
					  r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
					  r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
					  r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
					  r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
					  r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
					  r"tr\.im|link\.zip\.net"

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
# browser= webdriver.Chrome('E:/OnDownload/chromedriver_win32/chromedriver.exe')
browser=webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
       
@app.route('/')
def hello():
    return render_template('home.html')

@app.route('/urlCheck', methods=['GET', 'POST'])
def urlCheck():
    return render_template('urlCheck.html')

@app.route('/email_url_check',methods=['GET','POST'])
def email_url_check():
    return render_template('emailCheck.html')

@app.route('/Manual_urlCheck',methods=['GET','POST'])
def Manual_urlCheck():
    urls1=request.form.get("url1")
    # browser.get(urls1)
    urls11=urls1
    print("***************************current url************************",urls1)
    # urls=browser.current_url
    urls=urls1
    feature_obtained=list()
    match=re.search(shortening_services,urls1)#whether tiny URL or FD URL
    print("url division")
    if match:
        print('tiny url')
    else:
        a=urlparse(urls1)
        a1=urlparse(urls11)#*************extra*************
        a_netloc=(a.netloc.split(':'))[0]
        a1_netloc=(a1.netloc.split(':'))[0]
        print('url=',a)
        query_string=a.query
        # query_string1=a1.query
        print("inside else")
        output=''
        file_name=os.path.basename(a.path)#/aaaa/aaa/aaaaq.html
        # file_name1=os.path.basename(a1.path)
        directory=os.path.dirname(a.path[1:])
        # directoru1=os.path.dirname(a1.path[1:])
        try:
            # ip_address=socket.gethostbyname(a_netloc)
            ip_address1=socket.gethostname(a1_netloc)
        except:
            # ip_address=a_netloc
            ip_address1=a1_netloc
        base_url = a1_netloc
        # base_url1=a1_netloc
        search_string =urls11
        search_string = search_string.replace(' ', '+')
        print('search_string',search_string," url",a1.netloc)
        hostname = a1.scheme+'://'+base_url
        mails_list = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", urls1)
        print("begin of full url")
        
        #************************************COMPLETE URL*************************1-16
        feature_obtained.append(UrlDivision.qty_dots(urls))
        feature_obtained.append(UrlDivision.qty_hyphen(urls))
        feature_obtained.append(UrlDivision.qty_under_score(urls))
        feature_obtained.append(UrlDivision.qty_slash(urls))
        feature_obtained.append(UrlDivision.qty_questionMark(urls))
        feature_obtained.append(UrlDivision.qty_equal(urls))
        feature_obtained.append(UrlDivision.qty_at(urls))
        feature_obtained.append(UrlDivision.qty_and(urls))
        feature_obtained.append(UrlDivision.qty_exclamation(urls))
        feature_obtained.append(UrlDivision.qty_tilde(urls))
        feature_obtained.append(UrlDivision.qty_comma(urls))
        feature_obtained.append(UrlDivision.qty_plus(urls))
        feature_obtained.append(UrlDivision.qty_astrisk(urls))
        feature_obtained.append(UrlDivision.qty_percent(urls))
        feature_obtained.append(UrlDivision.qty_tld(a_netloc))
        feature_obtained.append(len(urls))
        print("begin of domain")
        feature_obtained.append(UrlDivision.qty_dot_domains(a_netloc))
        feature_obtained.append(UrlDivision.qty_hyphen_domain(a_netloc))
        feature_obtained.append(UrlDivision.qty_vowels_domain(a_netloc))
        feature_obtained.append(len(a_netloc)-1)
        feature_obtained.append(UrlDivision.domain_in_ip(a_netloc))
        print("begin of directory")
        if len((directory)) == '' or len(directory)==0:
            for i in range(17):
                feature_obtained.append(-1)
        else:
            feature_obtained.append(UrlDivision.qty_dot_directory(directory))
            feature_obtained.append(UrlDivision.qty_hyphen_directory(directory))
            feature_obtained.append(UrlDivision.qty_underline_directory(directory))
            feature_obtained.append(UrlDivision.qty_slash_directory(directory))
            feature_obtained.append(UrlDivision.qty_equal_directory(directory))
            feature_obtained.append(UrlDivision.qty_at_directory(directory))
            feature_obtained.append(UrlDivision.qty_and_directory(directory))
            feature_obtained.append(UrlDivision.qty_exclamation_directory(directory))
            feature_obtained.append(UrlDivision.qty_space_directory(directory))
            feature_obtained.append(UrlDivision.qty_tilde_directory(directory))
            feature_obtained.append(UrlDivision.qty_comma_directory(directory))
            feature_obtained.append(UrlDivision.qty_plus_directory(directory))
            feature_obtained.append(UrlDivision.qty_asterisk_directory(directory))
            feature_obtained.append(UrlDivision.qty_hashtag_directory(directory))
            feature_obtained.append(UrlDivision.qty_dollar_directory(directory))
            feature_obtained.append(UrlDivision.qty_percent_directory(directory))
            feature_obtained.append(len(directory))
        print("begin of files")
        if len((file_name)) == 0:
            for i in range(17):
                feature_obtained.append(-1)
        else:
            feature_obtained.append(UrlDivision.qty_dot_file(file_name))
            feature_obtained.append(UrlDivision.qty_hyphen_file(file_name))
            feature_obtained.append(UrlDivision.qty_underline_file(file_name))
            feature_obtained.append(UrlDivision.qty_questionmark_file(file_name))
            feature_obtained.append(UrlDivision.qty_equal_file(file_name))
            feature_obtained.append(UrlDivision.qty_at_file(file_name))
            feature_obtained.append(UrlDivision.qty_and_file(file_name))
            feature_obtained.append(UrlDivision.qty_exclamation_file(file_name))
            feature_obtained.append(UrlDivision.qty_space_file(file_name))
            feature_obtained.append(UrlDivision.qty_tilde_file(file_name))
            feature_obtained.append(UrlDivision.qty_comma_file(file_name))
            feature_obtained.append(UrlDivision.qty_plus_file(file_name))
            feature_obtained.append(UrlDivision.qty_astrisk_file(file_name))
            feature_obtained.append(UrlDivision.qty_hashtag_file(file_name))
            feature_obtained.append(UrlDivision.qty_dollar_file(file_name))
            feature_obtained.append(UrlDivision.qty_percentage_file(file_name))
            feature_obtained.append(len(file_name))
        print("begin of parameter")
        if len(query_string)==0:
            for i in range(20):
                feature_obtained.append(-1)
        else:
            feature_obtained.append(UrlDivision.qty_param_dot(query_string))
            feature_obtained.append(UrlDivision.qty_param_hyphen(query_string))
            feature_obtained.append(UrlDivision.qty_param_underscore(query_string))
            feature_obtained.append(UrlDivision.qty_param_slash(query_string))
            feature_obtained.append(UrlDivision.qty_param_questionMark(query_string))
            feature_obtained.append(UrlDivision.qty_param_equal(query_string))
            feature_obtained.append(UrlDivision.qty_param_at(query_string))
            feature_obtained.append(UrlDivision.qty_param_and(query_string))
            feature_obtained.append(UrlDivision.qty_param_exclamation(query_string))
            feature_obtained.append(UrlDivision.qty_param_space(query_string))
            feature_obtained.append(UrlDivision.qty_param_tilde(query_string))
            feature_obtained.append(UrlDivision.qty_param_comma(query_string))
            feature_obtained.append(UrlDivision.qty_param_plus(query_string))
            feature_obtained.append(UrlDivision.qty_param_astrisk(query_string))
            feature_obtained.append(UrlDivision.qty_param_hashtag(query_string))
            feature_obtained.append(UrlDivision.qty_param_dollar(query_string))
            feature_obtained.append(UrlDivision.qty_param_percentage(query_string))
            feature_obtained.append(UrlDivision.qty_param_length(query_string))
            feature_obtained.append(UrlDivision.tld_in_params(query_string))
            feature_obtained.append(UrlDivision.number_of_params(query_string))
        feature_obtained.append(UrlDivision.mail_id_check(mails_list))
        print("feature1")
        feature_obtained.extend(UrlDivision.services(hostname,ip_address1,a1_netloc))#4,[1,1,2,3]=4 4
        print("feature2")
        feature_obtained.append(UrlDivision.dns_resolver(a1_netloc))
        print("feature3 ")
        feature_obtained.append(UrlDivision.qty_nameservers(a1_netloc))
        print("feature 4")
        feature_obtained.append(UrlDivision.qty_mx_server(a1_netloc))
        print("feature 5")
        feature_obtained.append(UrlDivision.qty_ttl(a1_netloc))
        print("feature 6")
        feature_obtained.append(UrlDivision.tls_ssl_certificate(base_url))
        print("feature 7")
        feature_obtained.append(UrlDivision.url_google_index(search_string))
        print("feature 8")
        feature_obtained.append(UrlDivision.domain_google_index(a1_netloc))
        print("feature 9")
        feature_obtained.append(0)
        print("feature 10")
        print(feature_obtained)
    try :
        if (model.predict([feature_obtained]))==[0]:
            output='safer'
        else:
            output='phished'
    except:
        output='phished'
    return render_template('urlCheck.html',result=output)


@app.route('/email_urlCheck',methods=['GET','POST'])
def email_urlCheck():
    username=request.form.get("username")
    session["USERNAME"] = username
    email_id=request.form.get("email_id")
    password=request.form.get("passwd")
    a=email_links_scrapper.email_parser(username,email_id,password)
    return render_template('final_email_result.html',result=a)

@app.route('/email_url_startCheck',methods=['GET','POST'])
def email_url_startCheck():
    csv_file1='G://python_project/phishing/scanned_data/'+session.get("USERNAME")+".csv"#csv file that created while scrapping
    csv_file2='G://python_project/phishing/scanned_data/'+session.get("USERNAME")+"1.csv"#new csv file to store data after fed to model
    # to open new file
    header=['FROM','SUBJECT','LINK','PHISHING']
    data_list=list()
    user=''
    # csv_file3=open(csv_file2,'a+',newline='')
    with open(csv_file2, 'w') as f_object:
        print("***csv_ile2*****",f_object)
        writer1=csv.writer(f_object)
        writer1.writerow(header)
        with open(csv_file1, 'r+',errors="ignore") as read_obj:
            csv_dict_reader = DictReader(read_obj)
            for row in csv_dict_reader:
                user=checker(row['FROM'],row['SUBJECT'],row['LINK'])
                if user=='phish':
                    data_list.append([row['FROM'],row['SUBJECT'],row['LINK'],1])#[[],[],[]]
                    # print("*******************row data***********************",row['FROM'],row['SUBJECT'],row['LINK'],1)
                    # writer1.writerow([row['FROM'],row['SUBJECT'],row['LINK'],1])
                    # print("****************************url result*************************=",user)
        
        print(data_list)
        if len(data_list)==0:
            writer1.writerow(['NA','NA','NA','NA'])
        else:
            writer1.writerows(data_list)
    f_object.close()
    csv_data=pd.read_csv(csv_file2)
    result_Data = list(csv_data.values)
    return render_template('final_email_result.html',email_result=result_Data,result="scanned")
            
def checker(From,subject,link):
    feature_list=list()
    urls1=link
    urls=link
    match=re.search(shortening_services,urls1)
    output=''
    if match:
        print('tiny url')
        
    else:
        a=urlparse(urls1)
        a_netloc=(a.netloc.split(':'))[0]
        print('url=',a)
        query_string=a.query
        output='' #to store final output
        file_name=os.path.basename(a.path)
        directory=os.path.dirname(a.path[1:])
        try:
            ip_address=socket.gethostbyname(a_netloc)
        except:
            ip_address=a_netloc
        base_url = a_netloc
        search_string =urls1
        search_string = search_string.replace(' ', '+')
        hostname = a.scheme+'://'+base_url
        mails_list = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", urls1)
        feature_list.append(UrlDivision.qty_dots(urls))
        feature_list.append(UrlDivision.qty_hyphen(urls))
        feature_list.append(UrlDivision.qty_under_score(urls))
        feature_list.append(UrlDivision.qty_slash(urls))
        feature_list.append(UrlDivision.qty_questionMark(urls))
        feature_list.append(UrlDivision.qty_equal(urls))
        feature_list.append(UrlDivision.qty_at(urls))
        feature_list.append(UrlDivision.qty_and(urls))
        feature_list.append(UrlDivision.qty_exclamation(urls))
        feature_list.append(UrlDivision.qty_tilde(urls))
        feature_list.append(UrlDivision.qty_comma(urls))
        feature_list.append(UrlDivision.qty_plus(urls))
        feature_list.append(UrlDivision.qty_astrisk(urls))
        feature_list.append(UrlDivision.qty_percent(urls))
        feature_list.append(UrlDivision.qty_tld(a_netloc))
        feature_list.append(len(urls))
        feature_list.append(UrlDivision.qty_dot_domains(a_netloc))
        feature_list.append(UrlDivision.qty_hyphen_domain(a_netloc))
        feature_list.append(UrlDivision.qty_vowels_domain(a_netloc))
        feature_list.append(len(a_netloc)-1)
        feature_list.append(UrlDivision.domain_in_ip(a_netloc))
        if len((directory)) == '' or len(directory)==0:
            for i in range(17):
                feature_list.append(-1)
        else:
            feature_list.append(UrlDivision.qty_dot_directory(directory))
            feature_list.append(UrlDivision.qty_hyphen_directory(directory))
            feature_list.append(UrlDivision.qty_underline_directory(directory))
            feature_list.append(UrlDivision.qty_slash_directory(directory))
            feature_list.append(UrlDivision.qty_equal_directory(directory))
            feature_list.append(UrlDivision.qty_at_directory(directory))
            feature_list.append(UrlDivision.qty_and_directory(directory))
            feature_list.append(UrlDivision.qty_exclamation_directory(directory))
            feature_list.append(UrlDivision.qty_space_directory(directory))
            feature_list.append(UrlDivision.qty_tilde_directory(directory))
            feature_list.append(UrlDivision.qty_comma_directory(directory))
            feature_list.append(UrlDivision.qty_plus_directory(directory))
            feature_list.append(UrlDivision.qty_asterisk_directory(directory))
            feature_list.append(UrlDivision.qty_hashtag_directory(directory))
            feature_list.append(UrlDivision.qty_dollar_directory(directory))
            feature_list.append(UrlDivision.qty_percent_directory(directory))
            feature_list.append(len(directory))
        if len((file_name)) == 0:
            for i in range(17):
                feature_list.append(-1)
        else:
            feature_list.append(UrlDivision.qty_dot_file(file_name))
            feature_list.append(UrlDivision.qty_hyphen_file(file_name))
            feature_list.append(UrlDivision.qty_underline_file(file_name))
            feature_list.append(UrlDivision.qty_questionmark_file(file_name))
            feature_list.append(UrlDivision.qty_equal_file(file_name))
            feature_list.append(UrlDivision.qty_at_file(file_name))
            feature_list.append(UrlDivision.qty_and_file(file_name))
            feature_list.append(UrlDivision.qty_exclamation_file(file_name))
            feature_list.append(UrlDivision.qty_space_file(file_name))
            feature_list.append(UrlDivision.qty_tilde_file(file_name))
            feature_list.append(UrlDivision.qty_comma_file(file_name))
            feature_list.append(UrlDivision.qty_plus_file(file_name))
            feature_list.append(UrlDivision.qty_astrisk_file(file_name))
            feature_list.append(UrlDivision.qty_hashtag_file(file_name))
            feature_list.append(UrlDivision.qty_dollar_file(file_name))
            feature_list.append(UrlDivision.qty_percentage_file(file_name))
            feature_list.append(len(file_name))
        if len(query_string)==0:
            for i in range(20):
                feature_list.append(-1)
        else:
            feature_list.append(UrlDivision.qty_param_dot(query_string))
            feature_list.append(UrlDivision.qty_param_hyphen(query_string))
            feature_list.append(UrlDivision.qty_param_underscore(query_string))
            feature_list.append(UrlDivision.qty_param_slash(query_string))
            feature_list.append(UrlDivision.qty_param_questionMark(query_string))
            feature_list.append(UrlDivision.qty_param_equal(query_string))
            feature_list.append(UrlDivision.qty_param_at(query_string))
            feature_list.append(UrlDivision.qty_param_and(query_string))
            feature_list.append(UrlDivision.qty_param_exclamation(query_string))
            feature_list.append(UrlDivision.qty_param_space(query_string))
            feature_list.append(UrlDivision.qty_param_tilde(query_string))
            feature_list.append(UrlDivision.qty_param_comma(query_string))
            feature_list.append(UrlDivision.qty_param_plus(query_string))
            feature_list.append(UrlDivision.qty_param_astrisk(query_string))
            feature_list.append(UrlDivision.qty_param_hashtag(query_string))
            feature_list.append(UrlDivision.qty_param_dollar(query_string))
            feature_list.append(UrlDivision.qty_param_percentage(query_string))
            feature_list.append(UrlDivision.qty_param_length(query_string))
            feature_list.append(UrlDivision.tld_in_params(query_string))
            feature_list.append(UrlDivision.number_of_params(query_string))
        feature_list.append(UrlDivision.mail_id_check(mails_list))
        feature_list.extend(UrlDivision.services(hostname,ip_address,a_netloc))
        feature_list.append(UrlDivision.dns_resolver(a_netloc))
        feature_list.append(UrlDivision.qty_nameservers(a_netloc))
        feature_list.append(UrlDivision.qty_mx_server(a_netloc))
        feature_list.append(UrlDivision.qty_ttl(a_netloc))
        feature_list.append(UrlDivision.tls_ssl_certificate(base_url))
        feature_list.append(UrlDivision.url_google_index(search_string))
        feature_list.append(UrlDivision.domain_google_index(a_netloc))
        feature_list.append(0)
        try :
            if (model.predict([feature_list]))==[0]:
                output='safer'
            else:
                output='phish'
        except:
            output='phish'
    return output

if __name__ == "__main__":
    app.run(debug=True)