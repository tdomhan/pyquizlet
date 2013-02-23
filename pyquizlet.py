import httplib
import httplib2
import json
import urllib
import random
import string
import base64

#author: Tobias Domhan


class Quizlet():
    def __init__(self, qid):
        self.qid = qid
        self.base_url = "https://api.quizlet.com/2.0/"
        self.authorized = False
        self.access_token = None

    #generate an authentication url 
    #redirect the user to this url
    def generate_auth_url(self, scopes):
        #TODO: check if scope is a list of strings
        #TODO: url redirect parameter
        auth_url = 'https://quizlet.com/authorize/'
        state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(5))
        params = {'scope': " ".join(scopes),
                  'client_id': self.qid,
                  'response_type': 'code',
                  'state': state }
        request_string = auth_url + '?' + urllib.urlencode(params)

        return (request_string,state)

    def request_token(self, code, redirect_uri, secret):
        self.authorized = False
        auth_url = 'https://api.quizlet.com/oauth/token'
        params = {'grant_type': 'authorization_code',
                  'code': code,
                  'redirect_uri': redirect_uri}
        auth = base64.encodestring( self.qid + ':' + secret)
        headers = {'Content-type': 'application/x-www-form-urlencoded',
                   'Authorization' : 'Basic ' + auth}

        h = httplib2.Http()
        #h.add_credentials(self.qid, secret)

        print urllib.urlencode(params)

        response, content = h.request(auth_url, "POST", headers=headers, body=urllib.urlencode(params))

        if response['status'] != '200':
            raise Exception("request not successful(return code: %s): %s" % (response['status'], content))

        response_data = json.loads(content)
        self.access_token = response_data
        self.authorized = True

    def make_request(self, apistring, params={}):
        base_url = self.base_url + apistring
        params['client_id'] = self.qid
        connection = httplib.HTTPSConnection('quizlet.com')
        if self.authorized and self.access_token:
            connection.putheader('Authorization','Bearer ' + self.access_token['access_token'])
        request_string = base_url + '?' + urllib.urlencode(params)

        connection.request('GET', request_string)
        response = connection.getresponse()

        if response.status != 200:
            raise Exception('respose status %d' % response.status)
        try:
            response_data = json.load(response)
            return response_data
        except Exception, e:
             print 'Problem parsing response: %s' % e
             raise e

    def make_paged_request(self, apistring, params={}):
        r = self.make_request(apistring, params)
        pages = r['total_pages']
        results = [r]
        for i in range(1,pages):
            params['page'] = str(i)
            r = self.make_request('search/sets', params)
            results.append(r)
        return results

    def get_set(self, setid):
        s = "sets/%s" % setid
        return self.make_request(s)


    def search_sets(self, sstring, paged=True):
        if not paged:
            return self.make_request('search/sets', {'q': sstring})
        else:
            return self.make_paged_request('search/sets', {'q': sstring})



