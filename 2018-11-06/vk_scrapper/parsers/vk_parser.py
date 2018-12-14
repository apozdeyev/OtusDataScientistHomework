import json
import pandas as pd

def parse_with_dict(key, dict, default=None):
    if key in dict:
        return dict[key]
    else:
        return default


class VKParser(object):
    def parse_profile(self, json_string):
        """
        :param json_string: json with fields
            'id'
            'first_name'
            'last_name'
            'screen_name'
            'maiden_name'
            'nickname'

            'sex': m/f
            'bdate'
            'relation': True/False
            'followers_count'

            'has_photo': True/False
            'status'
            'about'
            'quotes'
            'activities'
            'interests'
            'music'
            'movies'
            'tv'
            'books'
            'games'

            'city'
            'country'
            'home_town'

            'high_education': True/False
            'occupation': work/school/university
            'military': True/False

        :rtype: DataFrame of profile attributes.
        """
        profile = json.loads(json_string)['response'][0]

        user_id = profile['id'] if 'id' in profile else profile['uid']

        first_name = profile['first_name']
        last_name = profile['last_name']
        screen_name = profile.get('screen_name', None)
        maiden_name = profile.get('maiden_name', None)
        nickname = profile.get('nickname', None)

        sex = parse_with_dict(profile.get('sex', ''), {1: 'f', 2: 'm'})
        bdate_string = profile.get('bdate', '')
        bdate = bdate_string if bdate_string is not None and bdate_string.count('.') == 2 else None
        relation = parse_with_dict(profile.get('relation', 0), {1: False, 2: True, 3: True, 4: True, 5: True, 6: False, 7: True, 8: True}, False)
        followers_count = profile.get('followers_count', None)

        has_photo = parse_with_dict(profile.get('has_photo', 0), {1: True, 2: False})
        status = profile.get('status', None)
        about = profile.get('about', None)
        quotes = profile.get('quotes', None)
        activities = profile.get('activities', None)
        interests = profile.get('interests', None)
        music = profile.get('music', None)
        movies = profile.get('movies', None)
        tv = profile.get('tv', None)
        books = profile.get('books', None)
        games = profile.get('games', None)

        # city = profile['city']['title'] if 'city' in profile else None
        city = None
        # country = profile['country']['title'] if 'city' in profile else None
        country = None
        home_town = profile.get('home_town', None)

        high_education = True if 'education' in profile else False
        occupation = profile['occupation']['type'] if 'occupation' in profile else None
        military = True if 'military' in profile else False

        data = [[user_id, first_name, last_name, screen_name, maiden_name, nickname, sex, bdate, relation, followers_count, has_photo, status, about, quotes, activities, interests, music, movies, tv, books, games, city, country, home_town, high_education, occupation, military]]
        columns = ['id', 'first_name', 'last_name', 'screen_name', 'maiden_name', 'nickname', 'sex', 'bdate', 'relation', 'followers_count', 'has_photo', 'status', 'about', 'quotes', 'activities', 'interests', 'music', 'movies', 'tv', 'books', 'games', 'city', 'country', 'home_town', 'high_education', 'occupation', 'military']
        df = pd.DataFrame(data, columns=columns)
        return df

    def parse_wall(self, json_string):
        """
        :param json_string: json with fields: 'from_id', 'text'.
        :return:
        :rtype: DataFrame of wall posts. Columns: 'id', 'text'.
        """
        posts = json.loads(json_string)['response'][1:]
        textual_posts = [post
                         for post in posts
                            if 'text' in post and
                            'from_id' in post and
                            post['text'].strip()]

        data = []
        for post in textual_posts:
            user_id = post['from_id']
            text = post['text']
            data.append((user_id, text))

        columns = ['id', 'text']
        df = pd.DataFrame(data=data, columns=columns)

        return df


