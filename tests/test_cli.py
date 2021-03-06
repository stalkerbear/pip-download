import json
from pathlib import Path

from click.testing import CliRunner
from pipdownload import settings
from pipdownload.cli import pipdownload


# TODO: How to avoid the situation where there has already been a config file.
def test_download_click_package(tmp_path: Path):
    runner = CliRunner()
    result = runner.invoke(pipdownload, ["click==7.0", "-d", str(tmp_path)])
    assert result.exit_code == 0
    files = list(tmp_path.iterdir())
    assert len(files) == 2


# Add-on for ignoring unused version - Conflict between platform and version check #13
# --python-version py3 --python-version cp37 --platform-tag manylinux1_x86_64 --dest . --no-source beautifulsoup4==4.8.2
# Should download beautifulsoup4-4.8.2-py3-none-any.whl, soupsieve-2.0.1-py3-none-any.whl
# NOT TO BE DOWNLOADED :  beautifulsoup4-4.8.2-py2-none-any.whl
def test_download_bs4_package(tmp_path: Path):
    runner = CliRunner()
    result = runner.invoke(pipdownload, ["--python-version", "py3", "--python-version", "cp37",
                                         "--platform-tag", "manylinux1_x86_64", "-d", str(tmp_path), "--no-source",
                                         "beautifulsoup4==4.8.2"])
    assert result.exit_code == 0
    files = list(tmp_path.iterdir())
    assert len(files) == 2


# Add-on for ignoring unused version - Conflict between platform and version check #13
# --python-version py3 --python-version cp37 --platform-tag manylinux1_x86_64 --dest . --no-source beautifulsoup4==4.8.2
# Should download beautifulsoup4-4.8.2-py3-none-any.whl, soupsieve-2.0.1-py3-none-any.whl
# NOT TO BE DOWNLOADED :  beautifulsoup4-4.8.2-py2-none-any.whl
def test_download_bs4_package_noparam(tmp_path: Path):
    runner = CliRunner()
    result = runner.invoke(pipdownload, ["beautifulsoup4==4.8.2", "-d", str(tmp_path)])
    assert result.exit_code == 0
    files = list(tmp_path.iterdir())
    assert len(files) == 5


# Add-on for ignoring unused version - Conflict between platform and version check #13
# --python-version py3 --python-version cp37 --platform-tag manylinux1_x86_64 --dest . --no-source beautifulsoup4==4.8.2
# Should download beautifulsoup4-4.8.2-py3-none-any.whl, soupsieve-2.0.1-py3-none-any.whl
# NOT TO BE DOWNLOADED :  beautifulsoup4-4.8.2-py2-none-any.whl
def test_download_bs4_package_veronly(tmp_path: Path):
    runner = CliRunner()
    result = runner.invoke(pipdownload, ["--python-version", "cp37", "beautifulsoup4==4.8.2", "-d", str(tmp_path)])
    assert result.exit_code == 0
    files = list(tmp_path.iterdir())
    assert len(files) == 2


# Add-on for ignoring unused version - Conflict between platform and version check #13
# --python-version py3 --python-version cp37 --platform-tag manylinux1_x86_64 --dest . --no-source beautifulsoup4==4.8.2
# Should download beautifulsoup4-4.8.2-py3-none-any.whl, soupsieve-2.0.1-py3-none-any.whl
# NOT TO BE DOWNLOADED :  beautifulsoup4-4.8.2-py2-none-any.whl
def test_download_pip20_2_3_package(tmp_path: Path):
    runner = CliRunner()
    result = runner.invoke(pipdownload, ["--python-version", "py3", "pip==20.2.3", "-d", str(tmp_path)])
    assert result.exit_code == 0
    files = list(tmp_path.iterdir())
    assert len(files) == 2


# "redundant" means there are redundant blank lines in requirement file.
def test_download_from_requirement_file_redundant(
        requirement_file_redundant, tmp_path: Path
):
    runner = CliRunner()
    result = runner.invoke(
        pipdownload, ["-r", requirement_file_redundant, "-d", tmp_path]
    )
    assert result.exit_code == 0
    files = list(tmp_path.iterdir())
    assert len(files) == 2


def test_download_from_requirement_file_normal(requirement_file_normal, tmp_path):
    runner = CliRunner()
    result = runner.invoke(pipdownload, ["-r", requirement_file_normal, "-d", tmp_path])
    assert result.exit_code == 0
    files = list(tmp_path.iterdir())
    assert len(files) == 2


def test_download_with_option_whl_suffixes(tmp_path):
    runner = CliRunner()
    result = runner.invoke(
        pipdownload, ["MarkupSafe==1.1.1", "--suffix", "win_amd64", "-d", tmp_path]
    )
    assert result.exit_code == 0
    files = list(tmp_path.iterdir())
    # TODO: This should be consider again!
    assert len(files) == 7


def test_download_with_option_python_versions(tmp_path):
    runner = CliRunner()
    result = runner.invoke(
        pipdownload, ["MarkupSafe==1.1.1", "-py", "cp27", "-d", tmp_path]
    )
    assert result.exit_code == 0
    files = list(tmp_path.iterdir())
    assert len(files) == 8


# Added -no-source because other way round 4 files were returned
def test_download_with_option_python_versions_and_platform_tags(tmp_path):
    runner = CliRunner()
    result = runner.invoke(
        pipdownload, ["ujson", "-py", "cp36", "-p", "manylinux", "-d", tmp_path, "--no-source"]
    )
    assert result.exit_code == 0
    files = list(tmp_path.iterdir())
    assert len(files) == 3


def test_download_when_dest_dir_does_not_exists(tmp_path: Path):
    runner = CliRunner()
    dir_name = "tmp"
    result = runner.invoke(pipdownload, ["click", "-d", str(tmp_path / dir_name)])
    assert result.exit_code == 0
    dirs = list(tmp_path.iterdir())
    assert len(dirs) == 1
    files = list((tmp_path / dir_name).iterdir())
    assert len(files) == 2


def test_option_platform_tag(tmp_path):
    runner = CliRunner()
    result = runner.invoke(
        pipdownload, ["ujson==3.0.0", "-p", "win_amd64", "-d", tmp_path]
    )
    assert result.exit_code == 0
    files = list(tmp_path.iterdir())
    # TODO: This should be consider again!
    assert len(files) == 5


def test_option_on_source(tmp_path: Path):
    runner = CliRunner()
    result = runner.invoke(
        pipdownload, ["click==7.0", "--no-source", "-d", str(tmp_path)]
    )
    assert result.exit_code == 0
    files = list(tmp_path.iterdir())
    assert len(files) == 1


def test_packege_with_egg_file(tmp_path: Path):
    runner = CliRunner()
    result = runner.invoke(
        pipdownload, ["protobuf", "-d", str(tmp_path), "-py", "cp37"]
    )
    assert result.exit_code == 0
    # files = list(tmp_path.iterdir())
    # assert len(files) == 1


def test_download_with_config_file(tmp_path: Path):
    runner = CliRunner()
    result = runner.invoke(pipdownload, ["--show-config"])
    assert result.exit_code == 0

    runner = CliRunner()
    settings_dict = {"python-versions": ["cp37"], "platform-tags": ["win_amd64"]}
    with open(settings.SETTINGS_FILE, "w") as f:
        json.dump(settings_dict, f, indent=True)

    _ = runner.invoke(pipdownload, ["MarkupSafe==1.1.1", "-d", str(tmp_path)])

    files = list(tmp_path.iterdir())
    assert len(files) == 2
    Path(settings.SETTINGS_FILE).unlink()
