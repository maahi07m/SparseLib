#!/bin/bash
echo started!
source venv/bin/activate
start=`date +%s`
for size_index in 5000 7000 9000 11000 13000 15000 17000 19000 21000 23000
do
    echo ${size_index} start
    for (( count = 1; count<11; ++count)); do
        for density_index in 0.005 0.01 0.015 0.02
        do
            echo with ${density_index} start
            python generator.py ${size_index} ${density_index} ${count}
            python diagonal_csc.py ${size_index} ${density_index} ${count}
            python csr_coo.py ${size_index} ${density_index} ${count}
        done
    done
done
end=`date +%s`
runtime=$((end-start))
echo ${runtime} 'time' taken