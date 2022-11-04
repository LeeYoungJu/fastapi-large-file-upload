import os


def get_file_name_only(file_name_with_ext: str):
    name, _ = os.path.splitext(file_name_with_ext)
    return name

def get_file_ext(file_path: str):
    _, extension = os.path.splitext(file_path)
    return extension[1:]
