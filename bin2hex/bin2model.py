#
# Copyright 2025 Yitao Zhang
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#

def bin_to_denali(input_data:bytes) -> str:
    output_data = ""
    count = 0

    if len(input_data) != 0:
        while True:
            # Bytes to convert
            data_bytes = input_data[count : count + 1]
            # Convert the binary bytes to hex string
            hex_str = data_bytes.hex().upper()
            # Append the hex string
            output_data += f"{count:X}" + "/" + hex_str + ";"
            count = count + 1
            # Break if no more data to handle
            if count >= len(input_data):
                break
            else:
                output_data += "\n"

    return output_data

bin2model_dict = {
    "denali": {
        "function": bin_to_denali,
        "description": [
            "Convert to the file which can be used by Cadence denali model",
            "No option is accepted",
            "The format will be:",
            "  0/00",
            "  1/01",
            "  ......",
        ],
    },
}