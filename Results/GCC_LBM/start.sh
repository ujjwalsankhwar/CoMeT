mkdir 4core_lbm_gcc_3Dmem
cd 4core_lbm_gcc_3Dmem
ls -lrt .
../../../../run-sniper -v -s memTherm_core -c gainestown_3Dmem -n 4 --sim-end=last --pinballs "../../benchmarks/lbm/lbm.try_30208_t0r8_warmup101500_prolog0_region100000059_epilog0_008_0-69692.0.address","../../benchmarks/gcc/gcc.try_33001_t0r15_warmup101500_prolog0_region100000013_epilog0_015_0-48648.0.address","../../benchmarks/lbm/lbm.try_30208_t0r8_warmup101500_prolog0_region100000059_epilog0_008_0-69692.0.address","../../benchmarks/gcc/gcc.try_33001_t0r15_warmup101500_prolog0_region100000013_epilog0_015_0-48648.0.address" > log
cd ..