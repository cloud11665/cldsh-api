from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from vlo import router as vlo

app = FastAPI()

app.add_middleware(
	CORSMiddleware,
	allow_credentials=True,
	allow_origins=["*"],
	allow_methods=["*"],
	allow_headers=["*"],
)
app.add_middleware(
	GZipMiddleware,
	minimum_size=1000,
)

app.include_router(vlo)


if __name__ == "__main__":
	if __import__("os").system("grep -i microsoft /proc/version") == 0:
		exit("Run it using a real operating system.")

	pid = None
	while pid is None:
		__import__("os").system("2>/dev/null 1>&2 memcached &")
		pid = __import__("subprocess").check_output("ps -o 'cmd,pid' | grep '^memcached' | awk '{print $2}'", shell=True)\
					.decode()\
					.strip()
		pid = int(pid) if pid.isdigit() else None

	__import__("uvicorn").run("app:app", port=7001, reload=True, log_level="debug")
	print(f"Killing memcached process [{pid}]")
	__import__("os").system(f"kill -9 {pid}")
