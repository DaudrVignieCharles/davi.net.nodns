#!/usr/bin/python3
# -*-coding:UTF8 -*

from requests import post

class Api():
    def __init__(self, devKey, userKey):
        self.__url = "https://pastebin.com/api/api_post.php"
        self.std_data = {
            "api_dev_key" : devKey,
            "api_user_key" : userKey,
            "api_option" : None
        }

    def paste(self, text, name, expire_date="1D", private=2):
        """data = text that you want paste
        name = name of your paste
        expire_date = paste will be delete after this date
        private = 0 Public, 1 Unlisted, 2 Private
        """
        data = dict(self.std_data)
        data["api_option"] = "paste"
        data["api_paste_name"] = name
        data["api_paste_expire_date"] = expire_date
        data["api_paste_private"] = private
        data["api_paste_code"] = text
        return post(self.__url, data)

    def delete(self, pasteKey):
        data = dict(self.std_data)
        data["api_option"] = "delete"
        data["api_paste_key"] = pasteKey
        return post(self.__url, data)

    def list_paste(self, resultsLimit):
        data = dict(self.std_data)
        data["api_option"] = "list"
        data["results_limit"] = resultsLimit
        return post(self.__url, data)

    def show_paste(self, pasteKey):
        data = dict(self.std_data)
        data["api_option"] = "show_paste"
        data["api_paste_key"] = pasteKey
        return post("https://pastebin.com/api/api_raw.php", data)
