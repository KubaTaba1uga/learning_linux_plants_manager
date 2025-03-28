###############################################
#                Imports                      #
###############################################
import glob
import os
import subprocess

from invoke import task

from buildroot import build as build_buildroot
from read_sensors_job import build as build_read_sensors_job
from read_sensors_web import build as build_read_sensors_web
from rpi_linux import build as build_rpi_linux

###############################################
#                Public API                   #
###############################################
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(ROOT_PATH, "src")
BUILD_PATH = os.path.join(ROOT_PATH, "build")


@task
def install(c):
    """
    Install dependencies if they are not already installed.

    Usage:
        inv install
    """
    dependencies = {
        "git": "git",
        "clang-check": "clang-tools",
        "llvm-config": "llvm",
        "clang": "clang",
        "lld": "lld",
        "jq": "jq",
        "tar": "tar",
    }
    _pr_info("Installing dependencies...")

    for dep_cmd, dep_package in dependencies.items():
        if not _command_exists(dep_cmd):
            _pr_warn(f"{dep_cmd} not found. Installing {dep_package}...")
            _run_command(c, f"sudo apt-get install -y {dep_package}")
        else:
            _pr_info(f"{dep_package} already installed")

    _pr_info("Dependencies are installed")


@task
def build(c):
    repos_to_download = [
        {
            "name": "rpi_linux",
            "git_url": "https://github.com/raspberrypi/linux",
            "git_commit": "08d4e8f52256bd422d8a1f876411603f627d0a82",
            "build_func": build_rpi_linux,
        },
        {
            "name": "am2303_driver",
            "git_url": "https://github.com/KubaTaba1uga/kernel_am2303_driver",
            "git_commit": "95c33d6815e9945a1a5d2a1a9e623b116cc18a56",
            "build_func": None,
        },
        {
            "name": "adc7830_soil_humid_driver",
            "git_url": "https://github.com/KubaTaba1uga/kernel_ads7830_soil_humid_driver",
            "git_commit": "2e3978cb1422c79b136d8ea6d47c0d7e12bd64af",
            "build_func": None,
        },
        {
            "name": "read_sensors_job",
            "build_func": build_read_sensors_job,
        },
        {
            "name": "read_sensors_web",
            "build_func": build_read_sensors_web,
        },
        {
            "name": "buildroot",
            "git_url": "https://github.com/buildroot/buildroot",
            "git_commit": "aa2d7ca53f704af901f6c33c13e4bb1591886700",
            "build_func": build_buildroot,
        },
    ]

    _pr_info("Building app...")

    with c.cd(BUILD_PATH):
        for repo in repos_to_download:
            _pr_info(f"Building {repo['name']}...")

            repo_path = os.path.join(BUILD_PATH, repo["name"])
            if not os.path.exists(repo_path):
                if repo.get("git_url"):
                    _run_command(
                        c,
                        f"git clone {repo['git_url']} {repo_path} && cd {repo_path} && git checkout {repo['git_commit']}",
                    )
                else:
                    _run_command(c, f"cp -r ../{repo['name']} {repo_path}")

            if repo["build_func"]:
                with c.cd(repo_path):
                    repo["build_func"](
                        utils={
                            "ctx": c,
                            "_run_command": _run_command,
                            "repo_path": repo_path,
                        },
                        repo=repo,
                    )

            _pr_info(f"Build {repo['name']} succesfully")

    _run_command(
        c,
        f"cp {os.path.join(BUILD_PATH, 'buildroot', 'output', 'images', 'sdcard.img')} {os.path.join(BUILD_PATH, 'sdcard.img')}",
    )

    _pr_info("Build app succesfully")


@task
def fritzing(c):
    repos_to_download = [
        {
            "name": "fritizing_adafruit_library",
            "git_url": "https://github.com/adafruit/Fritzing-Library.git",
            "git_commit": "ce9919b1994e67d8e60108fd94d6928e671f1572",
            "build_func": None,
        },
    ]

    _pr_info("Starting fritizng...")

    with c.cd(BUILD_PATH):
        for repo in repos_to_download:
            _pr_info(f"Building {repo['name']}...")

            repo_path = os.path.join(BUILD_PATH, repo["name"])
            if not os.path.exists(repo_path):
                if repo.get("git_url"):
                    _run_command(
                        c,
                        f"git clone {repo['git_url']} {repo_path} && cd {repo_path} && git checkout {repo['git_commit']}",
                    )
                else:
                    _run_command(c, f"cp -r ../{repo['name']} {repo_path}")

            if repo["build_func"]:
                with c.cd(repo_path):
                    repo["build_func"](
                        utils={
                            "ctx": c,
                            "_run_command": _run_command,
                            "repo_path": repo_path,
                        },
                        repo=repo,
                    )

            _pr_info(f"Build {repo['name']} succesfully")

    _pr_info(
        "Now in fritzing import build/fritizing_adafruit_library/AdaFrui.fzbz."
        " To do so, open fritzing/breadboard.fzz and rigth-click on empty space"
        " on Parts section on rigth side of breadboard, there should be `import`"
        " option available."
    )

    _run_command(c, "fritzing")

    _pr_info("Finshed fritzing")


@task
def clean(c, extra=""):
    """
    Clean up build and temporary files recursively.

    This task removes specified patterns of files and directories,
    including build artifacts and temporary files.

    Args:
        extra (str, optional): Additional pattern to remove. Defaults to "".

    Usage:
        inv clean
        inv clean --bytecode
        inv clean --extra='**/*.log'
    """
    patterns = [
        "build/*",
        "**/*~",
        "**/#*",
        "*~",
        "#*",
    ]

    if extra:
        patterns.append(extra)

    for pattern in patterns:
        _pr_info(f"Removing files matching pattern '{pattern}'")

        # Use glob to find files recursively and remove each one
        for path in glob.glob(pattern, recursive=True):
            if os.path.isfile(path):
                os.remove(path)
                print(f"Removed file {path}")
            elif os.path.isdir(path):
                os.rmdir(path)
                print(f"Removed directory {path}")

    _pr_info("Clean up completed.")


###############################################
#                Private API                  #
###############################################
def _get_file_extension(file_path):
    _, file_extension = os.path.splitext(file_path)
    return file_extension


def _command_exists(command):
    try:
        # Attempt to run the command with '--version' or any other flag that doesn't change system state
        subprocess.run(
            [command, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return True
    except FileNotFoundError:
        return False
    except subprocess.CalledProcessError:
        # The command exists but returned an error
        return True
    except Exception:
        # Catch any other exceptions
        return False


def _run_command(c, command):
    _pr_debug(f"Executing '{command}'...")

    try:
        # Attempt to run the command with '--version' or any other flag that doesn't change system state
        result = c.run(command, warn=True)

        if not result.ok:
            raise Exception("Result not ok")

    except Exception as exc:
        _pr_error(f"Command {command} failed: {exc}")
        exit(1)


def _cut_path_to_directory(full_path, target_directory):
    """
    Cuts the path up to the specified target directory.

    :param full_path: The full path to be cut.
    :param target_directory: The directory up to which the path should be cut.
    :return: The cut path if the target directory is found, otherwise raises ValueError.
    """
    parts = full_path.split(os.sep)

    target_index = parts.index(target_directory)
    return os.sep.join(parts[: target_index + 1])


def _pr_info(message: str):
    """
    Print an informational message in blue color.

    Args:
        message (str): The message to print.

    Usage:
        pr_info("This is an info message.")
    """
    print(f"\033[94m[INFO] {message}\033[0m")


def _pr_warn(message: str):
    """
    Print a warning message in yellow color.

    Args:
        message (str): The message to print.

    Usage:
        pr_warn("This is a warning message.")
    """
    print(f"\033[93m[WARN] {message}\033[0m")


def _pr_debug(message: str):
    """
    Print a debug message in cyan color.

    Args:
        message (str): The message to print.

    Usage:
        pr_debug("This is a debug message.")
    """
    print(f"\033[96m[DEBUG] {message}\033[0m")


def _pr_error(message: str):
    """
    Print an error message in red color.

    Args:
        message (str): The message to print.

    Usage:
        pr_error("This is an error message.")
    """
    print(f"\033[91m[ERROR] {message}\033[0m")
