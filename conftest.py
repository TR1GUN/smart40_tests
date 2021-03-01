import pytest
import time
import docker


def pytest_addoption(parser):
    parser.addoption(
        "--type_connect", action="store", default="virtualbox", help="my option: type1 or type2"
                    )

@pytest.fixture
def type_connect(request):
    return request.config.getoption("--type_connect")