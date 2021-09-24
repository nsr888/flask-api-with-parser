import time


def is_timeout(start_time, timeout):
    diff = int(time.time() - start_time)
    print("Execution time:", diff)
    if diff > timeout:
        return True
    return False
