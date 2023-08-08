from plugins.Plugin import Plugin
from plugins.dummyApi.DummyApi import DummyApi

api: Plugin = DummyApi()

api.run()