import pytest
from pytest_helm_templates import HelmRunner

from tests.test_helpers import make_helm_runner


@pytest.fixture(scope="module")
def helm_runner() -> HelmRunner:
    return make_helm_runner()
