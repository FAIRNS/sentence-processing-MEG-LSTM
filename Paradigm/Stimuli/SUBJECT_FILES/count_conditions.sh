# A sanity check for trial counts in all subject files:

for S in 1 2 3 4 5 6 7 8 9 10;
do
    python count_conditions.py --subject $S > count_conditions_subj_$S.log &
done