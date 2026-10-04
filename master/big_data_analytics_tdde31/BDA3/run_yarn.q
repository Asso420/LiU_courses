#!/bin/bash
#SBATCH --time=30:00
#SBATCH --nodes=2
#SBATCH --exclusive

echo "START AT: $(date)"

module load spark/3.5.1-hadoop-3.3.6-hpc1-bdist

# Cleanup and start from scratch
rm -rf spark

# Startup hadoop filesystem and yarn
hadoop_setup

echo "Prepare output and input directories and files..."
# The following command will make folders on your home folder on HDFS, the input and output folders should be corresponding to the parameter you give to textFile and saveAsTextFile functions in the code
hadoop fs -mkdir -p "/user/x_ahmso/BDA" "/user/x_ahmso/BDA/input"
hadoop fs -test -d "/user/x_ahmso/BDA/output"
if [ "$?" == "0" ]; then
    hadoop fs -rm -r "/user/x_ahmso/BDA/output"
fi

#hadoop fs -copyFromLocal ./input_data/temperature-readings-small.csv "/user/x_ahmso/BDA/input/"
# Remove the comment when you need specifc file below
hadoop fs -copyFromLocal ./input_data/temperature-readings.csv "/user/x_ahmso/BDA/input/"
#hadoop fs -copyFromLocal ./input_data/precipitation-readings.csv "/user/x_ahmso/BDA/input/"
hadoop fs -copyFromLocal ./input_data/stations.csv "/user/x_ahmso/BDA/input/"
#hadoop fs -copyFromLocal ./input_data/stations-Ostergotland.csv "/user/x_ahmso/BDA/input/"

# Run your program
echo "Running Your program..."

# spark-submit comes here and you need to replace "BDA1_demo.py" when you have/run your own code
spark-submit --deploy-mode cluster --master yarn --num-executors 9 --driver-memory 2g --executor-memory 2g --executor-cores 4 BDA3_demo.py

echo "================= FINAL OUTPUT =========================================="
hadoop fs -cat "/user/x_ahmso/BDA/output"/*

rm -rf output
hadoop fs -copyToLocal '/user/x_ahmso/BDA/output' ./
hadoop_stop

echo "END AT: $(date)"