from dataclasses import dataclass

from utils.parsing import parse_input


@dataclass
class Program:
    id: int
    direct_links: list["Program"]


def parse_programs() -> dict[int, Program]:
    programs_by_id = {}

    def get_program_from_id(program_id: int) -> Program:
        if program_id not in programs_by_id:
            programs_by_id[program_id] = Program(program_id, [])
        return programs_by_id[program_id]

    for line in parse_input():
        left, right = line.split(" <-> ")
        program = get_program_from_id(int(left))
        program.direct_links = [
            get_program_from_id(int(connection_id))
            for connection_id in right.split(", ")
            if int(connection_id) != program.id
        ]
    return programs_by_id


def main1() -> int:
    programs_by_id = parse_programs()
    queue = [programs_by_id[0]]
    group: set[int] = set()
    while queue:
        program = queue.pop(0)
        if program.id not in group:
            group.add(program.id)
            queue += program.direct_links
    return len(group)


def main2() -> int:
    programs_by_id = parse_programs()
    groups: list[set[int]] = []
    queue: list[Program] = []
    while programs_by_id:
        if not queue:
            queue = [programs_by_id.popitem()[1]]
            groups.append(set())

        program = queue.pop(0)
        group = groups[-1]
        if program.id not in group:
            group.add(program.id)
            queue += [
                programs_by_id.pop(link.id)
                for link in program.direct_links
                if link.id in programs_by_id
            ]
    return len(groups)
