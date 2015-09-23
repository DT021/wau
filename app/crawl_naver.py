# -*- coding: utf-8 -*- 
import requests
import re
import urlparse
import time
import csv
import json 
import codecs
import time
# In this example we're trying to collect e-mail addresses from a website

# Basic e-mail regexp:
# letter/number/dot/comma @ letter/number/dot/comma . letter/number
# email_re = re.compile(r'([\w\.,]+@[\w\.,]+\.\w+)')

# HTML <a> regexp
# Matches href="" attribute
# link_re = re.compile(r'href="(.*?)"')

import csv, StringIO

class UnicodeWriter(object):
    
    def __init__(self, f, dialect=csv.excel_tab, encoding="utf-16", **kwds):
        # Redirect output to a queue
        self.queue = StringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoding = encoding
    
    def writerow(self, row):
        # Modified from original: now using unicode(s) to deal with e.g. ints
        self.writer.writerow([unicode(s).encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = data.encode(self.encoding)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)
    
    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

class UnicodeDictWriter(UnicodeWriter):
   
    
    def __init__(self, f, fields, dialect=csv.excel_tab,
            encoding="utf-16", **kwds):
        super(UnicodeDictWriter, self).__init__(f, dialect, encoding, **kwds)
        self.fields = fields
    
    def writerow(self, drow):
        row = [drow.get(field, '') for field in self.fields]
        super(UnicodeDictWriter, self).writerow(row)



def crawl(index_from, crawl_size):
    base_url = 'http://map.naver.com/search2/getSiteInfo.nhn?id=p'
    # base_url = 'http://www.schoolxcess.com/index.php?q=aHR0cDovL21hcC5uYXZlci5jb20vc2VhcmNoMi9nZXRTaXRlSW5mby5uaG4%2FaWQ9cD'
    headers = {'Accept':'application/json, text/javascript, */*; q=0.01',
    'Cookie':'npic=IhHf0sIV2sNKzQWajD4MaBwbICouHNRqL1nNOqO2UonEKdRkaylWM4W4CeiWb7PVCA==; NNB=5FIFGLS5NDWFG; WMONID=ZzV3T54OUA2; nsr_acl=1; BMR=s=1431578263011&r=http%3A%2F%2Ftvcast.naver.com%2Fv%2F368791%2Flist%2F33215&r2=http%3A%2F%2Ftvcast.naver.com%2Fv%2F366519; nid_inf=611665233; NID_AUT=9QZuR23S9LQ7QBjvLANeSh0M1EZ3+agZ/9aMV50PEtWhNBjpjMnae3Nn+cp9dARD; NID_SES=AAABThR1q17xHlztdAbeV9JamitaH1MHMr5F8HnuchL0JKOFaYBhzkycsGNFKqKnSfG3eYZeycNv28ELaNO9ueFAJC5fGjcw0mK3uxd5UInjv+nB7/2FmJGxCBIkoZZ8RiJNxea7RL6DVV/4xWkjwX0ym8I6zDf2nt4b8JjIlvG3S4SHzTZqb7R2lXEMrdy0ixXq1+zUm3EtOp/UC/NS5wxcX513F0gl8TNtEzEbjpD4oKBw8aIYj8+QQ+//CxkK3XItDBagxXMZ4F33AEK9XrK6iNVdI4+9fWM3fDphClhgy5K0M/8bvgajppPyt39fOEFpsV3pEQuMSkatFm7ioS52hdhKhVDI3oQXDPar37Yy41svh7lGvF46XHXr6GWuwrndUahdrKtC0FJ5iWBr9HcgmImq+FZ8J9r9qCMAV8/ecUjxzP1Q6nNFfskzlwUru56+Ow==; ns_load_time=1431690925387; ns_sid=45dc8c80-faf9-11e4-823e-836f0b3835a6; JSESSIONID=918A0B13C8717968F0C70A2B5FADFD9E; page_uid=SSUPrwpyLjRssa60D5RssssssZw-166244; _naver_usersession_=sMJVm/9grSbKBn0vg2lFzg==',
    'Host':'map.naver.com',
    'Referer':'http://map.naver.com/',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36',
    'X-Requested-With':'XMLHttpRequest'}

    result_list = []
    start = time.time()
    index_to = index_from + crawl_size
    for idx in range(index_from, index_to):

        url = base_url+str(idx)
        # print url
        res = requests.get(url,headers=headers)
        if idx%1000 == 0:
            print idx
            # print res.json()
        try:

            if 'result' in res.json():
                map_dict = {}
                result = res.json()['result']
                result_list.append(result)
            elif 'error' in res.json():
                pass
            else:
                # print res.json()['error']['msg']
                pass
        except Exception as e:
            print e
        # time.sleep(1)
    # Check if successful
    if(res.status_code != 200):
        return []

    end = time.time()
    print end - start
    return result_list

# crawl()
# map_json = readJson()

# def readJson():
#     with open('map_data.json', 'wr') as f:
#         f = '['+f.read()[:-1]+']'
#         data = json.loads(f)
#         return data

# import ijson

# for prefix, theType, value in ijson.parse(open('map_data.json')):
#     print prefix, theType, value




# map_data = readJson()
# for each in map_data:
#    print each['name'], each['category'],'x:',each['x'], 'y:',each['y'], each['address'],each['phone']

# map_dict['id'] = result['id']
            # map_dict['isSite'] = result['isSite']
            # map_dict['name'] = result['name']
            # map_dict['type'] = result['type']
            # map_dict['x'] = result['x']
            # map_dict['y'] = result['y']
            # map_dict['posExact']= result['posExact']
            # map_dict['address']= result['address']
            # map_dict['roadAddr']= result['roadAddr']
            # map_dict['phone']= result['phone']
            # map_dict['isCallLink']= result['isCallLink']
            # map_dict['displayHomepage']= result['displayHomepage']
            # map_dict['landingHomepage']= result['landingHomepage']
            # map_dict['ppc']= result['ppc']
            # map_dict['ktCallMd']= result['ktCallMd']
            # map_dict['couponUrl']= result['couponUrl']
            # map_dict['imageURL']= result['imageURL']
            # map_dict['imageModDate']= result['imageModDate']
            # map_dict['point']= result['point']
            # map_dict['starPoint']= result['starPoint']
            # map_dict['pointCount']= result['pointCount']
            # map_dict['reviewScoreDisplay']= result['reviewScoreDisplay']
            # map_dict['description']= result['description']
            # map_dict['reviewCount']= result['reviewCount']
            # map_dict['reviewDisplay']= result['reviewDisplay']
            # map_dict['category']= result['category']
            # map_dict['streetPanorama']= result['streetPanorama']
            # map_dict['skyPanorama']= result['skyPanorama']
            # map_dict['insidePanorama']= result['insidePanorama']
            # map_dict['interiorPanorama']= result['interiorPanorama']
            # map_dict['bizHour']= result['bizHour']
            # map_dict['options']= result['options']
            # map_dict['indoor']= result['indoor']
            # map_dict['poiInfo']= result['poiInfo']
            # map_dict['itemMetaData']= result['itemMetaData']
            # map_dict['subwayId']= result['subwayId']
            # map_dict['endPageUrl']= result['endPageUrl']
            # map_dict['entranceCoords']= result['entranceCoords']
            # map_dict['movieInfo']= result['movieInfo']
            # map_dict['petrolInfo']= result['petrolInfo']
            # map_dict['theme']= result['theme']
            # map_dict['hasCardBenefit']= result['hasCardBenefit']
            # map_dict['isPollingPlace']= result['isPollingPlace']
            # map_dict['menuExist']= result['menuExist']
            # map_dict['isDeadUrl']= result['isDeadUrl']

            # w = UnicodeWriter(outfile, map_dict.items())
            # w.writerow(map_dict)


