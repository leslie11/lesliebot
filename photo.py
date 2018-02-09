# -*- coding: utf-8 -*-
import urllib2
import urllib
import time
import requests
def get_info(url):
    s = requests.session()
    photo = s.get(url).content
    http_url='https://api-cn.faceplusplus.com/facepp/v3/detect'
    key = "dZ55wWc-Nd2zOcHISdWAeqHh-RqcH_br"
    secret = "hXhZX1ZWFAwWYdlYyjb9ADCXIi_duZJq"
    #filepath = r"C:\Users\Leslie\Downloads\webwxgetmsgimg.jpg"
    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_key')
    data.append(key)
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_secret')
    data.append(secret)
    data.append('--%s' % boundary)
    #fr=open(filepath,'rb')
    data.append('Content-Disposition: form-data; name="%s"; filename=" "' % 'image_file')
    data.append('Content-Type: %s\r\n' % 'application/octet-stream')
    data.append(photo)
    #fr.close()
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_landmark')
    data.append('1')
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_attributes')
    data.append("gender,age,beauty")
    data.append('--%s--\r\n' % boundary)

    http_body='\r\n'.join(data)
    #buld http request
    req=urllib2.Request(http_url)
    #header
    req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
    req.add_data(http_body)
    try:
        #req.add_header('Referer','http://remotserver.com/')
        #post data to server
        resp = urllib2.urlopen(req, timeout=5)
        #get response
        return resp.read()



    except urllib2.HTTPError as e:
        False