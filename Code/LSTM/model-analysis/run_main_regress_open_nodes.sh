# How to run this script:
#    ./run_main.sh  <GROUP>
#

set GROUP = $1
mkdir -p /tmp/Logs
mkdir -p /RunScripts

set st = `expr $GROUP \* 5- 5 + 1`
set ed = `expr $GROUP \* 5`

#set SEED = 1
foreach SEED ( `seq ${st} ${ed}` )
	 set path2code='/neurospin/unicog/protocols/intracranial/FAIRNS/sentence-processing-MEG-LSTM/Code/LSTM/model-analysis/regress_open_nodes.py'
	 set filename_bash=RunScripts/run_$CH.sh
	 set output_log='Logs/log_o_channel_'$CH
	 set error_log='Logs/log_e_channel_'$CH
	 set queue='Unicog_long'
	 set job_name='SEED_'$CH
	 set walltime='72:00:00'
	 
     rm -f $filename_bash
     touch $filename_bash

	 echo "python $path2code -s $SEED" >> $filename_bash
         
	 qsub -q $queue -N $job_name -l walltime=$walltime -o $output_log -e $error_log $filename_bash
         
end

