import os

this_script_dir = os.path.dirname(os.path.abspath(__file__))

sinppets_to_insert = [
    {
        "path": os.path.join(
            "arch", "arm64", "boot", "dts", "broadcom", "bcm2712-rpi-5-b.dts"
        ),
        "snippet": """
    am2303_device {
        compatible = "raspberrypi,am2303_device";
        data-gpios = <&rp1_gpio 15 0>;
        status = "okay";
    };
""",
        "insert_before": "leds:leds",
    },
    {
        "path": os.path.join(
            "arch", "arm64", "boot", "dts", "broadcom", "bcm2712-rpi-5-b.dts"
        ),
        "snippet": """
   &i2c1 {
       #address-cells = <1>;
       #size-cells = <0>;
       ads7830_soil_humid_device@48 {
           compatible = "raspberrypi,ads7830_soil_humid_device";
           reg = <0x48>;
           status = "okay";
       };
   };    
""",
        "insert_before": "&cooling_maps",
    },
]


def build(utils, repo):
    c, _run_command = (
        utils["ctx"],
        utils["_run_command"],
    )

    _run_command(c, f"cp {this_script_dir}/.config ./")

    _run_command(
        c,
        (
            "export KERNEL=kernel_2712 && "
            "export KDIR=$(pwd) && "
            "export CROSS_COMPILE=aarch64-linux-gnu- && "
            "export ARCH=arm64 && "
            "export CC=clang && "
            "export LLVM=1 && "
            "make -j 16 all"
        ),
    )


def _insert_snippet(repo_path):
    # Define the snippet to insert (ensure it has a leading newline for proper formatting)
    snippet = """
    am2303_device {
        compatible = "raspberrypi,am2303_device";
        data-gpios = <&rp1_gpio 15 0>;
        status = "okay";
    };
"""
    dts_file = os.path.join(
        repo_path, "arch", "arm64", "boot", "dts", "broadcom", "bcm2712-rpi-5-b.dts"
    )

    # Read the file lines
    with open(dts_file, "r") as f:
        lines = f.readlines()

    new_lines = []
    inserted = False
    for line in lines:
        # Check if this line contains the marker text
        if "leds: leds" in line and not inserted:
            new_lines.append(snippet)
            inserted = True

        new_lines.append(line)

    if not inserted:
        raise RuntimeError("Could not find 'leds: leds' section in the file.")

    # Write the updated content back to the file
    with open(dts_file, "w") as f:
        f.writelines(new_lines)
