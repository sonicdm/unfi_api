from __future__ import annotations
from typing import TYPE_CHECKING, Callable, Dict, Union

from unfi_api.exceptions import JobRunningException

if TYPE_CHECKING:
    from concurrent.futures import Future, ThreadPoolExecutor, ProcessPoolExecutor

from dataclasses import dataclass, field

JOB_STATUSES = ["pending", "running", "finished", "error", "cancelled"]
FINISHED_STATUSES = ["finished", "error", "cancelled"]
RUNNING_STATUSES = ["running"]


@dataclass
class Job:
    """
    This class defines a job.
    possible statuses:
    - pending
    - running
    - finished
    - cancelled
    - error
    """

    job_id: Union[str, int]
    job_fn: Callable
    job_status: str = field(default="pending")
    # args: tuple = field(default_factory=tuple)
    # kwargs: Dict = field(default_factory=dict)
    executor: Union[ThreadPoolExecutor, ProcessPoolExecutor] = None
    error: Exception = None

    def cancel(self) -> None:
        """
        Cancel the job.
        """
        self.end("cancelled")

    def finish(self) -> None:
        """
        Finish the job.
        """
        self.end("finished")

    def run(self, *args) -> None:
        """
        Run the job.
        """
        self.set_status("running")

    def end(self, status="finished") -> None:
        """
        End the job.
        """
        if self.running():
            if self.executor:
                self.executor.shutdown(wait=False)
                self.executor = None
        self.set_status(status)

    def set_status(self, status: str) -> None:
        """
        Set the job status.
        """
        if status not in JOB_STATUSES:
            raise ValueError(
                f"Invalid job status: {status} must be one of {JOB_STATUSES}"
            )
        self.job_status = status

    def exception(self, exception: Exception) -> None:
        """
        Set the exception.
        """
        self.error = exception
        self.job_status = "error"
        raise exception

    def fn(self, *args, **kwargs) -> Callable:
        """
        Get the function.
        """
        try:
            return self.job_fn(*args, **kwargs)
        except Exception as e:
            self.exception(e)

    def start(self, *args, **kwargs) -> None:
        """
        Start the job.
        """
        if not self.running():
            self.run()
            self.fn(*args, **kwargs)

    # status checks
    def ended(self) -> bool:
        """
        Check if the job is ended.
        """
        return self.job_status in FINISHED_STATUSES

    def cancelled(self) -> bool:
        """
        Check if the job is cancelled.
        """
        return self.job_status == "cancelled"

    def pending(self) -> bool:
        """
        Check if the job is pending.
        """
        return self.job_status == "pending"

    def finished(self) -> bool:
        """
        Check if the job is finished.
        """
        return self.job_status == "finished"

    def running(self) -> bool:
        """
        Check if the job is running.
        """
        return self.job_status in RUNNING_STATUSES

    def errored(self) -> bool:
        """
        Check if the job is errored.
        """
        return self.job_status == "error"


@dataclass
class Jobs:
    jobs: Dict[str, Job] = field(default_factory=dict)

    def create_job(
        self,
        job_id: Union[str, int],
        job_fn: Callable,
        executor: Union[ThreadPoolExecutor, ProcessPoolExecutor] = None,
    ) -> Job:
        if job_id in self.jobs:
            if self.jobs[job_id].ended():
                del self.jobs[job_id]
            else:
                job = self.jobs[job_id]
                raise JobRunningException(
                    f"Job: {job_id} exists and status is: {job.job_status}"
                )
        job =Job(job_id, executor=executor, job_fn=job_fn)
        self.add_job(job)
        return job

    def add_job(self, job: Job) -> None:
        """
        Add a job to the list of jobs.
        """
        self.jobs[job.job_id] = job

    def cancel_job(self, job_id: Union[str, int]) -> None:
        """
        Cancel the job.
        """
        self.jobs[job_id].cancel()

    def get_job(self, job_id: Union[str, int]) -> Job:
        """
        Get the job.
        """
        return self.jobs[job_id]

    def delete_job(self, job_id: Union[str, int]) -> None:
        """
        Delete the job.
        """
        del self.jobs[job_id]

    def get_job_status(self, job_id: Union[str, int]) -> str:
        """
        Get status of a job.
        """
        return self.jobs[job_id].job_status

    def set_job_status(self, job_id: Union[str, int], status: str) -> None:
        """
        Set the status of a job.
        """
        self.jobs[job_id].set_status(status)

    def get_running_jobs(self) -> Dict[str, Job]:
        """
        return dict of running jobs
        """
        return {job_id: job for job_id, job in self.jobs.items() if job.running()}

    def get_finished_jobs(self) -> Dict[str, Job]:
        """
        return dict of running jobs
        """
        return {job_id: job for job_id, job in self.jobs.items() if job.finished()}

    def get_failed_jobs(self) -> Dict[str, Job]:
        """
        get dict of jobs that failed
        """
        return {job_id: job for job_id, job in self.jobs.items() if job.errored()}

    def get_jobs(self) -> Dict[str, Job]:
        """
        Get the list of jobs.
        """
        return self.jobs

    def __getitem__(self, job_id: Union[str, int]) -> Job:
        """
        Get the job.
        """
        return self.jobs[job_id]

    def __setitem__(self, job_id: Union[str, int], job: Job) -> None:
        """
        Set the job.
        """
        self.jobs[job_id] = job

    def __iadd__(self, job: Job) -> "Jobs":
        """
        Add a job to the list of jobs.
        """
        self.add_job(job)
        return self

    def __add__(self, job: Job) -> "Jobs":
        """
        Add a job to the list of jobs.
        """
        self.add_job(job)
        return self

    def __contains__(self, job_id: Union[str, int]) -> bool:
        """
        Check if the job is in the list of jobs.
        """
        return job_id in self.jobs
