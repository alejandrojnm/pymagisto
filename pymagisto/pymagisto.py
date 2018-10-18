import datetime
import base64, hmac, hashlib
import json
import requests

class Pymagisto:

    def __init__(self, key, secret):
        self.api_key = key
        self.api_secret = secret
        self.host = 'api.magisto.com'

    def __sign_request(self, url, timestamp):
        canonical = "{}:{}:{}".format(url, self.host, timestamp)
        key_bytes = bytes(self.api_secret, 'utf-8')
        data_bytes = bytes(canonical, 'utf-8')
        sig_hmac = hmac.new(key_bytes, data_bytes, digestmod=hashlib.sha256)
        b64_hmac = base64.encodestring(sig_hmac.digest()).strip()
        return b64_hmac

    def __request(self, path, extra_data=None, protocol='http'):
        if not extra_data or not isinstance(extra_data, dict):
            extra_data = {}

        timestamp = datetime.datetime.utcnow().isoformat("T") + "Z"
        api_signature = self.__sign_request(self.api_key, path, self.host, timestamp)

        data = {'api_key': self.api_key,
                'api_signature': api_signature,
                'api_timestamp': timestamp}

        data.update(extra_data)

        headers = {'Content-Type': 'application/json'}
        response = requests.post('{}://{}{}'.format(protocol, self.host, path), data=json.dumps(data), headers=headers)

        return json.loads(response.text)

    def get_themes(self):
        url = '/v3/musiclib/themes'

        timestamp = datetime.datetime.utcnow().isoformat("T") + "Z"
        sig = self.__sign_request(url, timestamp)

        data = {'api_key': self.api_key,
                'api_signature': sig,
                'api_timestamp': timestamp}

        response = requests.get('https://{}{}'.format(self.host, url), data)

        return response.json()

    def get_tracks(self):
        url = '/v3/musiclib/tracks'

        timestamp = datetime.datetime.utcnow().isoformat("T") + "Z"
        sig = self.__sign_request(url, timestamp)

        data = {'api_key': self.api_key,
                'api_signature': sig.decode("utf-8"),
                'api_timestamp': timestamp
                }

        headers = {'Content-Type': 'application/json'}
        response = requests.post('https://{}{}'.format(self.host, url), json.dumps(data), headers=headers)

        return response.json()

    def create_video(self, image_list, themeid, title=None, ):
        """
        :param image_list: list [{'url': 'https://my-url.s3.amazon.com/test.{png, mp4, gif, jpeg}', 'counter': {1,2,3}, 'text': 'the text for this image'}]
        :param themeid: str
        :param title: str
        :return:
        """
        url = '/v3/video/create'

        timestamp = datetime.datetime.utcnow().isoformat("T") + "Z"
        sig = self.__sign_request(url, timestamp)

        data = {'api_key': self.api_key,
                'api_signature': sig.decode("utf-8"),
                'api_timestamp': timestamp
                }

        sources = []

        for mediaid, media in enumerate(image_list, start=1):

            if mediaid == 1:
                title_type = 'title'
                titles = [title]
            else:
                title_type = 'subtitle'
                titles = media['text']

            sources.append(
                {'url': media['url'], 'mandatory': 'as-is', 'order': media['counter'], 'title_type': title_type,
                 'titles': titles})

        data['sources'] = sources
        data['theme_id'] = themeid
        data['orientation'] = 'portrait'
        data['max_duration'] = '59'

        headers = {'Content-Type': 'application/json'}
        response = requests.post('https://{}{}'.format(self.host, url), json.dumps(data), headers=headers)

        return response.json()

    def get_video(self, video_session_id):
        url = '/v3/video'

        timestamp = datetime.datetime.utcnow().isoformat("T") + "Z"
        sig = self.__sign_request(url, timestamp)

        data = {'api_key': self.api_key,
                'api_signature': sig,
                'api_timestamp': timestamp,
                'video_session_id': video_session_id
                }

        response = requests.get('https://{}{}'.format(self.host, url), data)

        return response.json()
