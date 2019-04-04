from django.test import TestCase, Client
from ShortUrl.settings import STATUS_CODE
import json
from shorturlapp.models import Info
# Create your tests here.


class SetShortUrlTests(TestCase):
    """
    测试setshorturl
    """
    def setUp(self):
        self.client = Client(HTTP_HOST='127.0.0.1:8000')

    def test_format_long_url(self):
        data = {
            'long_url': 'http://www.baidu.com'
        }
        response = self.client.post('/setshorturl/', data)
        self.assertEqual(response.json()['code'], STATUS_CODE['OK'])

        data = {
            'long_url': 'http://www.bai-du.com/1?dsaf!3@.sdf-'
        }
        response = self.client.post('/setshorturl/', data)
        self.assertEqual(response.json()['code'], STATUS_CODE['OK'])

        data = {
            'long_url': 'https://www.baidu.com'
        }
        response = self.client.post('/setshorturl/', data)
        self.assertEqual(response.json()['code'], STATUS_CODE['OK'])

        data = {
            'long_url': 'https://www.bai-du.com/1?dsaf!3@.sdf-'
        }
        response = self.client.post('/setshorturl/', data)
        self.assertEqual(response.json()['code'], STATUS_CODE['OK'])

        data = {
            'long_url': 'HTTPS://BAI-dU.Com/1?dsAf!3@.sdf-'
        }
        response = self.client.post('/setshorturl/', data)
        self.assertEqual(response.json()['code'], STATUS_CODE['OK'])

        data = {
            'long_url': 'www.bai-du.com/1?dsaf!3@.sdf-'
        }
        response = self.client.post('/setshorturl/', data)
        self.assertEqual(response.json()['code'], STATUS_CODE['LONG_URL_FORMAT_ERROR'])

        data = {
            'long_url': 'http://www.baidu.co-m/1?dsaf!3@.sdf-'
        }
        response = self.client.post('/setshorturl/', data)
        self.assertEqual(response.json()['code'], STATUS_CODE['LONG_URL_FORMAT_ERROR'])

        data = {
            'long_url': 'http://www.baid@u.co-m/1?dsaf!3@.sdf-'
        }
        response = self.client.post('/setshorturl/', data)
        self.assertEqual(response.json()['code'], STATUS_CODE['LONG_URL_FORMAT_ERROR'])

        data = {
            'long_url': 'http://fdsafdasfsaf/1?dsaf!3@.sdf-'
        }
        response = self.client.post('/setshorturl/', data)
        self.assertEqual(response.json()['code'], STATUS_CODE['LONG_URL_FORMAT_ERROR'])

        data = {
            'long_url': 'http://fdafasfsafdsaf'
        }
        response = self.client.post('/setshorturl/', data)
        self.assertEqual(response.json()['code'], STATUS_CODE['LONG_URL_FORMAT_ERROR'])

        data = {
            'long_url': 'http://fdafasfsafdsaf/'
        }
        response = self.client.post('/setshorturl/', data)
        self.assertEqual(response.json()['code'], STATUS_CODE['LONG_URL_FORMAT_ERROR'])

        data = {
            'long_url': 'http:///fdafasfsafdsaf/'
        }
        response = self.client.post('/setshorturl/', data)
        self.assertEqual(response.json()['code'], STATUS_CODE['LONG_URL_FORMAT_ERROR'])

        data = {
            'long_url': 'http://www.adfsafdfdsafsadfasfasfasfasfdsafsafsadfsafdsafvdsfgfdg'
                        'gfdsgsdfgsdfgdsgfdsgsdfgsdfgsdfgdsfgsdfgsdfgsdfgsdfgdsfgsdfgsdfgsfd'
                        'gfdsgsdfgsdgfsdgsfdgsdfgsdfgsdfgsdfgdsfg-gfdsgfdsgsfdgds-fg-dfsg-dfsg'
                        'gfdsgfsdgsdfgsdfgsdfgdsfgsdfgdsfgsdfgsdfgsdfgsdfvdsfgdsfgdfgdfsgsdfg'
                        'gfdsgsdfgsdfgfdsgsdfgsdgfsdgsdfgsdfgsdfgsdfgsdfgdfgdfsgsdfgsgfsdgsfdg'
                        'gfdsgsdfgsdfgsdfgsdfgsdfgsdfgfdsgsdfgsdfgdsfgdfsgdsfgsdfgsdfgdsfgdfg'
                        'fdsafasdfasdfa.com'
        }
        response = self.client.post('/setshorturl/', data)
        self.assertEqual(response.json()['code'], STATUS_CODE['LONG_URL_TOO_LONG_ERROR'])

    def test_short_url(self):
        data = {
            'long_url': 'http://www.baidu.com/qwerty',
            'short_url': 'abcdefg'
        }
        response = self.client.post('/setshorturl/', data)
        self.assertEqual(response.json()['code'], STATUS_CODE['OK'])

        data = {
            'long_url': 'http://www.baidu.com/qwerty',
            'short_url': 'abcd😥efg'
        }
        response = self.client.post('/setshorturl/', data)
        self.assertEqual(response.json()['code'], STATUS_CODE['OK'])

        data = {
            'long_url': 'http://www.baidu.com/qwerty',
            'short_url': 'a阿萨!#$%!'
        }
        response = self.client.post('/setshorturl/', data)
        self.assertEqual(response.json()['code'], STATUS_CODE['INPUT_SHORT_URL_ERROR'])

        data = {
            'long_url': 'http://www.baidu.com/qwerty',
            'short_url': 'admin'
        }
        response = self.client.post('/setshorturl/', data)
        self.assertEqual(response.json()['code'], STATUS_CODE['SHOURT_URL_EXIST'])

        data = {
            'long_url': 'http://www.baidu.com/qwerty',
            'short_url': 'setshorturl?123'
        }
        response = self.client.post('/setshorturl/', data)
        self.assertEqual(response.json()['code'], STATUS_CODE['SHOURT_URL_EXIST'])

        data = {
            'long_url': 'http://www.baidu.com/qwerty',
            'short_url': 'admin/123'
        }
        response = self.client.post('/setshorturl/', data)
        self.assertEqual(response.json()['code'], STATUS_CODE['SHOURT_URL_EXIST'])

        data = {
            'long_url': 'http://www.baidu.com/qwerty',
            'short_url': 'admindd?'
        }
        response = self.client.post('/setshorturl/', data)
        self.assertEqual(response.json()['code'], STATUS_CODE['INPUT_SHORT_URL_ERROR'])

        data = {
            'long_url': 'http://www.baidu.com/qwerty',
            'short_url': 'admindd/'
        }
        response = self.client.post('/setshorturl/', data)
        self.assertEqual(response.json()['code'], STATUS_CODE['INPUT_SHORT_URL_ERROR'])

        data = {
            'long_url': 'http://www.baidu.com/qwerty',
            'short_url': 'admindd\\'
        }
        response = self.client.post('/setshorturl/', data)
        self.assertEqual(response.json()['code'], STATUS_CODE['INPUT_SHORT_URL_ERROR'])

        data = {
            'long_url': 'http://www.baidu.com/qwerty',
            'short_url': 'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
                         'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
                         'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
        }
        response = self.client.post('/setshorturl/', data)
        self.assertEqual(response.json()['code'], STATUS_CODE['SHORT_URL_TOO_LONG_ERROR'])

    def test_qrcode(self):
        data = {
            'long_url': 'http://www.baidu.com/qwerty',
            'short_url': 'asdf',
        }
        response = self.client.post('/setshorturl/', data)
        self.assertEqual(response.json()['qrcode'], False)

        data = {
            'long_url': 'http://www.baidu.com/qwerty',
            'short_url': 'asdfgg',
            'qrcode': ''
        }
        response = self.client.post('/setshorturl/', data)
        self.assertEqual(type(response.json()['qrcode']), str)

        data = {
            'long_url': 'http://www.baidu.com/qwerty',
            'short_url': 'asdfg',
            'qrcode': ' '
        }
        response = self.client.post('/setshorturl/', data)
        self.assertEqual(type(response.json()['qrcode']), str)

        data = {
            'long_url': 'http://www.baidu.com/qwerty',
            'short_url': 'asdfggg',
            'qrcode': 'undefine',
        }
        response = self.client.post('/setshorturl/', data)
        self.assertEqual(type(response.json()['qrcode']), str)

        data = {
            'long_url': 'http://www.baidu.com/qwerty',
            'short_url': 'asdfgggg',
            'qrcode': '!da#f*f德萨',
        }
        response = self.client.post('/setshorturl/', data)
        self.assertEqual(type(response.json()['qrcode']), str)

        data = {
            'long_url': 'http://www.baidu.com/qwertydddd',
            'qrcode': '!da#f*f德萨',
        }
        response = self.client.post('/setshorturl/', data)
        self.assertEqual(type(response.json()['qrcode']), str)

        data = {
            'long_url': 'http://www.baidu.com/qwertydddd',
            'qrcode': '!da#f*f德萨',
        }
        response = self.client.post('/setshorturl/', data)
        self.assertEqual(type(response.json()['qrcode']), str)



class RedirectTests(TestCase):
    """
    测试访问短链接跳转
    """
    def setUp(self):
        self.client = Client(HTTP_HOST='127.0.0.1:8000')
        Info.objects.create(long_url='https://www.baidu.com', short_url='123456')
        Info.objects.create(long_url='https://www.baidu.com', short_url='123 56')
        Info.objects.create(long_url='https://www.baidu.com', short_url='123!56')
        Info.objects.create(long_url='https://www.baidu.com', short_url='1aA456')
        Info.objects.create(long_url='https://www.baidu.com', short_url='124😁6')
        Info.objects.create(long_url='https://www.baidu.com', short_url='12是456')
        Info.objects.create(long_url='https://www.baidu.com', short_url='!1@123456范德萨😁!@ 123@!WR1aw-@@@-')

    def test_redirect(self):
        find_obj = Info.objects.get(short_url='123456')
        response = self.client.get('/123456/')
        self.assertEqual(response.url, find_obj.long_url)

        find_obj = Info.objects.get(short_url='123 56')
        response = self.client.get('/123 56/')
        self.assertEqual(response.url, find_obj.long_url)

        find_obj = Info.objects.get(short_url='123!56')
        response = self.client.get('/123!56/')
        self.assertEqual(response.url, find_obj.long_url)

        find_obj = Info.objects.get(short_url='1aA456')
        response = self.client.get('/1aA456/')
        self.assertEqual(response.url, find_obj.long_url)

        find_obj = Info.objects.get(short_url='124😁6')
        response = self.client.get('/124😁6/')
        self.assertEqual(response.url, find_obj.long_url)

        find_obj = Info.objects.get(short_url='!1@123456范德萨😁!@ 123@!WR1aw-@@@-')
        response = self.client.get('/!1@123456范德萨😁!@ 123@!WR1aw-@@@-/')
        self.assertEqual(response.url, find_obj.long_url)









