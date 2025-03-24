import os

this_script_dir = os.path.dirname(os.path.abspath(__file__))


def build(utils, repo):
    c, _run_command = (
        utils["ctx"],
        utils["_run_command"],
    )

    _run_command(c, f"cp -r {this_script_dir}/* ./")
