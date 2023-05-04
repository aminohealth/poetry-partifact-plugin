import pytest


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
