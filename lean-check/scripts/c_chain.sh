#!/bin/bash
# Wait for the first MassAction build, then run the pipeline over all targets in priority order.
P=$(cat /home/user/leanwork/logs/build_MassAction.pid)
while kill -0 $P 2>/dev/null; do sleep 30; done
cd /home/user/leanwork/tools
python3 c_pipeline.py MassAction SwitchChain SharpThreshold SecondKahnKalai DirectionalBallisticity ThreeStateSupercritical ThreeStateTreeClauses >> /home/user/leanwork/logs/pipeline_stdout.txt 2>&1
echo "chain done $(date)" >> /home/user/leanwork/logs/pipeline_stdout.txt
