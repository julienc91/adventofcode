from hashlib import md5


def main1() -> str:
    door_id = input().strip()
    index = 0
    res = ""
    while len(res) < 8:
        if (hash_ := md5(f"{door_id}{index}".encode()).hexdigest()).startswith("00000"):
            res += hash_[5]
        index += 1
    return res


def main2() -> str:
    door_id = input().strip()
    index = 0
    found = 0
    res = [""] * 8
    while found < len(res):
        if (hash_ := md5(f"{door_id}{index}".encode()).hexdigest()).startswith("00000"):
            if hash_[5].isdigit():
                n = int(hash_[5])
                if n < len(res) and not res[n]:
                    res[n] = hash_[6]
                    found += 1
        index += 1
    return "".join(res)
