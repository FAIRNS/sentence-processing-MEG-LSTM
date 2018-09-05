basefolder=$1

>$basefolder/abl_scripts/all_abl_exp.sh

for k in {10..21}
do
  python3 run-ablation.py -n 1000 -k 10 -base_folder $basefolder >> $basefolder/abl_scripts/all_abl_exp.sh
done
