import os
from pathlib import Path
import subprocess
from typing import Generator, Optional, Union

import fire
from fire.core import FireError


class Scripts:
    def __init__(self):
        self.scripts_dir_environment_name = "SCRIPT_DIR"
        self.executors_by_suffix = {
            ".sh": "bash",
            ".py": "python3",
        }

    @property
    def scripts_dir(self):
        res = self.__get_scripts_dir_path()
        if res is None:
            raise FireError(
                "Invalid scripts directory path. "
                f"The {self.scripts_dir_environment_name} environment variable may have an incorrect value."
            )
        return res

    def set_scripts_dir(self, dir_path: str) -> None:
        """Set scripts directory path"""
        if not self.__is_valid_scripts_dir(dir_path):
            raise FireError(f"Invalid directory path {dir_path}")

        print(os.environ.setdefault(self.scripts_dir_environment_name, dir_path))
        print(f"Current script dir: {dir_path}")

    def __get_scripts_dir_path(self) -> Optional[Path]:
        """Return path if path is valid else return None"""
        dir_path = os.environ.get(self.scripts_dir_environment_name)
        if dir_path is None or not self.__is_valid_scripts_dir(dir_path):
            return None
        return Path(dir_path)

    @staticmethod
    def __is_valid_scripts_dir(path: Union[Path, str]) -> bool:
        if isinstance(path, str):
            path = Path(path)
        return path.exists() and path.is_dir()

    def get_all_scripts_files(self) -> Generator[Path, None, None]:
        yield from filter(lambda x: x.is_file(), self.scripts_dir.iterdir())

    def all_scripts(self) -> Generator[str, None, None]:
        """Show all scripts"""
        yield from map(lambda file: file.name, self.get_all_scripts_files())

    def execute(self, file: str, executor: str = None) -> None:
        """Execute script by file name"""
        if file not in self.all_scripts():
            raise FireError(f"File: {file} doesn't exist")

        full_path = self.scripts_dir.joinpath(file)
        if executor:
            if not (
                code := subprocess.run([f"{executor} {full_path.resolve()}"], shell=True)
            ):
                raise FireError(f"script exit with code {code}")
        if not (code := subprocess.run([f".{full_path.resolve()}"], shell=True)):
            raise FireError(f"script exit with code {code}")


class Starter:
    def __init__(self):
        self.scripts = Scripts()

    def start_all(self) -> None:
        """Execute all scripts"""
        for script in self.scripts.get_all_scripts_files():
            print(f"Try execute {script.name}")
            self.scripts.execute(script.name)

    def execute(self, file: str, executor: str = None) -> None:
        """Execute script by file name"""
        self.scripts.execute(file, executor)


if __name__ == "__main__":
    fire.Fire(Starter)
