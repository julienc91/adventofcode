from collections.abc import Callable

Disk = list[tuple[int | None, int]]


def parse_disk() -> Disk:
    file_id = 0
    disk = []
    is_file = True
    for c in input():
        if is_file:
            disk.append((file_id, int(c)))
            file_id += 1
        elif c != "0":
            disk.append((None, int(c)))
        is_file = not is_file
    return disk


def defragment_v1(disk: Disk) -> Disk:
    left_idx, right_idx = 0, len(disk) - 1
    while left_idx < right_idx:
        if disk[left_idx][0] is not None:
            left_idx += 1
            continue
        elif disk[right_idx][0] is None:
            right_idx -= 1
            continue

        file_id, file_size = disk[right_idx]
        free_space = disk[left_idx][1]
        if free_space == file_size:
            disk[left_idx] = (file_id, file_size)
            disk[right_idx] = (None, file_size)
        elif free_space >= file_size:
            disk[left_idx] = (file_id, file_size)
            disk[right_idx] = (None, file_size)
            disk.insert(left_idx + 1, (None, free_space - file_size))
            right_idx += 1
        else:
            disk[left_idx] = (file_id, free_space)
            disk[right_idx] = (file_id, file_size - free_space)
            right_idx += 1

        right_idx -= 1
        left_idx += 1
    return disk


def defragment_v2(disk: Disk) -> Disk:
    min_left_idx = 0
    left_idx = min_left_idx
    right_idx = len(disk) - 1
    max_file_size = len(disk)

    while min_left_idx <= left_idx < right_idx:
        if disk[left_idx][0] is not None:
            if min_left_idx == left_idx:
                min_left_idx += 1
            left_idx += 1
        elif disk[right_idx][0] is None:
            right_idx -= 1
        else:
            file_id, file_size = disk[right_idx]
            if max_file_size is not None and file_size >= max_file_size:
                right_idx -= 1
            elif disk[left_idx][1] == file_size:
                disk[left_idx] = (file_id, file_size)
                disk[right_idx] = (None, file_size)
                left_idx = min_left_idx
            elif disk[left_idx][1] > file_size:
                free_space = disk[left_idx][1]
                disk[left_idx] = (file_id, file_size)
                disk[right_idx] = (None, file_size)
                disk.insert(left_idx + 1, (None, free_space - file_size))
                left_idx = min_left_idx
            else:
                left_idx += 1

            if left_idx >= right_idx:
                max_file_size = min(file_size, max_file_size or file_size)

        if left_idx >= right_idx:
            right_idx -= 1
            left_idx = min_left_idx

    for i, c in disk:
        assert c > 0

    return disk


def checksum(disk: Disk) -> int:
    total = 0
    idx = 0
    for file_id, count in disk:
        if file_id is not None:
            total += sum(file_id * (idx + i) for i in range(count))
        idx += count
    return total


def _main(defragmenter: Callable[[Disk], Disk]) -> int:
    disk = parse_disk()
    disk = defragmenter(disk)
    return checksum(disk)


def main1() -> int:
    return _main(defragment_v1)


def main2() -> int:
    return _main(defragment_v2)
