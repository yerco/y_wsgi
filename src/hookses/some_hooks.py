def before_request_hook():
    print("This runs before each request.")


def after_request_hook():
    print("This runs after each request.")


def teardown_request_hook():
    print("This runs after each request is completed.")


def before_first_request_hook():
    print("This runs only once, before the first request is processed.")
