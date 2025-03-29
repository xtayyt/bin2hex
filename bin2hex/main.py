#!/usr/bin/env python

# 
# Copyright 2025 Yitao Zhang
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#

import sys
import argparse
import inspect
from typing import Optional, BinaryIO, TextIO
from bin2hex import __version__
from bin2hex.bin2c import bin2c_dict
# from bin2hex.bin2ihex import bin2ihex_dict
from bin2hex.bin2model import bin2model_dict
# from bin2hex.bin2srec import bin2srec_dict
from bin2hex.bin2verilog import bin2verilog_dict

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
    #tool_epilog = tool_epilog + " " * 2 + f"{format_str}: {format_description[0]}" + "\n"
    tool_epilog = tool_epilog + " " * 2 + f"{format_str}:" + "\n"
    for i in range(0, len(format_description)):
        tool_epilog = tool_epilog + " " * 4 + f"{format_description[i]}" + "\n"
    tool_epilog = tool_epilog + "\n"
version_help = f"Show version information"
input_help = f"[Required] The raw binary input file to be converted"
output_help = f"[Required] The formatted hex output file to be converted to"
format_help = f"[Optional] The format to be converted to. Default is \"{tool_default_format}\""
address_help = f"[Optional] The start address of the image. Not all formats require. Default is 0x0"
alignment_help = f"[Optional] The byte count per line. Default is various according to the format"
# The entry address is reserved for future use, such as iHex and SRecord
#entry_help = f"[Optional] The start entry address of the executable binary. Default is \"No entry\""

def safe_open(file:str, mode: str = 'r') -> Optional[BinaryIO]:
    try:
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
    parse.add_argument('-i', '--input', type = argparse.FileType('rb'), help = input_help)
    parse.add_argument('-o', '--output', type = argparse.FileType('w'), help = output_help)
    parse.add_argument('-f', '--format', default = tool_default_format, help = format_help)
    parse.add_argument('-a', '--address', type = lambda x:int(x, 0), default = None, help = address_help)
    parse.add_argument('-A', '--alignment', type = lambda x:int(x, 0), default = None, help = alignment_help)
    #parse.add_argument('-e', '--entry', type = lambda x:int(x, 0), default = None, help=entry_help)
    args = parse.parse_args()

    input_file = args.input
    output_file = args.output
    convert_format = args.format
    start_address = args.address
    align_width = args.alignment
    #start_entry = args.entry
    
    # Check the format is supported
    if convert_format not in format_dict:
        print(f"Error: The format {convert_format} is not supported.")
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
    #if start_entry is not None:
    #    if "start_entry" in inspect.signature(convert_function).parameters:
    #        kwargs["start_entry"] = start_entry
    #    else:
    #        print(f"Warning: The format {convert_format} does not support \"entry\" option, which will be ignored.")

    # Read bytes from the input file
    input_data = input_file.read()

    # Perform the conversion
    output_data = convert_function(input_data, **kwargs)

    # Write the hex string to the output file
    output_file.write(output_data)

    return

if __name__ == '__main__':
    raise SystemExit(main())