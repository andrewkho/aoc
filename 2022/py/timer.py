from typing import Optional
import time


class Timer:
    def __init__(
        self,
        text_start: Optional[str] = None,
        show_end_text: bool = False,
    ):
        self.text_start = text_start
        self.show_end_text = show_end_text

    def __enter__(self):
        if self.text_start:
            print(self.text_start)
        self.start = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.time()
        dt = self.end-self.start
        for unit in ["s", "ms", "us", "ns"]:
            if dt < 1:
                dt *= 1000
            else:
                break

        if self.show_end_text and self.text_start:
            prefix = self.text_start + " "
        else:
            prefix = ""
            
        print(f"{prefix}took {dt:.03f} {unit}")
