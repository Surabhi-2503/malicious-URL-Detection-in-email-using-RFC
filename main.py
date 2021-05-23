from flask import Flask,render_template,request
import UrlDivision
import email_links_scrapper
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
app=Flask(__name__)#initiate
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
model=pickle.load(open('model1.pkl', 'rb'))

shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
					  r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
					  r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
					  r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
					  r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
					  r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
					  r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
					  r"tr\.im|link\.zip\.net"

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
	urls=urls1
	feature_obtained=list()
	match=re.search(shortening_services,urls1)#whether tiny URL or FD URL
	print("url division")
	if match:
		
		print('tiny url')
	else:
		a=urlparse(urls1)
		query_string=a.query
		print("inside else")
		output=''
		file_name=os.path.basename(a.path)
		directory=os.path.dirname(a.path[1:])
		ip_address=socket.gethostbyname(a.netloc)
		base_url = a.netloc
		search_string =urls1
		search_string = search_string.replace(' ', '+')
		hostname = a.scheme+'://'+base_url
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
		feature_obtained.append(UrlDivision.qty_tld(a.netloc))
		feature_obtained.append(len(urls))
		#*************************DOMAIN*****************17-21
		print("begin of domain")
		feature_obtained.append(UrlDivision.qty_dot_domains(a.netloc))
		feature_obtained.append(UrlDivision.qty_hyphen_domain(a.netloc))
		feature_obtained.append(UrlDivision.qty_vowels_domain(a.netloc))
		feature_obtained.append(len(a.netloc)-1)
		feature_obtained.append(UrlDivision.domain_in_ip(a.netloc))
		#**********************************DIRECTORY*******************************22-38
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
		#*******************************FILES***************************************39-55
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

		#******************************PARAMETER*********************56-75
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
		#***************************SERVICES***************************************76-88
		
		feature_obtained.append(UrlDivision.mail_id_check(mails_list))
		print("feature1")
		feature_obtained.extend(UrlDivision.services(hostname,ip_address,a.netloc))#4
		print("feature2")
		feature_obtained.append(UrlDivision.dns_resolver(a.netloc))
		print("feature3 ")
		feature_obtained.append(UrlDivision.qty_nameservers(a.netloc))
		print("feature 4")
		feature_obtained.append(UrlDivision.qty_mx_server(a.netloc))
		print("feature 5")
		feature_obtained.append(UrlDivision.qty_ttl(a.netloc))
		print("feature 6")
		feature_obtained.append(UrlDivision.tls_ssl_certificate(base_url))
		print("feature 7")
		feature_obtained.append(UrlDivision.url_or_domain__google_index(search_string))
		print("feature 8")
		feature_obtained.append(UrlDivision.url_or_domain__google_index(a.netloc))
		print("feature 9")
		feature_obtained.append(0)
		print("feature 10")
		print("end of service")
	if (model.predict([feature_obtained]))==[0]:
    		output='safer'
			
	else:
			output='phished'
			print("phished")
	print("end=",output)
	return render_template('urlCheck.html',result=output)
@app.route('/email_urlCheck',methods=['GET','POST'])
def email_urlCheck():
    username=request.form.get("username")
    email_id=request.form.get("email_id")
    password=request.form.get("passwd")
    a=email_links_scrapper.email_parser(username,email_id,password)
    return a
if __name__ == "__main__":
	app.run(debug=True)