from os import scandir
from pathlib import Path
import subprocess

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

    def get_all_scripts_files(self) -> list[Path]:
        return [*filter(lambda x: x.is_file(), self.scripts_dir.iterdir())]

    def show(self):
        print(*[file.name for file in self.get_all_scripts_files()])

    def execute(self, file: str):
        if not file in [*map(lambda x: x.name, self.get_all_scripts_files())]:
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
        for script in self.scripts.get_all_scripts_files():
            self.scripts.execute(script.name)


if __name__ == "__main__":
    fire.Fire(Starter)
