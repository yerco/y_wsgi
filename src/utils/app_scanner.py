import os


def get_user_apps(base_dir=None):
    apps = []
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(os.path.dirname(current_dir)) if base_dir is None else base_dir

    for entry in os.listdir(parent_dir):
        if os.path.isdir(os.path.join(parent_dir, entry)) and entry.endswith('_app'):
            apps.append(entry)

    return apps
