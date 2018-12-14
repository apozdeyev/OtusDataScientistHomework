import json
import time

from enum import Enum

from utils.json_utils import json2obj


def count_words_in_post(post):
    words_count = len(post.text.split())
    return words_count


def count_words_in_posts(posts):
    total_words = sum(count_words_in_post(post) for post in posts)
    return total_words


def is_user_deactivated(profile_json_string):
    responses_json = json.loads(profile_json_string)
    is_deactivated = 'deactivated' in responses_json['response'][0]
    return is_deactivated


def has_private_wall(profile_json_string):
    responses_json = json.loads(profile_json_string)
    key = 'can_see_all_posts'
    is_private = (key in responses_json['response'][0] and
                  responses_json['response'][0][key] == 0)
    return is_private

class ScrapProfileResult(Enum):
    Success = 0,
    Failed = 1,
    Skip = 2,

class VKScrapper:
    def __init__(self, vk_client):
        """
        Scrap group members and write to storage.
        :param vk_client: VKClient
        :param storage: Storage
        """
        self.__client = vk_client

    def scrap_group(self, group_name, storage, limit=1000, count=1000):
        """
        Returns actual scrapped members count.
        :param group_name:
        :param limit:
        :param count: count per request
        """
        total = 0
        while total < limit:
            string, _ = self.__client.groups_get_members(group_name, offset=total,
                                                      count=count)
            response = json2obj(string)

            received_ids_count = len(response.response.users)
            if received_ids_count > 0:
                count_to_process = min(limit - total, received_ids_count)
                total += count_to_process

                for user_id in response.response.users[:count_to_process]:
                    storage.append_data(str(user_id))
            else:
                break

        return total

    def scrap_profile(self, user_id, storage):
        # Return ScrapProfileResult.
        string, _ = self.__client.user_get_fields(user_id)

        is_success = string is not None
        if not is_success:
            print(f'Failed to scrap profile: {user_id}')
            return ScrapProfileResult.Failed

        is_deactivated = is_user_deactivated(string)
        if is_deactivated:
            print(f'User deactivated: {user_id}')
            return ScrapProfileResult.Skip

        storage.write_data(string)
        return ScrapProfileResult.Success

    def scrap_wall(self, user_id, storage, words_count):
        """
        Return False in case of error otherwise True
        :param words_count: Amount of words we want to gain from user's posts.
        """
        total_words = 0
        offset = 0
        posts = []
        while total_words < words_count:
            string, error_code = self.__client.wall_get_posts(user_id, offset=offset)

            # Skip wall scrapping if it is private.
            if (error_code is not None and
                error_code in [15, 30]):
                return True

            is_success = string is not None
            if not is_success:
                return False

            response = json2obj(string)

            # Save new received posts.
            posts.append(string)
            new_posts = response.response[1:]
            total_words += count_words_in_posts(new_posts)

            if len(new_posts) == 0:
                # All posts have been scrapped
                break

            # Increment offset and request next posts.
            offset += len(new_posts)

            user_posts_count = response.response[0]
            if offset >= user_posts_count:
                # All posts have been scrapped
                break

            # Sleep to prevent more 3 request per second.
            time.sleep(1. / 2.)

        storage.write_data(posts)

        return True
