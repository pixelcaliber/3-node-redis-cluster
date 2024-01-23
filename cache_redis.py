import os
import redis

class CacheApp:
    def __init__(self, nodes, redis_host="localhost", redis_port=7002):
        self.nodes = nodes
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_password = redis_password

        self.connections = [
            redis.StrictRedis(
                host=redis_host,
                port=redis_port,
                password=redis_password,
                decode_responses=True
            )
            for _ in nodes
        ]

    def _get_connection(self, key):
        node_index = hash(key) % 3
        return self.connections[node_index]

    def put(self, key, value):
        connection = self._get_connection(key)
        connection.set(key, value)

    def get(self, key):
        connection = self._get_connection(key)
        return connection.get(key)

    def delete(self, key):
        connection = self._get_connection(key)
        connection.delete(key)

if __name__ == "__main__":
    nodes = [7004, 7002, 7003]
    redis_host = "192.168.50.218"
    redis_port = int(os.environ.get("REDIS_PORT", 7002))
    redis_password = 123

    cache_app = CacheApp(nodes, redis_host, redis_port)
    cache_app.put(2, "Abhinav")

    result_before_delete = cache_app.get(2)
    print("Get result for key:", result_before_delete)

    cache_app.delete(2)

    result_after_delete = cache_app.get(2)
    print("Get result for name after deletion:", result_after_delete)
