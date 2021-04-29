import pytest
import platform


def pytest_addoption(parser):
    if str(platform.system()) == 'Windows':
        parser.addoption(
            "--type_connect", action="store", default="ssh", help="coonect"
        )
    else:
        parser.addoption(
            "--type_connect", action="store", default="linux", help="connect"
        )


@pytest.fixture
def type_connect(request):
    return request.config.getoption("--type_connect")
