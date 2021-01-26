import os


def integration_test(f):
    def wrapper(self, *args, **kwargs):
        if os.getenv("WAVYFM_RUN_INTEGRATION_TESTS", "0") == "1":
            f(self, *args, **kwargs)
        else:
            self.skipTest("Integration tests disabled; enable with WAVYFM_RUN_INTEGRATION_TESTS=1")

    return wrapper
