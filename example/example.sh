#!/bin/sh
bin2hex -v
bin2hex -h
bin2hex -i random_1024.bin -o output_c_uint8.h -f c_uint8 -A 16
bin2hex -i random_1024.bin -o output_c_uint16.h -f c_uint16 -A 16
bin2hex -i random_1024.bin -o output_c_uint32.h -f c_uint32 -A 16
bin2hex -i random_1024.bin -o output_c_uint64.h -f c_uint64 -A 16
bin2hex -i random_1024.bin -o output_model_denali.hex -f denali
bin2hex -i random_1024.bin -o output_verilog_dw1.hex -f verilog_dw1
bin2hex -i random_1024.bin -o output_verilog_dw2.hex -f verilog_dw2
bin2hex -i random_1024.bin -o output_verilog_dw4.hex -f verilog_dw4
bin2hex -i random_1024.bin -o output_verilog_dw8.hex -f verilog_dw8
bin2hex -i random_1024.bin -o output_verilog_dw16.hex -f verilog_dw16
bin2hex -i random_1024.bin -o output_verilog_addr_dw1.hex -f verilog_addr_dw1 -a 0 -A 32
bin2hex -i random_1024.bin -o output_verilog_addr_dw2.hex -f verilog_addr_dw2 -a 0 -A 32
bin2hex -i random_1024.bin -o output_verilog_addr_dw4.hex -f verilog_addr_dw4 -a 0 -A 32
bin2hex -i random_1024.bin -o output_verilog_addr_dw8.hex -f verilog_addr_dw8 -a 0 -A 32
bin2hex -i random_1024.bin -o output_verilog_addr_dw16.hex -f verilog_addr_dw16 -a 0 -A 32
