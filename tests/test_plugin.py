import os

import pytest

from poetry_partifact_plugin.plugin import PartifactPlugin


def test_object_initialization():
    """Should correctly initialize the poetry plugin class."""
    plugin = PartifactPlugin()
    assert isinstance(plugin, PartifactPlugin)


def test_get_profile_name(correct_parsed_pyproject_toml):
    """Should get the profile name from a parsed toml object."""
    plugin = PartifactPlugin()

    output = plugin._get_profile_name(correct_parsed_pyproject_toml)
    assert output == "my_source_name"


def test_get_profile_name_no_name(parsed_pyproject_toml_no_name):
    """Should raise a Runtime error if a parsed toml object doesn't have a profile."""
    plugin = PartifactPlugin()

    with pytest.raises(RuntimeError):
        plugin._get_profile_name(parsed_pyproject_toml_no_name)


def test_pyproject_toml_has_codeartifact(correct_parsed_pyproject_toml):
    """Should test if a toml object has codeartifact source in it."""
    plugin = PartifactPlugin()

    output = plugin._pyproject_toml_has_codeartifact(correct_parsed_pyproject_toml)

    assert output is True


def test_pyproject_toml_has_codeartifact_missing(
    parsed_pyproject_toml_with_non_codeartifact_source,
):
    """Should test if a toml object doesn't have a codeartifact source in it."""
    plugin = PartifactPlugin()

    output = plugin._pyproject_toml_has_codeartifact(
        parsed_pyproject_toml_with_non_codeartifact_source
    )

    assert output is False

def test_set_env_vars(mocker, correct_parsed_pyproject_toml):
    """Should test if the right env variables are set."""
    plugin = PartifactPlugin()

    mocked_config = mocker.patch("poetry_partifact_plugin.plugin.Configuration.load")
    mocked_get_token = mocker.patch("poetry_partifact_plugin.plugin.get_token")
    mocked_get_token.return_value = "mocked_token"

    plugin._set_env_vars(correct_parsed_pyproject_toml)

    assert os.getenv("POETRY_HTTP_BASIC_MY_SOURCE_NAME_PASSWORD") == "mocked_token"
    assert os.getenv("POETRY_HTTP_BASIC_MY_SOURCE_NAME_USERNAME") == "aws"

    mocked_config.assert_called_once_with("my_source_name", profile="my_source_name")
    mocked_get_token.assert_called_once_with(mocked_config.return_value)

def test_set_env_vars_no_profile_name(parsed_pyproject_toml_no_name):
    """Should raise an Exception when trying to set env vars for an invalid pyproject.toml file."""
    plugin = PartifactPlugin()

    with pytest.raises(Exception) as exc_info:
        plugin._set_env_vars(parsed_pyproject_toml_no_name)

    assert str(exc_info.value) == "Could not find a valid tool.poetry.source.name field"