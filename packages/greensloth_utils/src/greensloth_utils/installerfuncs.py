import os
from pathlib import Path
from typing import Optional

def iterate_files(path_to_scan: Path, model_name: str, target_dir: Path, dirs = ''):

    for src_file in os.scandir(path_to_scan):
        if os.path.isdir(src_file):
            new_dirs = dirs
            new_dirs += src_file.name + '/'

            os.makedirs(
                target_dir / new_dirs,
                exist_ok=True
            )

            iterate_files(src_file, model_name, target_dir, dirs=new_dirs)

        elif os.path.isfile(src_file):
            if src_file.name.endswith('.py'):
                with open(src_file, 'r') as f:
                    content = f.read().replace('{{MODEL_NAME}}', model_name)

                dest = target_dir / dirs / src_file.name

                with open(dest, 'w') as f:
                    f.write(content)


def gs_install(
    model_name: str,
    target_dir: Optional[Path] = None
):
    if target_dir is None:
        target_dir = Path('./')

    try:
        os.makedirs(
            target_dir / model_name,
            exist_ok=False
        )
    except FileExistsError:
        raise FileExistsError(f'There already exists a folder with name "{model_name}"')

    iterate_files(Path(__file__).parent / 'modelinit', model_name, target_dir= target_dir / model_name)