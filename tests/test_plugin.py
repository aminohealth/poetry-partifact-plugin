import pytest

from poetry_partifact_plugin.plugin import PartifactPlugin


@pytest.fixture
def parsed_pyproject_toml_with_non_codeartifact_source() -> dict:
    return {
        "tool": {
            "poetry": {
                "source": [
                    {
                        "url": "https://pypi.org",
                        "name": "my_source_name",
                    }
                ]
            }
        }
    }


@pytest.fixture
def correct_parsed_pyproject_toml() -> dict:
    return {
        "tool": {
            "poetry": {
                "source": [
                    {
                        "url": "https://my-domain-123456789012.d.codeartifact.us-west-2.amazonaws.com/pypi/my-repo/simple/",
                        "name": "my_source_name",
                    }
                ]
            }
        }
    }


@pytest.fixture
def parsed_pyproject_toml_no_name() -> dict:
    return {
        "tool": {
            "poetry": {
                "source": [
                    {
                        "url": "https://my-domain-123456789012.d.codeartifact.us-west-2.amazonaws.com/pypi/my-repo/simple/",
                    }
                ]
            }
        }
    }


def test_object_initialization():
    """Unsure of the best way to test a poetry plugin..."""
    plugin = PartifactPlugin()
    assert isinstance(plugin, PartifactPlugin)


def test_get_profile_name(correct_parsed_pyproject_toml):
    plugin = PartifactPlugin()

    output = plugin._get_profile_name(correct_parsed_pyproject_toml)
    assert output == "my_source_name"


def test_get_profile_name_no_name(parsed_pyproject_toml_no_name):
    plugin = PartifactPlugin()

    with pytest.raises(RuntimeError):
        plugin._get_profile_name(parsed_pyproject_toml_no_name)


def test_pyproject_toml_has_codeartifact(correct_parsed_pyproject_toml):
    plugin = PartifactPlugin()

    output = plugin._pyproject_toml_has_codeartifact(correct_parsed_pyproject_toml)

    assert output is True


def test_pyproject_toml_has_codeartifact_missing(
    parsed_pyproject_toml_with_non_codeartifact_source,
):
    plugin = PartifactPlugin()

    output = plugin._pyproject_toml_has_codeartifact(
        parsed_pyproject_toml_with_non_codeartifact_source
    )

    assert output is False