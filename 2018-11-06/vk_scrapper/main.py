import logging
import os
import random
import sys
import glob
import time

import pandas as pd

from pathlib import Path
from parsers.vk_parser import VKParser
from scrappers.preauth_vk_client import PreAuthVKClient
from scrappers.vk_scrapper import VKScrapper, ScrapProfileResult
from storages.file_storage import FileStorage
from utils.user_id_fetcher import UserIDFetcher

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GROUP_MEMBERS_DIR = 'data/groups/'
USER_PROFILES_DIR = 'data/users/profiles/'
USER_WALLS_DIR = 'data/users/walls/'
USER_IDS_FILE_NAME = 'users.csv'
USER_PROFILES_FILE_NAME = 'user_profiles.csv'
USER_POSTS_FILE_NAME = 'user_posts.csv'
PROCESSED_USER_IDS_FILE_NAME = 'users_processed.csv'


def scrap_group(group_name):
    file_path = os.path.join(GROUP_MEMBERS_DIR, group_name + '.csv')
    storage = FileStorage(file_path)
    client = PreAuthVKClient()
    scrapper = VKScrapper(client)
    total = scrapper.scrap_group(group_name, storage, 10000)
    print(f'scrapped {total} group({group_name}) members.')


def combine_groups():
    files = glob.glob(os.path.join(GROUP_MEMBERS_DIR, '*.csv'))
    contents = [pd.read_csv(f).iloc[:, 0] for f in files]
    contents_series = pd.concat(contents, ignore_index=True)
    contents_series.to_csv(USER_IDS_FILE_NAME, index=False)


def scrap_rand_user():
    # Return False in case of error otherwise True
    fetcher = UserIDFetcher(FileStorage(USER_IDS_FILE_NAME),
                            FileStorage(PROCESSED_USER_IDS_FILE_NAME))
    user_id = fetcher.get_not_processed_user_id()
    result = scrap_user(user_id)

    if result:
        fetcher.mark_user_id_as_processed(user_id)

    return result


def scrap_user(user_id):
    # Return False in case of error otherwise True
    print(f'User scrapping start.')

    if user_id is None:
        print('All users processed!')
        return

    client = PreAuthVKClient()
    scrapper = VKScrapper(client)

    # Scrap profile.
    file_path = os.path.join(USER_PROFILES_DIR, user_id + '.json')
    profile_storage = FileStorage(file_path)
    scrap_profile_result = scrapper.scrap_profile(user_id, profile_storage)
    if scrap_profile_result == ScrapProfileResult.Failed:
        print(f'User scrapping failed: {user_id}.')
        return False
    elif scrap_profile_result == ScrapProfileResult.Skip:
        print(f'User scrapping skipped: {user_id}.')
        return True

    # Scrap wall.
    file_path = os.path.join(USER_WALLS_DIR, user_id + '.json')
    wall_storage = FileStorage(file_path)
    success = scrapper.scrap_wall(user_id, wall_storage, 1000)
    if not success:
        print('Failed to request wall posts!')
        return False

    print(f'User scrapping end: {user_id}.')

    return True


def scrap_rand_users():
    count = 0
    while scrap_rand_user():
        count += 1
        print(f'Scrapped {count} users.')
        # Sleep to prevent more 3 request per second.
        time.sleep(1. / 2.)

    print(f'Scrapping users end.')


def print_help():
    print('usage vk_scrapper group [group_name].')


def parse_users():
    files = glob.glob(os.path.join(USER_PROFILES_DIR, '*.json'))
    parser = VKParser()
    contents = [parser.parse_profile(Path(f).read_text()) for f in files]
    df = pd.concat(contents, ignore_index=True)
    df.to_csv(USER_PROFILES_FILE_NAME, index=False)
    print(f'Parsed {len(df)} profiles.')


def parse_walls():
    files = glob.glob(os.path.join(USER_WALLS_DIR, '*.json'))
    parser = VKParser()
    contents = [parser.parse_wall(line)
                for f in files
                    for line in Path(f).read_text().split('\n') if line.split()]
    df = pd.concat(contents, ignore_index=True)
    df.to_csv(USER_POSTS_FILE_NAME, index=False)
    print(f'Parsed {len(df)} posts.')


if __name__ == '__main__':
    logger.info("Work started")

    random.seed()

    if len(sys.argv) == 0:
        print_help()
    elif sys.argv[1] == 'group' and len(sys.argv) == 3:
        scrap_group(sys.argv[2])
    elif sys.argv[1] == 'combine_groups':
        combine_groups()
    elif sys.argv[1] == 'user' and len(sys.argv) == 3:
        scrap_user(sys.argv[2])
    elif sys.argv[1] == 'rand_user':
        scrap_rand_user()
    elif sys.argv[1] == 'users':
        scrap_rand_users()
    elif sys.argv[1] == 'parse_users':
        parse_users()
    elif sys.argv[1] == 'parse_walls':
        parse_walls()
    else:
        print_help()

    logger.info("work ended")
