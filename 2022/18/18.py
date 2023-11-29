from utils.parsing import parse_input

Voxel = tuple[int, int, int]


def parse_voxels() -> set[Voxel]:
    res: set[Voxel] = set()
    for line in parse_input():
        x, y, z = line.split(",")
        res.add((int(x), int(y), int(z)))
    return res


def main1() -> int:
    voxels = parse_voxels()
    count_faces = 0
    for x, y, z in voxels:
        for dx, dy, dz in [(1, 0, 0), (0, 1, 0), (0, 0, 1)]:
            for factor in (-1, 1):
                if (x + dx * factor, y + dy * factor, z + dz * factor) not in voxels:
                    count_faces += 1
    return count_faces


def main2() -> int:
    object_voxels = parse_voxels()

    # Find the coordinates of a cuboid surrounding the lava droplet
    x_min, x_max, y_min, y_max, z_min, z_max = 0, 0, 0, 0, 0, 0
    for x, y, z in object_voxels:
        x_min = min(x_min, x - 1)
        x_max = max(x_max, x + 1)
        y_min = min(y_min, y - 1)
        y_max = max(y_max, y + 1)
        z_min = min(z_min, y - 1)
        z_max = max(z_max, y + 1)

    # Find the coordinates of voxels inside that cuboid, that are neither on nor inside the lava droplet:
    # they correspond to water coordinates. For each of themn determine if they are in contact to the lava droplet.
    water_voxels: set[Voxel] = set()
    queue = [(x_min, y_min, z_min)]
    count_faces = 0
    while queue:
        voxel = queue.pop(0)
        x, y, z = voxel
        for dx, dy, dz in [(1, 0, 0), (0, 1, 0), (0, 0, 1)]:
            for factor in (-1, 1):
                x2, y2, z2 = (x + dx * factor, y + dy * factor, z + dz * factor)
                if not x_min <= x2 <= x_max:
                    continue
                if not y_min <= y2 <= y_max:
                    continue
                if not z_min <= z2 <= z_max:
                    continue
                if (x2, y2, z2) in water_voxels:
                    continue
                if (x2, y2, z2) in object_voxels:
                    count_faces += 1
                    continue

                water_voxels.add((x2, y2, z2))
                queue.append((x2, y2, z2))

    return count_faces
