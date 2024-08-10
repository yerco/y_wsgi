class BaseConfig:
    pass


def merge_configs(primary_config: BaseConfig, fallback_config: BaseConfig) -> BaseConfig:
    merged_config = BaseConfig()

    # Iterate over all attributes in the fallback config
    for attr in dir(fallback_config):
        if not callable(getattr(fallback_config, attr)) and not attr.startswith("__"):
            # Set attribute in merged_config
            setattr(merged_config, attr, getattr(fallback_config, attr))

    # Override with attributes from the primary config if they exist
    for attr in dir(primary_config):
        if not callable(getattr(primary_config, attr)) and not attr.startswith("__"):
            setattr(merged_config, attr, getattr(primary_config, attr))

    return merged_config
