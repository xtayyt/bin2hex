# 
# Copyright 2025 Yitao Zhang
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#

from typing import Optional, BinaryIO

def bin_to_c_uintx(input_data:bytes, align_width:int = 16, data_width:int = 1, swap_endian:bool = False) -> str:
    output_data = ""
    count = 0
    align_count = 0

    if align_width % data_width != 0:
        print(f"Warning: The alignment width {align_width} is not aligned to the data width {data_width}. Expanding the alignment width to {align_width + data_width - (align_width % data_width)}.")
        align_width += data_width - (align_width % data_width)

    if len(input_data) != 0:
        while True:
            # Bytes to convert
            data_bytes = input_data[count : count + data_width]
            # Pad zeros if the data is not aligned to the data width
            if len(data_bytes) < data_width:
                print(f"Warning: The input data is not aligned to the data width {data_width}. Padding zeros.")
                data_bytes += b'\x00' * (data_width - len(data_bytes))
            # Convert the binary bytes to hex string sequence
            hex_seq = data_bytes.hex().upper()
            # Handle the endian sequence
            if swap_endian:
                hex_str = hex_seq
            else:
                hex_str = ''.join([hex_seq[i-1:i] + hex_seq[i:i+1] for i in range(len(hex_seq) - 1, -1, -2)])
            # Append the hex string
            output_data += '0x' + hex_str
            count += data_width
            align_count += data_width
            # Break if no more data to handle
            if count >= len(input_data):
                break
            else:
                output_data += ","
            # Alignment control
            if align_count >= align_width:
                output_data += '\n'
                align_count = 0
            else:
                output_data += ' '

    return output_data

def bin_to_c_uint8(input_data:bytes, align_width:int = 16) -> str:
    return bin_to_c_uintx(input_data, align_width, 1, False)

def bin_to_c_uint16(input_data:bytes, align_width:int = 16) -> str:
    return bin_to_c_uintx(input_data, align_width, 2, False)

def bin_to_c_uint32(input_data:bytes, align_width:int = 16) -> str:
    return bin_to_c_uintx(input_data, align_width, 4, False)

def bin_to_c_uint64(input_data:bytes, align_width:int = 16) -> str:
    return bin_to_c_uintx(input_data, align_width, 8, False)

bin2c_dict = {
    "c_uint8": {
        "function": bin_to_c_uint8,
        "description": [
            "Convert to the c header file which can be included by C source file to init an 'uint8_t' table",
            "The option \"alignment\" is accepted as optional. Default is 16, which means 16 bytes per line",
            "The format will be:",
            "  0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F",
            "  0x10, 0x11 ......",
        ],
    },
    "c_uint16": {
        "function": bin_to_c_uint16,
        "description": [
            "Convert to the c header file which can be included by C source file to init an 'uint16_t' table",
            "The option \"alignment\" is accepted as optional. Default is 16, which means 16 bytes per line",
            "The format will be:",
            "  0x0100, 0x0302, 0x0504, 0x0706, 0x0908, 0x0B0A, 0x0D0C, 0x0F0E",
            "  0x1110, 0x1312 ......",
        ],
    },
    "c_uint32": {
        "function": bin_to_c_uint32,
        "description": [
            "Convert to the c header file which can be included by C source file to init an 'uint32_t' table",
            "The option \"alignment\" is accepted as optional. Default is 16, which means 16 bytes per line",
            "The format will be:",
            "  0x03020100, 0x07060504, 0x0B0A0908, 0x0F0E0D0C, ",
            "  0x13121110, 0x17161514 ......",
        ],
    },
    "c_uint64": {
        "function": bin_to_c_uint64,
        "description": [
            "Convert to the c header file which can be included by C source file to init an 'uint64_t' table.",
            "The option \"alignment\" is accepted as optional. Default is 16, which means 16 bytes per line",
            "The format will be:",
            "  0x0706050403020100, 0x0F0E0D0C0B0A0908, ",
            "  0x1716151413121110,  ......",
        ],
    },
}