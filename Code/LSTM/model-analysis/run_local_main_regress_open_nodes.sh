# How to run this script:
#    ./run_main.sh  <GROUP>
#

set GROUP = $1
#mkdir -p /tmp/Logs
#mkdir -p /RunScripts

set st = `expr $GROUP \* 5- 5 + 1`
set ed = `expr $GROUP \* 5`

#set SEED = 1
foreach SEED ( `seq ${st} ${ed}` )
	 set path2code='/neurospin/unicog/protocols/intracranial/FAIRNS/sentence-processing-MEG-LSTM/Code/LSTM/model-analysis/regress_open_nodes.py'
	 #set path2code='~/Projects/FAIRNS/sentence-processing-MEG-LSTM/Code/LSTM/model-analysis/regress_open_nodes.py'
	 set filename_bash=RunScripts/run_$SEED.sh
	 set output_log='/neurospin/unicog/protocols/intracranial/FAIRNS/sentence-processing-MEG-LSTM/Code/LSTM/model-analysis/Logs/log_o_channel_'$SEED
	 set error_log='Logs/log_e_channel_'$SEED
	 set queue='Unicog_long'
	 set job_name='SEED_'$SEED
	 set walltime='72:00:00'
	 
	 rm -f $filename_bash
	 touch $filename_bash

#	 echo "python3 $path2code -s $SEED >> $output_log &" >> $filename_bash
	 echo "python3 $path2code -s $SEED" >> $filename_bash
         
	 #python3 #path2code -s $SEED &!

	 chmod u+x $filename_bash

	 echo "python3 $path2code -s $SEED &" >> $filename_bash

	 ./$filename_bash &
         
end

