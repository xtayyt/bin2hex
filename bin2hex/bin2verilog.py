#
# Copyright 2025 Yitao Zhang
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
import inspect

def bin_to_vhex_dwn(input_data:bytes, data_width:int = 1, ecc_encode:callable = None, ecc_skip:int = None, pad_count:int = 0, pad_byte:int = 0xFF, start_address:int = 0x0, swap_endian:int = False) -> str:
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

            if ecc_encode is not None:
                clean_ecc = False
                if ecc_skip is not None:
                    if all(b == (ecc_skip & 0xFF) for b in data):
                        clean_ecc = True
                if "start_address" in inspect.signature(ecc_encode).parameters:
                    data = ecc_encode(data, data_width, start_address)
                else:
                    data = ecc_encode(data, data_width)
                # We cannot skip ECC encoding, because the ECC bit count is unknown here
                if clean_ecc:
                    data = bytes([ecc_skip] * len(data))

            # Pad the data if required
            if pad_count > 0:
               data += bytes([pad_byte] * pad_count)

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
            start_address += data_width
            # Break if no more data to handle
            if count >= len(input_data):
                break
            else:
                output_data += '\n'

    return output_data

def bin_to_vhex_dw1(input_data:bytes, ecc_encode:callable = None, ecc_skip:int = None, pad_count:int = 0, pad_byte:int = 0xFF, start_address:int = 0x0) -> str:
    return bin_to_vhex_dwn(input_data, 1, ecc_encode, ecc_skip, pad_count, pad_byte, start_address, False)

def bin_to_vhex_dw2(input_data:bytes, ecc_encode:callable = None, ecc_skip:int = None, pad_count:int = 0, pad_byte:int = 0xFF, start_address:int = 0x0) -> str:
    return bin_to_vhex_dwn(input_data, 2, ecc_encode, ecc_skip, pad_count, pad_byte, start_address, False)

def bin_to_vhex_dw4(input_data:bytes, ecc_encode:callable = None, ecc_skip:int = None, pad_count:int = 0, pad_byte:int = 0xFF, start_address:int = 0x0) -> str:
    return bin_to_vhex_dwn(input_data, 4, ecc_encode, ecc_skip, pad_count, pad_byte, start_address, False)

def bin_to_vhex_dw8(input_data:bytes, ecc_encode:callable = None, ecc_skip:int = None, pad_count:int = 0, pad_byte:int = 0xFF, start_address:int = 0x0) -> str:
    return bin_to_vhex_dwn(input_data, 8, ecc_encode, ecc_skip, pad_count, pad_byte, start_address, False)

def bin_to_vhex_dw16(input_data:bytes, ecc_encode:callable = None, ecc_skip:int = None, pad_count:int = 0, pad_byte:int = 0xFF, start_address:int = 0x0) -> str:
    return bin_to_vhex_dwn(input_data, 16, ecc_encode, ecc_skip, pad_count, pad_byte, start_address, False)

def bin_to_vhex_addr_dwn(input_data:bytes , start_address:int = 0x0, align_width:int = 4, data_width:int = 1, swap_endian:bool = False) -> str:
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

def bin_to_vhex_addr_dw1(input_data:bytes, start_address:int = 0x0, align_width:int = 32) -> str:
    return bin_to_vhex_addr_dwn(input_data, start_address, align_width, 1, False)

def bin_to_vhex_addr_dw2(input_data:bytes, start_address:int = 0x0, align_width:int = 32) -> str:
    return bin_to_vhex_addr_dwn(input_data, start_address, align_width, 2, False)

def bin_to_vhex_addr_dw4(input_data:bytes, start_address:int = 0x0, align_width:int = 32) -> str:
    return bin_to_vhex_addr_dwn(input_data, start_address, align_width, 4, False)

def bin_to_vhex_addr_dw8(input_data:bytes, start_address:int = 0x0, align_width:int = 32) -> str:
    return bin_to_vhex_addr_dwn(input_data, start_address, align_width, 8, False)

def bin_to_vhex_addr_dw16(input_data:bytes, start_address:int = 0x0, align_width:int = 32) -> str:
    return bin_to_vhex_addr_dwn(input_data, start_address, align_width, 16, False)

def bin_to_vbin_dwn(input_data:bytes, data_width:int = 1, ecc_encode:callable = None, ecc_skip:int = None, pad_count:int = 0, pad_byte: int = 0xFF, start_address:int = 0x0, swap_endian:int = False) -> str:
    data = bin_to_vhex_dwn(input_data, data_width, ecc_encode, ecc_skip, pad_count, pad_byte, start_address, swap_endian)
    data_lines = data.splitlines()
    data_bin = ""
    for data_line in data_lines:
        data_bin += bin(int(data_line,16))[2:].zfill(len(data_line)*4) + '\n'
    return data_bin.rstrip('\n')

def bin_to_vbin_dw1(input_data:bytes, ecc_encode:callable = None, ecc_skip:int = None, pad_count:int = 0, pad_byte:int = 0xFF, start_address:int = 0x0) -> str:
    return bin_to_vbin_dwn(input_data, 1, ecc_encode, ecc_skip, pad_count, pad_byte, start_address, False)

def bin_to_vbin_dw2(input_data:bytes, ecc_encode:callable = None, ecc_skip:int = None, pad_count:int = 0, pad_byte:int = 0xFF, start_address:int = 0x0) -> str:
    return bin_to_vbin_dwn(input_data, 2, ecc_encode, ecc_skip, pad_count, pad_byte, start_address, False)

def bin_to_vbin_dw4(input_data:bytes, ecc_encode:callable = None, ecc_skip:int = None, pad_count:int = 0, pad_byte:int = 0xFF, start_address:int = 0x0) -> str:
    return bin_to_vbin_dwn(input_data, 4, ecc_encode, ecc_skip, pad_count, pad_byte, start_address, False)

def bin_to_vbin_dw8(input_data:bytes, ecc_encode:callable = None, ecc_skip:int = None, pad_count:int = 0, pad_byte:int = 0xFF, start_address:int = 0x0) -> str:
    return bin_to_vbin_dwn(input_data, 8, ecc_encode, ecc_skip, pad_count, pad_byte, start_address, False)

def bin_to_vbin_dw16(input_data:bytes, ecc_encode:callable = None, ecc_skip:int = None, pad_count:int = 0, pad_byte:int = 0xFF, start_address:int = 0x0) -> str:
    return bin_to_vbin_dwn(input_data, 16, ecc_encode, ecc_skip, pad_count, pad_byte, start_address, False)

bin2verilog_dict = {
    "vhex_dw1": {
        "function": bin_to_vhex_dw1,
        "description": [
            "Convert to the file which can be loaded by $readmemh to a common memory with 1-byte(8-bit) width",
            "The option \"ecc\" is accepted as optional. Default is \"none\"",
            "The option \"ecc-skip-all-ones\" is accepted as optional. Default is False which means no skip",
            "The option \"ecc-skip-all-zeros\" is accepted as optional. Default is False which means no skip",
            "The option \"address\" is accepted as optional for ECC calculation. Default is 0x0",
            "The option \"pad-count\" is accepted as optional. Default is 0 which means no padding",
            "The option \"pad-byte\" is accepted as optional. Default is \"0xFF\"",
            "The format will be:",
            "  00",
            "  01",
            "  ......",
        ],
    },
    "vhex_dw2": {
        "function": bin_to_vhex_dw2,
        "description": [
            "Convert to the file which can be loaded by $readmemh to a common memory with 2-byte(16-bit) width",
            "The option \"ecc\" is accepted as optional. Default is \"none\"",
            "The option \"ecc-skip-all-ones\" is accepted as optional. Default is False which means no skip",
            "The option \"ecc-skip-all-zeros\" is accepted as optional. Default is False which means no skip",
            "The option \"address\" is accepted as optional for ECC calculation. Default is 0x0",
            "The option \"pad-count\" is accepted as optional. Default is 0 which means no padding",
            "The option \"pad-byte\" is accepted as optional. Default is \"0xFF\"",
            "The format will be:",
            "  0100",
            "  0302",
            "  ......",
        ],
    },
    "vhex_dw4": {
        "function": bin_to_vhex_dw4,
        "description": [
            "Convert to the file which can be loaded by $readmemh to a common memory with 4-byte(32-bit) width",
            "The option \"ecc\" is accepted as optional. Default is \"none\"",
            "The option \"ecc-skip-all-ones\" is accepted as optional. Default is False which means no skip",
            "The option \"ecc-skip-all-zeros\" is accepted as optional. Default is False which means no skip",
            "The option \"address\" is accepted as optional for ECC calculation. Default is 0x0",
            "The option \"pad-count\" is accepted as optional. Default is 0 which means no padding",
            "The option \"pad-byte\" is accepted as optional. Default is \"0xFF\"",
            "The format will be:",
            "  03020100",
            "  07060504",
            "  ......",
        ],
    },
    "vhex_dw8": {
        "function": bin_to_vhex_dw8,
        "description": [
            "Convert to the file which can be loaded by $readmemh to a common memory with 8-byte(64-bit) width",
            "The option \"ecc\" is accepted as optional. Default is \"none\"",
            "The option \"ecc-skip-all-ones\" is accepted as optional. Default is False which means no skip",
            "The option \"ecc-skip-all-zeros\" is accepted as optional. Default is False which means no skip",
            "The option \"address\" is accepted as optional for ECC calculation. Default is 0x0",
            "The option \"pad-count\" is accepted as optional. Default is 0 which means no padding",
            "The option \"pad-byte\" is accepted as optional. Default is \"0xFF\"",
            "The format will be:",
            "  0706050403020100",
            "  0F0E0D0C0B0A0908",
            "  ......",
        ],
    },
    "vhex_dw16": {
        "function": bin_to_vhex_dw16,
        "description": [
            "Convert to the file which can be loaded by $readmemh to a common memory with 16-byte(128-bit) width",
            "The option \"ecc\" is accepted as optional. Default is \"none\"",
            "The option \"ecc-skip-all-ones\" is accepted as optional. Default is False which means no skip",
            "The option \"ecc-skip-all-zeros\" is accepted as optional. Default is False which means no skip",
            "The option \"address\" is accepted as optional for ECC calculation. Default is 0x0",
            "The option \"pad-count\" is accepted as optional. Default is 0 which means no padding",
            "The option \"pad-byte\" is accepted as optional. Default is \"0xFF\"",
            "The format will be:",
            "  0F0E0D0C0B0A09080706050403020100",
            "  1F1E1D1C1B1A19181716151413121110",
            "  ......",
        ],
    },
    "verilog_dw1": {
        "function": bin_to_vhex_dw1,
        "description": [
            "Alias name of \"vhex_dw1\" format",
        ],
    },
    "verilog_dw2": {
        "function": bin_to_vhex_dw2,
        "description": [
            "Alias name of \"vhex_dw2\" format",
        ],
    },
    "verilog_dw4": {
        "function": bin_to_vhex_dw4,
        "description": [
            "Alias name of \"vhex_dw4\" format",
        ],
    },
    "verilog_dw8": {
        "function": bin_to_vhex_dw8,
        "description": [
            "Alias name of \"vhex_dw8\" format",
        ],
    },
    "verilog_dw16": {
        "function": bin_to_vhex_dw16,
        "description": [
            "Alias name of \"vhex_dw16\" format",
        ],
    },
    "vhex_addr_dw1": {
        "function": bin_to_vhex_addr_dw1,
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
    "vhex_addr_dw2": {
        "function": bin_to_vhex_addr_dw2,
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
    "vhex_addr_dw4": {
        "function": bin_to_vhex_addr_dw4,
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
    "vhex_addr_dw8": {
        "function": bin_to_vhex_addr_dw8,
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
    "vhex_addr_dw16": {
        "function": bin_to_vhex_addr_dw16,
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
    "verilog_addr_dw1": {
        "function": bin_to_vhex_addr_dw1,
        "description": [
            "Alias name of \"vhex_addr_dw1\" format",
        ],
    },
    "verilog_addr_dw2": {
        "function": bin_to_vhex_addr_dw2,
        "description": [
            "Alias name of \"vhex_addr_dw2\" format",
        ],
    },
    "verilog_addr_dw4": {
        "function": bin_to_vhex_addr_dw4,
        "description": [
            "Alias name of \"vhex_addr_dw4\" format",
        ],
    },
    "verilog_addr_dw8": {
        "function": bin_to_vhex_addr_dw8,
        "description": [
            "Alias name of \"vhex_addr_dw8\" format",
        ],
    },
    "verilog_addr_dw16": {
        "function": bin_to_vhex_addr_dw16,
        "description": [
            "Alias name of \"vhex_addr_dw16\" format",
        ],
    },
    "vbin_dw1": {
        "function": bin_to_vbin_dw1,
        "description": [
            "Convert to the file which can be loaded by $readmemb to a common memory with 1-byte(8-bit) width",
            "The option \"ecc\" is accepted as optional. Default is \"none\"",
            "The option \"ecc-skip-all-ones\" is accepted as optional. Default is False which means no skip",
            "The option \"ecc-skip-all-zeros\" is accepted as optional. Default is False which means no skip",
            "The option \"address\" is accepted as optional for ECC calculation. Default is 0x0",
            "The option \"pad-count\" is accepted as optional. Default is 0 which means no padding",
            "The option \"pad-byte\" is accepted as optional. Default is \"0xFF\"",
            "The format will be:",
            "  00000000",
            "  00000001",
            "  ......",
        ],
    },
    "vbin_dw2": {
        "function": bin_to_vbin_dw2,
        "description": [
            "Convert to the file which can be loaded by $readmemb to a common memory with 2-byte(16-bit) width",
            "The option \"ecc\" is accepted as optional. Default is \"none\"",
            "The option \"ecc-skip-all-ones\" is accepted as optional. Default is False which means no skip",
            "The option \"ecc-skip-all-zeros\" is accepted as optional. Default is False which means no skip",
            "The option \"address\" is accepted as optional for ECC calculation. Default is 0x0",
            "The option \"pad-count\" is accepted as optional. Default is 0 which means no padding",
            "The option \"pad-byte\" is accepted as optional. Default is \"0xFF\"",
            "The format will be:",
            "  0000000100000000",
            "  0000001100000010",
            "  ......",
        ],
    },
    "vbin_dw4": {
        "function": bin_to_vbin_dw4,
        "description": [
            "Convert to the file which can be loaded by $readmemb to a common memory with 4-byte(32-bit) width",
            "The option \"ecc\" is accepted as optional. Default is \"none\"",
            "The option \"ecc-skip-all-ones\" is accepted as optional. Default is False which means no skip",
            "The option \"ecc-skip-all-zeros\" is accepted as optional. Default is False which means no skip",
            "The option \"address\" is accepted as optional for ECC calculation. Default is 0x0",
            "The option \"pad-count\" is accepted as optional. Default is 0 which means no padding",
            "The option \"pad-byte\" is accepted as optional. Default is \"0xFF\"",
            "The format will be:",
            "  00000011000000100000000100000000",
            "  00000111000001100000010100000100",
            "  ......",
        ],
    },
    "vbin_dw8": {
        "function": bin_to_vbin_dw8,
        "description": [
            "Convert to the file which can be loaded by $readmemb to a common memory with 8-byte(64-bit) width",
            "The option \"ecc\" is accepted as optional. Default is \"none\"",
            "The option \"ecc-skip-all-ones\" is accepted as optional. Default is False which means no skip",
            "The option \"ecc-skip-all-zeros\" is accepted as optional. Default is False which means no skip",
            "The option \"address\" is accepted as optional for ECC calculation. Default is 0x0",
            "The option \"pad-count\" is accepted as optional. Default is 0 which means no padding",
            "The option \"pad-byte\" is accepted as optional. Default is \"0xFF\"",
            "The format will be:",
            "  0000011100000110000001010000010000000011000000100000000100000000",
            "  0000111100001110000011010000110000001011000010100000100100001000",
            "  ......",
        ],
    },
    "vbin_dw16": {
        "function": bin_to_vbin_dw16,
        "description": [
            "Convert to the file which can be loaded by $readmemb to a common memory with 16-byte(128-bit) width",
            "The option \"ecc\" is accepted as optional. Default is \"none\"",
            "The option \"ecc-skip-all-ones\" is accepted as optional. Default is False which means no skip",
            "The option \"ecc-skip-all-zeros\" is accepted as optional. Default is False which means no skip",
            "The option \"address\" is accepted as optional for ECC calculation. Default is 0x0",
            "The option \"pad-count\" is accepted as optional. Default is 0 which means no padding",
            "The option \"pad-byte\" is accepted as optional. Default is \"0xFF\"",
            "The format will be:",
            "  00001111000011100000110100001100000010110000101000001001000010000000011100000110000001010000010000000011000000100000000100000000",
            "  00011111000111100001110100011100000110110001101000011001000110000001011100010110000101010001010000010011000100100001000100010000",
            "  ......",
        ],
    },
}