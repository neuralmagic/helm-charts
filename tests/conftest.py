import pytest
from pytest_helm_templates import HelmRunner

from tests.test_helpers import charts_path


@pytest.fixture(scope="session")
def helm_runner() -> HelmRunner:
    return HelmRunner(cwd=charts_path())
