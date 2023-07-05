from config.models import Config


def test_get_config_file():
    Config._write_default_config()
    result = Config._get_config_file()
    assert result is not None


def test_get_default_config_file():
    result = Config._write_default_config()
    # TODO: spy open() function to assert content
    print(result)
    assert 1
