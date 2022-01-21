#*******************************************************************************
#* (c) 2011-2021, Cypress Semiconductor Corporation (an Infineon company)
#* or an affiliate of Cypress Semiconductor Corporation. All rights
#* reserved.
#* 
#* This software, including source code, documentation and related
#* materials ("Software") is owned by Cypress Semiconductor
#* Corporation or one of its affiliates ("Cypress") and is protected by
#* and subject to worldwide patent protection (United States and foreign),
#* United States copyright laws and international treaty provisions.
#* Therefore, you may use this Software only as provided in the license
#* agreement accompanying the software package from which you
#* obtained this Software ("EULA").
#* 
#* If no EULA applies, Cypress hereby grants you a personal, non-
#* exclusive, non-transferable license to copy, modify, and compile the
#* Software source code solely for use in connection with Cypress's
#* integrated circuit products. Any reproduction, modification, translation,
#* compilation, or representation of this Software except as specified
#* above is prohibited without the express written permission of Cypress.
#* 
#* Disclaimer: THIS SOFTWARE IS PROVIDED AS-IS, WITH NO
#* WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING,
#* BUT NOT LIMITED TO, NONINFRINGEMENT, IMPLIED
#* WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#* PARTICULAR PURPOSE. Cypress reserves the right to make
#* changes to the Software without notice. Cypress does not assume any
#* liability arising out of the application or use of the Software or any
#* product or circuit described in the Software. Cypress does not
#* authorize its products for use in any products where a malfunction or
#* failure of the Cypress product may reasonably be expected to result in
#* significant property damage, injury or death ("High Risk Product"). By
#* including Cypress's product in a High Risk Product, the manufacturer
#* of such system or application assumes all risk of such use and in doing
#* so agrees to indemnify Cypress against all liability.
#********************************************************************************
class enumeCanPowerDevice:
	CAN_MEASURE_POWER             =0x4        # from enum enumCanPowerDevice
	CAN_POWER_DEVICE              =0x1        # from enum enumCanPowerDevice
	CAN_READ_POWER                =0x2        # from enum enumCanPowerDevice
	CAN_MEASURE_POWER_2           =0x8        # from enum enumCanPowerDevice

class enumCanProgram:
	CAN_PROGRAM_CARBON            =0x1        # from enum enumCanProgram
	CAN_PROGRAM_ENCORE            =0x2        # from enum enumCanProgram
	
class enumInterfaces:
	I2C                           =0x4        # from enum enumInterfaces
	ISSP                          =0x2        # from enum enumInterfaces
	JTAG                          =0x1        # from enum enumInterfaces
	SWD                           =0x8        # from enum enumInterfaces
	SPI                           =0x16       # from enum enumInterfaces

class enumFrequencies:
	FREQ_01_5                     =0xc0       # from enum enumFrequencies
	FREQ_01_6                     =0x98       # from enum enumFrequencies
	FREQ_03_0                     =0xe0       # from enum enumFrequencies
	FREQ_03_2                     =0x18       # from enum enumFrequencies
	FREQ_06_0                     =0x60       # from enum enumFrequencies
	FREQ_08_0                     =0x90       # from enum enumFrequencies
	FREQ_12_0                     =0x84       # from enum enumFrequencies
	FREQ_16_0                     =0x10       # from enum enumFrequencies
	FREQ_24_0                     =0x4        # from enum enumFrequencies
	FREQ_48_0                     =0x0        # from enum enumFrequencies
	FREQ_RESET                    =0xfc       # from enum enumFrequencies

class enumI2Cspeed:
	CLK_100K                      =0x1        # from enum enumI2Cspeed
	CLK_400K                      =0x2        # from enum enumI2Cspeed
	CLK_50K                       =0x4        # from enum enumI2Cspeed

class enumSonosArrays:
	ARRAY_ALL                     =0x1f       # from enum __MIDL___MIDL_itf_PSoCProgrammerCOM_0000_0001
	ARRAY_EEPROM                  =0x2        # from enum __MIDL___MIDL_itf_PSoCProgrammerCOM_0000_0001
	ARRAY_FLASH                   =0x1        # from enum __MIDL___MIDL_itf_PSoCProgrammerCOM_0000_0001
	ARRAY_NVL_FACTORY             =0x8        # from enum __MIDL___MIDL_itf_PSoCProgrammerCOM_0000_0001
	ARRAY_NVL_USER                =0x4        # from enum __MIDL___MIDL_itf_PSoCProgrammerCOM_0000_0001
	ARRAY_NVL_WO_LATCHES          =0x10       # from enum __MIDL___MIDL_itf_PSoCProgrammerCOM_0000_0001

class enumUpgradeFirmware:
	FINALIZE                      =0x3        # from enum enumUpgradeFirmware
	INITIALIZE                    =0x0        # from enum enumUpgradeFirmware
	UPGRADE_BLOCK                 =0x1        # from enum enumUpgradeFirmware
	VERIFY_BLOCK                  =0x2        # from enum enumUpgradeFirmware

class enumValidAcquireModes:
	CAN_POWER_CYCLE_ACQUIRE       =0x2        # from enum enumValidAcquireModes
	CAN_POWER_DETECT_ACQUIRE      =0x4        # from enum enumValidAcquireModes
	CAN_RESET_ACQUIRE             =0x1        # from enum enumValidAcquireModes
	
class enumVoltages:
	VOLT_18V                      =0x8        # from enum enumVoltages
	VOLT_25V                      =0x4        # from enum enumVoltages
	VOLT_33V                      =0x2        # from enum enumVoltages
	VOLT_50V                      =0x1        # from enum enumVoltages