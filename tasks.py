###############################################
#                Imports                      #
###############################################
import glob
import os
import subprocess

from invoke import task

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
    dependencies = {"git": "git"}
    _pr_info("Installing dependencies...")

    for dep_cmd, dep_package in dependencies.items():
        if not _command_exists(dep_cmd):
            _pr_warn(f"{dep_cmd} not found. Installing {dep_cmd}...")
            c.run(
                f"sudo apt-get install -y {dep_package}",
                warn=True,
            )
        else:
            _pr_info(f"{dep_cmd} already installed")

    _pr_info("Dependencies are installed")


@task
def build(c):
    repos_to_download = [
        {
            "name": "rpi_linux",
            "git_url": "https://github.com/raspberrypi/linux",
            "git_commit": "08d4e8f52256bd422d8a1f876411603f627d0a82",
            "build_func": None,
        },
        {
            "name": "am2303_driver",
            "git_url": "https://github.com/KubaTaba1uga/kernel_am2303_driver",
            "git_commit": "4a8617769e31499a7db18ec5029593d835aa6c07",
            "build_func": None,
        },
        {
            "name": "ads7830_soil_humid_driver",
            "git_url": "https://github.com/KubaTaba1uga/kernel_ads7830_soil_humid_driver",
            "git_commit": "fc8c9b00cf09b538667e2370823bf7f83546b5e4",
            "build_func": None,
        },
        {
            "name": "sqlite",
            "git_url": "https://github.com/sqlite/sqlite",
            "git_commit": "62d9d70eddda991bd3dedb55c1beb5a23fb6cae8",
            "build_func": None,
        },
        {
            "name": "buildroot",
            "git_url": "https://github.com/buildroot/buildroot",
            "git_commit": "aa2d7ca53f704af901f6c33c13e4bb1591886700",
            "build_func": None,
        },
    ]

    _pr_info("Building app...")

    c.cd(BUILD_PATH)

    for repo in repos_to_download:
        _pr_info(f"Building {repo['name']}...")

        c.run(
            f"git clone {repo['git_url']} {repo['name']} && cd {repo['name']} && git checkout {repo['git_commit']}"
        )

        if repo["build_func"]:
            c.cd(repo["name"])
            repo["build_func"](repo)
            c.cd("..")

        _pr_info(f"Build {repo['name']} succesfully")

    _pr_info("Build app succesfully")


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


@task
def deploy(c, machines=None):
    """
    Deploy the main Ansible playbook for all single-board computers (SBCs).

    Args:
        machines (str, optional): A comma-separated list of machines to target.
                                  If not provided, deploys to all machines.

    Usage:
        inv deploy
        inv deploy --machines=machine1,machine2
    """
    _pr_info("Running main playbook for SBCs deployment...")

    # Check if Ansible and ansible-playbook are installed
    if not _command_exists("ansible"):
        _pr_error("Ansible command not found. Please install Ansible first.")
        return
    if not _command_exists("ansible-playbook"):
        _pr_error("ansible-playbook command not found. Please install Ansible first.")
        return

    # Define the paths for the playbook and inventory files
    playbook_path = os.path.join(SRC_PATH, "main.yaml")
    inventory_path = os.path.join(SRC_PATH, "inventory.yaml")

    # Check if the playbook and inventory files exist
    if not os.path.isfile(playbook_path):
        _pr_error(f"Playbook file not found at {playbook_path}.")
        return
    if not os.path.isfile(inventory_path):
        _pr_error(f"Inventory file not found at {inventory_path}.")
        return

    # Run the ansible-playbook command
    command = (
        f"ansible-playbook -i {inventory_path}"
        + ("" if not machines else f" -l {machines}")
        + f" {playbook_path}"
    )
    result = c.run(command, warn=True)

    if result.ok:
        _pr_info("Playbook ran successfully.")
    else:
        _pr_error("Playbook execution failed.")


@task
def run(c, command="", machines=None):
    """
    Run a specified command on all machines in the inventory or on a subset if specified.

    Args:
        command (str): The command to execute on the machines.
        machines (str, optional): A comma-separated list of machines to target.
                                  If None, runs the command on all machines in the inventory.

    Usage:
        inv run --command='uptime'
        inv run --command='uptime' --machines='machine1,machine2'
    """
    inventory_path = os.path.join(SRC_PATH, "inventory.yaml")

    # Check if the inventory file exists
    if not os.path.isfile(inventory_path):
        _pr_error(f"Inventory file not found at {inventory_path}.")
        return

    ansible_command = (
        f"ansible -i {inventory_path} "
        + ("" if not machines else f" -l {machines} ")
        + f"-m shell -a '{command}'"
    )

    # Execute the command on specified machines or all in the inventory
    _pr_info(f"Running command on target machines: {ansible_command}")
    result = c.run(ansible_command, warn=True)

    if result.ok:
        _pr_info("Command ran successfully on target machines.")
    else:
        _pr_error("Command execution failed on target machines.")


@task
def preconfigure(c):
    """
    Run the preconfiguration playbook for all boards.

    Usage:
        inv preconfigure
    """
    _pr_info("Running preconfiguration playbook...")

    # Check if Ansible and ansible-playbook are installed
    if not _command_exists("ansible"):
        _pr_error("Ansible command not found. Please install Ansible first.")
        return
    if not _command_exists("ansible-playbook"):
        _pr_error("ansible-playbook command not found. Please install Ansible first.")
        return

    # Define the paths for the playbook and inventory files
    playbook_path = os.path.join(SRC_PATH, "prepare_board", "main.yaml")
    inventory_path = os.path.join(SRC_PATH, "prepare_board", "inventory.yaml")

    # Check if the playbook file exists
    if not os.path.isfile(playbook_path):
        _pr_error(f"Playbook file not found at {playbook_path}.")
        return
    # Check if the inventory file exists
    if not os.path.isfile(inventory_path):
        _pr_error(f"Inventory file not found at {inventory_path}.")
        return

    # Construct and run the ansible-playbook command
    command = f"ansible-playbook -v -i {inventory_path} {playbook_path}"
    result = c.run(command, warn=True)

    if result.ok:
        _pr_info("Preconfiguration completed successfully.")
    else:
        _pr_error("Preconfiguration failed.")


@task
def create_image(c, board=None):
    """
    Prepare image for requested board.

    Usage:
        inv prepare_image --board <board>

    Available boards:
        - rpi-5
        - orangepi-5
    """
    boards = {
        "rpi-5": {},
        "orangepi-5": {},
    }

    if board not in boards:
        _pr_error(f"Invalid board: {board}.")
        return

    _pr_info("Running create_image playbook on localhost...")

    # Check if Ansible and ansible-playbook are installed
    if not _command_exists("ansible"):
        _pr_error("Ansible command not found. Please install Ansible first.")
        return
    if not _command_exists("ansible-playbook"):
        _pr_error("ansible-playbook command not found. Please install Ansible first.")
        return
    # Define the path for the playbook
    playbook_path = os.path.join(SRC_PATH, "create_image", "main.yaml")

    # Check if the playbook file exists
    if not os.path.isfile(playbook_path):
        _pr_error(f"Playbook file not found at {playbook_path}.")
        return

    # Run the ansible-playbook command
    command = (
        f'ansible-playbook {playbook_path} -i localhost, -c local -e "board={board}"'
    )
    result = c.run(command, warn=True)

    if result.ok:
        _pr_info("Prepare image playbook ran successfully.")
    else:
        _pr_error("Prepare image playbook execution failed.")
        return

    _pr_info(f"Adjusting image for {board}...")

    # Run the compile.sh script
    script_file = os.path.join(BUILD_PATH, "create-image.sh")
    result = c.run(f"{script_file}", warn=True)

    if not result.ok:
        _pr_error("Image customization failed.")
        return

    _pr_info(f"Image for {board} ready in {BUILD_PATH}")


@task
def prepare_image(c, board=None):
    """
    Prepare image for requested board.

    Usage:
        inv prepare_image --board <board>

    Available boards:
        - rpi-5b
        - orangepi-5
    """
    boards_scripts_map = {
        "rpi-5b": "rpi-5b-compile.sh",
        "orangepi-5": "opi-5-compile.sh",
    }

    if board not in boards_scripts_map:
        _pr_error(f"Invalid board: {board}.")
        return

    _pr_info("Running prepare_image playbook on localhost...")

    # Check if Ansible and ansible-playbook are installed
    if not _command_exists("ansible"):
        _pr_error("Ansible command not found. Please install Ansible first.")
        return
    if not _command_exists("ansible-playbook"):
        _pr_error("ansible-playbook command not found. Please install Ansible first.")
        return

    # Define the path for the playbook
    playbook_path = os.path.join(SRC_PATH, "prepare_image", "main.yaml")

    # Check if the playbook file exists
    if not os.path.isfile(playbook_path):
        _pr_error(f"Playbook file not found at {playbook_path}.")
        return

    # Run the ansible-playbook command
    command = f"ansible-playbook {playbook_path} -i localhost, -c local"
    result = c.run(command, warn=True)

    if result.ok:
        _pr_info("Prepare image playbook ran successfully.")
    else:
        _pr_error("Prepare image playbook execution failed.")
        return

    _pr_info(f"Compiling image for {board}...")

    # Run the compile.sh script
    armbian_dir = os.path.join(BUILD_PATH, "armbian")
    script_path = os.path.join(armbian_dir, boards_scripts_map[board])
    result = c.run(f"cd {armbian_dir} && {script_path}", warn=True)

    if not result.ok:
        _pr_error("Image compilation failed.")
        return

    c.run(
        f"mv {os.path.join(f'{armbian_dir}', 'output', 'images', '*.img')} {BUILD_PATH}",
        warn=True,
    )

    _pr_info("Image compiled successfully.")


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
