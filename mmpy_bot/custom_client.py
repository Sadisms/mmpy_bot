import sys

from httpx import ConnectTimeout
from mattermostautodriver import Client


class CustomClient(Client):

    def __init__(
        self,
        options,
        request_timeout: int = 5,
        request_timeout_files: int = 60,
        count_request_attempts: int = 5
    ):
        super().__init__(options)

        self.request_timeout_custom = request_timeout
        self.request_timeout_files = request_timeout_files
        self.count_request_attempts = count_request_attempts

    def make_request(self, method, endpoint, options=None, params=None, data=None, files=None, basepath=None):
        count_execute = 0
        while True:
            try:
                request, url, request_params = self._build_request(method, options, params, data, files, basepath)

                request_params["timeout"] = self.request_timeout_custom
                if sys.getsizeof(data) > 1024 * 10:  # 10kb
                    request_params["timeout"] = self.request_timeout_files

                response = request(url + endpoint, **request_params)

                self._check_response(response)
                return response

            except ConnectTimeout as e:
                if count_execute < self.count_request_attempts:
                    count_execute += 1
                    continue

                raise e
