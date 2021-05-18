from fastapi import Response
import rapidjson

def JsonObjResponse(data):
	return Response(content=rapidjson.dumps(data, ensure_ascii=False), media_type="application/json")

def JsonStrResponse(data):
	return Response(content=data, media_type="application/json")
