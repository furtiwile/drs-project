import os
from gunicorn.arbiter import Arbiter 
from gunicorn.workers.base import Worker
from gunicorn.http.message import Request
from gunicorn.http.wsgi import Response

# Server socket
bind = f"0.0.0.0:{os.getenv('SERVER_PORT', '5000')}"
backlog = 2048

# Worker processes
workers = int(os.getenv('GUNICORN_WORKERS', '1'))
worker_class = 'gevent'
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 120
keepalive = 5

# Logging
accesslog = '-'  # Log to stdout
errorlog = '-'   # Log to stderr
loglevel = os.getenv('LOG_LEVEL', 'info')
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = 'server'

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL
# keyfile = None
# certfile = None

# Server hooks
def on_starting(server: Arbiter) -> None:
    """Called just before the master process is initialized."""
    server.log.info("Starting Server with Gunicorn + Gevent") # type: ignore

def on_reload(server: Arbiter) -> None:
    """Called to recycle workers during a reload via SIGHUP."""
    server.log.info("Reloading Server") # type: ignore

def when_ready(server: Arbiter) -> None:
    """Called just after the server is started."""
    server.log.info("Server is ready to handle requests") # type: ignore

def on_exit(server: Arbiter) -> None:
    """Called just before exiting Gunicorn."""
    server.log.info("Shutting down Server") # type: ignore

def worker_int(worker: Worker) -> None:
    """Called when a worker receives the SIGINT or SIGQUIT signal."""
    worker.log.info("Worker received INT or QUIT signal")

def pre_fork(server: Arbiter, worker: Worker) -> None:
    """Called just before a worker is forked."""
    pass

def post_fork(server: Arbiter, worker: Worker) -> None:
    """Called just after a worker has been forked."""
    server.log.info(f"Worker spawned (pid: {worker.pid})") # type: ignore

def pre_exec(server: Arbiter) -> None:
    """Called just before a new master process is forked."""
    server.log.info("Forked child, re-executing") # type: ignore

def pre_request(worker: Worker, req: Request) -> None:
    """Called just before a worker processes the request."""
    worker.log.debug(f"{req.method} {req.path}")

def post_request(worker: Worker, req: Request, environ: dict[str, str], resp: Response) -> None:
    """Called after a worker processes the request."""
    pass

def child_exit(server: Arbiter, worker: Worker) -> None:
    """Called just after a worker has been exited."""
    server.log.info(f"Worker exited (pid: {worker.pid})") # type: ignore

def worker_abort(worker: Worker) -> None:
    """Called when a worker received the SIGABRT signal."""
    worker.log.info("Worker received SIGABRT signal")

def nworkers_changed(server: Arbiter, new_value: int, old_value: int) -> None:
    """Called just after num_workers has been changed."""
    server.log.info(f"Number of workers changed from {old_value} to {new_value}") # type: ignore
