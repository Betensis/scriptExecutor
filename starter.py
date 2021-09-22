from os import scandir
from pathlib import Path
import subprocess
from typing import Generator

import fire
from fire.core import FireError


class Scripts:
    executors_by_suffix = {".sh": "bash", ".py": "python3.9"}

    @property
    def scripts_dir(self):
        scripts_dir = Path("./scripts")
        if not scripts_dir.exists():
            raise FireError(f"scripts directory {scripts_dir.resolve()} didn't exists")
        if scripts_dir.is_file():
            raise FireError(f"{scripts_dir.resolve()} must be directory not file")
        return scripts_dir

    def _get_all_scripts_files(self) -> Generator[Path, None, None]:
        yield from filter(lambda x: x.is_file(), self.scripts_dir.iterdir())

    def all_scripts(self) -> Generator[str, None, None]:
        """Show all scripts"""
        yield from map(lambda file: file.name, self._get_all_scripts_files())

    def execute(self, file: str) -> None:
        """Execute script by name"""
        if not file in self.all_scripts():
            raise FireError(f"file doesn't exist")

        full_path = self.scripts_dir.joinpath(file)
        file_executor = self.executors_by_suffix[full_path.suffix]
        if not (
            code := subprocess.run(
                [f"{file_executor} {full_path.resolve()}"], shell=True
            )
        ):
            raise FireError(f"script exit with code {code}")


class Starter:
    def __init__(self):
        self.scripts = Scripts()

    def start_all(self):
        """Execute all scripts"""
        for script in self.scripts._get_all_scripts_files():
            print(f'Try execute {script.name}')
            self.scripts.execute(script.name)


if __name__ == "__main__":
    fire.Fire(Starter)
