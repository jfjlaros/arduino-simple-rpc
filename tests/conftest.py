from pytest import fixture, skip


def pytest_addoption(parser: object) -> None:
    parser.addoption('--device', type=str, default='')


@fixture
def device(pytestconfig: object) -> str:
    return pytestconfig.getoption('device')


@fixture(autouse=True)
def test_device(request: object, device: str) -> None:
    if request.node.get_closest_marker('test_device'):
        if request.node.get_closest_marker('test_device').args[0] != device:
            skip('skipped device: not {}'.format(device))


def pytest_configure(config: object) -> None:
    config.addinivalue_line(
        'markers', 'test_device(device): test the given device')
