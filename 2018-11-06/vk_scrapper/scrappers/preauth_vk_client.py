import logging
import requests
from requests import ReadTimeout

from scrappers.vk_client import VKClient

logger = logging.getLogger(__name__)
TIMEOUT = 5
TIMEOUT_REPEAT_COUNT = 10


class PreAuthVKClient(VKClient):
    """Class for calling VK API under preauthenticated account."""

    def __init__(self):
        # This not commited python file contains only one var VK_APP_TOKEN.
        # Hot to obtain own such token you can read here https://vk.com/dev/first_guide
        # App auth url https://oauth.vk.com/authorize?client_id=6751508&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends&response_type=token&v=5.52
        from scrappers.vk_token import VK_APP_TOKEN
        self.__access_token = VK_APP_TOKEN

    def __combine_params(self, params):
        result = {
            'access_token': self.__access_token,
            'version': '5.87',
        }

        if params is not None:
            result.update(params)

        return result

    def __construct_url(self, end_point):
        url = f'https://api.vk.com/method/{end_point}'
        return url

    def __get_error_code(self, response):
        # Returns int error code or None.
        # error string {"error":{"error_code":5,"error_msg":"User authorization failed: access_token has expired.","request_params":[{"key":"oauth","value":"1"},{"key":"method","value":"wall.get"},{"key":"version","value":"5.87"},{"key":"owner_id","value":"-86529522"},{"key":"offset","value":"0"},{"key":"filter","value":"owner"}]}}
        json = response.json()
        error_code = None
        if 'error' in json:
            error_code = json['error']['error_code']
        return error_code


    def base_request(self, end_point, params=None):
        """
        :param params: request specific params.
        :return: JSON response or None in case of error, VK API Error code or None.
        """
        logger.info('requesting API: ' + end_point)

        final_params = self.__combine_params(params)
        url = self.__construct_url(end_point)

        headers = {
            'content-type': 'application/json; charset=utf-8',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:63.0) Gecko/20100101 Firefox/63.0',
            'Host': 'api.vk.com',
        }

        response = None
        repeat_count = TIMEOUT_REPEAT_COUNT
        while response is None and repeat_count > 0:
            try:
                response = requests.get(url, params=final_params, timeout=TIMEOUT, headers=headers)
            except ReadTimeout:
                repeat_count -= 1
                logger.info('request timeout, tries count: {}'
                            .format(repeat_count))
            except Exception as ex:
                logger.info('request failed: {}'
                            .format(ex))

        if response is not None:
            logger.info('requesting page completed, response HTTP status: {}, '
                        'response content length: {}'
                        .format(response.status_code, len(response.content)))
            error_code = self.__get_error_code(response)
            is_error = response.text is None or error_code is not None
            if is_error:
                print(f'Request failed: {response.text}')
            response = None if is_error else response.text
            return response, error_code
        else:
            logger.info('requesting page failed')
            return None, None

    def groups_get_members(self, group_id, offset, count=1000):
        end_point = 'groups.getMembers'
        params = {
            'group_id': group_id,
            'offset': offset,
            'count': count,
        }
        response = self.base_request(end_point, params)
        return response

    def wall_get_posts(self, owner_id, offset):
        end_point = 'wall.get'
        params = {
            'owner_id': owner_id,
            'offset': offset,
            'filter': 'owner',
            'count': 100,
        }
        response = self.base_request(end_point, params)
        return response

    def user_get_fields(self, user_id):
        end_point = 'users.get'
        params = {
            'user_id': user_id,
            'fields': ','.join(['can_see_all_posts', 'sex', 'bdate', 'city', 'country', 'home_town', 'has_photo', 'domain', 'has_mobile', 'contacts', 'site', 'education', 'universities', 'schools', 'status', 'last_seen', 'followers_count', 'common_count', 'occupation', 'nickname', 'relatives', 'relation', 'personal', 'connections', 'exports', 'activities', 'interests', 'music', 'movies', 'tv', 'books', 'games', 'about', 'quotes', 'screen_name', 'maiden_name', 'career', 'military']),
        }
        response = self.base_request(end_point, params)
        return response

