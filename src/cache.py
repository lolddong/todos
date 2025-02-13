# /c/Users/관리자/Desktop/projects/todos/src/cache.py 내용
import redis

# 아래와 같이 할 경우 다음 에러 발생: TypeError: Redis.__init__() got an unexpected keyword argument 'decode_response'
# redis_client = redis.Redis(
#     host='127.0.0.1', port=6379, db=0, encoding='UTF-8', decode_response=True
# )

redis_client = redis.Redis(
    host='127.0.0.1', port=6379, db=0, encoding='UTF-8'
)