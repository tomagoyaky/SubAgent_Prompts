"""
Thread Pool Manager
Provides thread pool and task queue functionality
"""

import concurrent.futures
import queue
import threading
from typing import Callable, Any, Optional
from .logger import global_logger as logger


class ThreadPoolManager:
    """
    Thread pool manager for managing concurrent tasks
    """

    def __init__(self, max_workers: int = 4):
        """
        Initialize thread pool manager

        Args:
            max_workers: Maximum number of worker threads
        """
        self.max_workers = max_workers
        self.executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=max_workers,
            thread_name_prefix="AutoAgentWorker"
        )
        self.task_queue = queue.Queue()
        self.active_tasks = {}  # Map of task IDs to futures
        self.task_counter = 0
        self.lock = threading.Lock()

    def submit_task(self, func: Callable, *args, **kwargs) -> int:
        """
        Submit a task to the thread pool

        Args:
            func: Function to execute
            *args: Positional arguments for the function
            **kwargs: Keyword arguments for the function

        Returns:
            Task ID
        """
        with self.lock:
            task_id = self.task_counter
            self.task_counter += 1

        # Submit task to executor
        future = self.executor.submit(func, *args, **kwargs)
        
        # Store future
        with self.lock:
            self.active_tasks[task_id] = future
        
        # Add callback to clean up
        future.add_done_callback(lambda f: self._task_completed(task_id))
        
        logger.info(f"Submitted task {task_id} to thread pool")
        return task_id

    def _task_completed(self, task_id: int):
        """
        Callback when task is completed

        Args:
            task_id: Task ID
        """
        with self.lock:
            if task_id in self.active_tasks:
                del self.active_tasks[task_id]
                logger.info(f"Task {task_id} completed and removed from active tasks")

    def get_task_result(self, task_id: int, timeout: Optional[float] = None) -> Any:
        """
        Get result of a task

        Args:
            task_id: Task ID
            timeout: Optional timeout in seconds

        Returns:
            Task result

        Raises:
            ValueError: If task ID is not found
            concurrent.futures.TimeoutError: If task times out
        """
        with self.lock:
            if task_id not in self.active_tasks:
                raise ValueError(f"Task {task_id} not found")
            future = self.active_tasks[task_id]

        return future.result(timeout=timeout)

    def shutdown(self, wait: bool = True):
        """
        Shutdown the thread pool

        Args:
            wait: Whether to wait for all tasks to complete
        """
        logger.info(f"Shutting down thread pool with {len(self.active_tasks)} active tasks")
        self.executor.shutdown(wait=wait)
        logger.info("Thread pool shutdown completed")

    def get_active_task_count(self) -> int:
        """
        Get number of active tasks

        Returns:
            Number of active tasks
        """
        with self.lock:
            return len(self.active_tasks)

    def is_task_done(self, task_id: int) -> bool:
        """
        Check if a task is done

        Args:
            task_id: Task ID

        Returns:
            Whether task is done
        """
        with self.lock:
            if task_id not in self.active_tasks:
                return True
            future = self.active_tasks[task_id]

        return future.done()


# Global thread pool manager instance
thread_pool_manager = ThreadPoolManager()