
from concurrent.futures import ThreadPoolExecutor, as_completed
import concurrent.futures.thread
import logging
logger = logging.getLogger(__name__)

def threader(func, args, callback=None, max_threads=10):
    """
    This function takes in a function and a list of arguments, and runs the
    function with the arguments in a new thread.
    """
    results = []
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
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
    return results