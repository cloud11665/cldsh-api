from pymemcache.client import base
from pymemcache.serde import pickle_serde
import json

client = base.Client(("127.0.0.1", 11211), serde=pickle_serde)

class __noneVal: ...

def memcache(ttl:int=0):
	def outer(func):
		def inner(*args, **kwargs):
			arghash = hex(hash((args,json.dumps(kwargs, sort_keys=True, default=str))))[2:]
			name = f"{__name__}{func.__name__}_{arghash}"
			ret = client.get(name, __noneVal)
			if ret is __noneVal:
				#print(name, args, kwargs)
				ret = func(*args, **kwargs)
				client.set(name, ret, expire=ttl)
			return ret

		return inner
	return outer

client.Func = memcache
