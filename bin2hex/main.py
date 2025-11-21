#!/usr/bin/env python

#
# Copyright 2025 Yitao Zhang
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#

import os
import sys
import argparse
import inspect
import importlib.util

from typing import Optional, BinaryIO
from bin2hex import __version__
from bin2hex.bin2c import bin2c_dict
# from bin2hex.bin2ihex import bin2ihex_dict
from bin2hex.bin2model import bin2model_dict
# from bin2hex.bin2srec import bin2srec_dict
from bin2hex.bin2verilog import bin2verilog_dict
from bin2hex.ecc import ecc_dict

format_dict = {
    **bin2c_dict,
    #**bin2ihex_dict,
    **bin2model_dict,
    #**bin2srec_dict,
    **bin2verilog_dict,
}

tool_default_format= "verilog_dw1"

tool_description = f"bin2hex is an utility to convert binary file to multiple types of hexadecimal text file"
tool_epilog = f"Supported format:\n"
for format_str, format_sub_dict in format_dict.items():
    format_description = format_sub_dict["description"]
    tool_epilog = tool_epilog + " " * 2 + f"{format_str}:" + "\n"
    for i in range(0, len(format_description)):
        tool_epilog = tool_epilog + " " * 4 + f"{format_description[i]}" + "\n"
    tool_epilog = tool_epilog + "\n"
tool_epilog = tool_epilog + f"Supported ECC algorithm: \n"
for ecc_str, ecc_sub_dict in ecc_dict.items():
    ecc_description = ecc_sub_dict["description"]
    tool_epilog = tool_epilog + " " * 2 + f"{ecc_str}:" + "\n"
    for i in range(0, len(ecc_description)):
        tool_epilog = tool_epilog + " " * 4 + f"{ecc_description[i]}" + "\n"
version_help = f"Show version information"
input_help = f"[Required] The raw binary input file to be converted"
output_help = f"[Required] The formatted hex output file to be converted to"
format_help = f"[Optional] The format to be converted to. Default is \"{tool_default_format}\""
address_help = f"[Optional] The start address of the image. Not all formats require. Default is 0x0"
alignment_help = f"[Optional] The byte count per line. Default is various according to the format"
ecc_help = f"[Optional] The ECC type to be calculated. Not all formats require. Default is \"none\""
ecc_skip_all_ones_help = f"[Optional] Skip ECC calculation for all-ones data blocks. Useful for FLASH memory with erased state as all-ones"
ecc_skip_all_zeros_help = f"[Optional] Skip ECC calculation for all-zeros data blocks. Useful for FLASH memory with erased state as all-zeros"
pad_count_help = f"[Optional] The byte count to be padded to hex lines. Default is 0." + \
                f"It is useful to generate the hex file which's memory width is larger than data width, such as FLASH memory with ECC"
pad_byte_help = f"[Optional] The padding byte. Due to the typical use case of FLASH memory, default is \"0xFF\""
split_help = f"[Optional] Split the output into multiple files with suffix \"_0\", \"_1\", ... according to the split byte count" + \
             f"Must be power of 2. Default is 1(no split)"
# The entry address is reserved for future use, such as iHex and SRecord
#entry_help = f"[Optional] The start entry address of the executable binary. Default is \"No entry\""

def safe_open(file:str, mode: str = 'r') -> Optional[BinaryIO]:
    try:
        if file is None:
            print(f"Error: No file specified.")
            return None
        if 'b' in mode:
            return open(file, mode)
        else:
            # With newline='', no conversion between CRLF and LF is performed automatically
            return open(file, mode, newline='')
    except FileNotFoundError:
        print(f"Error: {file} doesn't exist.")
    except PermissionError:
        print(f"Error: Permission denied for {file}")
    except IsADirectoryError:
        print(f"Error: {file} is a directory, not a file")
    except OSError as e:
        print(f"Error: Failed to open {file}.")
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
    return None

def main() -> bool:
    # parse the input arguments
    parse = argparse.ArgumentParser(formatter_class = argparse.RawDescriptionHelpFormatter and argparse.RawTextHelpFormatter, description = tool_description, epilog = tool_epilog)
    parse.add_argument('-v', '--version', action = 'version', version=__version__, help = version_help)
    parse.add_argument('-i', '--input', type = str, help = input_help)
    parse.add_argument('-o', '--output', type = str, help = output_help)
    parse.add_argument('-f', '--format', default = tool_default_format, help = format_help)
    parse.add_argument('-a', '--address', type = lambda x:int(x, 0), default = None, help = address_help)
    parse.add_argument('-A', '--alignment', type = lambda x:int(x, 0), default = None, help = alignment_help)
    parse.add_argument('-e', '--ecc', default = None, help = ecc_help)
    parse.add_argument('--ecc-skip-all-ones', action='store_true', help = ecc_skip_all_ones_help)
    parse.add_argument('--ecc-skip-all-zeros', action='store_true', help = ecc_skip_all_zeros_help)
    parse.add_argument('-c', '--pad-count', type = lambda x:int(x, 0), default = None, help = pad_count_help)
    parse.add_argument('-b', '--pad-byte', type = lambda x:int(x, 0), default = None, help = pad_byte_help)
    parse.add_argument('-s', '--split', type = lambda x:int(x, 0), default = None, help = split_help)
    #parse.add_argument('-E', '--entry', type = lambda x:int(x, 0), default = None, help=entry_help)
    args = parse.parse_args()

    input_file = args.input
    output_file = args.output
    convert_format = args.format
    start_address = args.address
    align_width = args.alignment
    ecc = args.ecc
    ecc_skip_all_ones = args.ecc_skip_all_ones
    ecc_skip_all_zeros = args.ecc_skip_all_zeros
    pad_count = args.pad_count
    pad_byte = args.pad_byte
    split_count = args.split
    #start_entry = args.entry

    if len(sys.argv) == 1:
        parse.print_usage()
        return True

    if split_count is not None:
        if split_count <= 0 or (split_count & (split_count - 1)) != 0:
            print(f"Warning: The split count {split_count} is not valid. It must be a power of 2 (1, 2, 4, 8, ...). The option will be ignored.")
            split_count = 1
    else:
        split_count = 1

    ifile = safe_open(input_file, 'rb')
    if ifile is None:
        return False

    ofiles = []
    if split_count == 1:
        ofiles.append(safe_open(output_file, 'w'))
    else:
        for i in range(split_count):
            name, extension = output_file.rsplit('.', 1)
            ofiles.append(safe_open(f"{name}_{i}.{extension}", 'w'))

    # Check the format is supported
    if convert_format not in format_dict:
        print(f"Error: The format {convert_format} is not supported.")
        return False

    if ecc_skip_all_ones is True and ecc_skip_all_zeros is True:
        print(f"Error: Both ecc-skip-all-ones and ecc-skip-all-zeros are enabled. Only one of them can be enabled at a time.")
        return False

    # Prepare the conversion function and arguments
    convert_function = format_dict[convert_format]["function"]
    kwargs = {}
    if start_address is not None:
        if "start_address" in inspect.signature(convert_function).parameters:
            kwargs["start_address"] = start_address
        else:
            print(f"Warning: The format {convert_format} does not support \"address\" option, which will be ignored.")
    if align_width is not None:
        if "align_width" in inspect.signature(convert_function).parameters:
            kwargs["align_width"] = align_width
        else:
            print(f"Warning: The format {convert_format} does not support \"alignment\" option, which will be ignored.")
    if ecc is not None:
        if "ecc_encode" in inspect.signature(convert_function).parameters:
            if ecc_skip_all_ones is True:
                kwargs["ecc_skip"] = 0xFF
            if ecc_skip_all_zeros is True:
                kwargs["ecc_skip"] = 0x00
            if ecc in ecc_dict:
                kwargs["ecc_encode"] = ecc_dict[ecc]["function"]
            else:
                if (os.path.isfile(ecc)):
                    ecc_spec = importlib.util.spec_from_file_location("python2_module", ecc)
                    ecc_module = importlib.util.module_from_spec(ecc_spec)
                    ecc_spec.loader.exec_module(ecc_module)
                    if hasattr(ecc_module, 'ecc_encode'):
                        kwargs["ecc_encode"] = getattr(ecc_module, 'ecc_encode')
                    else:
                        print(f"Warning: Doesn't find ecc_encode function in {ecc}. Using default \"none\".")
                        kwargs["ecc_encode"] = None
                else:
                    print(f"Warning: The ECC type {ecc} is not supported. Using default \"none\".")
                    kwargs["ecc_encode"] = None
        else:
            print(f"Warning: The format {convert_format} does not support \"ecc\" option, which will be ignored.")
            if ecc_skip_all_ones is True:
                print(f"Warning: The format {convert_format} does not support \"ecc\" option, so the \"ecc-skip-all-ones\" option will be ignored.")
            if ecc_skip_all_zeros is True:
                print(f"Warning: The format {convert_format} does not support \"ecc\" option, so the \"ecc-skip-all-zeros\" option will be ignored.")
    if pad_count is not None:
        if "pad_count" in inspect.signature(convert_function).parameters:
            kwargs["pad_count"] = pad_count
        else:
            print(f"Warning: The format {convert_format} does not support \"padcount\" option, which will be ignored.")
    if pad_byte is not None:
        if pad_count is not None:
            if "pad_byte" in inspect.signature(convert_function).parameters:
                if pad_byte < 0 or pad_byte > 255:
                    print(f"Warning: The pad byte {pad_byte} is out of range (0-255). Pad byte will be masked to 0-255.")
                kwargs["pad_byte"] = pad_byte & 0xFF
            else:
                print(f"Warning: The format {convert_format} does not support \"padbyte\" option, which will be ignored.")
        else:
            print(f"Warning: The pad byte is specified but pad count is not specified. The pad byte option will be ignored.")

    #if start_entry is not None:
    #    if "start_entry" in inspect.signature(convert_function).parameters:
    #        kwargs["start_entry"] = start_entry
    #    else:
    #        print(f"Warning: The format {convert_format} does not support \"entry\" option, which will be ignored.")

    # Read bytes from the input file
    input_data = ifile.read()

    # Perform the conversion
    output_data = convert_function(input_data, **kwargs)


    # Write the hex string to the output file
    output_data_lines = output_data.splitlines(keepends=True)
    i = 0
    for output_data_line in output_data_lines:
        ofiles[i % split_count].write(output_data_line)
        i = i + 1

    return

if __name__ == '__main__':
    raise SystemExit(main())