# STM32H743ZIT6

LQFP-144 physical pin contract from DS12110 Rev 11 Figure 7 / Table 9.
Each VDD, VSS and VCAP package contact has a separate pin. This definition
contains no alternate-function solver contract: consumers must verify mux
assignments explicitly. PC2_C/PC3_C are analog-only contacts in this view.

Use local 100 nF at every VDD, adequate bulk, separate 2.2 uF low-ESR VCAP
capacitors, analog supply/reference decoupling and a defined VBAT supply.
PDR_ON must be high for the internal supply supervisor. Pull BOOT0 low and
provide reset/service SWD access. VDD33USB must be supplied even when USB is
unused per the selected supply scheme. Review DS12110 section 3.5 and VCAP
operating conditions, AN4938 and the matching ST evaluation schematic/layout
before physical freeze. Local PDF cache/hash remains unresolved; datasheet
was inspected through the web tool. No physical or assembly qualification.
