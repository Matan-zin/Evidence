import os
from datetime import datetime
from abc import ABC, abstractmethod


class Plugin(ABC):


    def __init__(self):
        self.date = datetime.now().utcnow()


    @abstractmethod
    def run(self):
        pass


    @abstractmethod
    def save(self, path: str, data: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        file_path: str = path + '/{0}.json'.format(self.date)
        with open(file_path, 'a') as f:
                f.write(data)
        pass



