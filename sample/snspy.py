#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '1.0.0'
__author__ = 'Liao Xuefeng (askxuefeng@gmail.com)'

'''
Python client SDK for SNS API using OAuth 2. Require Python 2.6/2.7.
'''

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

import time
import json

import hmac
import hashlib
import base64

import urllib
import urllib2
import urlparse
import gzip

import logging
import mimetypes
import collections


class JsonDict(dict):
    '''
    General json object that allows attributes to be bound to and also behaves like a dict.

    >>> jd = JsonDict(a=1, b='test')
    >>> jd.a
    1
    >>> jd.b
    'test'
    >>> jd['b']
    'test'
    >>> jd.c
    Traceback (most recent call last):
      ...
    AttributeError: 'JsonDict' object has no attribute 'c'
    >>> jd['c']
    Traceback (most recent call last):
      ...
    KeyError: 'c'
    '''
    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(r"'JsonDict' object has no attribute '%s'" % attr)

    def __setattr__(self, attr, value):
        self[attr] = value


class APIError(StandardError):
    '''
    raise APIError if receiving json message indicating failure.
    '''
    def __init__(self, error_code, error, request):
        self.error_code = error_code
        self.error = error
        self.request = request
        StandardError.__init__(self, error)

    def __str__(self):
        return 'APIError: %s: %s, request: %s' % (self.error_code, self.error, self.request)


def _parse_json(s):
    '''
    Parse json string into JsonDict.

    >>> r = _parse_json(r'{"name":"Michael","score":95}')
    >>> r.name
    u'Michael'
    >>> r['score']
    95
    '''
    return json.loads(s, object_hook=lambda pairs: JsonDict(pairs.iteritems()))


def _encode_params(**kw):
    '''
    Do url-encode parameters

    >>> _encode_params(a=1, b='R&D')
    'a=1&b=R%26D'
    >>> _encode_params(a=u'\u4e2d\u6587', b=['A', 'B', 123])
    'a=%E4%B8%AD%E6%96%87&b=A&b=B&b=123'
    '''
    def _encode(L, k, v):
        if isinstance(v, unicode):
            L.append('%s=%s' % (k, urllib.quote(v.encode('utf-8'))))
        elif isinstance(v, str):
            L.append('%s=%s' % (k, urllib.quote(v)))
        elif isinstance(v, collections.Iterable):
            for x in v:
                _encode(L, k, x)
        else:
            L.append('%s=%s' % (k, urllib.quote(str(v))))
    args = []
    for k, v in kw.iteritems():
        _encode(args, k, v)
    return '&'.join(args)


def _encode_multipart(**kw):
    ' build a multipart/form-data body with randomly generated boundary '
    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    for k, v in kw.iteritems():
        data.append('--%s' % boundary)
        if hasattr(v, 'read'):
            # file-like object:
            filename = getattr(v, 'name', '')
            content = v.read()
            data.append('Content-Disposition: form-data; name="%s"; filename="hidden"' % k)
            data.append('Content-Length: %d' % len(content))
            data.append('Content-Type: %s\r\n' % _guess_content_type(filename))
            data.append(content)
        else:
            data.append('Content-Disposition: form-data; name="%s"\r\n' % k)
            data.append(v.encode('utf-8') if isinstance(v, unicode) else v)
    data.append('--%s--\r\n' % boundary)
    return '\r\n'.join(data), boundary


def _guess_content_type(url):
    '''
    Guess content type by url.

    >>> _guess_content_type('http://test/A.HTML')
    'text/html'
    >>> _guess_content_type('http://test/a.jpg')
    'image/jpeg'
    >>> _guess_content_type('/path.txt/aaa')
    'application/octet-stream'
    '''
    OCTET_STREAM = 'application/octet-stream'
    n = url.rfind('.')
    if n == -1:
        return OCTET_STREAM
    return mimetypes.types_map.get(url[n:].lower(), OCTET_STREAM)

_HTTP_GET = 'GET'
_HTTP_POST = 'POST'
_HTTP_UPLOAD = 'UPLOAD'


def _read_http_body(http_obj):
    using_gzip = http_obj.headers.get('Content-Encoding', '') == 'gzip'
    body = http_obj.read()
    if using_gzip:
        gzipper = gzip.GzipFile(fileobj=StringIO(body))
        fcontent = gzipper.read()
        gzipper.close()
        return fcontent
    return body


def _http(method, url, headers=None, **kw):
    '''
    Send http request and return response text.
    '''
    params = None
    boundary = None
    if method == 'UPLOAD':
        params, boundary = _encode_multipart(**kw)
    else:
        params = _encode_params(**kw)
    http_url = '%s?%s' % (url, params) if method == _HTTP_GET else url
    http_body = None if method == 'GET' else params
    logging.error('%s: %s' % (method, http_url))
    req = urllib2.Request(http_url, data=http_body)
    req.add_header('Accept-Encoding', 'gzip')
    if headers:
        for k, v in headers.iteritems():
            req.add_header(k, v)
    if boundary:
        req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
    try:
        resp = urllib2.urlopen(req, timeout=5)
        return _read_http_body(resp)
    finally:
        pass


class SNSMixin(object):

    def __init__(self, app_key, app_secret, redirect_uri):
        self._client_id = app_key
        self._client_secret = app_secret
        self._redirect_uri = redirect_uri

    def _prepare_api(self, method, path, access_token, **kw):
        raise StandardError('Subclass must implement \'_prepare_api\' method.')

    def on_http_error(self, e):
        try:
            r = _parse_json(_read_http_body(e))
        except:
            r = None
        if hasattr(r, 'error_code'):
            raise APIError(r.error_code, r.get('error', ''), r.get('request', ''))
        raise e


class SinaWeiboMixin(SNSMixin):

    def get_authorize_url(self, redirect_uri, **kw):
        '''
        return the authorization url that the user should be redirected to.
        '''
        redirect = redirect_uri if redirect_uri else self._redirect_uri
        if not redirect:
            raise APIError('21305', 'Parameter absent: redirect_uri', 'OAuth2 request')
        response_type = kw.pop('response_type', 'code')
        return 'https://api.weibo.com/oauth2/authorize?%s' % \
               _encode_params(client_id=self._client_id,
                              response_type=response_type,
                              redirect_uri=redirect, **kw)

    def _prepare_api(self, method, path, access_token, **kw):
        '''
        Get api url.
        '''
        headers = None
        if access_token:
            headers = {'Authorization': 'OAuth2 %s' % access_token}
        if '/remind/' in path:
            # sina remind api url is different:
            return method, 'https://rm.api.weibo.com/2/%s.json' % path, headers, kw
        if method == 'POST' and 'pic' in kw:
            # if 'pic' in parameter, set to UPLOAD mode:
            return 'UPLOAD', 'https://api.weibo.com/2/%s.json' % path, headers, kw
        return method, 'https://api.weibo.com/2/%s.json' % path, headers, kw

    def request_access_token(self, code, redirect_uri=None):
        '''
        Return access token as a JsonDict: {"access_token":"your-access-token","expires":12345678,"uid":1234}, expires is represented using standard unix-epoch-time
        '''
        redirect = redirect_uri or self._redirect_uri
        resp_text = _http('POST', 'https://api.weibo.com/oauth2/access_token',
                          client_id=self._client_id, client_secret=self._client_secret,
                          redirect_uri=redirect, code=code, grant_type='authorization_code')
        r = _parse_json(resp_text)
        current = int(time.time())
        expires = r.expires_in + current
        remind_in = r.get('remind_in', None)
        if remind_in:
            rtime = int(remind_in) + current
            if rtime < expires:
                expires = rtime
        return JsonDict(access_token=r.access_token, expires=expires, uid=r.get('uid', None))

    def parse_signed_request(self, signed_request):
        '''
        parse signed request when using in-site app.

        Returns:
            dict object like { 'uid': 12345, 'access_token': 'ABC123XYZ', 'expires': unix-timestamp },
            or None if parse failed.
        '''
        def _b64_normalize(s):
            appendix = '=' * (4 - len(s) % 4)
            return s.replace('-', '+').replace('_', '/') + appendix

        sr = str(signed_request)
        logging.info('parse signed request: %s' % sr)
        enc_sig, enc_payload = sr.split('.', 1)
        sig = base64.b64decode(_b64_normalize(enc_sig))
        data = _parse_json(base64.b64decode(_b64_normalize(enc_payload)))
        if data['algorithm'] != u'HMAC-SHA256':
            return None
        expected_sig = hmac.new(self.client_secret, enc_payload, hashlib.sha256).digest()
        if expected_sig == sig:
            data.user_id = data.uid = data.get('user_id', None)
            data.access_token = data.get('oauth_token', None)
            expires = data.get('expires', None)
            if expires:
                data.expires = data.expires_in = time.time() + expires
            return data
        return None


class QQMixin(SNSMixin):

    def get_authorize_url(self, redirect_uri='', **kw):
        '''
        return the authorization url that the user should be redirected to.
        '''
        redirect = redirect_uri if redirect_uri else self._redirect_uri
        if not redirect:
            raise APIError('21305', 'Parameter absent: redirect_uri', 'OAuth2 request')
        response_type = kw.pop('response_type', 'code')
        return 'https://graph.qq.com/oauth2.0/authorize?%s' % \
               _encode_params(client_id=self._client_id,
                              response_type=response_type,
                              redirect_uri=redirect, **kw)

    def _prepare_api(self, method, path, access_token, **kw):
        kw['access_token'] = access_token
        kw['oauth_consumer_key'] = self._client_id
        return method, 'https://graph.qq.com/%s' % path, None, kw

    def request_access_token(self, code, redirect_uri=None):
        '''
        Return access token as a JsonDict: {"access_token":"your-access-token","expires":12345678,"uid":1234}, expires is represented using standard unix-epoch-time
        '''
        redirect = redirect_uri or self._redirect_uri
        resp_text = _http('POST', 'https://graph.qq.com/oauth2.0/token',
                          client_id=self._client_id, client_secret=self._client_secret,
                          redirect_uri=redirect, code=code, grant_type='authorization_code')
        return self._parse_access_token(resp_text)

    def refresh_access_token(self, refresh_token, redirect_uri=None):
        '''
        Refresh access token.
        '''
        redirect = redirect_uri or self._redirect_uri
        resp_text = _http('POST', 'https://graph.qq.com/oauth2.0/token',
                          refresh_token=refresh_token,
                          client_id=self._client_id, client_secret=self._client_secret,
                          redirect_uri=redirect, grant_type='refresh_token')
        return self._parse_access_token(resp_text)
        # FIXME: get oauthid from 'https://graph.z.qq.com/moc2/me?access_token=%s' % access_token

    def _parse_access_token(self, resp_text):
        ' parse access token from urlencoded str like access_token=abcxyz&expires_in=123000&other=true '
        r = self._qs2dict(resp_text)
        access_token = r.pop('access_token')
        expires = time.time() + float(r.pop('expires_in'))
        return JsonDict(access_token=access_token, expires=expires, **r)

    def _qs2dict(self, text):
        qs = urlparse.parse_qs(text)
        return dict(((k, v[0]) for k, v in qs.iteritems()))

    def get_openid(self, access_token):
        resp_text = _http('GET', 'https://graph.z.qq.com/moc2/me', access_token=access_token)
        r = self._qs2dict(resp_text)
        return r['openid']


class APIClient(object):
    '''
    API client using synchronized invocation.
    '''
    def __init__(self, mixin, app_key, app_secret, redirect_uri='', access_token='', expires=0.0):
        self._mixin = mixin(app_key, app_secret, redirect_uri)
        self._access_token = str(access_token)
        self._expires = expires

    def set_access_token(self, access_token, expires):
        self._access_token = str(access_token)
        self._expires = float(expires)

    def get_authorize_url(self, redirect_uri='', **kw):
        '''
        return the authorization url that the user should be redirected to.
        '''
        return self._mixin.get_authorize_url(redirect_uri or self._mixin._redirect_uri, **kw)

    def request_access_token(self, code, redirect_uri=None):
        '''
        Return access token as a JsonDict:
        {
            "access_token": "your-access-token",
            "expires": 12345678, # represented using standard unix-epoch-time
            "uid": 1234 # other fields
        }
        '''
        r = self._mixin.request_access_token(code, redirect_uri)
        self._access_token = r.access_token
        return r

    def refresh_token(self, refresh_token):
        req_str = '%s%s' % (self.auth_url, 'access_token')
        r = _http('POST', req_str,
                  client_id=self.client_id,
                  client_secret=self.client_secret,
                  refresh_token=refresh_token,
                  grant_type='refresh_token')
        return self._parse_access_token(r)

    def is_expires(self):
        return not self.access_token or time.time() > self.expires

    def call_api(self, http_method, http_path, **kw):
        method, the_url, headers, params = self._mixin._prepare_api(http_method, http_path, self._access_token, **kw)
        logging.debug('Call API: %s: %s' % (method, the_url))
        try:
            resp = _http(method, the_url, headers, **params)
        except urllib2.HTTPError, e:
            return self._mixin.on_http_error(e)
        r = _parse_json(resp)
        if hasattr(r, 'error_code'):
            raise APIError(r.error_code, r.get('error', ''), r.get('request', ''))
        return r

    def __getattr__(self, attr):
        if hasattr(self._mixin, attr):
            return getattr(self._mixin, attr)
        return _Callable(self, attr)


class _Executable(object):

    def __init__(self, client, method, path):
        self._client = client
        self._method = method
        self._path = path

    def __call__(self, **kw):
        return self._client.call_api(self._method, self._path, **kw)

    def __str__(self):
        return '_Executable (%s %s)' % (self._method, self._path)

    __repr__ = __str__


class _Callable(object):

    def __init__(self, client, name):
        self._client = client
        self._name = name

    def __getattr__(self, attr):
        if attr == 'get':
            return _Executable(self._client, 'GET', self._name)
        if attr == 'post':
            return _Executable(self._client, 'POST', self._name)
        name = '%s/%s' % (self._name, attr)
        return _Callable(self._client, name)

    def __str__(self):
        return '_Callable (%s)' % self._name

    __repr__ = __str__

if __name__ == '__main__':
    APP_KEY = '255479695'
    APP_SECRET = '909e9b6025d5e500577b194bab50e1a6'
    access_token = '2.00fcTNKH0PwxRR53eb3ad4470jtWn3'
    expires = 1393739173.5
    c = APIClient(SinaWeiboMixin, APP_KEY, APP_SECRET, 'https://api.weibo.com/oauth2/default.html', access_token,
                  expires)
    print c.get_openid(access_token)
