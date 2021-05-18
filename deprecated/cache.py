from functools import lru_cache, wraps
from datetime import datetime, timedelta

def TimedLRUcache(h:int=0,m:int=5,s:int=0):
	def wrapper_cache(func):
		func = lru_cache(1024*64, True)(func)
		func.lifetime = timedelta(hours=h, minutes=m, seconds=s)
		func.expiration = datetime.utcnow() + func.lifetime

		@wraps(func)
		def wrapped_func(*args, **kwargs):
			if datetime.utcnow() >= func.expiration:
				func.cache_clear()
				func.expiration = datetime.utcnow() + func.lifetime

			return func(*args, **kwargs)

		return wrapped_func

	return wrapper_cache

