import urllib2
def detect_com(postid):
    r = urllib2.urlopen('http://www.kuaidi100.com/autonumber/autoComNum?text='+postid)
    h = r.read()
    k = eval(h)
    kuaiditpye = k["auto"][0]['comCode']
#print kuaiditpye
    return kuaiditpye