from settings import get_config_file, write_default_config


def test_get_config_file():
    write_default_config()
    result = get_config_file()
    assert result is not None


def test_get_default_config_file():
    result = write_default_config()
    # TODO: spy open() function to assert content
    print(result)
    assert 1
