import sys

import yaml


def validate_primary_key_tag(file_path: str) -> bool:
    """
    Check if there are any primary-key tags in each dbt model.

    Args:
        file_path (str): The path to the YAML file containing the DBT model configurations.

    Returns:
        bool: False if no primary-key tags are found, True otherwise.
    """
    with open(file_path, "r") as file:
        models = yaml.safe_load(file)
        for model in models.get("models", []):
            model_has_primary_key = False
            for column in model.get("columns", []):
                if "primary-key" in column.get("tags", []):
                    model_has_primary_key = True
            if not model_has_primary_key:
                print(f"No primary key found in: {model.get('name')}")
                return False
        return True


def main():
    """
    Main function to validate DBT model configurations for missing primary keys.
    """
    file_path = sys.argv[1]
    if not validate_primary_key_tag(file_path):
        sys.exit(1)


if __name__ == "__main__":
    main()
