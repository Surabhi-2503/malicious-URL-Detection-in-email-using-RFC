# import statements
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
tld_list=['org','com','net','edu','info','co','biz','io','gov','in']


# ********************complete url********************
def qty_dots(urls):#1
    return urls.count('.')
def  qty_hyphen(urls):# No of hyphen in URL 2
    return urls.count('-')
def qty_under_score(urls):# No of underscore in URL 3
    return (urls.count('_'))
def qty_slash(urls):# No of slash in URL 4
    return (urls.count('/'))
def qty_questionMark(urls):# No of question_mark in URL 5
    return (urls.count('?'))
def qty_equal(urls):# No of equals in URL 6
    return (urls.count('='))
def qty_at(urls):# No of at in URL 7
    return (urls.count('@'))
def qty_and(urls):# No of and in URL 8
    return (urls.count('&'))
def qty_exclamation(urls):# No of exclamation in URL 9
    return (urls.count('!'))
def qty_tilde(urls):# No of tilde in URL 10
    return (urls.count('~'))
def qty_comma(urls):# No of comma in URL 11
    return (urls.count(','))
def qty_plus(urls):# No of plus in URL 12
    return (urls.count('+'))
def qty_astrisk(urls):# No of astrisk in URL 13
    return (urls.count('*'))
def qty_percent(urls):# No of percent in URL 14
    return (urls.count('%'))
def qty_tld(network_locality):# No of tld in URL 15
    tlds=[]
    try:
        tlds=list(get_tld(network_locality, fix_protocol=True).split('.'))
    except:
        s=socket.gethostbyaddr(network_locality)
        tlds=list(get_tld(s[0],fix_protocol=True).split('.'))

        
    return (len(tlds))
#16th attribute length
#***************************DOMAIN*********************************
def qty_dot_domains(domains):
    return (domains.count('.'))
def qty_hyphen_domain(domains):#21 
    return (domains.count('-'))
def qty_vowels_domain(domains):#22,23
    count=0
    for i1 in domains:
        if i1 in ['a','e','i','o','u','A','E','I','O','U']:
            count+=1
    return (count)
    return (len(domains)-1)
def domain_in_ip(a_netloc):
    try:
        if socket.gethostbyname(a_netloc)==a_netloc:
            return (1)
        else:
            return (0)
    except:
        return (-1)
def qty_dot_directory(directory):#24
    return (directory.count('.'))
def qty_hyphen_directory(directory):#25
    return (directory.count('-'))
def qty_underline_directory(directory):#26
    return (directory.count('_'))
def qty_slash_directory(directory):#27
    return (directory.count('/'))
def qty_equal_directory(directory):#28
    return (directory.count('='))
def qty_at_directory(directory):# No of @ in Directory 29
    return (directory.count('@'))
def qty_and_directory(directory):# No of & in Directory 30
    return (directory.count('&'))
def qty_exclamation_directory(directory): #No of ! in Directory 31
    return (directory.count('!'))
def qty_space_directory(directory): #No of space in Directory 32
    return (directory.count(' '))
def qty_tilde_directory(directory): #No of ~ in Directory 33
    return (directory.count('~'))
def qty_comma_directory(directory): #No of , in Directory 34
    return (directory.count(','))
def qty_plus_directory(directory): #No of + in Directory 35
    return (directory.count('+'))
def qty_asterisk_directory(directory): #No of * in Directory 36
    return (directory.count('*'))
def qty_hashtag_directory(directory): #No of # in Directory 37
    return (directory.count('#'))
def qty_dollar_directory(directory): #No of $ in Directory 38
    return (directory.count('$'))
def qty_percent_directory(directory): #No of % in Directory 39,40
    return (directory.count('%'))
    #**************************FILES****************************
def qty_dot_file(file_name): #No of . in Filename 41
    return (file_name.count('.'))
def qty_hyphen_file(file_name): #No of - in Filename 42
    return (file_name.count('-'))
def qty_underline_file(file_name): #No of _ in Filename 43
    return (file_name.count('_'))
def qty_questionmark_file(file_name): #No of = in Filename 45
    return (file_name.count('?'))
def qty_equal_file(file_name): #No of = in Filename 45
    return (file_name.count('='))
def qty_at_file(file_name): #No of @ in Filename 46
    return (file_name.count('@'))
def qty_and_file(file_name): #No of & in Filename 47
    return (file_name.count('&'))
def qty_exclamation_file(file_name): #No of ! in Filename 48
    return (file_name.count('!'))
def qty_space_file(file_name): #No of '  in Filename 49
    return (file_name.count(' '))
def qty_tilde_file(file_name): #No of ~ in Filename 50
    return (file_name.count('~'))
def qty_comma_file(file_name): #No of , in Filename 51
    return (file_name.count(','))
def qty_plus_file(file_name): #No of + in Filename 52
    return (file_name.count('+'))
def qty_astrisk_file(file_name): #No of * in Filename 53
    return (file_name.count('*'))
def qty_hashtag_file(file_name):
    return (file_name.count('#'))
def qty_dollar_file(file_name): #No of $ in Filename 54
    return (file_name.count('$'))
def qty_percentage_file(file_name):
    return (file_name.count('%'))
#******************************PARAMETER**************************
def qty_param_dot(params):#57-77
    return (params.count('.'))
def qty_param_hyphen(params):
    return (params.count('-'))
def qty_param_underscore(params):
    return (params.count('_'))
def qty_param_slash(params):
    return (params.count('/'))
def qty_param_questionMark(params):
    return (params.count('?'))
def qty_param_equal(params):
    return (params.count('='))
def qty_param_at(params):
    return (params.count('@'))
def qty_param_and(params):
    return (params.count('&'))
def qty_param_exclamation(params):
    return (params.count('!'))
def qty_param_space(params):
    return (params.count(' '))
def qty_param_tilde(params):
    return (params.count('~'))
def qty_param_comma(params):
    return (params.count(','))
def qty_param_plus(params):
    return (params.count('+'))
def qty_param_astrisk(params):
    return (params.count('*'))
def qty_param_hashtag(params):
    return (params.count('#'))
def qty_param_dollar(params):
    return (params.count('$'))
def qty_param_percentage(params):
    return (params.count('%'))
def qty_param_length(params):
    return (len(params))
def tld_in_params(params):
    try:
        tld_contains = any(tlds in params for tlds in tld_list)
        return (1)
    except:
        return (0)
def number_of_params(params):
    return (len(params.split('&')))
def mail_id_check(mails_list):
    if(len(mails_list)>0):
        return (1)
    else:
        return (0)
    #calling service function
def services(hostname,ip_address,a_netloc):
    lists=[] 
    features=list()
    try:#78
        response = requests.get(hostname)
        lists=str(response.elapsed).split(':') 
        features.append(float(lists[2][1:]))
    except:
        features.append(-1)

    try:#79
        obj = IPWhois(ip_address)
        res=obj.lookup_whois()
        features.append(int(res['asn']))
    except:
        features.append(-1)

    now=datetime.datetime.now()
    try:
        whois_info=whois.whois(a_netloc)
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
            features.append(activation_time.days)#80
        else:
            features.append(-1)
        if(expiration_time.days>=365):
            features.append(expiration_time.days)#81
        else:
            features.append(-1)
    except:
        features.append(-1)
        features.append(-1)
    return features#list return
    
def dns_resolver(a_netloc):#82
    try:
        ans=dns.resolver.resolve(a_netloc)
        lis=[i for i in ans]
        return (len(lis)) 
    except:
        return (-1)   
def qty_nameservers(a_netloc):#83
    try:
        return (len(whois.whois(a_netloc).name_servers))
    except:
        return (-1)
def qty_mx_server(a_netloc):#84
    domains=(a_netloc).replace("www.","")
    try:
        return (len(dns.resolver.resolve(domains, 'MX')))
    except:
        return (0)
def qty_ttl(a_netloc):#85
    answer=0
    try:
        answer = dns.resolver.resolve(a_netloc)
    except:
        s=socket.gethostbyaddr(a_netloc)
        answer=dns.resolver.resolve(s[0])
    return (answer.rrset.ttl)
def tls_ssl_certificate(base_url):#86
    try:
        with socket.create_connection((base_url, port)) as sock:
            with context.wrap_socket(sock, server_hostname=base_url) as ssock:
                datetime_str=ssock.getpeercert()['notAfter'].split(' ')
                datetime_str = list(filter(lambda x: x != val, datetime_str))
                datetime_str1=(datetime_str[3]+'/'+datetime_str[1]+'/'+datetime_str[0])
                o=datetime.datetime.strptime(datetime_str1, '%Y/%d/%b')
                dtime = (datetime.datetime.now())
                if (o.date()>=dtime.date()):
                    return (1)
                else:
                    return (0)
    except:
        return (-1)
def url_or_domain__google_index(urls_value):#87,88
    # print('google indexing')
    try:
        matched_elements = browser.get("https://www.google.com/search?q=site:" +urls_value+ "&start=" + str(1))
        results = browser.find_elements_by_id('result-stats')
        element=browser.find_element_by_xpath('//div[@id ="result-stats"]')
        text = element.get_attribute('innerHTML')
        if 'about' in text:
            result=re.search('%s(.*)%s' % ('of about ', ' results'), text).group(1)
        else:
            result = re.search('%s(.*)%s' % ('of ', ' results'), text).group(1)
        if int(result.replace(",",""))>0:
            return (1)
        else:
            return (-1)
    except:
        return (0)

if __name__ == '__main__':
    qty_dots(urls)
    qty_hyphen(urls)
    qty_under_score(urls)# No of underscore in URL 3
    qty_slash(urls)# No of slash in URL 4
    qty_questionMark(urls)# No of question_mark in URL 5
    qty_equal(urls)# No of equals in URL 6
    qty_at(urls)# No of at in URL 7
    qty_and(urls)# No of and in URL 8
    qty_exclamation(urls)# No of exclamation in URL 9
    qty_tilde(urls)# No of tilde in URL 10
    qty_comma(urls)# No of comma in URL 11
    qty_plus(urls)# No of plus in URL 12
    qty_astrisk(urls)# No of astrisk in URL 13
    qty_percent(urls)# No of percent in URL 14
    qty_tld(network_locality)
    qty_dot_domains(domains)#17
    qty_hyphen_domain(domains)#18
    qty_vowels_domain(domains)#19
    domain_in_ip(domains)#20
    qty_dot_directory(directory)#24
    qty_hyphen_directory(directory)#25
    qty_underline_directory(directory)#26
    qty_slash_directory(directory)#27
    qty_equal_directory(directory)#28
    qty_and_directory(directory)# No of & in Directory 30
    qty_exclamation_directory(directory)#No of ! in Directory 31
    qty_space_directory(directory)#No of space in Directory 32
    qty_tilde_directory(directory) #No of ~ in Directory 33
    qty_comma_directory(directory) #No of , in Directory 34
    qty_plus_directory(directory) #No of + in Directory 35
    qty_asterisk_directory(directory) #No of * in Directory 36
    qty_hashtag_directory(directory) #No of # in Directory 37
    qty_dollar_directory(directory) #No of $ in Directory 38
    qty_percent_directory(directory) #No of % in Directory 39,40
    qty_dot_file(file_name)#No of . in Filename 41
    qty_hyphen_file(file_name) #No of - in Filename 42
    qty_underline_file(file_name) #No of _ in Filename 43
    qty_questionmark_file(file_name) #No of = in Filename 45
    qty_equal_file(file_name)#No of = in Filename 45
    qty_at_file(file_name) #No of @ in Filename 46
    qty_and_file(file_name) #No of & in Filename 47
    qty_exclamation_file(file_name) #No of ! in Filename 48
    qty_space_file(file_name)#No of '  in Filename 49
    qty_tilde_file(file_name) #No of ~ in Filename 50
    qty_comma_file(file_name) #No of , in Filename 51
    qty_plus_file(file_name)#No of + in Filename 52
    qty_astrisk_file(file_name) #No of * in Filename 53
    qty_hashtag_file(filename)
    qty_dollar_file(file_name) #No of $ in Filename 54
    qty_percentage_file(file_name)
    qty_param_dot(params)
    qty_param_hyphen(params)
    qty_param_underscore(params)
    qty_param_slash(params)
    qty_param_questionMark(params)
    qty_param_equal(params)
    qty_param_at(params)
    qty_param_and(params)
    qty_param_exclamation(params)
    qty_param_space(params)
    qty_param_tilde(params)
    qty_param_comma(params)
    qty_param_plus(params)
    qty_param_astrisk(params)
    qty_param_hashtag(params)
    qty_param_dollar(params)
    qty_param_percentage(params)
    qty_param_length(params)
    tld_in_params(params)
    number_of_params(params)
    mail_id_check(mails_list)
    services(hostname,ip_address,a_netloc)#ttl,asn,expiration,creation
    dns_resolver(a_netloc)#82
    qty_nameservers(a_netloc)#83
    qty_mx_server(a_netloc)#84
    qty_ttl(a_netloc)#85
    tls_ssl_certificate(base_url)#86
    url_or_domain__google_index(urls_value)#87,88
    


