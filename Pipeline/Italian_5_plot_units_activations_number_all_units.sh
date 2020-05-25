######!/bin/bash -x

queue="Nspin_long"
walltime="2:00:00"

for UNIT in {0..1300}; do 
    #eval 'python3 ../Code/LSTM/model-analysis/plot_units_activations.py -sentences ../Data/Stimuli/Italian_double_subjrel_V1.text -meta ../Data/Stimuli/Italian_double_subjrel_V1.info -activations ../Data/LSTM/activations/Italian/Italian_double_subjrel_V1.pkl -o ../Figures/Italian_double_subjrel_V1_'$UNIT'.png -c double_subjrel_V1 -g 1 g "\-" 6 '$UNIT' cell -y "\$C\_t\$" --no-legend --figheight 4 --figwidth 16'
     CMD='python3 /neurospin/unicog/protocols/Yair/FAIRNS/sentence-processing-MEG-LSTM/Code/LSTM/model-analysis/plot_units_activations.py -sentences /neurospin/unicog/protocols/Yair/FAIRNS/sentence-processing-MEG-LSTM/Data/Stimuli/Italian_double_subjrel_V1.text -meta /neurospin/unicog/protocols/Yair/FAIRNS/sentence-processing-MEG-LSTM/Data/Stimuli/Italian_double_subjrel_V1.info -activations /neurospin/unicog/protocols/Yair/FAIRNS/sentence-processing-MEG-LSTM/Data/LSTM/activations/Italian/Italian_double_subjrel_V1.pkl -o /neurospin/unicog/protocols/Yair/FAIRNS/sentence-processing-MEG-LSTM/Figures/Italian_double_subjrel_V1_'$UNIT'.png -c double_subjrel_V1 -g 1 g "\-" 6 '$UNIT' cell -y "\$C\_t\$" --no-legend --figheight 4 --figwidth 16'

     job_name='unit'$UNIT
     echo $CMD | qsub -q $queue -N $job_name -l walltime=$walltime -o 'out.log' -e 'err.log'

done
