import os

this_script_dir = os.path.dirname(os.path.abspath(__file__))


def build(utils, repo):
    c, _run_command = (utils["ctx"], utils["_run_command"])

    _run_command(c, f"cp {this_script_dir}/local.mk ./")
    _run_command(c, f"cp {this_script_dir}/.config ./")

    _run_command(c, "unset LLVM CC && make BR2_EXTERNAL=../../buildroot -j24")
