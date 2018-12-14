# import unittest
#
# from storages.memory_storage import MemoryStorage
#
#
# class TestMemoryStorage(unittest.TestCase):
#     def test_write_and_read(self):
#         storage = MemoryStorage()
#
#         def compare_storage_to_list(desired_lines):
#             checking_lines = list(storage.read_data())
#             self.assertEqual(checking_lines, desired_lines)
#
#         compare_storage_to_list([])
#
#         storage.append_data("1")
#         compare_storage_to_list(["1"])
#
#         storage.write_data(["2", "3"])
#         compare_storage_to_list(["1", "2", "3"])
#
#
# if __name__ == '__main__':
#     unittest.main()
