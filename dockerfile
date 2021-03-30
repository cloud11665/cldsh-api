FROM python:3.8

COPY . /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

ENV NUM_WORKERS=4
ENV NUM_THREADS=2
ENV PORT=5001
ENV ENTRY="app:app"

CMD ["gunicorn" \
	,"--bind=0.0.0.0:${PORT}" \
	,"--workers=${NUM_WORKERS}" \
	,"--threads=${NUM_THREADS}" \
	,"--worker_connections=1000" \
	,"--worker-class=uvicorn.workers.UvicornWorker" \
	,"${ENTRY}"]
