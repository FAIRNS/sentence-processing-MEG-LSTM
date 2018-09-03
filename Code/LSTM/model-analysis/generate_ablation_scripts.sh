basefolder=$1

for k in {10..21}
do
  python3 run-ablation.py -n 1000 -k 10 -base_folder $basefolder > abl_scripts/abl_exp_k$k.sh
done
