from typing import Dict

from tests.test_helpers.test_assertions import assert_values_are_known_to_schema


def test_values_are_known_to_schema(
    chart_values: Dict,
    chart_values_schema: Dict,
) -> None:
    assert_values_are_known_to_schema(
        chart_values=chart_values,
        chart_values_schema=chart_values_schema,
    )
