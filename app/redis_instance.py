from threading import Lock
from redis import Redis
    
class SingletonMeta(type):
    _instance = None
    _lock: Lock = Lock()
    

    def __call__(self, *args, **kargs):
        with self._lock:
          if self._instance is None:
              self._instance = super().__call__(*args, **kargs)
        return self._instance
  
  
class Redis_App(metaclass=SingletonMeta):
    def __init__(self):
        self._redis = Redis(host="127.0.0.1", port=6379, password="pa33w0r5", decode_responses=True)
    
    def get_str(self, key):
        return self._redis.get(key)
      
    def set_str(self, key, value):
        return self._redis.set(key, value)

    def hset(self, name, mapping):
        return self._redis.hset(name=name, mapping=mapping)
    


    def hget(self, name, key):
        return self._redis.hget(name=name, key=key)
    
    def hget_all(self, name):
        return self._redis.hgetall(name)
    


