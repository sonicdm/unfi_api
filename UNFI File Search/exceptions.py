
class ViewRequiredException(Exception):
    """
    Raised when a frame is required but not found.
    """
    def __init__(self, message=None):
        self.frame_id = frame_id
        self.message = "Frame {} is required but not found.".format(frame_id)
        super().__init__(self.message)


class UnfiApiClientNotSetException(Exception):
    """
    Raised when a client is required but not found.
    """
    def __init__(self, message=None):
        self.message = "UnfiApiClient is required but not found."
        super().__init__(self.message)