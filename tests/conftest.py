from os import path
from pathlib import Path

import pytest
from pytest_helm_templates import HelmRunner


def charts_path() -> str:
    test_helpers_path = Path(__file__).parent
    _charts_path = test_helpers_path.joinpath("../charts")
    return path.normpath(str(_charts_path.absolute()))


@pytest.fixture
def helm_runner() -> HelmRunner:
    return HelmRunner(cwd=charts_path())
