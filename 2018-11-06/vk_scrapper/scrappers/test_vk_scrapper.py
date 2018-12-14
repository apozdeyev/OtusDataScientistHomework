import unittest

from scrappers.fake_vk_client import FakeVKClient
from scrappers.vk_scrapper import VKScrapper, count_words_in_post, \
    count_words_in_posts, is_user_deactivated
from storages.memory_storage import MemoryStorage
from utils.json_utils import json2obj


class TestVKScrapper(unittest.TestCase):
    def test_scrap_group(self):
        storage = MemoryStorage()
        client = FakeVKClient()
        scrapper = VKScrapper(client)
        total = 6
        actual_total = scrapper.scrap_group('test', storage, total, 2)

        self.assertEqual(total, actual_total)

        ids = list(storage.read_data())
        self.assertEqual(len(ids), total)

        self.assertEqual(ids, ['34', '47', '79', '84', '177', '219'])

    def test_count_words_in_post(self):
        client = FakeVKClient()
        string, _ = client.wall_get_posts('123', offset=0)
        response = json2obj(string)

        # А вот и официальный репортаж с VK Fest 2018! ❤<br><br>Смотрите и вспоминайте, как это было. Совсем скоро мы поделимся фотографиями из каждой зоны фестиваля. А вы пока не забудьте поделиться своими фотокарточками. <br><br>Вот здесь: vk.com/album-86529522_255347798
        words_count = count_words_in_post(response.response[1])
        self.assertEqual(words_count, 35)

        # Empty string
        words_count = count_words_in_post(response.response[2])
        self.assertEqual(words_count, 0)

        # All posts.
        words_count = count_words_in_posts(response.response[1:])
        # Don't know exactly how much words but sure > 100.
        self.assertGreater(words_count, 100)

    def test_not_deactivated_profile(self):
        client = FakeVKClient()
        string, _ = client.user_get_fields('123')
        self.assertFalse(is_user_deactivated(string))

    def test_deactivated_profile(self):
        string = '{"response":[{"id":225455329,"first_name":"Катя","last_name":"Иванова","deactivated":"deleted","sex":1}]}'
        self.assertTrue(is_user_deactivated(string))



if __name__ == '__main__':
    unittest.main()
