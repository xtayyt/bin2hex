# 
# Copyright 2025 Yitao Zhang
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#

from typing import Optional, BinaryIO

def bin_to_verilog_dwn(input_data:bytes, data_width:int = 1, swap_endian:int = False) -> str:
    output_data = ""
    count = 0

    if len(input_data) != 0:
        while True:
            # Bytes to convert
            data = input_data[count : count + data_width]
            # Pad zeros if the data is not aligned to the data width
            if len(data) < data_width:
                print(f"Warning: The input data is not aligned to the data width {data_width}. Padding zeros.")
                data +=b'\x00' * (data_width - len(data))
            # Convert the binary data to hex string sequence
            hex_seq = data.hex().upper()
            # Handle the endian sequence
            if swap_endian:
                hex_str = hex_seq
            else:
                hex_str = ''.join([hex_seq[i-1:i] + hex_seq[i:i+1] for i in range(len(hex_seq) - 1, -1, -2)])
            # Append the hex string
            output_data += hex_str
            count += data_width
            # Break if no more data to handle
            if count >= len(input_data):
                break
            else:
                output_data += '\n'

    return output_data

def bin_to_verilog_dw1(input_data:bytes) -> str:
    return bin_to_verilog_dwn(input_data, 1, False)

def bin_to_verilog_dw2(input_data:bytes) -> str:
    return bin_to_verilog_dwn(input_data, 2)

def bin_to_verilog_dw4(input_data:bytes) -> str:
    return bin_to_verilog_dwn(input_data, 4)

def bin_to_verilog_dw8(input_data:bytes) -> str:
    return bin_to_verilog_dwn(input_data, 8)

def bin_to_verilog_dw16(input_data:bytes) -> str:
    return bin_to_verilog_dwn(input_data, 16)

def bin_to_verilog_addr_dwn(input_data:bytes , start_address:int = 0x0, align_width:int = 4, data_width:int = 1, swap_endian:bool = False) -> str:
    output_data = ""
    count = 0
    align_count = 0

    if start_address % data_width != 0:
        raise ValueError(f"Error: The start address {start_address} is not aligned to the data width {data_width}.")

    if align_width % data_width != 0:
        print(f"Warning: The alignment width {align_width} is not aligned to the data width {data_width}. Expanding the alignment width to {align_width + data_width - (align_width % data_width)}.")
        align_width += data_width - (align_width % data_width)

    if len(input_data) != 0:
        while True:
            # Bytes to convert
            data = input_data[count : count + data_width]
            # Pad zeros if the data is not aligned to the data width
            if len(data) < data_width:
                print(f"Warning: The input data is not aligned to the data width {data_width}. Padding zeros.")
                data +=b'\x00' * (data_width - len(data))
            # Convert the binary data to hex string sequence
            hex_seq = data.hex().upper()
            # Handle the endian sequence
            if swap_endian:
                hex_str = hex_seq
            else:
                hex_str = ''.join([hex_seq[i-1:i] + hex_seq[i:i+1] for i in range(len(hex_seq) - 1, -1, -2)])
            # Append the hex string
            if align_count == 0:
                output_data += '@' + f"{start_address:08X}" + " "
            output_data += hex_str
            count += data_width
            align_count += data_width
            start_address += data_width
            # Break if no more data to handle
            if count >= len(input_data):
                break
            # Alignment control
            if align_count >= align_width:
                output_data += '\n'
                align_count = 0
            else:
                output_data += ' '

    return output_data

def bin_to_verilog_addr_dw1(input_data:bytes, start_address:int = 0x0, align_width:int = 32) -> str:
    return bin_to_verilog_addr_dwn(input_data, start_address, align_width, 1, False)

def bin_to_verilog_addr_dw2(input_data:bytes, start_address:int = 0x0, align_width:int = 32) -> str:
    return bin_to_verilog_addr_dwn(input_data, start_address, align_width, 2, False)

def bin_to_verilog_addr_dw4(input_data:bytes, start_address:int = 0x0, align_width:int = 32) -> str:
    return bin_to_verilog_addr_dwn(input_data, start_address, align_width, 4, False)

def bin_to_verilog_addr_dw8(input_data:bytes, start_address:int = 0x0, align_width:int = 32) -> str:
    return bin_to_verilog_addr_dwn(input_data, start_address, align_width, 8, False)

def bin_to_verilog_addr_dw16(input_data:bytes, start_address:int = 0x0, align_width:int = 32) -> str:
    return bin_to_verilog_addr_dwn(input_data, start_address, align_width, 16, False)

bin2verilog_dict = {
    "verilog_dw1": {
        "function": bin_to_verilog_dw1,
        "description": [
            "Convert to the file which can be loaded by $readmemh to a common memory with 1-byte(8-bit) width",
            "No option is accepted",
            "The format will be:",
            "  00",
            "  01",
            "  ......",
        ],
    },
    "verilog_dw2": {
        "function": bin_to_verilog_dw2,
        "description": [
            "Convert to the file which can be loaded by $readmemh to a common memory with 2-byte(16-bit) width",
            "No option is accepted",
            "The format will be:",
            "  0100",
            "  0302",
            "  ......",
        ],
    },
    "verilog_dw4": {
        "function": bin_to_verilog_dw4,
        "description": [
            "Convert to the file which can be loaded by $readmemh to a common memory with 4-byte(32-bit) width",
            "No option is accepted",
            "The format will be:",
            "  03020100",
            "  07060504",
            "  ......",
        ],
    },
    "verilog_dw8": {
        "function": bin_to_verilog_dw8,
        "description": [
            "Convert to the file which can be loaded by $readmemh to a common memory with 8-byte(64-bit) width",
            "No option is accepted",
            "The format will be:",
            "  0706050403020100",
            "  0F0E0D0C0B0A0908",
            "  ......",
        ],
    },
    "verilog_dw16": {
        "function": bin_to_verilog_dw16,
        "description": [
            "Convert to the file which can be loaded by $readmemh to a common memory with 16-byte(128-bit) width",
            "No option is accepted",
            "The format will be:",
            "  0F0E0D0C0B0A09080706050403020100",
            "  1F1E1D1C1B1A19181716151413121110",
            "  ......",
        ],
    },
    "verilog_addr_dw1": {
        "function": bin_to_verilog_addr_dw1,
        "description": [
            "Convert to the file which can be loaded by $readmemh to a specific offset of a common memory with 1-byte(8-bit) width",
            "The option \"address\" is accepted as optional. Default is 0x0",
            "The option \"alignment\" is accepted as optional. Default is 32 which means 32 bytes per line",
            "The format will be:",
            "  @0x00000000 00 01 02 03 ...... 1E 1F",
            "  @0x00000020 20 21 22 23 ...... 3E 3F",
            "  ......",
        ],
    },
    "verilog_addr_dw2": {
        "function": bin_to_verilog_addr_dw2,
        "description": [
            "Convert to the file which can be loaded by $readmemh to a specific offset of a common memory with 2-byte(16-bit) width",
            "The option \"address\" is accepted as optional. Default is 0x0",
            "The option \"alignment\" is accepted as optional. Default is 32 which means 32 bytes per line",
            "The format will be:",
            "  @0x00000000 0100 0302 0504 0706 ...... 1D1C 1F1E",
            "  @0x00000020 2120 2322 2524 2726 ...... 3D3C 3F3E",
            "  ......",
        ],
    },
    "verilog_addr_dw4": {
        "function": bin_to_verilog_addr_dw4,
        "description": [
            "Convert to the file which can be loaded by $readmemh to a specific offset of a common memory with 4-byte(32-bit) width",
            "The option \"address\" is accepted as optional. Default is 0x0",
            "The option \"alignment\" is accepted as optional. Default is 32 which means 32 bytes per line",
            "The format will be:",
            "  @0x00000000 03020100 07060504 0B0A0908 0F0E0D0C ...... 1B1A1918 1F1E1D1C",
            "  @0x00000020 23222120 27262524 2B2A2928 2F2E2D2C ...... 3B3A3938 3F3E3D3C",
            "  ......",
        ],
    },
    "verilog_addr_dw8": {
        "function": bin_to_verilog_addr_dw8,
        "description": [
            "Convert to the file which can be loaded by $readmemh to a specific offset of a common memory with 8-byte(64-bit) width",
            "The option \"address\" is accepted as optional. Default is 0x0",
            "The option \"alignment\" is accepted as optional. Default is 32 which means 32 bytes per line",
            "The format will be:",
            "  @0x00000000 0706050403020100 0F0E0D0C0B0A0908 1716151413121110 1F1E1D1C1B1A1918",
            "  @0x00000020 2726252423222120 2F2E2D2C2B2A2928 3736353433323130 3F3E3D3C3B3A3938",
            "  ......",
        ],
    },
    "verilog_addr_dw16": {
        "function": bin_to_verilog_addr_dw16,
        "description": [
            "Convert to the file which can be loaded by $readmemh to a specific offset of a common memory with 16-byte(128-bit) width",
            "The option \"address\" is accepted as optional. Default is 0x0",
            "The option \"alignment\" is accepted as optional. Default is 32 which means 32 bytes per line",
            "The format will be:",
            "  @0x00000000 0F0E0D0C0B0A09080706050403020100 1F1E1D1C1B1A19181716151413121110",
            "  @0x00000020 2F2E2D2C2B2A29282726252423222120 3F3E3D3C3B3A39383736353433323130",
            "  ......",
        ],
    },
}