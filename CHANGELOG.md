# ChangeLog

## V2.2.0 - 2025-09-18
=======================
### Feature
- Add support to generate split files
  - Some memory might be constructed by multiple of banks
  - This feature is useful to generate files in this scenario
### Bug fix
- Fix issue when calling safe_open


## V2.1.0 - 2025-09-15
=======================
### Bug fix
- Fix limitation of User specific ECC algorithm location


## V2.0.0 - 2025-09-15
=======================

### Feature
- Add support for ECC
  - Supported ECC algorithms and relative formats:
    - ARM SECDED ECC for 32bit, 64bit 128bit
      - verilog_dwx(x = 4, 8, 16)
    - User specific ECC algorithm
      - verilog_dwx (x = 1, 2, 4, 8, 16)
- Add padding options for FLASH memory HEX
  - Some FLASH memory may have extra bytes for ECC.
  - Base on the implementation, not all ECC bytes might be used.
  - Padding them to specified byte
  - Supported formats:
    - verilog_dwx (x = 1, 2, 4, 8, 16)

### Bug fix
- Fix error when no option is specified
  - Help text shall be printed


## V1.0.0 - 2025-03-30
=======================

### Feature
- Initial release
- Add support for the following HEX formats:
  - C (uint8, uint16, uint32 and uint64)
  - Verilog HDL (8-bit, 16-bit, 32-bit, 64-bit and 128-bit data width with/without address)
  - Cadence Denali model