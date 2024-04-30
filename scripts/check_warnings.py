import sys

import yaml


def check_tests_for_warn(file_path: str) -> bool:
    """
    Check if any DBT test configurations in a YAML file have a severity level of "warn" or use `warn_if` conditions.

    Args:
    file_path (str): The path to the YAML file containing the DBT model configurations.

    Returns:
    bool: True if no test with "warn" severity or `warn_if` condition is found, False otherwise.
    """
    with open(file_path, "r") as file:
        project_config = yaml.safe_load(file)
        for model in project_config.get("models", []):
            for column in model.get("columns", []):
                for test in column.get("tests", []):
                    if isinstance(test, dict):
                        if test.get("severity") == "warn" or "warn_if" in str(test):
                            print(f"Warning found in test configuration: {test}")
                            return False
    return True


def main():
    files = sys.argv[1:]
    errors = False
    for file_path in files:
        if not check_tests_for_warn(file_path):
            print(f"Error: Errors found in test {file_path}")
            errors = True
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
