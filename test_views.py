import unittest
import requests

class TestUserBannerView(unittest.TestCase):
    "Интеграционные тесты"
    tag_id = ''
    feature_id = ''

    def setUp(self):
        self.base_url = 'http://0.0.0.0:8888/'
        self.token_url = self.base_url + 'token/'
        self.banner_url = self.base_url + 'user_banner/'
        self.banners_url = self.base_url + 'banner/'

        self.username = 'test_user'
        self.password = 'test_password'

        response = requests.post(self.token_url, data={
            "is_admin": True,
            'username': self.username, 
            'password': self.password})
        self.token = response.json().get('admin_token')

    def test_get_banners_with_valid(self):
        headers = {'Authorization': f'{self.token}'}
        response = requests.get(self.banners_url, params={
            'offset': 0,
            'limit': 100,
            'tag_id': None, 
            'feature_id': None}, headers=headers)

        first_banner = response.json()[2]
        self.tag_id = first_banner['tag_ids'][0]
        self.feature_id = first_banner['feature_id']

        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
