from pathlib import Path
from datetime import datetime, timedelta
from platform import system


def remove_files_older_than(days: int, folder: Path) -> None:
    """
    Removes files in folder if they are older than days passed.
    :param days: number of days
    :param folder: path to folder with files
    :return: None
    """
    now = datetime.now()
    for item in folder.iterdir():
        if item.is_file():
            if system() == 'Windows':
                creation_timestamp = item.stat().st_ctime
            else:
                try:
                    creation_timestamp = item.stat().st_birthtime
                except AttributeError:
                    print('Cannot get file creation time on current OS.')
                    break
            creation_time = datetime.fromtimestamp(creation_timestamp)
            if now - timedelta(days=days) < creation_time:
                item.unlink()


if __name__ == '__main__':
    remove_files_older_than(0, Path(r'path\to\folder'))
