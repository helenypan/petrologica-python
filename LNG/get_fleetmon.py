import sys
sys.path.append('../includes')
import requests
import urllib
import ssl
from datetime import datetime
import url_info
import os


headers ={
	"Host": "www.fleetmon.com",
	"Connection": "keep-alive",
	"Upgrade-Insecure-Requests": "1",
	"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	"Referer": "https://www.fleetmon.com/my/vessels/",
	"Accept-Encoding": "gzip, deflate, sdch, br",
	"Accept-Language": "en-GB,en-US;q=0.8,en;q=0.6,zh-CN;q=0.4,zh-TW;q=0.2",
	"Cookie": "intercom-id-kwshk9to=f237a359-ceff-48fa-8ecd-511b1b78f407; _hjIncludedInSample=1;\
csrftoken=Q8L2H0vKLlI5dcLeiaiXqVdH63RKGMSb; ajs_anonymous_id=null; \
_ga=GA1.2.373668620.1495546644; _gid=GA1.2.846791572.1495747134; _gat=1;\
intercom-session-kwshk9to=cWlTVmVkbTAyMkxCRDhuSU1mVlFsOE94Q3duMmRjcTM3NXFtR2lJd0ErU1hJMGVqc0dsbUtMZytkQnlqWGE3bC0tV2d1eEFqSTZ4QWhtWHRPa1dncHBBUT09--ea2808ba991daa5ba1d8f8e82bcd9b744a3dc762;\
fmc_session=6aqgobkyg8ehxm9skcy4skl8ct1itzt0; _gali=download-export-module"
}

cur_time  = datetime.now().strftime("%Y%m%dH%H")
file_name = "./archive/" + cur_time + ".csv"
dir_name =  os.path.dirname(file_name)
if not os.path.exists(dir_name):
    os.makedirs(dir_name)

s = requests.Session() 
login_data={"username":url_info.username, "password":url_info.password}

login_header ={
	"Host": "www.fleetmon.com",
	"Connection": "keep-alive",
	"Content-Length": "97",
	"Cache-Control": "max-age=0",
	"Origin": "https://www.fleetmon.com",
	"Upgrade-Insecure-Requests": "1",
	"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
	"Content-Type": "application/x-www-form-urlencoded",
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	"Referer": "https://www.fleetmon.com/users/login/",
	"Accept-Encoding": "gzip, deflate, br",
	"Accept-Language": "en-GB,en-US;q=0.8,en;q=0.6,zh-CN;q=0.4,zh-TW;q=0.2",
	"Cookie": "intercom-id-kwshk9to=f237a359-ceff-48fa-8ecd-511b1b78f407; _hjIncludedInSample=1; fmc_session=4zwr88j3a1bb0ygcff042721f8ciebl3; csrftoken=ew9eCGfd9wS97JA2IM0LR1CE0GOl9W84; ajs_user_id=null; ajs_group_id=null; ajs_anonymous_id=%2296fe625f-25e3-42aa-a545-78b4d38f6435%22; _ga=GA1.2.373668620.1495546644; _gid=GA1.2.1465568261.1495837822; _gat=1; intercom-session-kwshk9to=NVZvWlFOUTE2RVRpc3BxS2VTS0pZa25ZNzlZbHViK2FTb2tUM3BXRkRRUnZhaHpYdndLMGYyUUhSVml3NGZRby0tRUNDZHZMOFFqOGFZYnRjNlJHVUdCQT09--9c50b292baca9a7e9907347812cc60bf45177cde; _gali=login_form"
}

context = ssl._create_unverified_context()
data = urllib.parse.urlencode(login_data).encode()
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
req = urllib.request.Request(url_info.login_url,data=data, headers=hdr)
try:
	f = request.urlopen(req, context = context)
except e:
	print(e.fp.read())

# r1 = requests.post(url_info.login_url,data=data, headers = login_header)
# print(r1.content)
# response = requests.get(url_info.tracker_url,headers=headers)
# with open(file_name, 'wb') as f:
# 	f.write(response.content)
		
  	
