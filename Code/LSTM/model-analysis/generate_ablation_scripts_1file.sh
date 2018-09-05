basefolder=$1

>abl_scripts/all_abl_exp.sh

for k in {10..21}
do
  python3 run-ablation.py -n 1000 -k $k -base_folder $basefolder >> abl_scripts/all_abl_exp.sh
done
