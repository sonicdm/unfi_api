import concurrent.futures.thread
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor
from typing import Callable, Dict, Union
from dataclasses import dataclass, field
from unfi_api.exceptions import CancelledJobException
from unfi_api.utils.jobs import Job, Jobs

logger = logging.getLogger(__name__)
cancel = False
job_executors: Dict[Union[str, int], ThreadPoolExecutor] = {}  # job_id: executor
job_status: Dict[str, str] = {}  # job_id: status

jobs: Jobs = Jobs()


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
        job = Job(job_id=job_id, executor=executor, job_fn=func, job_status="pending")
        jobs.add_job(job)
        job.run()
        futures = [executor.submit(job.fn, arg) for arg in args]
        try:
            for future in as_completed(futures):
                try:
                    result = future.result()
                    if job.job_status == "running":
                        results.append(result)
                        if callback:
                            callback(result)
                    elif job.cancelled():
                        raise CancelledJobException(f"Job {job_id} cancelled")
                except CancelledJobException:
                    job.end("cancelled")
                    break
                except Exception as exc:
                    logger.exception("Something went wrong...")
                    raise
                except KeyboardInterrupt:
                    executor.shutdown(wait=False)
                    raise
        except KeyboardInterrupt:

            executor._threads.clear()
            concurrent.futures.thread._threads_queues.clear()
            raise
        finally:
            job.finish()
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


