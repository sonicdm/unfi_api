import unittest
from unfi_api.exceptions import CancelledJobException
from unfi_api.utils import threading
from unfi_api.utils.jobs import Job, Jobs, status
from threading import Thread
import time
import logging


logger = logging.getLogger("jobs")
logger.disabled = False


def test_func(num):
    print(num)
    return num

def slow_func(num):
    print(f"Sleeping for {num} seconds.")
    time.sleep(num)
    return num

class TestJobs(unittest.TestCase):
    def test_non_threaded_job(self):
        output = []



        test_data = [x for x in range(10)]
        job = Job(
            job_id="test_job",
            job_data=test_data,
            job_fn=test_func,
            # job_args=None,
            # job_kwargs={},
            job_output=output,
            threaded=False,
        )
        
        job.start()
        self.assertEqual(job.job_output,test_data)
        pass
    
    
    def test_threaded_job(self):
        test_data = [x for x in range(10)]
        job = Job(
            job_id="test_job",
            job_data=test_data,
            job_fn=test_func,
            # job_args=None,
            # job_kwargs={},
            threaded=True,
        )
        
        job.start()
        self.assertTrue(all(job_data in test_data for job_data in job.job_output))
        pass
    
    
    def test_cancel_job(self):
        test_data = [x for x in range(10)]
        job = Job(
            job_id="test_job",
            job_data=test_data,
            job_fn=slow_func,
            # job_args=None,
            # job_kwargs={},
            # threaded=True,
        )
        with self.assertRaises(CancelledJobException):
            # run the job in a secondary thread then cancel it after 2 seconds
            # this should raise a CancelledJobException
            # create Thread object
            t = Thread(target=job.start, daemon=True)
            # start the thread
            t.start()
            # wait for the thread to start running
            time.sleep(2)
            # cancel the job
            job.cancel()
        self.assertTrue(job.cancelled())
        # self.assertFalse(len(job.job_output) == len(test_data))
        pass

    def test_cancel_job_with_threaded_job(self):

        test_data = [x for x in range(10)]
        job = Job(
            job_id="test_job",
            job_data=test_data,
            job_fn=slow_func,
            # job_args=None,
            # job_kwargs={},
            threaded=True,
        )
        with self.assertRaises(CancelledJobException) as e:
            # run the job in a secondary thread then cancel it after 2 seconds
            # this should raise a CancelledJobException
            # create Thread object
            t = Thread(target=job.start, daemon=True)
            # start the thread
            t.start()
            # wait for the thread to start running
            time.sleep(2)
            # cancel the job
            job.cancel()
        self.assertTrue(job.cancelled())
        print(job.job_output)
        print(test_data)
        self.assertFalse(all(data in job.job_output for data in test_data))
        # self.assertFalse(len(job.job_output) == len(test_data))
        pass