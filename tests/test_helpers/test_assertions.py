from typing import Any, Dict, List, Set, Tuple, Union


def assert_dependency_value_override(
    dependency_computed_values: Dict,
    dependency_default_values: Dict,
    expected_default_value: Any,
    expected_override_value: Any,
    path: List[Union[int, str]],
) -> None:
    # First, check the expected default value is there to help detect if a config moves
    _target = dependency_default_values
    for path_component in path:
        _target = _target[path_component]
    assert _target == expected_default_value

    # Now it's safe to check the expected override value
    _target = dependency_computed_values
    for path_component in path:
        _target = _target[path_component]
    assert _target == expected_override_value


def assert_values_are_known_to_schema(
    chart_values: Dict,
    chart_values_schema: Dict,
) -> None:
    chart_values_paths = _get_nested_paths(chart_values)
    chart_values_schema_paths = _get_values_schema_paths(chart_values_schema)

    assert chart_values_paths == chart_values_schema_paths, (
        "Values in values.yaml (left set) do not match values in values.schema.json"
        " (right set)"
    )


def _get_values_schema_paths(
    nested_dict: Dict,
    current_path: Tuple[str, ...] = (),
) -> Set[Tuple[str]]:
    paths = set()
    # Skip the first layer of the schema and jump straight to properties
    _nested_dict = nested_dict if len(current_path) > 0 else nested_dict["properties"]

    for key, value in _nested_dict.items():
        new_path = current_path + (key,)
        if value["type"] == "object" and "properties" in value:
            paths.update(
                _get_values_schema_paths(
                    _nested_dict[key]["properties"],
                    new_path,
                )
            )
        else:
            paths.add(new_path)

    return paths


def _get_nested_paths(
    nested_dict: Dict,
    current_path: Tuple[str, ...] = (),
) -> Set[Tuple[str]]:
    paths = set()
    for key, value in nested_dict.items():
        new_path = current_path + (key,)
        if value and isinstance(value, dict):
            paths.update(_get_nested_paths(value, new_path))
        else:
            paths.add(new_path)
    return paths
