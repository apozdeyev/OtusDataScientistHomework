import unittest
from pathlib import Path

from parsers.vk_parser import VKParser

class TestVKParser(unittest.TestCase):
    def test_profile_parser(self):
        parser = VKParser()
        json_string = '{"response":[{"id":210700286,"first_name":"Lindsey","last_name":"Stirling"}]}'
        profile = parser.parse_profile(json_string)

        self.assertEqual(profile.iloc[0, 0], 210700286)
        self.assertEqual(profile.iloc[0, 1], 'Lindsey')
        self.assertEqual(profile.iloc[0, 2], 'Stirling')

    def test_wall_parser(self):
        parser = VKParser()
        test_file_path = 'parsers/6151.json'
        json_strings = Path(test_file_path).read_text()
        json_strings = list(filter(lambda line: len(line) > 0, json_strings.split('\n')))
        posts = parser.parse_wall(json_strings[0])

        self.assertTrue((posts['id'] != 6151).sum() == 0)
        self.assertEqual(posts.iloc[0, 1], '#НовыйГод2019')

if __name__ == '__main__':
    unittest.main()
