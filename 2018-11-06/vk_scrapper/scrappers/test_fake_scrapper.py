# import logging
# import unittest
#
# import dateutil as dateutil
# from mock import mock
#
# from scrappers.fake_spider import FakeSpider
# from scrappers.fake_vk_client import FakeWebClient
# from scrappers.scrapper import Scrapper
# from storages.memory_storage import MemoryStorage
# from utils.list_utils import lmap, lflatten
#
# logging.basicConfig(level=logging.INFO)
#
#
# def _get_rand_delay_factory(delays):
#     def get_rand_delay():
#         if len(delays) == 0:
#             raise Exception('Invalid count of testing delays')
#         delay = delays.pop()
#         return delay
#
#     return get_rand_delay
#
#
# class TestFakeScrapper(unittest.TestCase):
#     @mock.patch('scrappers.scrapper._get_rand_delay')
#     def test_scrapped_pages_content(self, mocked_get_rand_delay):
#         start_urls = ['http://google.com/1', 'http://google.com/2']
#         client = FakeWebClient()
#         storage = MemoryStorage()
#         spider_deep = 6
#         spider = FakeSpider(deep=spider_deep)
#         # Set zero delay in order to speedup test.
#         mocked_get_rand_delay.return_value = 0
#         scrapper_limit = 3
#         scrapper = Scrapper(start_urls,
#                             client,
#                             storage,
#                             spider,
#                             limit=scrapper_limit)
#
#         scrapper.scrap_process()
#
#         reference_limit_per_root_url = min(spider_deep, scrapper_limit)
#         scrapped_data = list(storage.read_data())
#         self.assertEqual(len(scrapped_data),
#                          len(start_urls) * reference_limit_per_root_url)
#
#         scrapped_pages = lmap(lambda line: line.split()[0], scrapped_data)
#
#         def urls_sequence(url):
#             urls = map(lambda j: url + FakeSpider.next_page_keyword * j
#                        , range(reference_limit_per_root_url))
#             return urls
#
#         reference_pages = lflatten(map(urls_sequence, start_urls))
#         self.assertEqual(reference_pages, scrapped_pages)
#
#     testing_delays = [0, 0.5, 1, 2]
#
#     @mock.patch('scrappers.scrapper._get_rand_delay',
#                 new=_get_rand_delay_factory(testing_delays))
#     def test_requests_delay(self):
#         start_urls = ['http://google.com'] * 2
#         client = FakeWebClient()
#         storage = MemoryStorage()
#         spider = FakeSpider()
#         scrapper = Scrapper(start_urls, client, storage, spider)
#         # After scrapping testing_delays will be emptied, so need to copy it
#         # for future check.
#         reference_intervals = self.testing_delays[::-1][:-1]
#         scrapper.scrap_process()
#
#         scrapped_data = list(storage.read_data())
#
#         scrapped_times = lmap(lambda line: dateutil.parser.parse(
#             line.split()[1]), scrapped_data)
#         scrapped_intervals = [
#             (scrapped_times[i + 1] - scrapped_times[i]) for i in
#             range(len(scrapped_times) - 1)]
#         scrapped_intervals = lmap(
#             lambda interval: round(interval.total_seconds(), 1),
#             scrapped_intervals)
#         self.assertEqual(reference_intervals, scrapped_intervals)
#
#     @mock.patch('scrappers.scrapper._get_rand_delay')
#     def test_skipped_requests(self, mocked_get_rand_delay):
#         start_urls = ['http://google.com/1', 'http://google.com/2']
#         client = FakeWebClient([None, start_urls[1], None, start_urls[0]])
#         storage = MemoryStorage()
#         spider = FakeSpider()
#         # Set zero delay in order to speedup test.
#         mocked_get_rand_delay.return_value = 0
#         scrapper = Scrapper(start_urls, client, storage, spider)
#         scrapper.scrap_process()
#
#         scrapped_data = list(storage.read_data())
#         reference_data = start_urls
#         self.assertEqual(reference_data, scrapped_data)
#
#         skipped_pages = scrapper.skipped_pages
#         reference_skipped_pages = ['http://google.com/1/next',
#                                    'http://google.com/2/next']
#         self.assertEqual(reference_skipped_pages, skipped_pages)
#
#
# if __name__ == '__main__':
#     unittest.main()
