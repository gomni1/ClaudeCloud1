#!/bin/bash
# wait for K1, then K2 on up to 2 K1 cycles (cap 1100 CPU-s each)
cd "$(dirname "$0")"
while kill -0 $(cat /tmp/k1.pid) 2>/dev/null; do sleep 30; done
python3 k2_k1cycles.py > evidence/k2_k1cycles_stdout.txt 2>&1
for j in 0 1; do
  [ -f evidence/k2_start_$j.json ] && taskset -c 2,3 python3 k2.py lamK1 1100 evidence/k2_start_$j.json lamK1_$j > evidence/k2_lamK1_${j}_stdout.txt 2>&1 &
done
wait
echo done > evidence/k2_k1cycles_done.txt
