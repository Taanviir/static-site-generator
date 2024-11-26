import os
import shutil


def copytree(src_dir: str, dest_dir: str) -> None:
    if not os.path.exists(src_dir):
        raise ValueError("Source directory does not exist!")

    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    for filename in os.listdir(src_dir):
        file_path = os.path.join(src_dir, filename)
        dest_path = os.path.join(dest_dir, filename)

        if os.path.isfile(file_path):
            shutil.copy(file_path, dest_path)
        else:
            copytree(file_path, dest_path)
