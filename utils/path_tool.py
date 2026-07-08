
import os


def get_project_root() -> str:
    # abpath
    current_file =  os.path.abspath(__file__)
    # get root
    current_dir =  os.path.dirname(current_file)
    # get root dir
    project_root = os.path.dirname(current_dir)
    return project_root

def get_abs_path(relative_path: str) -> str:
    project_root = get_project_root()
    return os.path.join(project_root, relative_path)

if __name__ == '__main__':
    print(get_abs_path("config/config.json"))