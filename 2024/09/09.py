import bisect
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
    right_idx = len(disk) - 1
    max_file_size = len(disk)

    free_space_ranges = [
        (i, size) for i, (file_type, size) in enumerate(disk) if file_type is None
    ]

    while right_idx > 0:
        if disk[right_idx][0] is None:
            right_idx -= 1
            continue

        file_id, file_size = disk[right_idx]
        if max_file_size is not None and file_size >= max_file_size:
            right_idx -= 1
            continue

        for i, (free_space_idx, size) in enumerate(free_space_ranges):
            if free_space_idx >= right_idx:
                max_file_size = min(file_size, max_file_size or file_size)
                break

            if size >= file_size:
                disk[free_space_idx] = (file_id, file_size)
                disk[right_idx] = (None, file_size)
                if size > file_size:
                    disk.insert(free_space_idx + 1, (None, size - file_size))
                    right_idx += 1

                _fill_free_space(free_space_ranges, i, file_size)
                _insert_free_space(free_space_ranges, right_idx, file_size)
                break

        right_idx -= 1

    return disk


def _fill_free_space(
    free_space_ranges: list[tuple[int, int]], idx: int, size: int
) -> None:
    free_space_idx, free_space_size = free_space_ranges[idx]
    if free_space_size > size:
        free_space_ranges[idx] = (free_space_idx + 1, free_space_size - size)
        # shift all following indexes by 1
        for i in range(idx + 1, len(free_space_ranges)):
            free_space_ranges[i] = (
                free_space_ranges[i][0] + 1,
                free_space_ranges[i][1],
            )
    elif free_space_size == size:
        free_space_ranges.pop(idx)
    else:
        raise RuntimeError("Not enough space to insert at this index")


def _insert_free_space(
    free_space_ranges: list[tuple[int, int]], idx: int, size: int
) -> None:
    k = bisect.bisect_left(free_space_ranges, (idx, size))
    if k < len(free_space_ranges) - 1 and free_space_ranges[k + 1][0] == idx + 1:
        # Merge with next free_space range if contiguous
        size += free_space_ranges[k + 1][1]
        free_space_ranges.pop(k + 1)
    if k > 0 and free_space_ranges[k - 1][0] == idx - 1:
        # Merge with previous free_space range if contiguous
        size += free_space_ranges[k - 1][1]
        free_space_ranges.pop(k - 1)
        k -= 1
    free_space_ranges.insert(k, (idx, size))


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
