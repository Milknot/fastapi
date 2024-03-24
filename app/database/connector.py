
from abc import ABC, abstractmethod

class dbConnector(ABC):

    @abstractmethod
    def connect(self):
        return
    
    @abstractmethod
    def close(self):
        return

    @abstractmethod
    def query(self):
        pass
    
    @abstractmethod
    def insert(self):
        pass

    @abstractmethod
    def first(self):
        pass