import pytest
import platform


def pytest_addoption(parser):
    if str(platform.system()) == 'Windows':
        parser.addoption(
            "--type_connect", action="store", default="ssh", help="Способ коннекта с нашей машиной"
        )
    else:
        parser.addoption(
            "--type_connect", action="store", default="linux", help="Способ коннекта с нашей машиной"
        )


@pytest.fixture
def type_connect(request):
    return request.config.getoption("--type_connect")
