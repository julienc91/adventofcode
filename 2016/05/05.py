from hashlib import md5

from utils.cache import pre_compute


def build_cache(door_id) -> list[str]:
    res = []
    for index in range(30_000_000):
        hash_ = md5(f"{door_id}{index}".encode(), usedforsecurity=False).hexdigest()
        if hash_.startswith("00000"):
            res.append(hash_)
    return res


def main1() -> str:
    door_id = input().strip()
    res = ""

    with pre_compute(lambda: build_cache(door_id), 2016, 5) as cache:
        for hash_ in cache:
            res += hash_[5]
            if len(res) >= 8:
                break
    return res


def main2() -> str:
    door_id = input().strip()
    res = [""] * 8

    with pre_compute(lambda: build_cache(door_id), 2016, 5) as cache:
        for hash_ in cache:
            if hash_[5].isdigit():
                n = int(hash_[5])
                if n < len(res) and not res[n]:
                    res[n] = hash_[6]
                    if all(res):
                        break
    return "".join(res)
