ratio="0.9"

echo simple
python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/compute_accuracy.py simple_data.pkl correct_wrong_simple.txt 1 2 2
performances="$(python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/compute_accuracy.py simple_data.pkl correct_wrong_simple.txt 1 2 2 | awk '{print $2}')"
p1="$(echo $performances | awk '{print $1}')"
p2="$(echo $performances | awk '{print $2}')"
echo "	simple singular"
python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/process_ablation_accuracies.py singular simple_ablation | sort -nk4 | perl -ne 's/singular//; s/_.*abl//; print'| python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/print_ablation_accuracies.py --base_perf $p1 --ratio $ratio 
echo "	simple plural"
python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/process_ablation_accuracies.py plural simple_ablation | sort -nk4 | perl -ne 's/plural//; s/_.*abl//; print' | python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/print_ablation_accuracies.py --base_perf $p2 --ratio $ratio
echo

echo adv
performances="$(python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/compute_accuracy.py adv_data.pkl correct_wrong_adv.txt 1 2 3 | awk '{print $2}')"
p1="$(echo $performances | awk '{print $1}')"
p2="$(echo $performances | awk '{print $2}')"
python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/compute_accuracy.py adv_data.pkl correct_wrong_adv.txt 1 2 3
echo "	adv singular"
python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/process_ablation_accuracies.py singular adv_ablation | sort -nk4 | perl -ne 's/singular//; s/_.*abl//; print' | python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/print_ablation_accuracies.py --base_perf $p1 --ratio $ratio
echo "	adv plural"
python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/process_ablation_accuracies.py plural adv_ablation | sort -nk4 | perl -ne 's/plural//; s/_.*abl//; print' | python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/print_ablation_accuracies.py --base_perf $p2 --ratio $ratio
echo

echo adv_adv
python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/compute_accuracy.py adv_adv_data.pkl correct_wrong_adv_adv.txt 1 2 4
performances="$(python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/compute_accuracy.py adv_adv_data.pkl correct_wrong_adv_adv.txt 1 2 4 | awk '{print $2}')"
p1="$(echo $performances | awk '{print $1}')"
p2="$(echo $performances | awk '{print $2}')"
echo "	adv_adv singular"
python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/process_ablation_accuracies.py singular adv_adv_ablation | sort -nk4 | perl -ne 's/singular//; s/_.*abl//; print' | python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/print_ablation_accuracies.py --base_perf $p1 --ratio $ratio
echo "	adv_adv plural"
python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/process_ablation_accuracies.py plural adv_adv_ablation | sort -nk4 | perl -ne 's/plural//; s/_.*abl//; print' | python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/print_ablation_accuracies.py --base_perf $p2 --ratio $ratio
echo

echo namepp
python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/compute_accuracy.py namepp_data.pkl correct_wrong_namepp.txt 1 2 4
performances="$(python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/compute_accuracy.py namepp_data.pkl correct_wrong_namepp.txt 1 2 4 | awk '{print $2}')"
p1="$(echo $performances | awk '{print $1}')"
p2="$(echo $performances | awk '{print $2}')"
echo "	namepp singular"
python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/process_ablation_accuracies.py singular namepp_ablation | sort -nk4 | perl -ne 's/singular//; s/_.*abl//; print' | python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/print_ablation_accuracies.py --base_perf $p1 --ratio $ratio 
echo "	namepp plural"
python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/process_ablation_accuracies.py plural namepp_ablation | sort -nk4 | perl -ne 's/plural//; s/_.*abl//; print' | python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/print_ablation_accuracies.py --base_perf $p2 --ratio $ratio
echo

echo adv_conjunction
python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/compute_accuracy.py adv_conjunction_data.pkl correct_wrong_adv_conjunction.txt 1 2 5
performances="$(python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/compute_accuracy.py adv_conjunction_data.pkl correct_wrong_adv_conjunction.txt 1 2 5 | awk '{print $2}')"
p1="$(echo $performances | awk '{print $1}')"
p2="$(echo $performances | awk '{print $2}')"
echo "	adv_conjunction singular"
python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/process_ablation_accuracies.py singular adv_conjunction_ablation | sort -nk4 | perl -ne 's/singular//; s/_.*abl//; print' | python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/print_ablation_accuracies.py --base_perf $p1 --ratio $ratio
echo "	adv_conjunction plural"
python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/process_ablation_accuracies.py plural adv_conjunction_ablation | sort -nk4 | perl -ne 's/plural//; s/_.*abl//; print' | python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/print_ablation_accuracies.py --base_perf $p2 --ratio $ratio
echo

echo nounpp
python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/compute_accuracy.py nounpp_data.pkl correct_wrong_nounpp.txt 1 2 5
performances="$(python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/compute_accuracy.py nounpp_data.pkl correct_wrong_nounpp.txt 1 2 5 | awk '{print $2}')"
p1="$(echo $performances | awk '{print $1}')"
p2="$(echo $performances | awk '{print $2}')"
p3="$(echo $performances | awk '{print $3}')"
p4="$(echo $performances | awk '{print $4}')"
echo "	nounpp singular singular"
python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/process_ablation_accuracies.py singular_singular nounpp_ablation | sort -nk4 | perl -ne 's/singular_singular//; s/_.*abl//; print' | python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/print_ablation_accuracies.py --base_perf $p1 --ratio $ratio 
echo "	nounpp singular plural"
python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/process_ablation_accuracies.py singular_plural nounpp_ablation | sort -nk4 | perl -ne 's/singular_plural//; s/_.*abl//; print' | python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/print_ablation_accuracies.py --base_perf $p2 --ratio $ratio
echo "	nounpp plural singular"
python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/process_ablation_accuracies.py plural_singular nounpp_ablation | sort -nk4 | perl -ne 's/plural_singular//; s/_.*abl//; print' | python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/print_ablation_accuracies.py --base_perf $p3 --ratio $ratio 
echo "	nounpp plural plural"
python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/process_ablation_accuracies.py plural_plural nounpp_ablation | sort -nk4 | perl -ne 's/plural_plural//; s/_.*abl//; print' | python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/print_ablation_accuracies.py --base_perf $p4 --ratio $ratio
echo

echo objrel_that
python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/compute_accuracy.py objrel_that_data.pkl correct_wrong_objrel_that.txt 1 2 6
performances="$(python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/compute_accuracy.py objrel_that_data.pkl correct_wrong_objrel_that.txt 1 2 6 | awk '{print $2}')"
p1="$(echo $performances | awk '{print $1}')"
p2="$(echo $performances | awk '{print $2}')"
p3="$(echo $performances | awk '{print $3}')"
p4="$(echo $performances | awk '{print $4}')"
echo "  objrel_that singular singular"
python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/process_ablation_accuracies.py singular_singular objrel_that_ablation | sort -nk4 | perl -ne 's/singular_singular//; s/_.*abl//; print' | python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/print_ablation_accuracies.py --base_perf $p1 --ratio $ratio
echo "  objrel_that singular plural"
python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/process_ablation_accuracies.py singular_plural objrel_that_ablation | sort -nk4 | perl -ne 's/singular_plural//; s/_.*abl//; print' | python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/print_ablation_accuracies.py --base_perf $p2 --ratio $ratio
echo "  objrel_that plural singular"
python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/process_ablation_accuracies.py plural_singular objrel_that_ablation | sort -nk4 | perl -ne 's/plural_singular//; s/_.*abl//; print' | python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/print_ablation_accuracies.py --base_perf $p3 --ratio $ratio
echo "  objrel_that plural plural"
python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/process_ablation_accuracies.py plural_plural objrel_that_ablation | sort -nk4 | perl -ne 's/plural_plural//; s/_.*abl//; print' | python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/print_ablation_accuracies.py --base_perf $p4 --ratio $ratio
echo

echo subjrel_that
performances="$(python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/compute_accuracy.py subjrel_that_data.pkl correct_wrong_subjrel_that.txt 1 2 6 | awk '{print $2}')"
p1="$(echo $performances | awk '{print $1}')"
p2="$(echo $performances | awk '{print $2}')"
p3="$(echo $performances | awk '{print $3}')"
p4="$(echo $performances | awk '{print $4}')"
python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/compute_accuracy.py subjrel_that_data.pkl correct_wrong_subjrel_that.txt 1 2 6
echo "  subjrel_that singular singular"
python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/process_ablation_accuracies.py singular_singular subjrel_that_ablation | sort -nk4 | perl -ne 's/singular_singular//; s/_.*abl//; print' | python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/print_ablation_accuracies.py --base_perf $p1 --ratio $ratio
echo "  subjrel_that singular plural"
python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/process_ablation_accuracies.py singular_plural subjrel_that_ablation | sort -nk4 | perl -ne 's/singular_plural//; s/_.*abl//; print' | python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/print_ablation_accuracies.py --base_perf $p2 --ratio $ratio
echo "  subjrel_that plural singular"
python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/process_ablation_accuracies.py plural_singular subjrel_that_ablation | sort -nk4 | perl -ne 's/plural_singular//; s/_.*abl//; print' |python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/print_ablation_accuracies.py --base_perf $p3 --ratio $ratio
echo "  subjrel_that plural plural"
python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/process_ablation_accuracies.py plural_plural subjrel_that_ablation | sort -nk4 | perl -ne 's/plural_plural//; s/_.*abl//; print' | python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/print_ablation_accuracies.py --base_perf $p4 --ratio $ratio
echo

echo objrel
python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/compute_accuracy.py objrel_data.pkl correct_wrong_objrel.txt 1 2 5
performances="$(python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/compute_accuracy.py objrel_data.pkl correct_wrong_objrel.txt 1 2 5 | awk '{print $2}')"
p1="$(echo $performances | awk '{print $1}')"
p2="$(echo $performances | awk '{print $2}')"
p3="$(echo $performances | awk '{print $3}')"
p4="$(echo $performances | awk '{print $4}')"
echo "  objrel singular singular"
python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/process_ablation_accuracies.py singular_singular objrel_ablation | sort -nk4 | perl -ne 's/singular_singular//; s/_.*abl//; print' | python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/print_ablation_accuracies.py --base_perf $p1 --ratio $ratio
echo "  objrel singular plural"
python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/process_ablation_accuracies.py singular_plural objrel_ablation | sort -nk4 | perl -ne 's/singular_plural//; s/_.*abl//; print' | python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/print_ablation_accuracies.py --base_perf $p2 --ratio $ratio
echo "  objrel plural singular"
python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/process_ablation_accuracies.py plural_singular objrel_ablation | sort -nk4 | perl -ne 's/plural_singular//; s/_.*abl//; print' | python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/print_ablation_accuracies.py --base_perf $p3 --ratio $ratio
echo "  objrel plural plural"
python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/process_ablation_accuracies.py plural_plural objrel_ablation | sort -nk4 | perl -ne 's/plural_plural//; s/_.*abl//; print' | python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/print_ablation_accuracies.py --base_perf $p4 --ratio $ratio
echo

echo nounpp_adv
python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/compute_accuracy.py nounpp_adv_data.pkl correct_wrong_nounpp_adv.txt 1 2 6
performances="$(python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/compute_accuracy.py nounpp_adv_data.pkl correct_wrong_nounpp_adv.txt 1 2 6 | awk '{print $2}')"
p1="$(echo $performances | awk '{print $1}')"
p2="$(echo $performances | awk '{print $2}')"
p3="$(echo $performances | awk '{print $3}')"
p4="$(echo $performances | awk '{print $4}')"
echo "  nounpp_adv singular singular"
python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/process_ablation_accuracies.py singular_singular nounpp_adv_ablation | sort -nk4 | perl -ne 's/singular_singular//; s/_.*abl//; print' | python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/print_ablation_accuracies.py --base_perf $p1 --ratio $ratio
echo "  nounpp_adv singular plural"
python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/process_ablation_accuracies.py singular_plural nounpp_adv_ablation | sort -nk4 | perl -ne 's/singular_plural//; s/_.*abl//; print' | python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/print_ablation_accuracies.py --base_perf $p2 --ratio $ratio
echo "  nounpp_adv plural singular"
python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/process_ablation_accuracies.py plural_singular nounpp_adv_ablation | sort -nk4 | perl -ne 's/plural_singular//; s/_.*abl//; print' | python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/print_ablation_accuracies.py --base_perf $p3 --ratio $ratio
echo "  nounpp_adv plural plural"
python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/process_ablation_accuracies.py plural_plural nounpp_adv_ablation | sort -nk4 | perl -ne 's/plural_plural//; s/_.*abl//; print' | python ~/sentence-processing-MEG-LSTM/Code/Stimuli/Relative_clause_Marco/print_ablation_accuracies.py --base_perf $p4 --ratio $ratio

