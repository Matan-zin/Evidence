import os
import json
from threading import Thread
from utilities import approotdir
from plugins.Plugin import Plugin
from utilities.HttpService import HttpService
from concurrent.futures import ThreadPoolExecutor

USERS_PATH = '{0}/saved-evidence/users/'.format(approotdir.ROOT_DIR)
POSTS_PATH = '{0}/saved-evidence/posts/'.format(approotdir.ROOT_DIR)


class DummyApi(Plugin):


    def collect_users(self):
        page = 0
        http = HttpService(headers={'app-id': self.token})
        self.save(USERS_PATH, '{ "evidence": [')
        while(True):
            res = http.get('https://dummyapi.io/data/v1/user?limit=50&page={0}'.format(page))
            if(len(res['data']) == 0):
                break
            for user in res['data']:
                self.save(USERS_PATH, json.dumps(user) + ',')
            page+=1
        self.save(USERS_PATH, ']}')


    
    def collect_comments(self, post):
        http = HttpService(headers={'app-id': self.token})
        response = http.get('https://dummyapi.io/data/v1/post/{0}/comment'.format(post['id']))
        self.save(POSTS_PATH, json.dumps({'post': post, 'comments': response['data']}) + ',')



    def collect_posts_and_comments(self):
        http = HttpService(headers={'app-id': self.token})
        res = http.get('https://dummyapi.io/data/v1/post?limit=50&page=0')

        self.save(POSTS_PATH, '{ "evidence": [')
        with ThreadPoolExecutor(os.cpu_count()) as executer:
            executer.map(self.collect_comments, res['data'])
        self.save(POSTS_PATH, ']}')



    def collect(self) -> None | Exception:
        self.token = input('DummyApi required an app-id token\nPlease Enter your token: ')
            
        http = HttpService(headers={'app-id': self.token})
        http.check_connectivity('https://dummyapi.io/data/v1/post?limit=50&page=0')
        
        targets = [
            self.collect_users, 
            self.collect_posts_and_comments
        ]
        threads = [Thread(target=target) for target in targets]
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()



    def save(self, path: str, data: str) -> None:
        super().save(path, data)



    def run(self) -> None:
        try:
            self.collect()
        except Exception as e:
            print('DummyApi exit with errors', e)





