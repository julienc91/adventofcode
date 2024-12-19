import re


def findone(pattern, string, *, group=1) -> str:
    """
    Find the first occurrence of a pattern in a string. Mosty used for convenience
    with type checkers.
    """
    match = re.search(pattern, string)
    if match:
        return match.group(group)
    raise ValueError("Group not found")
