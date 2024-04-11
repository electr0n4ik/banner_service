import unittest
import requests

class TestUserBannerView(unittest.TestCase):
    "Интеграционные тесты"
    tag_id = ''
    feature_id = ''

    # params = {'tag_id': tag_id, 'feature_id': feature_id}
    # user_banner_response = requests.get(self.user_banner_url, params=params, headers=headers)
    # data=json.dumps(body)

    def setUp(self):
        self.base_url = 'http://localhost:8000/'
        self.token_url = self.base_url + 'token/'
        self.banner_url = self.base_url + 'user_banner/'
        self.banners_url = self.base_url + 'banner/'

        self.username = 'test_user'
        self.password = 'test_password'

        response = requests.post(self.token_url, data={
            "is_admin": True,
            'username': self.username, 
            'password': self.password})
        self.token = response.json().get('admin_token')  # user_token

        print(self.token)

    def test_get_banners_with_valid(self):
        headers = {'Authorization': f'{self.token}'}
        response = requests.get(self.banners_url, params={
            'offset': 0,
            'limit': 100,
            'tag_id': None, 
            'feature_id': None}, headers=headers)

        first_banner = response.json()[2]
        print(first_banner)
        self.tag_id = first_banner['tag_ids'][0]
        self.feature_id = first_banner['feature_id']

        self.assertEqual(response.status_code, 200)

        # self.assertIn('error', response.json())

    # def test_get_banner_with_valid(self):

    #     tag_id = '1'
    #     feature_id = '1'

    #     headers = {'Authorization': f'{self.token}'}
    #     response = requests.get(self.banner_url, params={
    #         'tag_id': self.tag_id, 
    #         'feature_id': self.feature_id}, headers=headers)

    #     self.assertEqual(response.status_code, 200)

    #     self.assertIn('title', response.json())
    #     self.assertIn('text', response.json())
    #     self.assertIn('url', response.json())

    # def test_get_banner_with_invalid_ids(self):

    #     tag_id = '999'
    #     feature_id = '999'

    #     headers = {'Authorization': f'{self.token}'}
    #     response = requests.get(self.banner_url, params={'tag_id': tag_id, 'feature_id': feature_id}, headers=headers)

    #     self.assertEqual(response.status_code, 404)

    #     self.assertIn('error', response.json())

if __name__ == '__main__':
    unittest.main()
