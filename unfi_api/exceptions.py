from functools import partial
from typing import Callable, Union, Tuple

from decorator import decorator

from unfi_api.utils import ask_yesno


def __retry_with_prompt(
    func,
    exception=Exception,
    prompt: str = "Retry?",
    message="Exception thrown...",
    max_tries: int = None,
    default_prompt_response=True,
) -> Callable:
    tries = 0
    while True:
        try:
            return func()
        except exception as e:
            print(message if message else str(e))
            if max_tries is not None and tries >= max_tries:
                print("Max tries reached.")
                raise
            tries += 1
            if not ask_yesno(prompt, default_prompt_response):
                print("Aborted.")
                raise


def exception_retry_prompt(
    exception: Union[Exception, Tuple[Exception]] = Exception,
    prompt: str = "Retry?",
    message="Exception thrown...",
    max_tries: int = None,
    default_prompt_response=True,
) -> Callable:
    @decorator
    def exception_retry_prompt_decorator(func, *fargs, **fkwargs):
        args = fargs if fargs else list()
        kwargs = fkwargs if fkwargs else dict()
        return __retry_with_prompt(
            partial(func, *args, **kwargs),
            prompt=prompt,
            message=message,
            max_tries=max_tries,
            default_prompt_response=default_prompt_response,
        )
    return exception_retry_prompt_decorator


class JobException(Exception):
    def __init__(self, message=None, job_id=None,  job=None) -> None:
        self.job_id = job_id
        self.job = job
        super().__init__(message)

class CancelledJobException(JobException):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs) 
        
        
class JobRunningException(JobException):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs) 
        
class PausedJobException(JobException):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs) 
        
class JobErrorException(JobException):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)