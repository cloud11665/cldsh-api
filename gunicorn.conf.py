import uvicorn

bind = "127.0.0.1:5001"

workers = 4
worker_connections = 1000
worker_class = uvicorn.workers.UvicornWorker

timeout = 30
keepalive = 2
log_level = "error"
proc_name = "api.sabat.dev"

wsgi_app = "app:app"