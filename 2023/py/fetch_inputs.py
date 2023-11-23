import sys
import time
import requests


TEMPLATE: str = "https://adventofcode.com/2023/day/{}/input"
COOKIE_FILE: str = "../.session"
OUTDIR: str = "../inputs"


def readCookie(filename: str) -> str:
    with open(filename, "r") as f:
        cookie = f.readlines()[0].strip()
    return cookie


def main():
    day = int(sys.argv[1])

    t0 = time.time()
    print(f"Reading cookie from {COOKIE_FILE} ...")
    cookie = readCookie(COOKIE_FILE)
    print(cookie)

    url = TEMPLATE.format(day)
    print(f"Reading from {url} ...")

    with requests.session() as s:
        s.cookies.set(name="session", value=cookie)
        resp = s.get(url)
        if not resp.ok:
            raise ValueError(resp)
        
    outpath = f"{OUTDIR}/day{day:02d}.txt"
    print(f"Writing to {outpath} ...")
    with open(outpath, "w") as f:
        f.write(resp.text)
    print("Done!")
    print(f"  took {time.time()-t0:0.06f} s")


if __name__ == '__main__':
    main()
