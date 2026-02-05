"""
Background Task Manager - Infrastructure Layer
Handles asynchronous processing of long-running tasks
"""
import threading
from queue import Queue
import time
from typing import Callable
from datetime import datetime, timezone
import uuid
from ...domain.types.task_types import TaskStatus
from app.utils.logger_service import get_logger

logger = get_logger(__name__)


class BackgroundTaskManager:
    """Manages background tasks for asynchronous processing"""
    
    def __init__(self, app=None):
        self.app = app  # Store Flask app for context
        self.task_queue = Queue()
        self.task_results = {}
        self.results_lock = threading.Lock()
        self.worker_thread = None
        self.running = threading.Event()
    
    def start(self):
        """Start the background worker thread"""
        if not self.running.is_set():
            self.running.set()
            self.worker_thread = threading.Thread(target=self._worker, daemon=True)
            self.worker_thread.start()
            logger.info("Background task manager started")
    
    def stop(self):
        """Stop the background worker thread"""
        self.running.clear()
        if self.worker_thread and self.worker_thread.is_alive():
            self.worker_thread.join(timeout=5)
        logger.info("Background task manager stopped")
    
    def _worker(self):
        """Worker thread that processes tasks from the queue"""
        while self.running.is_set():
            try:
                if not self.task_queue.empty():
                    task = self.task_queue.get()
                    task_id = task['id']
                    func = task['func']
                    args = task.get('args', ())
                    kwargs = task.get('kwargs', {})
                    
                    # Update task status to processing
                    with self.results_lock:
                        task_result = self.task_results[task_id].copy()
                        task_result['status'] = 'processing'
                        task_result['started_at'] = datetime.now(timezone.utc).isoformat()
                        self.task_results[task_id] = task_result
                    
                    try:
                        if self.app:
                            with self.app.app_context():
                                result = func(*args, **kwargs)
                        else:
                            result = func(*args, **kwargs)
                        
                        with self.results_lock:
                            task_result = self.task_results[task_id].copy()
                            task_result['status'] = 'completed'
                            task_result['result'] = result
                            task_result['completed_at'] = datetime.now(timezone.utc).isoformat()
                            self.task_results[task_id] = task_result
                        logger.info(f"Task {task_id} completed successfully")
                    except Exception as e:
                        logger.error(f"Task {task_id} failed: {str(e)}")
                        with self.results_lock:
                            task_result = self.task_results[task_id].copy()
                            task_result['status'] = 'failed'
                            task_result['error'] = str(e)
                            task_result['completed_at'] = datetime.now(timezone.utc).isoformat()
                            self.task_results[task_id] = task_result
                    
                else:
                    time.sleep(0.1)  # Small sleep to prevent busy waiting
            except Exception as e:
                logger.error(f"Worker thread error: {str(e)}")
                time.sleep(1)
    
    def submit_task(self, func: Callable, *args, **kwargs) -> str:
        """
        Submit a task for background processing
        
        Args:
            func: The function to execute
            *args: Positional arguments for the function
            **kwargs: Keyword arguments for the function
            
        Returns:
            str: Task ID for tracking
        """
        task_id = str(uuid.uuid4())
        
        with self.results_lock:
            self.task_results[task_id] = {
                'status': 'pending',
                'created_at': datetime.now(timezone.utc).isoformat(),
                'started_at': None,
                'completed_at': None,
                'result': None,
                'error': None
            }
        
        task = {
            'id': task_id,
            'func': func,
            'args': args,
            'kwargs': kwargs
        }
        
        self.task_queue.put(task)
        logger.info(f"Task {task_id} submitted for processing")
        return task_id
    
    def get_task_status(self, task_id: str) -> TaskStatus:
        """
        Get the status of a task
        
        Args:
            task_id: The task ID
            
        Returns:
            TaskStatus: Task status information
        """
        with self.results_lock:
            return self.task_results.get(task_id, {'status': 'not_found'})
    
    def cleanup_old_results(self, max_age_seconds: int = 3600):
        """
        Clean up old task results
        
        Args:
            max_age_seconds: Maximum age of results to keep (default 1 hour)
        """
        current_time = datetime.now(timezone.utc)
        to_remove = []
        
        with self.results_lock:
            for task_id, task_info in self.task_results.items():
                completed_at = task_info.get('completed_at')
                if completed_at:
                    completed_time = datetime.fromisoformat(completed_at)
                    age = (current_time - completed_time).total_seconds()
                    if age > max_age_seconds:
                        to_remove.append(task_id)
            
            for task_id in to_remove:
                del self.task_results[task_id]
        
        if to_remove:
            logger.info(f"Cleaned up {len(to_remove)} old task results")
