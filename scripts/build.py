from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "src"
DIST = ROOT / "dist"
BUILD = ROOT / "build"
RELEASES = ROOT / "Releases"


def run(command: list[str]) -> None:
    print(f"[RUN] {' '.join(command)}")
    subprocess.run(command, check=True, cwd=ROOT)


def clean() -> None:
    for path in (DIST, BUILD, RELEASES):
        if path.exists():
            shutil.rmtree(path)

    for spec_file in ROOT.glob("*.spec"):
        spec_file.unlink()


def build_executable(script_path: Path, exe_name: str) -> Path:
    run(
        [
            sys.executable,
            "-m",
            "PyInstaller",
            "--clean",
            "--onefile",
            "--name",
            exe_name,
            str(script_path),
        ]
    )
    return DIST / f"{exe_name}.exe"


def package_release(binary_patcher_exe: Path, apply_patch_exe: Path) -> None:
    shutil.copy2(binary_patcher_exe, RELEASES / binary_patcher_exe.name)
    shutil.copy2(apply_patch_exe, RELEASES / apply_patch_exe.name)


def main() -> None:
    clean()
    binary_patcher_exe = build_executable(SRC_DIR / "binary_patcher.py", "binary_patcher")
    apply_patch_exe = build_executable(SRC_DIR / "apply_patch.py", "apply_patch")
    package_release(binary_patcher_exe, apply_patch_exe)
    print("\n构建完成。输出目录:")
    print(f"- 可执行文件: {DIST}")
    print(f"- 发布包: {RELEASES}")


if __name__ == "__main__":
    main()
