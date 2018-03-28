# How to run this script: 
# 
#    cd 
#    ./run_jobs.sh  <GROUP>
# 

set GROUP = $1
#set SRC_DIR = "/neurospin/unicog/protocols/intracranial/Code"
#mkdir -p /tmp/Logs
#mkdir -p /RunScripts

set st = `expr $GROUP \* 32 - 32 + 1`
set ed = `expr $GROUP \* 32`

set SEED = 1
foreach CH ( `seq ${st} ${ed}` )
	 set eos='"<eos>"'
	 set path2code='/neurospin/unicog/protocols/intracranial/FAIRNS/sentence-processing-MEG-LSTM/Code/LSTM/model-analysis/ablation-experiment.py'
	 set path2model='/neurospin/unicog/protocols/intracranial/FAIRNS/sentence-processing-MEG-LSTM/Data/LSTM/hidden650_batch128_dropout0.2_lr20.0.cpu.pt'
	 set path2agreement_data='/neurospin/unicog/protocols/intracranial/FAIRNS/sentence-processing-MEG-LSTM/Data/LSTM/best_model.tab'
	 set path2vocab='/neurospin/unicog/protocols/intracranial/FAIRNS/sentence-processing-MEG-LSTM/Data/LSTM/english_vocab.txt'
	 set path2output='/neurospin/unicog/protocols/intracranial/FAIRNS/sentence-processing-MEG-LSTM/Output/ablation_results_killing_unit'
         set filename_bash=RunScripts/run_$CH.sh
	 set output_log='Logs/log_o_channel_'$CH
	 set error_log='Logs/log_e_channel_'$CH
	 set queue='Unicog_long'
	 set job_name='Channel_'$CH
	 set walltime='72:00:00'
	 
         rm -f $filename_bash
         touch $filename_bash
	 echo "python $path2code $path2model --input $path2agreement_data --vocabulary $path2vocab --output $path2output --eos-separator $eos --format pkl -u $CH -g 1 -s SEED" >> $filename_bash
         
	 qsub -q $queue -N $job_name -l walltime=$walltime -o $output_log -e $error_log $filename_bash
         
end

