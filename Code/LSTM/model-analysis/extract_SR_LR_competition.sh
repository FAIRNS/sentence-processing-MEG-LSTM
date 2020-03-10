# bash to run the corresponding py file

#for INPUT in nounpp English_objrel_nounpp_V1 English_objrel_nounpp_V2
for INPUT in English_objrel_nounpp_V2
do
    echo python plot_SR_LR_competition.py --input $INPUT --cuda
    #python extract_SR_LR_competition.py --input $INPUT --cuda #> plot_SR_LR_$INPUT.log 2>&1 &
done

