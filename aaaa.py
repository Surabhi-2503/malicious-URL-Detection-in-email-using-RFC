import pickle
import urlexpander
from urllib.parse import urlparse
from urllib.request import Request, urlopen, ssl, socket
from sklearn import metrics
from tld import get_tld, get_fld
import os
import re
import requests #to interact with dns
from ipwhois import IPWhois #to get ASN(autonomous system number)
import socket #domain to ip address conversion
import datetime #to get datetime
import dns.resolver
import whois
from selenium import webdriver   # for webdriver
from selenium.webdriver.support.ui import WebDriverWait  # for implicit and explict waits
from selenium.webdriver.chrome.options import Options  # for suppressing the browser
import pandas as pd
import numpy as np
from pprint import pprint
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

browser= webdriver.Chrome(ChromeDriverManager().install())
# ['https://weaver-at-work.com/ss/index.php','https://www1.micard.co.jp.macys15.tokyo/404.html','https://esterlinbhaiacharicpt.revisewaves.online/gv2.php',https://www-kraken-logins-ie.com/sign-in/home.html?hash=0.177023797851']
urls11='https://www.teamlease.com/?src=alert_mail_new'
browser.get(urls11)
urls1=browser.current_url
# urls1='https://www-kraken-logins-ie.com/sign-in/home.html?hash=0.177023797851'
urls=browser.current_url
a=urlparse(urls1)
# a=urlparse(urlexpander.expand(urls))
print(a)
paths=a.path
query_string=a.query
tld_list=['org','com','net','edu','info','co','biz','io','gov','in']
mails_list = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", urls1)
splitted=os.path.split(a.path)
file_name=os.path.basename(a.path)
directory=os.path.dirname(a.path[1:])
ip_address=socket.gethostbyname(a.netloc)
base_url = a.netloc
port = '443'
expiration_date=''
val='' #to remove if any space present in list while finding the certifiation expiration time

# for checking google index
search_string =urls1
search_string = search_string.replace(' ', '+') 
print(search_string,"           and        ",a.netloc)
# chrome_options = Options()
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--ignore-certificate-errors')
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-dev-shm-usage')
# browser= webdriver.Chrome(ChromeDriverManager().install())
# browser=webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
#end of selenium driver load
hostname = a.scheme+'://'+base_url
context = ssl.create_default_context()

shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                      r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                      r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                      r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                      r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                      r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                      r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                      r"tr\.im|link\.zip\.net"
# list to store the features
feature_obtained=list()

def qty_dots(urls):
    feature_obtained.append(urls.count('.'))
    return urls.count('.')
    # qty_hyphen(urls)
def  qty_hyphen(urls):# No of hyphen in URL 2
    feature_obtained.append(urls.count('-'))
    qty_under_score(urls)
def qty_under_score(urls):# No of underscore in URL 3
    feature_obtained.append(urls.count('_'))
    qty_slash(urls)
def qty_slash(urls):# No of slash in URL 4
    feature_obtained.append(urls.count('/'))
    qty_questionMark(urls)
def qty_questionMark(urls):# No of question_mark in URL 5
    feature_obtained.append(urls.count('?'))
    qty_equal(urls)
def qty_equal(urls):# No of equals in URL 6
    feature_obtained.append(urls.count('='))
    qty_at(urls)
def qty_at(urls):# No of at in URL 7
    feature_obtained.append(urls.count('@'))
    qty_and(urls)
def qty_and(urls):# No of and in URL 8
    feature_obtained.append(urls.count('&'))
    qty_exclamation(urls)
def qty_exclamation(urls):# No of exclamation in URL 9
    feature_obtained.append(urls.count('!'))
    qty_tilde(urls)
def qty_tilde(urls):# No of tilde in URL 11
    feature_obtained.append(urls.count('~'))
    qty_comma(urls)
def qty_comma(urls):# No of comma in URL 12
    feature_obtained.append(urls.count(','))
    qty_plus(urls)
def qty_plus(urls):# No of plus in URL 13
    feature_obtained.append(urls.count('+'))
    qty_astrisk(urls)
def qty_astrisk(urls):# No of astrisk in URL 14
    feature_obtained.append(urls.count('*'))
    qty_percent(urls)
def qty_percent(urls):# No of percent in URL 17
    feature_obtained.append(urls.count('%'))
    qty_tld(a.netloc)
def qty_tld(network_locality):# No of tld in URL 18
    # print('tlds:',network_locality)
    tlds=list(get_tld(network_locality, fix_protocol=True).split('.'))
    feature_obtained.append(len(tlds))
    feature_obtained.append(len(urls))
    qty_dot_domains(a.netloc)
# qty of dot in domain 20
def qty_dot_domains(domains):
    feature_obtained.append(domains.count('.'))
    qty_hyphen_domain(domains)
def qty_hyphen_domain(domains):#21
    feature_obtained.append(domains.count('-'))
    qty_vowels_domain(domains)
def qty_vowels_domain(domains):#22,23
    count=0
    for i1 in domains:
        if i1 in ['a','e','i','o','u','A','E','I','O','U']:
            count+=1
    feature_obtained.append(count)
    feature_obtained.append(len(domains)-1)
    domain_in_ip()
def domain_in_ip():
    try:
        if socket.gethostbyname(a.netloc)==a.netloc:
            feature_obtained.append(1)
        else:
            feature_obtained.append(0)
    except:
        feature_obtained.append(-1)

def qty_dot_directory(directory):#24
    feature_obtained.append(directory.count('.'))
    qty_hyphen_directory(directory)
def qty_hyphen_directory(directory):#25
    feature_obtained.append(directory.count('-'))
    qty_underline_directory(directory)
def qty_underline_directory(directory):#26
    feature_obtained.append(directory.count('_'))
    qty_slash_directory(directory)
def qty_slash_directory(directory):#27
    feature_obtained.append(directory.count('/'))
    qty_equal_directory(directory)
def qty_equal_directory(directory):#28
    feature_obtained.append(directory.count('='))
    qty_at_directory(directory)
def qty_at_directory(directory):# No of @ in Directory 29
    feature_obtained.append(directory.count('@'))
    qty_and_directory(directory)
def qty_and_directory(directory):# No of & in Directory 30
    feature_obtained.append(directory.count('&'))
    qty_exclamation_directory(directory)
def qty_exclamation_directory(directory): #No of ! in Directory 31
    feature_obtained.append(directory.count('!'))
    qty_space_directory(directory)
def qty_space_directory(directory): #No of space in Directory 32
    feature_obtained.append(directory.count(' '))
    qty_tilde_directory(directory)
def qty_tilde_directory(directory): #No of ~ in Directory 33
    feature_obtained.append(directory.count('~'))
    qty_comma_directory(directory)
def qty_comma_directory(directory): #No of , in Directory 34
    feature_obtained.append(directory.count(','))
    qty_plus_directory(directory)
def qty_plus_directory(directory): #No of + in Directory 35
    feature_obtained.append(directory.count('+'))
    qty_asterisk_directory(directory)
def qty_asterisk_directory(directory): #No of * in Directory 36
    feature_obtained.append(directory.count('*'))
    qty_hashtag_directory(directory)
def qty_hashtag_directory(directory): #No of # in Directory 37
    feature_obtained.append(directory.count('#'))
    qty_dollar_directory(directory)
def qty_dollar_directory(directory): #No of $ in Directory 38
    feature_obtained.append(directory.count('$'))
    qty_percent_directory(directory)
def qty_percent_directory(directory): #No of % in Directory 39,40
    feature_obtained.append(directory.count('%'))
    feature_obtained.append(len(directory))

    
def qty_dot_file(file_name): #No of . in Filename 41
    feature_obtained.append(file_name.count('.'))
    qty_hyphen_file(file_name)
def qty_hyphen_file(file_name): #No of - in Filename 42
    feature_obtained.append(file_name.count('-'))
    qty_underline_file(file_name)
def qty_underline_file(file_name): #No of _ in Filename 43
    feature_obtained.append(file_name.count('_'))
    qty_questionmark_file(file_name)
def qty_questionmark_file(file_name): #No of = in Filename 45
    feature_obtained.append(file_name.count('?'))
    qty_equal_file(file_name)
def qty_equal_file(file_name): #No of = in Filename 45
    feature_obtained.append(file_name.count('='))
    qty_at_file(file_name)
def qty_at_file(file_name): #No of @ in Filename 46
    feature_obtained.append(file_name.count('@'))
    qty_and_file(file_name)
def qty_and_file(file_name): #No of & in Filename 47
    feature_obtained.append(file_name.count('&'))
    qty_exclamation_file(file_name)
def qty_exclamation_file(file_name): #No of ! in Filename 48
    feature_obtained.append(file_name.count('!'))
    qty_space_file(file_name)
def qty_space_file(file_name): #No of '  in Filename 49
    feature_obtained.append(file_name.count(' '))
    qty_tilde_file(file_name)
def qty_tilde_file(file_name): #No of ~ in Filename 50
    feature_obtained.append(file_name.count('~'))
    qty_comma_file(file_name)
def qty_comma_file(file_name): #No of , in Filename 51
    feature_obtained.append(file_name.count(','))
    qty_plus_file(file_name)
def qty_plus_file(file_name): #No of + in Filename 52
    feature_obtained.append(file_name.count('+'))
    qty_astrisk_file(file_name)
def qty_astrisk_file(file_name): #No of * in Filename 53
    feature_obtained.append(file_name.count('*'))
    qty_hashtag_file(file_name)
def qty_hashtag_file(filename):
    feature_obtained.append(file_name.count('#'))
    qty_dollar_file(file_name)
def qty_dollar_file(file_name): #No of $ in Filename 54
    feature_obtained.append(file_name.count('$'))
    qty_percentage_file(file_name)
def qty_percentage_file(file_name):
    feature_obtained.append(file_name.count('%'))
    feature_obtained.append(len(file_name))
def qty_params(params):#57-77
    feature_obtained.append(params.count('.'))
    feature_obtained.append(params.count('-'))
    feature_obtained.append(params.count('_'))
    feature_obtained.append(params.count('/'))
    feature_obtained.append(params.count('?'))
    feature_obtained.append(params.count('='))
    feature_obtained.append(params.count('@'))
    feature_obtained.append(params.count('&'))
    feature_obtained.append(params.count('!'))
    feature_obtained.append(params.count(' '))
    feature_obtained.append(params.count('~'))
    feature_obtained.append(params.count(','))
    feature_obtained.append(params.count('+'))
    feature_obtained.append(params.count('*'))
    feature_obtained.append(params.count('#'))
    feature_obtained.append(params.count('$'))
    feature_obtained.append(params.count('%'))
    feature_obtained.append(len(params))
    try:
        tld_contains = any(tlds in params for tlds in tld_list)
        feature_obtained.append(1)
    except:
        feature_obtained.append(0)
    feature_obtained.append(len(params.split('&')))
def mail_id_check():
    if(len(mails_list)>0):
        feature_obtained.append(1)
    else:
        feature_obtained.append(0)
    #calling service function
def services():
    lists=[] 
    try:#78
        response = requests.get(hostname)
        lists=str(response.elapsed).split(':') 
        feature_obtained.append(float(lists[2][1:]))
    except:
        feature_obtained.append(-1)

    try:#79
        obj = IPWhois(ip_address)
        res=obj.lookup_whois()
        feature_obtained.append(int(res['asn']))
    except:
        feature_obtained.append(-1)
    now=datetime.datetime.now()
    try:
        whois_info=whois.whois(a.netloc)
        pprint(whois_info)
        if (isinstance(whois_info.expiration_date,list)):
            exp_date=whois_info.expiration_date[0]
            expiration_time=whois_info.expiration_date[0]-now
        else:
            exp_date=whois_info.expiration_date
            expiration_time=whois_info.expiration_date-now
        if (isinstance(whois_info.creation_date,list)):
            activation_time= exp_date-whois_info.creation_date[0]
        else:
            activation_time= exp_date-(whois_info.creation_date)
        if(activation_time.days>=365):
            feature_obtained.append(activation_time.days)#80
        else:
            feature_obtained.append(-1)
        if(expiration_time.days>=365):
            feature_obtained.append(expiration_time.days)#81
        else:
            feature_obtained.append(-1)
    except:
        feature_obtained.append(-1)
        feature_obtained.append(-1)
    dns_resolver()
    qty_nameservers()    
    qty_mx_server()
    qty_ttl()
    tls_ssl_certificate()
    url_google_index(search_string)
    domain_google_index(a.netloc)
    url_shortened()
def dns_resolver():#82
    try:
        ans=dns.resolver.resolve(a.netloc)
        lis=[i for i in ans]
        feature_obtained.append(len(lis)) 
    except:
        feature_obtained.append(-1)   
def qty_nameservers():#83
    try:
        feature_obtained.append(len(whois.whois(a.netloc).name_servers))
    except:
        feature_obtained.append(-1)
def qty_mx_server():#84
    domains=(a.netloc).replace("www.","")
    try:
        feature_obtained.append(len(dns.resolver.resolve(domains, 'MX')))
    except:
        feature_obtained.append(0)
def qty_ttl():#85
    answer = dns.resolver.resolve(a.netloc)
    feature_obtained.append(answer.rrset.ttl)
def tls_ssl_certificate():#86
    try:
        with socket.create_connection((base_url, port)) as sock:
            with context.wrap_socket(sock, server_hostname=base_url) as ssock:
                datetime_str=ssock.getpeercert()['notAfter'].split(' ')
                datetime_str = list(filter(lambda x: x != val, datetime_str))
                datetime_str1=(datetime_str[3]+'/'+datetime_str[1]+'/'+datetime_str[0])
                o=datetime.datetime.strptime(datetime_str1, '%Y/%d/%b')
                dtime = (datetime.datetime.now())
                if (o.date()>=dtime.date()):
                    feature_obtained.append(1)
                else:
                    feature_obtained.append(0)
    except:
        feature_obtained.append(-1)
def url_google_index(urls_value):#87,88
    print('url google indexing=',urls_value)
    try:
        # l=['result','<nobr>','&nbsp','</nobr>']
        
        # wait = WebDriverWait(browser, 10)
        # wait.until(lambda driver: driver.current_url != urls_value)
        browser.get(urls_value)
       
        url_value=browser.current_url
        print('redirection:',url_value)
        matched_elements = browser.get("https://www.google.com/search?q=site:" +url_value)
        print('matched=',matched_elements)
        results = browser.find_elements_by_id('result-stats')
        print('results=',results)
        element=browser.find_element_by_xpath('//div[@id ="result-stats"]')
        print('element=',element)
        text = element.get_attribute("innerHTML")
        pprint(text)
        # AUG\|(.*?)\|UGA
        
        if 'About' in text:
            result=re.search('%s(.*)%s' % ('About ', ' results'), text).group(1)
            
        else:
            result =re.findall('(.*?)%s'%('result|results'),text)[0]
            
        #     print('result',result)
        if int(result.replace(",",""))>0:
            print(result,' founddddddddddddddddddddddddddddddd')
            
        else:
            print('not foundsssssssssssssssssssssssssssssssssssssss')
            
    except:
        print('errorrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr')
def domain_google_index(a_netloc):
    print('url google indexing=',a_netloc)
    try:
        # l=['result','<nobr>','&nbsp']
        print('redirection:',a_netloc)
        matched_elements = browser.get("https://www.google.com/search?q=site:" +a_netloc)
        print('matched=',matched_elements)
        results = browser.find_elements_by_id('result-stats')
        print('results=',results)
        element=browser.find_element_by_xpath('//div[@id ="result-stats"]')
        print('element=',element)
        text = element.get_attribute("innerHTML")
        text1='1,233,111 results'
        # AUG\|(.*?)\|UGA
        # print('text=',re.findall('(.*?)%s'%('result|results'),text1)[0])
        if 'About' in text:
            result=re.search('%s(.*)%s' % ('About ', ' results'), text).group(1)
        else:
            result =re.findall('(.*?)%s'%('result|results'),text1)[0]
        #     print('result',result)
        if int(result.replace(",",""))>0:
            print(result,' founddddddddddddddddddddddddddddddd')
            
        else:
            print('not foundsssssssssssssssssssssssssssssssssssssss')
            
    except:
        print('errorrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr')

def url_shortened():
    match=re.search(shortening_services,urls1)
    if match:
        feature_obtained.append(1)
    else:
        feature_obtained.append(0)

if __name__ == '__main__':
    qty_dots(urls)
    if len((directory)) == '' or len(directory)==0:
        for i in range(17):
            feature_obtained.append(-1)
    else:
        qty_dot_directory(directory)
        
    if len((file_name)) == 0:
        for i in range(17):
            feature_obtained.append(-1)
    else:
        qty_dot_file(file_name)
    if len(query_string)==0:
        for i in range(20):
            feature_obtained.append(-1)
    else:
        qty_params(query_string)
    mail_id_check()
    services()
    # print(feature_obtained)
    # print(len(feature_obtained))
    