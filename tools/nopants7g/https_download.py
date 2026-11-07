"""HTTPS transport that rejects unsafe redirect targets BEFORE making the request."""
import urllib.parse
import urllib.request

def validate_url(url):
    p=urllib.parse.urlsplit(url)
    if p.scheme!='https' or not p.hostname or p.username is not None or p.password is not None:
        raise ValueError('Private download requires HTTPS without userinfo')
    return url

class HTTPSOnlyRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        validate_url(newurl)
        return super().redirect_request(req,fp,code,msg,headers,newurl)

def fetch_https(url,limit,user_agent):
    validate_url(url)
    request=urllib.request.Request(url,headers={'User-Agent':user_agent})
    opener=urllib.request.build_opener(HTTPSOnlyRedirect())
    with opener.open(request,timeout=60) as response:
        validate_url(response.geturl())
        raw=response.read(limit+1)
    if len(raw)>limit:raise ValueError('Private download exceeds size cap')
    return raw
