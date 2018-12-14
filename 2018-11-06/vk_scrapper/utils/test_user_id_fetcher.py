import unittest

from storages.memory_storage import MemoryStorage
from utils.user_id_fetcher import UserIDFetcher


class TestUserIDFetcher(unittest.TestCase):
    def test(self):
        pool = MemoryStorage()
        processed = MemoryStorage()
        fetcher = UserIDFetcher(pool, processed)
        all_entries = set(['1', '2', '3'])
        fetched_reference = all_entries.copy()
        processed_entry = fetched_reference.pop()

        pool.write_data(all_entries)

        processed.append_data(processed_entry)

        fetched = set()
        user_id = fetcher.get_not_processed_user_id()
        fetched.add(user_id)
        self.assertIn(user_id, fetched_reference)
        fetcher.mark_user_id_as_processed(user_id)

        user_id = fetcher.get_not_processed_user_id()
        fetched.add(user_id)
        self.assertIn(user_id, fetched_reference)
        fetcher.mark_user_id_as_processed(user_id)

        self.assertEqual(fetched, fetched_reference)

        user_id = fetcher.get_not_processed_user_id()
        self.assertIsNone(user_id)


if __name__ == '__main__':
    unittest.main()
