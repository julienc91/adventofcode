from _pytest.config import Config
from _pytest.config.argparsing import Parser
from _pytest.nodes import Node


def pytest_addoption(parser: Parser) -> None:
    parser.addoption(
        "--benchmark", action="store_true", help="only run benchmark tests"
    )


def pytest_configure(config: Config) -> None:
    config.addinivalue_line("markers", "benchmark: only run benchmark tests")


def pytest_collection_modifyitems(config: Config, items: list[Node]) -> None:
    run_benchmark = config.getoption("--benchmark")
    new_items = []
    for item in items:
        mark = item.get_closest_marker("benchmark")
        if mark and run_benchmark:
            new_items.append(item)
        elif not mark and not run_benchmark:
            new_items.append(item)
    items[:] = new_items
