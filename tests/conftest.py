def pytest_configure(config):
    """
    This function is called during pytest configuration.

    It checks if the 'markexpr' option is not set and sets it to 'not integration' by default.
    This ensures that tests marked as 'integration' are skipped by default.

    :param config: The pytest configuration object.
    """
    if not config.option.markexpr:
        setattr(config.option, 'markexpr', 'not integration')
