# bin2hex

## What is bin2hex

bin2hex is an utility to convert binary file to multiple types of hexadecimal text file

## How to use bin2hex

```
bin2hex [-h] [-v] [-i INPUT] [-o OUTPUT] [-f FORMAT] [-a ADDRESS] [-A ALIGNMENT]

options:
  -h, --help            show this help message and exit
  -v, --version         Show version information
  -i, --input INPUT     [Required] The raw binary input file to be converted
  -o, --output OUTPUT   [Required] The formatted hex output file to be converted to
  -f, --format FORMAT   [Optional] The format to be converted to. Default is "verilog_dw1"
  -a, --address ADDRESS
                        [Optional] The start address of the image. Not all formats require. Default is 0x0
  -A, --alignment ALIGNMENT
                        [Optional] The byte count per line. Default is various according to the format
```

## Supported text file types

### C
1. uint8:
- Convert to the c header file which can be included by C source file to init an 'uint8_t' table
- The option "alignment" is accepted as optional. Default is 16, which means 16 bytes per line
- The format will be:
```
0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F
0x10, 0x11 ......
```
2. uint16:
- Convert to the c header file which can be included by C source file to init an 'uint16_t' table
- The option "alignment" is accepted as optional. Default is 16, which means 16 bytes per line
- The format will be:
```
0x0100, 0x0302, 0x0504, 0x0706, 0x0908, 0x0B0A, 0x0D0C, 0x0F0E
0x1110, 0x1312 ......
```
3. uint32:
- Convert to the c header file which can be included by C source file to init an 'uint32_t' table
- The option "alignment" is accepted as optional. Default is 16, which means 16 bytes per line
- The format will be:
```
0x03020100, 0x07060504, 0x0B0A0908, 0x0F0E0D0C,
0x13121110, 0x17161514 ......
```
4. uint64:
- Convert to the c header file which can be included by C source file to init an 'uint64_t' table.
- The option "alignment" is accepted as optional. Default is 16, which means 16 bytes per line
- The format will be:
```
0x0706050403020100, 0x0F0E0D0C0B0A0908,
0x1716151413121110,  ......
```
### Sim Model
1. Cadence Denali Model
- Convert to the file which can be used by Cadence denali model
- No option is accepted
- The format will be:
```
      0/00
      1/01
      ......
```

### Verilog HDL
1. Verilog Data Width 1-Byte:
- Convert to the file which can be loaded by $readmemh to a common memory with 1-byte(8-bit) width
- No option is accepted
- The format will be:
```
00
01
......
```

2. Verilog Data Width 2-Byte:
- Convert to the file which can be loaded by $readmemh to a common memory with 2-byte(16-bit) width
- No option is accepted
- The format will be:
```
0100
0302
......
```

3. Verilog Data Width 4-Byte:
- Convert to the file which can be loaded by $readmemh to a common memory with 4-byte(32-bit) width
- No option is accepted
- The format will be:
```
03020100
07060504
......
```

4. Verilog Data Width 8-Byte:
- Convert to the file which can be loaded by $readmemh to a common memory with 8-byte(64-bit) width
- No option is accepted
- The format will be:
```
0706050403020100
0F0E0D0C0B0A0908
......
```

5. Verilog Data Width 16-Byte:
- Convert to the file which can be loaded by $readmemh to a common memory with 16-byte(128-bit) width
- No option is accepted
- The format will be:
```
0F0E0D0C0B0A09080706050403020100
1F1E1D1C1B1A19181716151413121110
......
```

6. Verilog Data Width 1-Byte with Address:
- Convert to the file which can be loaded by $readmemh to a specific offset of a common memory with 1-byte(8-bit) width
- The option "address" is accepted as optional. Default is 0x0
- The option "alignment" is accepted as optional. Default is 32 which means 32 bytes per line
- The format will be:
```
@0x00000000 00 01 02 03 ...... 1E 1F
@0x00000020 20 21 22 23 ...... 3E 3F
......
```

7. Verilog Data Width 2-Byte with Address:
- Convert to the file which can be loaded by $readmemh to a specific offset of a common memory with 2-byte(16-bit) width
- The option "address" is accepted as optional. Default is 0x0
- The option "alignment" is accepted as optional. Default is 32 which means 32 bytes per line
- The format will be:
```
@0x00000000 0100 0302 0504 0706 ...... 1D1C 1F1E
@0x00000020 2120 2322 2524 2726 ...... 3D3C 3F3E
......
```

8. Verilog Data Width 4-Byte with Address:
- Convert to the file which can be loaded by $readmemh to a specific offset of a common memory with 4-byte(32-bit) width
- The option "address" is accepted as optional. Default is 0x0
- The option "alignment" is accepted as optional. Default is 32 which means 32 bytes per line
- The format will be:
```
@0x00000000 03020100 07060504 0B0A0908 0F0E0D0C ...... 1B1A1918 1F1E1D1C
@0x00000020 23222120 27262524 2B2A2928 2F2E2D2C ...... 3B3A3938 3F3E3D3C
......
```

9. Verilog Data Width 8-Byte with Address:
- Convert to the file which can be loaded by $readmemh to a specific offset of a common memory with 8-byte(64-bit) width
- The option "address" is accepted as optional. Default is 0x0
- The option "alignment" is accepted as optional. Default is 32 which means 32 bytes per line
- The format will be:
```
@0x00000000 0706050403020100 0F0E0D0C0B0A0908 1716151413121110 1F1E1D1C1B1A1918
@0x00000020 2726252423222120 2F2E2D2C2B2A2928 3736353433323130 3F3E3D3C3B3A3938
......
```

9. Verilog Data Width 16-Byte with Address:
- Convert to the file which can be loaded by $readmemh to a specific offset of a common memory with 16-byte(128-bit) width
- The option "address" is accepted as optional. Default is 0x0
- The option "alignment" is accepted as optional. Default is 32 which means 32 bytes per line
- The format will be:
```
@0x00000000 0F0E0D0C0B0A09080706050403020100 1F1E1D1C1B1A19181716151413121110
@0x00000020 2F2E2D2C2B2A29282726252423222120 3F3E3D3C3B3A39383736353433323130
......
```

## Supported text file types
1. None:
- No ECC is added

2. ARM SECDED:
- Single Error Correction Double Error Detection (SECDED) code
- The ECC bits are appended to the MSB side of the data
- Only verilog_dwx (x = 4, 8, 16) formats support this ECC

3. User specific algorithm
- Custom ECC function defined in the specified Python file
- The Python file should define a function named ecc_encode
```
def ecc_encode(data: bytes, data_width: int) -> bytes
    # Add user specific algorithm here
    return data + ecc_bytes
```
- data is the input data in bytes
- data_width is the data width in bytes
- The function should return the data with ECC bits appended to the MSB side in bytes
- Only verilog_dwx (x = 1, 2, 4, 8, 16) formats support this ECC