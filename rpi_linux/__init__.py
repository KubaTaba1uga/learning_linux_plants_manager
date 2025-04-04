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
        "insert_before": "leds: leds",
    },
    {
        "path": os.path.join(
            "arch", "arm64", "boot", "dts", "broadcom", "bcm2712-rpi-5-b.dts"
        ),
        "snippet": """
	irrigation_controller: irrigation_controller {
	    compatible = "raspberrypi,irrigation_controller_device";
	    pump-gpios = <&rp1_gpio 1 GPIO_ACTIVE_HIGH>;
	    valve1-gpios = <&rp1_gpio 10 GPIO_ACTIVE_HIGH>;
	    valve2-gpios = <&rp1_gpio 9 GPIO_ACTIVE_HIGH>;
	    valve3-gpios = <&rp1_gpio 11 GPIO_ACTIVE_HIGH>;
	    valve4-gpios = <&rp1_gpio 0 GPIO_ACTIVE_HIGH>;
	    valve5-gpios = <&rp1_gpio 25 GPIO_ACTIVE_HIGH>;
	    valve6-gpios = <&rp1_gpio 8 GPIO_ACTIVE_HIGH>;
	    valve7-gpios = <&rp1_gpio 7 GPIO_ACTIVE_HIGH>;		
	    status = "okay";
	};
""",
        "insert_before": "leds: leds",
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
    c, _run_command, repo_path = (
        utils["ctx"],
        utils["_run_command"],
        utils["repo_path"],
    )

    _run_command(c, f"cp {this_script_dir}/.config ./")

    for snippet in sinppets_to_insert:
        _insert_snippet(
            os.path.join(repo_path, snippet["path"]),
            snippet["snippet"],
            snippet["insert_before"],
        )


def _insert_snippet(dts_file, snippet, insert_before):
    # Read the file lines
    with open(dts_file, "r") as f:
        lines = f.readlines()

    new_lines = []
    inserted = False
    marker = [line for line in snippet.split("\n") if len(line.strip()) > 0][0]
    for line in lines:
        if f"// AUTOMANAGED {marker}" in line:
            inserted = True

        if insert_before in line and not inserted:
            new_lines.append(f"\n// AUTOMANAGED {marker} START\n")
            new_lines.append(snippet)
            new_lines.append(f"\n// AUTOMANAGED {marker} END\n")
            inserted = True

        new_lines.append(line)

    if not inserted:
        raise RuntimeError(f"Could not find {insert_before} section in {dts_file}.")

    # Write the updated content back to the file
    with open(dts_file, "w") as f:
        f.writelines(new_lines)
