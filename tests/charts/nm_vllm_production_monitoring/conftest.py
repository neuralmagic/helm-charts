import pytest
from pytest_helm_templates import HelmRunner

from tests.test_helpers import make_chart_fixtures, make_helm_runner


CHART_DIR_NAME = "nm-vllm-production-monitoring"


# Override helm_runner fixture so we can use it as a hook to ensure chart
# dependencies are installed.
@pytest.fixture(scope="module")
def helm_runner() -> HelmRunner:
    helm_runner = make_helm_runner()
    helm_runner.dependency_update(chart=CHART_DIR_NAME)
    return helm_runner


make_chart_fixtures(
    chart_dir_name=CHART_DIR_NAME,
    conftest_globals=globals(),
)
