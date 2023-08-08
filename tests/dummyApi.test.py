import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from utilities import approotdir
from utilities.HttpService import HttpService
from plugins.dummyApi.DummyApi import DummyApi

PASS='[Pass]'
FAIL='[Fail]'
USERS_PATH = '{0}/saved-evidence/users/'.format(approotdir.ROOT_DIR)
POSTS_PATH = '{0}/saved-evidence/posts/'.format(approotdir.ROOT_DIR)

## checking for a given bad token 
## should throw an exception with an error of 403 forbidden
try:
    http = HttpService(headers={'app-id': 'bad-token'})
    http.check_connectivity('https://dummyapi.io/data/v1/post?limit=50&page=0')
except Exception as ex:
    if '403 Client Error' in str(ex):
        print(PASS, 'connectivity test')
    else:
        print(FAIL, 'connectivity test')


## checking for fetching data
## should return a json with a data object
try:
    api_token = input('token: ')
    http = HttpService(headers={'app-id': api_token})
    response = http.get('https://dummyapi.io/data/v1/post?limit=50&page=0')
    if response['data']:
        print(PASS, 'fetching data')
except Exception as ex:
    print(FAIL, 'fetching data')


## checking dummyApi for collecting evidences
## should create a folders with a files inside
## saved-evidence directory should be empty before this test 
try:
    dummyApi = DummyApi()
    dummyApi.collect()

    if os.path.exists(USERS_PATH) and os.path.isdir(USERS_PATH):
        if any(os.path.isfile(os.path.join(USERS_PATH, filename)) for filename in os.listdir(USERS_PATH)):
            print(PASS, 'collect users')
        else:
            print(FAIL, 'collect users')
    else:
        print(FAIL, 'collect users')


    if os.path.exists(POSTS_PATH) and os.path.isdir(POSTS_PATH):
        if any(os.path.isfile(os.path.join(POSTS_PATH, filename)) for filename in os.listdir(POSTS_PATH)):
            print(PASS, 'collect posts')
        else:
            print(FAIL, 'collect posts')
    else:
        print(FAIL, 'collect posts')

    print(PASS, 'dummyApi testing')
except Exception as ex:
    print(FAIL, 'dummyApi testing')