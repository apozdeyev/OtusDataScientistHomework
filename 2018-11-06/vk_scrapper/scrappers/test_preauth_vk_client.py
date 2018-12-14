import unittest
import logging

logging.basicConfig(level=logging.DEBUG)
from scrappers.preauth_vk_client import PreAuthVKClient
from utils.json_utils import json2obj


class TestPreAuthVKClient(unittest.TestCase):
    def test_base_request(self):
        client = PreAuthVKClient()
        end_point = 'account.getProfileInfo'
        string, _ = client.base_request(end_point)
        if string is None:
            print('Service error!')
            return
        response = json2obj(string)
        self.assertTrue(response.response.screen_name == 'anatoliy.pozdeyev')

    def test_user_get_fields(self):
        client = PreAuthVKClient()
        string, _ = client.user_get_fields('151946957')
        if string is None:
            return
        response = json2obj(string)
        self.assertTrue(response.response[0].first_name == 'Анатолий')
        self.assertTrue(response.response[0].sex == 2)
        self.assertTrue(response.response[0].bdate == '21.1.1984')

    def test_groups_get_members(self):
        client = PreAuthVKClient()
        string, _ = client.groups_get_members('europaplus', offset=0)
        if string is None:
            return
        response = json2obj(string)
        self.assertTrue(response.response.count > 0 and
                        len(response.response.users) > 0 and
                        response.response.users[0] > 0)

    def test_wall_get_posts(self):
        client = PreAuthVKClient()
        string, _ = client.wall_get_posts('-86529522', offset=0)
        if string is None:
            return
        response = json2obj(string)
        self.assertTrue(len(response.response) > 1 and
                        type(response.response[0] is int) and
                        response.response[0] > 0)


if __name__ == '__main__':
    unittest.main()
