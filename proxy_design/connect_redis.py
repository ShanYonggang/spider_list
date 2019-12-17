import redis

class RedisClient(object):
    def __init__(self):
        self.key = 'proxy'
        if not hasattr(self, 'pool'):
            self.pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
        self.getConnection()


    def getConnection(self):
        self._conn = redis.StrictRedis(connection_pool=self.pool)


    def add(self, value):
        return self._conn.sadd(self.key, value)


    def random(self):
        return self._conn.srandmember(self.key)


    def delete(self, value):
        return self._conn.srem(self.key, value)


r = RedisClient()