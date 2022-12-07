from collections import defaultdict


def get_absolute_path(pwd: list[str]) -> str:
    return "/" + "/".join(pwd)


def get_filesystem_size() -> dict[str, int]:
    size_by_path: dict[str, int] = defaultdict(int)
    pwd: list[str] = []
    try:
        while line := input().strip():
            if line.startswith("$ cd "):
                path = line.split(" ")[-1]
                if path == "/":
                    pwd = []
                elif path == "..":
                    pwd.pop()
                else:
                    pwd.append(path)

            elif line.startswith("$ "):
                continue

            elif line.startswith("dir "):
                continue

            else:
                size, name = line.split(" ", 1)
                for i in range(len(pwd) + 1):
                    absolute_path = get_absolute_path(pwd[:i])
                    size_by_path[absolute_path] += int(size)

    except EOFError:
        pass
    return size_by_path


def main1() -> int:
    size_by_path = get_filesystem_size()
    threshold = 100_000
    return sum(size for size in size_by_path.values() if size <= threshold)


def main2() -> int:
    size_by_path = get_filesystem_size()

    total_space = 70_000_000
    needed_free_space = 30_000_000
    current_occupied_space = size_by_path["/"]
    current_free_space = total_space - current_occupied_space
    target = needed_free_space - current_free_space
    return min(size for size in size_by_path.values() if size >= target)
