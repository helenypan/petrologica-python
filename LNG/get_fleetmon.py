import sys
sys.path.append('../includes')
import requests
from datetime import datetime
import url_info
import os

sess = requests.Session()
r = sess.get(url_info.login_url)
my_csrf_token = r.cookies['csrftoken']
data_login = {
	"csrfmiddlewaretoken":my_csrf_token,
	"username":"petrologica",
	"password":"Wivenh0e",
}

headers_login = {
	"Referer":url_info.login_url
}

data_tracker = {
	"format":"csv"
}

headers_tracker = {
	"Referer":url_info.tracker_url_refer
}

sess.post(url_info.login_url,data=data_login, headers = headers_login)
res = sess.get(url_info.tracker_url,data=data_tracker, headers = headers_tracker )

cur_time  = datetime.now().strftime("%Y%m%dH%H")
file_name = "./archive/" + cur_time + ".csv"
dir_name =  os.path.dirname(file_name)
if not os.path.exists(dir_name):
    os.makedirs(dir_name)

with open(file_name, 'wb') as f:
	f.write(res.content)
