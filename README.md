# bin2hex

## What is bin2hex

bin2hex is an utility to convert binary file to multiple types of hexadecimal text file

## How to use bin2hex

```
bin2hex [-h] [-v] [-i INPUT] [-o OUTPUT] [-f FORMAT] [-a ADDRESS] [-A ALIGNMENT] [-e ECC]
        [--ecc-skip-all-ones] [--ecc-skip-all-zeros] [-c PAD_COUNT] [-b PAD_BYTE] [-s SPLIT]

options:
  -h, --help            Show this help message and exit
  -v, --version         Show version information
  -i, --input INPUT     [Required] The raw binary input file to be converted
  -o, --output OUTPUT   [Required] The formatted hex output file to be converted to
  -f, --format FORMAT   [Optional] The format to be converted to. Default is "vhex_dw1"
  -a, --address ADDRESS
                        [Optional] The start address of the image. Not all formats require. Default is
                        0x0
  -A, --alignment ALIGNMENT
                        [Optional] The byte count per line. Default is various according to the format
  -e, --ecc ECC         [Optional] The ECC type to be calculated. Not all formats require. Default is
                        "none"
  --ecc-skip-all-ones   [Optional] Skip ECC calculation for all-ones data blocks. Useful for FLASH
                        memory with erased state as all-ones
  --ecc-skip-all-zeros  [Optional] Skip ECC calculation for all-zeros data blocks. Useful for FLASH
                        memory with erased state as all-zeros
  -c, --pad-count PADCOUNT
                        [Optional] The byte count to be padded to hex lines. Default is 0.
                        It is useful to generate the hex file which's memory width is larger than data
                        width, such as FLASH memory with ECC
  -b, --byte-count BYTECOUNT
                        [Optional] The padding byte. Due to the typical use case of FLASH memory.
                        Default is "0xFF"
  -s, --split SPLIT     [Optional] Split the output into multiple files with suffix "_0", "_1", ...
                        according to the split byte count.  Must be power of 2. Default is 1(no split)
```

## Supported text file types

### C
1. uint8(--format c_uint8):
- Convert to the c header file which can be included by C source file to init an 'uint8_t' table
- The option "alignment" is accepted as optional. Default is 16, which means 16 bytes per line
- The format will be:
```
0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F
0x10, 0x11 ......
```
2. uint16(--format c_uint16):
- Convert to the c header file which can be included by C source file to init an 'uint16_t' table
- The option "alignment" is accepted as optional. Default is 16, which means 16 bytes per line
- The format will be:
```
0x0100, 0x0302, 0x0504, 0x0706, 0x0908, 0x0B0A, 0x0D0C, 0x0F0E
0x1110, 0x1312 ......
```
3. uint32(--format c_uint32):
- Convert to the c header file which can be included by C source file to init an 'uint32_t' table
- The option "alignment" is accepted as optional. Default is 16, which means 16 bytes per line
- The format will be:
```
0x03020100, 0x07060504, 0x0B0A0908, 0x0F0E0D0C,
0x13121110, 0x17161514 ......
```
4. uint64(--format c_uint64):
- Convert to the c header file which can be included by C source file to init an 'uint64_t' table.
- The option "alignment" is accepted as optional. Default is 16, which means 16 bytes per line
- The format will be:
```
0x0706050403020100, 0x0F0E0D0C0B0A0908,
0x1716151413121110,  ......
```
### Sim Model
1. Cadence Denali Model(--format denali)
- Convert to the file which can be used by Cadence denali model
- No option is accepted
- The format will be:
```
      0/00
      1/01
      ......
```

### Verilog HDL(VHEX)
1. Verilog HEX, Data Width 1-Byte(--format vhex_dw1 or --format verilog_dw1):
- Convert to the file which can be loaded by $readmemh to a common memory with 1-byte(8-bit) width
- The option "ecc" is accepted as optional. Default is "none"
- The option "ecc-skip-all-ones" is accepted as optional. Default is False which means no skip
- The option "ecc-skip-all-zeros" is accepted as optional. Default is False which means no skip
- The option "address" is accepted as optional for ECC calculation. Default is 0x0
- The option "pad-count" is accepted as optional. Default is 0 which means no padding
- The option "pad-byte" is accepted as optional. Default is "0xFF"
- The format will be:
```
00
01
......
```

2. Verilog HEX, Data Width 2-Byte(--format vhex_dw2 or --format verilog_dw2):
- Convert to the file which can be loaded by $readmemh to a common memory with 2-byte(16-bit) width
- The option "ecc" is accepted as optional. Default is "none"
- The option "ecc-skip-all-ones" is accepted as optional. Default is False which means no skip
- The option "ecc-skip-all-zeros" is accepted as optional. Default is False which means no skip
- The option "address" is accepted as optional for ECC calculation. Default is 0x0
- The option "pad-count" is accepted as optional. Default is 0 which means no padding
- The option "pad-byte" is accepted as optional. Default is "0xFF"
- The format will be:
```
0100
0302
......
```

3. Verilog HEX, Data Width 4-Byte(--format vhex_dw4 or --format verilog_dw4):
- Convert to the file which can be loaded by $readmemh to a common memory with 4-byte(32-bit) width
- The option "ecc" is accepted as optional. Default is "none"
- The option "ecc-skip-all-ones" is accepted as optional. Default is False which means no skip
- The option "ecc-skip-all-zeros" is accepted as optional. Default is False which means no skip
- The option "address" is accepted as optional for ECC calculation. Default is 0x0
- The option "pad-count" is accepted as optional. Default is 0 which means no padding
- The option "pad-byte" is accepted as optional. Default is "0xFF"
- The format will be:
```
03020100
07060504
......
```

4. Verilog HEX, Data Width 8-Byte(--format vhex_dw8 or --format verilog_dw8):
- Convert to the file which can be loaded by $readmemh to a common memory with 8-byte(64-bit) width
- The option "ecc" is accepted as optional. Default is "none"
- The option "ecc-skip-all-ones" is accepted as optional. Default is False which means no skip
- The option "ecc-skip-all-zeros" is accepted as optional. Default is False which means no skip
- The option "address" is accepted as optional for ECC calculation. Default is 0x0
- The option "pad-count" is accepted as optional. Default is 0 which means no padding
- The option "pad-byte" is accepted as optional. Default is "0xFF"
- The format will be:
```
0706050403020100
0F0E0D0C0B0A0908
......
```

5. Verilog HEX, Data Width 16-Byte(--format vhex_dw16 or --format verilog_dw16):
- Convert to the file which can be loaded by $readmemh to a common memory with 16-byte(128-bit) width
- The option "ecc" is accepted as optional. Default is "none"
- The option "ecc-skip-all-ones" is accepted as optional. Default is False which means no skip
- The option "ecc-skip-all-zeros" is accepted as optional. Default is False which means no skip
- The option "address" is accepted as optional for ECC calculation. Default is 0x0
- The option "pad-count" is accepted as optional. Default is 0 which means no padding
- The option "pad-byte" is accepted as optional. Default is "0xFF"
- The format will be:
```
0F0E0D0C0B0A09080706050403020100
1F1E1D1C1B1A19181716151413121110
......
```

6. Verilog HEX, Data Width 1-Byte with Address(--format vhex_addr_dw1 or --format verilog_addr_dw1):
- Convert to the file which can be loaded by $readmemh to a specific offset of a common memory with 1-byte(8-bit) width
- The option "address" is accepted as optional. Default is 0x0
- The option "alignment" is accepted as optional. Default is 32 which means 32 bytes per line
- The format will be:
```
@0x00000000 00 01 02 03 ...... 1E 1F
@0x00000020 20 21 22 23 ...... 3E 3F
......
```

7. Verilog HEX, Data Width 2-Byte with Address(--format vhex_addr_dw2 or --format verilog_addr_dw2):
- Convert to the file which can be loaded by $readmemh to a specific offset of a common memory with 2-byte(16-bit) width
- The option "address" is accepted as optional. Default is 0x0
- The option "alignment" is accepted as optional. Default is 32 which means 32 bytes per line
- The format will be:
```
@0x00000000 0100 0302 0504 0706 ...... 1D1C 1F1E
@0x00000020 2120 2322 2524 2726 ...... 3D3C 3F3E
......
```

8. Verilog HEX, Data Width 4-Byte with Address(--format vhex_addr_dw4 or --format verilog_addr_dw4):
- Convert to the file which can be loaded by $readmemh to a specific offset of a common memory with 4-byte(32-bit) width
- The option "address" is accepted as optional. Default is 0x0
- The option "alignment" is accepted as optional. Default is 32 which means 32 bytes per line
- The format will be:
```
@0x00000000 03020100 07060504 0B0A0908 0F0E0D0C ...... 1B1A1918 1F1E1D1C
@0x00000020 23222120 27262524 2B2A2928 2F2E2D2C ...... 3B3A3938 3F3E3D3C
......
```

9. Verilog HEX, Data Width 8-Byte with Address(--format vhex_addr_dw8 or --format verilog_addr_dw8):
- Convert to the file which can be loaded by $readmemh to a specific offset of a common memory with 8-byte(64-bit) width
- The option "address" is accepted as optional. Default is 0x0
- The option "alignment" is accepted as optional. Default is 32 which means 32 bytes per line
- The format will be:
```
@0x00000000 0706050403020100 0F0E0D0C0B0A0908 1716151413121110 1F1E1D1C1B1A1918
@0x00000020 2726252423222120 2F2E2D2C2B2A2928 3736353433323130 3F3E3D3C3B3A3938
......
```

9. Verilog HEX, Data Width 16-Byte with Address(--format vhex_addr_dw16 or --format verilog_addr_dw16):
- Convert to the file which can be loaded by $readmemh to a specific offset of a common memory with 16-byte(128-bit) width
- The option "address" is accepted as optional. Default is 0x0
- The option "alignment" is accepted as optional. Default is 32 which means 32 bytes per line
- The format will be:
```
@0x00000000 0F0E0D0C0B0A09080706050403020100 1F1E1D1C1B1A19181716151413121110
@0x00000020 2F2E2D2C2B2A29282726252423222120 3F3E3D3C3B3A39383736353433323130
......
```
10. Verilog BIN, Data Width 1-Byte(--format vbin_dw1):
- Convert to the file which can be loaded by $readmemb to a common memory with 1-byte(8-bit) width
- The option "ecc" is accepted as optional. Default is "none"
- The option "ecc-skip-all-ones" is accepted as optional. Default is False which means no skip
- The option "ecc-skip-all-zeros" is accepted as optional. Default is False which means no skip
- The option "address" is accepted as optional for ECC calculation. Default is 0x0
- The option "pad-count" is accepted as optional. Default is 0 which means no padding
- The option "pad-byte" is accepted as optional. Default is "0xFF"
- The format will be:
```
    00000000
    00000001
    ......
```

11. Verilog BIN, Data Width 2-Byte(--format vbin_dw2):
- Convert to the file which can be loaded by $readmemb to a common memory with 2-byte(16-bit) width
- The option "ecc" is accepted as optional. Default is "none"
- The option "ecc-skip-all-ones" is accepted as optional. Default is False which means no skip
- The option "ecc-skip-all-zeros" is accepted as optional. Default is False which means no skip
- The option "address" is accepted as optional for ECC calculation. Default is 0x0
- The option "pad-count" is accepted as optional. Default is 0 which means no padding
- The option "pad-byte" is accepted as optional. Default is "0xFF"
- The format will be:
```
    0000000100000000
    0000001100000010
    ......
```

12. Verilog BIN, Data Width 4-Byte(--format vbin_dw4):
- Convert to the file which can be loaded by $readmemb to a common memory with 4-byte(32-bit) width
- The option "ecc" is accepted as optional. Default is "none"
- The option "ecc-skip-all-ones" is accepted as optional. Default is False which means no skip
- The option "ecc-skip-all-zeros" is accepted as optional. Default is False which means no skip
- The option "address" is accepted as optional for ECC calculation. Default is 0x0
- The option "pad-count" is accepted as optional. Default is 0 which means no padding
- The option "pad-byte" is accepted as optional. Default is "0xFF"
- The format will be:
```
    00000011000000100000000100000000
    00000111000001100000010100000100
    ......
```

13. Verilog BIN, Data Width 8-Byte(--format vbin_dw8):
- Convert to the file which can be loaded by $readmemb to a common memory with 8-byte(64-bit) width
- The option "ecc" is accepted as optional. Default is "none"
- The option "ecc-skip-all-ones" is accepted as optional. Default is False which means no skip
- The option "ecc-skip-all-zeros" is accepted as optional. Default is False which means no skip
- The option "address" is accepted as optional for ECC calculation. Default is 0x0
- The option "pad-count" is accepted as optional. Default is 0 which means no padding
- The option "pad-byte" is accepted as optional. Default is "0xFF"
- The format will be:
```
    0000011100000110000001010000010000000011000000100000000100000000
    0000111100001110000011010000110000001011000010100000100100001000
    ......
```

14. Verilog BIN, Data Width 16-Byte(--format vbin_dw16):
- Convert to the file which can be loaded by $readmemb to a common memory with 16-byte(128-bit) width
- The option "ecc" is accepted as optional. Default is "none"
- The option "ecc-skip-all-ones" is accepted as optional. Default is False which means no skip
- The option "ecc-skip-all-zeros" is accepted as optional. Default is False which means no skip
- The option "address" is accepted as optional for ECC calculation. Default is 0x0
- The option "pad-count" is accepted as optional. Default is 0 which means no padding
- The option "pad-byte" is accepted as optional. Default is "0xFF"
- The format will be:
```
    00001111000011100000110100001100000010110000101000001001000010000000011100000110000001010000010000000011000000100000000100000000
    00011111000111100001110100011100000110110001101000011001000110000001011100010110000101010001010000010011000100100001000100010000
    ......
```

## Supported ECC Algorithm
1. None:
- No ECC is added

2. ARM SECDED(--ecc arm_secded):
- Single Error Correction Double Error Detection (SECDED) code
- The ECC bits are appended to the MSB side of the data
- Only verilog_dwx (x = 4, 8, 16) formats support this ECC

3. User specific algorithm(--ecc <custom_ecc_func.py>)
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