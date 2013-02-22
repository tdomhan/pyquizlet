import httplib
import json
import urllib


class Quizlet():
    def __init__(self, qid):
        self.qid = qid
        self.base_url = "https://api.quizlet.com/2.0/"
    
    def make_request(self, apistring, params={}):
        base_url = self.base_url + apistring
        params['client_id'] = self.qid
        connection = httplib.HTTPSConnection('quizlet.com')
        request_string = base_url + '?' + urllib.urlencode(params)
        print request_string
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

    def get_set(self, setid, paged=True):
        s = "sets/%s" % setid
        if not paged:
            return self.make_request(s)
        else:
            return self.make_paged_request(s)



    def search_sets(self, sstring, paged=True):
        if not paged:
            return self.make_request('search/sets', {'q': sstring})
        else:
            return self.make_paged_request('search/sets', {'q': sstring})



