import time


class Timer:
    def __init__(self, name: str):
        self.name = name

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.time()
        dt = self.end-self.start
        for unit in ["s", "ms", "us", "ns"]:
            if dt < 1:
                dt *= 1000
            else:
                break

        print(f"{self.name} took {dt:.03f} {unit}")
