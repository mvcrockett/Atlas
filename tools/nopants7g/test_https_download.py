import io, unittest, urllib.request, urllib.response
from email.message import Message
from unittest.mock import patch
from https_download import HTTPSOnlyRedirect, fetch_https

class FakeHTTPS(urllib.request.HTTPSHandler):
    def __init__(self,target):
        super().__init__();self.target=target;self.seen=[]
    def https_open(self,req):
        self.seen.append(req.full_url)
        headers=Message();headers['Location']=self.target
        r=urllib.response.addinfourl(io.BytesIO(b''),headers,req.full_url,302)
        r.msg='Found'
        return r
    def http_open(self,req):
        raise AssertionError('HTTP network request must NEVER be issued')

class RedirectTest(unittest.TestCase):
    def test_downgrade_rejected_before_following(self):
        fake=FakeHTTPS('http://private.example/secret')
        opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),fake,HTTPSOnlyRedirect())
        with patch('https_download.urllib.request.build_opener',return_value=opener):
            with self.assertRaises(ValueError):fetch_https('https://private.example/start',100,'test')
        self.assertEqual(fake.seen,['https://private.example/start'])
    def test_userinfo_rejected_before_following(self):
        fake=FakeHTTPS('https://user:password@private.example/secret')
        opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),fake,HTTPSOnlyRedirect())
        with patch('https_download.urllib.request.build_opener',return_value=opener):
            with self.assertRaises(ValueError):fetch_https('https://private.example/start',100,'test')
        self.assertEqual(len(fake.seen),1)
    def test_https_redirect_allowed(self):
        h=HTTPSOnlyRedirect();r=h.redirect_request(urllib.request.Request('https://a.example'),None,302,'',{},'https://b.example/file')
        self.assertEqual(r.full_url,'https://b.example/file')
    def test_initial_plaintext_blocked_without_network(self):
        with patch('https_download.urllib.request.build_opener') as op:
            with self.assertRaises(ValueError):fetch_https('http://a.example',100,'test')
            op.assert_not_called()
if __name__=='__main__':unittest.main()
