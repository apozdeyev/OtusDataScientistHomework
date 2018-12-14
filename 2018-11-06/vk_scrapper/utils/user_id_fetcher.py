import random


class UserIDFetcher:
    def __init__(self, pool_storage, processed_storage):
        """
        Allow to read user id and mark it as processed.
        :param pool_storage: Storage
        :param processed_storage: Storage
        """
        self.__pool_storage = pool_storage
        self.__processed_storage = processed_storage


    def get_not_processed_user_id(self):
        pool = set(self.__pool_storage.read_data())
        processed = set(self.__processed_storage.read_data())
        pool_not_processed = pool.difference(processed)
        if len(pool_not_processed) == 0:
            return None

        user_id = random.choice(list(pool_not_processed))
        return user_id

    def mark_user_id_as_processed(self, user_id):
        self.__processed_storage.append_data(user_id)

