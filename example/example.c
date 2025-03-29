#include <stdio.h>
#include <stdint.h>

static const uint8_t array8[] =
{
#include "output_c_uint8.h"
};

static const uint16_t array16[] =
{
#include "output_c_uint16.h"
};

static const uint32_t array32[] =
{
#include "output_c_uint32.h"
};

static const uint64_t array64[] =
{
#include "output_c_uint64.h"
};
	
void main(void)
{
    for (int i = 0; i < sizeof(array8) / sizeof(array8[0]); i++)
    {
        printf("%#02x ", array8[i]);
    }
    printf("\n");
    for (int i = 0; i < sizeof(array16) / sizeof(array16[0]); i++)
    {
        printf("%#04x ", array16[i]);
    }
    printf("\n");
    for (int i = 0; i < sizeof(array32) / sizeof(array32[0]); i++)
    {
        printf("%#08x ", array32[i]);
    }
    printf("\n");
    for (int i = 0; i < sizeof(array64) / sizeof(array64[0]); i++)
    {
        printf("%#016lx ", array64[i]);
    }
    printf("\n");
}
