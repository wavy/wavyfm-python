class WavyException(Exception):
    """An error!"""

    def __init__(self,
                 message: str,
                 error_status: int = None,
                 error_code=None,
                 error_detail=None,
                 *args, **kwargs):
        self.error_name = message
        self.error_code = error_code
        self.error_status = error_status
        self.error_detail = error_detail
        self.__dict__.update(kwargs)
        super().__init__(message, *args)
