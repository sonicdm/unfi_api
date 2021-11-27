
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor
import concurrent.futures.thread
import logging
from os import kill
from typing import Dict, Union
logger = logging.getLogger(__name__)


job_executors: Dict[Union[str,int],ThreadPoolExecutor] = {}

def threader(func, args, callback=None, max_threads=10, job_id=None):
    """
    This function takes in a function and a list of arguments, and runs the
    function with the arguments in a new thread.
    """
    global job_executors
    results = []
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        if not job_id:
            job_id = len(job_executors)
        add_job_executor(job_id, executor)
        futures = [executor.submit(func, arg) for arg in args]
        try:
            for future in as_completed(futures):
                try:
                    result = future.result()
                except Exception as exc:
                    logger.exception("Something went wrong...")
                    raise
                except KeyboardInterrupt:
                    executor.shutdown(wait=False)
                    raise
                    
                results.append(result)
                if callback:
                    callback(result)
        except KeyboardInterrupt:
            executor._threads.clear()
            concurrent.futures.thread._threads_queues.clear()
            raise
        finally:
            del job_executors[job_id]
    return results


def shutdown_executor(executor: Union[ThreadPoolExecutor, ProcessPoolExecutor]):
    """
    This function shuts down the executor.
    """
    executor.shutdown(wait=False)


def kill_all_threads():
    """
    This function kills all threads in the current thread pool.
    """
    concurrent.futures.thread._threads_queues.clear()

def stop_job(job_id):
    """
    This function stops a job.
    """
    global cancel
    cancel = True
    executor = job_executors.get(job_id)
    if executor:
        executor.shutdown(wait=False)
        del job_executors[job_id]

def stop_all_jobs():
    """
    This function stops all jobs.
    """
    for executor in job_executors.values():
        executor.shutdown(wait=False)
    kill_all_threads()
    job_executors.clear()
    
def get_job_executor(job_id):
    """
    This function returns the executor for a job.
    """
    return job_executors.get(job_id)

def get_all_job_executors():
    """
    This function returns all executors.
    """
    return job_executors

def get_all_job_ids():
    """
    This function returns all job ids.
    """
    return job_executors.keys()

def add_job_executor(job_id, executor):
    """
    This function adds an executor to the job executor dictionary.
    """
    job_executors[job_id] = executor
    