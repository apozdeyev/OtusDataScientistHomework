import abc


class VKClient(object):
    """Abstract class for requesting vk API."""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def groups_get_members(self, group_id, offset, count):
        """
        :return: JSON string
        {
        "response": {
            "count": 4262400,
            "items": [
                34,
                47,
                79,
                ....
        """
        return None

    @abc.abstractmethod
    def wall_get_posts(self, owner_id, offset):
        """
        :return: JSON string
        {
        "response": {
            "count": 34,
            "items": [
                {
                    "id": 210,
                    "from_id": 177,
                    "owner_id": 177,
                    "date": 1506171506,
                    "post_type": "post",
                    "text": "some text",
        """
        return None

    @abc.abstractmethod
    def user_get_fields(self, user_id):
        """
        :return: JSON string
        {
            "response": [
                {
                    "id": 210700286,
                    "first_name": "Lindsey",
                    "last_name": "Stirling"
                    ...
                }
            ]
        }
        """
        return None
