import sqlite3
import os.path

from entity.user_entity import UserEntity
class UserProvider:
    _instance = None
    user=None

    def __new__(self, *args, **kwargs):
        if not self._instance:
            self._instance = super().__new__(self, *args, **kwargs)
        return self._instance
    
    
    def initialize_user(self,user:UserEntity):
        self.user=user
        
    
    def logout_user(self):
        self._instance=None
        
        
        
        