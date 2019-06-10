# $1 : path to model
# $2 : path to vocab
model_path="/private/home/tdesbordes/sentence-processing-MEG-LSTM/Code/models/best_model.pt"
vocab_path="/private/home/tdesbordes/sentence-processing-MEG-LSTM/Code/data/vocab.txt"	

mkdir ./results

## Simple
if true
then	

	perl ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/generate_relatives.pl 0 300 simple | perl ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/post_process_stimuli_ending_with_verb_to_create_correct_wrong.pl > correct_wrong_simple.txt

	perl -F'\t' -ane 'print $F[0],"\n"' correct_wrong_simple.txt > simple_prefixes.txt

	python ~/sentence-processing-MEG-LSTM/Code/LSTM/model-analysis/extract-activations.py $model_path -i simple_prefixes.txt -v $vocab_path -o ./simple_data --eos-separator "<eos>" --format pkl --cuda -g lstm --use-unk --unk-token "<unk>"

	python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/compute_accuracy.py simple_data.pkl correct_wrong_simple.txt 1 2 2

	python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/get_ALL_sentences_and_data.py simple_data.pkl correct_wrong_simple.txt 1 2 2 > temp_good_simple.txt

	perl ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/convert_sentences_to_tal_format.pl simple temp_good_simple.txt 

	mkdir simple_ablation

	bash ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/generate_ablation_commands.sh ./simple ./simple_ablation $model_path $vocab_path > temp_simple_ablation_commands.txt

	bash ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/run_ablation.sh temp_simple_ablation_commands.txt 


	python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/process_ablation_accuracies.py singular simple_ablation | sort -nk4 | perl -ne 's/singular//; s/_.*abl//; print' | awk '$4<1{print $1 "\t" $4}' > results/simple_singular_results.txt 

	python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/process_ablation_accuracies.py plural simple_ablation | sort -nk4 | perl -ne 's/plural//; s/_.*abl//; print' | awk '$4<1{print $1 "\t" $4}' > results/simple_plural_results.txt 

fi

## Adverbs
if true
then

	perl ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/generate_relatives.pl 0 900 simple_adv | perl ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/post_process_stimuli_ending_with_verb_to_create_correct_wrong.pl > correct_wrong_adv.txt

	perl -F'\t' -ane 'print $F[0],"\n"' correct_wrong_adv.txt > adv_prefixes.txt

	python ~/sentence-processing-MEG-LSTM/Code/LSTM/model-analysis/extract-activations.py $model_path -i adv_prefixes.txt -v $vocab_path -o ./adv_data --eos-separator "<eos>" --format pkl --cuda -g lstm --use-unk --unk-token "<unk>"

	python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/compute_accuracy.py adv_data.pkl correct_wrong_adv.txt 1 2 3

	python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/get_ALL_sentences_and_data.py adv_data.pkl correct_wrong_adv.txt 1 2 3 > temp_good_adv.txt

	perl ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/convert_sentences_to_tal_format.pl adv temp_good_adv.txt

	mkdir adv_ablation

	bash ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/generate_ablation_commands.sh ./adv ./adv_ablation $model_path $vocab_path > temp_adv_ablation_commands.txt

	bash ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/run_ablation.sh temp_adv_ablation_commands.txt  

	python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/process_ablation_accuracies.py singular adv_ablation | sort -nk4 | perl -ne 's/singular//; s/_.*abl//; print' | awk '$4<1{print $1 "\t" $4}' > results/adv_singular_results.txt

	python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/process_ablation_accuracies.py plural adv_ablation | sort -nk4 | perl -ne 's/plural//; s/_.*abl//; print' | awk '$4<1{print $1 "\t" $4}' > results/adv_plural_results.txt

fi

## Adv Adv
if true
then

	perl ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/generate_relatives.pl 0 900 adv_adv | perl ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/post_process_stimuli_ending_with_verb_to_create_correct_wrong.pl > correct_wrong_adv_adv.txt

	perl -F'\t' -ane 'print $F[0],"\n"' correct_wrong_adv_adv.txt > adv_adv_prefixes.txt

	python ~/sentence-processing-MEG-LSTM/Code/LSTM/model-analysis/extract-activations.py $model_path -i adv_adv_prefixes.txt -v $vocab_path -o ./adv_adv_data --eos-separator "<eos>" --format pkl --cuda -g lstm --use-unk --unk-token "<unk>"

	python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/compute_accuracy.py adv_adv_data.pkl correct_wrong_adv_adv.txt 1 2 4

	python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/get_ALL_sentences_and_data.py adv_adv_data.pkl correct_wrong_adv_adv.txt 1 2 4 > temp_good_adv_adv.txt

	perl ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/convert_sentences_to_tal_format.pl adv_adv temp_good_adv_adv.txt 

	mkdir adv_adv_ablation

	bash ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/generate_ablation_commands.sh ./adv_adv ./adv_adv_ablation $model_path $vocab_path > temp_adv_adv_ablation_commands.txt

	bash ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/run_ablation.sh temp_adv_adv_ablation_commands.txt 

	python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/process_ablation_accuracies.py singular adv_adv_ablation | sort -nk4 | perl -ne 's/singular//; s/_.*abl//; print' | awk '$4<1{print $1 "\t" $4}' > results/adv_adv_singular_results.txt

	python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/process_ablation_accuracies.py plural adv_adv_ablation | sort -nk4 | perl -ne 's/plural//; s/_.*abl//; print' | awk '$4<1{print $1 "\t" $4}' > results/adv_adv_plural_results.txt

fi

## NAMEPP
if true
then

	perl ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/generate_relatives.pl 0 900 simple_namepp | perl ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/post_process_stimuli_ending_with_verb_to_create_correct_wrong.pl > correct_wrong_namepp.txt

	perl -F'\t' -ane 'print $F[0],"\n"' correct_wrong_namepp.txt > namepp_prefixes.txt

	python ~/sentence-processing-MEG-LSTM/Code/LSTM/model-analysis/extract-activations.py $model_path -i namepp_prefixes.txt -v $vocab_path -o ./namepp_data --eos-separator "<eos>" --format pkl --cuda -g lstm --use-unk --unk-token "<unk>"

	python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/compute_accuracy.py namepp_data.pkl correct_wrong_namepp.txt 1 2 4

	python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/get_ALL_sentences_and_data.py namepp_data.pkl correct_wrong_namepp.txt 1 2 4 > temp_good_namepp.txt

	perl ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/convert_sentences_to_tal_format.pl namepp temp_good_namepp.txt 

	mkdir namepp_ablation

	bash ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/generate_ablation_commands.sh ./namepp ./namepp_ablation $model_path $vocab_path > temp_namepp_ablation_commands.txt

	bash ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/run_ablation.sh temp_namepp_ablation_commands.txt  

	python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/process_ablation_accuracies.py singular namepp_ablation | sort -nk4 | perl -ne 's/singular//; s/_.*abl//; print' | awk '$4<1{print $1 "\t" $4}' > results/namepp_singular_results.txt

	python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/process_ablation_accuracies.py plural namepp_ablation | sort -nk4 | perl -ne 's/plural//; s/_.*abl//; print' | awk '$4<1{print $1 "\t" $4}' > results/namepp_plural_results.txt

fi


## ADV_CONJUNCTION
if true
then

	perl ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/generate_relatives.pl 0 600 adv_conjunction | perl ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/post_process_stimuli_ending_with_verb_to_create_correct_wrong.pl > correct_wrong_adv_conjunction.txt

	perl -F'\t' -ane 'print $F[0],"\n"' correct_wrong_adv_conjunction.txt > adv_conjunction_prefixes.txt

	python ~/sentence-processing-MEG-LSTM/Code/LSTM/model-analysis/extract-activations.py $model_path -i adv_conjunction_prefixes.txt -v $vocab_path -o ./adv_conjunction_data --eos-separator "<eos>" --format pkl --cuda -g lstm --use-unk --unk-token "<unk>"

	python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/compute_accuracy.py adv_conjunction_data.pkl correct_wrong_adv_conjunction.txt 1 2 5


	python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/get_ALL_sentences_and_data.py adv_conjunction_data.pkl correct_wrong_adv_conjunction.txt 1 2 5 > temp_good_adv_conjunction.txt

	perl ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/convert_sentences_to_tal_format.pl adv_conjunction temp_good_adv_conjunction.txt 

	mkdir adv_conjunction_ablation

	bash ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/generate_ablation_commands.sh ./adv_conjunction ./adv_conjunction_ablation $model_path $vocab_path > temp_adv_conjunction_ablation_commands.txt

	bash ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/run_ablation.sh temp_adv_conjunction_ablation_commands.txt  

	python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/process_ablation_accuracies.py singular adj_conjunctionp_ablation | sort -nk4 | perl -ne 's/singular//; s/_.*abl//; print' | awk '$4<1{print $1 "\t" $4}' > results/adv_conjunction_singular_results.txt

	python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/process_ablation_accuracies.py plural adv_conjunction_ablation | sort -nk4 | perl -ne 's/plural//; s/_.*abl//; print' | awk '$4<1{print $1 "\t" $4}' > results/adv_conjunction_plural_results.txt

fi


## NOUNPP
if true
then

	#Generating sentences of the form "NP P NP V" ("the athlete beside the car avoids"). Note that in this case we have a distractor for both the singular and plural condition (athlete(s)/car(s)), so the analysis will be conducted in terms of the categories: singular_singular, singular_plural, plural_plural and plural_singular.
	#The extra command-line perl script in the following pipeline creates the composite number tags listed above:

	perl ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/generate_relatives.pl 0 600 nounpp| perl -F'\t' -ane 'print join "\t",(@F[0..1],"$F[2]_$F[3]",$F[4])' | perl ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/post_process_stimuli_ending_with_verb_to_create_correct_wrong.pl > correct_wrong_nounpp.txt

	perl -F'\t' -ane 'print $F[0],"\n"' correct_wrong_nounpp.txt > nounpp_prefixes.txt

	python ~/sentence-processing-MEG-LSTM/Code/LSTM/model-analysis/extract-activations.py $model_path -i nounpp_prefixes.txt -v $vocab_path -o ./nounpp_data --eos-separator "<eos>" --format pkl --cuda -g lstm --use-unk --unk-token "<unk>"

	python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/compute_accuracy.py nounpp_data.pkl correct_wrong_nounpp.txt 1 2 5

	python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/get_ALL_sentences_and_data.py nounpp_data.pkl correct_wrong_nounpp.txt 1 2 5 > temp_good_nounpp.txt

	#Note that, in the following step, we now generate separate file sets for all possible singular/plural combinations:

	perl ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/convert_sentences_to_tal_format.pl nounpp temp_good_nounpp.txt 

	mkdir nounpp_ablation

	bash ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/generate_ablation_commands.sh ./nounpp ./nounpp_ablation $model_path $vocab_path do_split > temp_nounpp_ablation_commands.txt

	bash ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/run_ablation.sh temp_nounpp_ablation_commands.txt 

	python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/process_ablation_accuracies.py singular_singular nounpp_ablation | sort -nk4 | perl -ne 's/singular_singular//; s/_.*abl//; print' | awk '$4<1{print $1 "\t" $4}' > results/nounpp_singular_singular_results.txt

	python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/process_ablation_accuracies.py singular_plural nounpp_ablation | sort -nk4 | perl -ne 's/singular_plural//; s/_.*abl//; print' | awk '$4<1{print $1 "\t" $4}' > results/nounpp_singular_plural_results.txt

	python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/process_ablation_accuracies.py plural_singular nounpp_ablation | sort -nk4 | perl -ne 's/plural_singular//; s/_.*abl//; print' | awk '$4<1{print $1 "\t" $4}' > results/nounpp_plural_singular_results.txt

	python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/process_ablation_accuracies.py plural_plural nounpp_ablation | sort -nk4 | perl -ne 's/plural_plural//; s/_.*abl//; print' | awk '$4<1{print $1 "\t" $4}' > results/nounpp_plural_plural_results.txt

fi


## objrel
if true
then

        perl ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/generate_relatives.pl 0 600 objrel | perl -F'\t' -ane 'print join "\t",(@F[0..1],"$F[2]_$F[3]",$F[4],$F[5])' | perl ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/post_process_stimuli_ending_with_verb_to_create_correct_wrong.pl > correct_wrong_objrel.txt

        perl -F'\t' -ane 'print $F[0],"\n"' correct_wrong_objrel.txt > objrel_prefixes.txt

        python ~/sentence-processing-MEG-LSTM/Code/LSTM/model-analysis/extract-activations.py $model_path -i objrel_prefixes.txt -v $vocab_path -o ./objrel_data --eos-separator "<eos>" --format pkl --cuda -g lstm --use-unk --unk-token "<unk>"

        python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/compute_accuracy.py objrel_data.pkl correct_wrong_objrel.txt 1 2 5

        python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/get_ALL_sentences_and_data.py objrel_data.pkl correct_wrong_objrel.txt 1 2 5 > temp_good_objrel.txt

        perl ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/convert_sentences_to_tal_format.pl objrel temp_good_objrel.txt

        mkdir objrel_ablation

        bash ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/generate_ablation_commands.sh ./objrel ./objrel_ablation $model_path $vocab_path do_split > temp_objrel_ablation_commands.txt

        bash ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/run_ablation.sh temp_objrel_ablation_commands.txt

        python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/process_ablation_accuracies.py singular_singular objrel_ablation | sort -nk4 | perl -ne 's/singular_singular//; s/_.*abl//; print' | awk '$4<1{print $1 "\t" $4}' > results/objrel_singular_singular_results.txt

        python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/process_ablation_accuracies.py singular_plural objrel_ablation | sort -nk4 | perl -ne 's/singular_plural//; s/_.*abl//; print' | awk '$4<1{print $1 "\t" $4}' > results/objrel_singular_plural_results.txt

        python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/process_ablation_accuracies.py plural_singular objrel_ablation | sort -nk4 | perl -ne 's/plural_singular//; s/_.*abl//; print' | awk '$4<1{print $1 "\t" $4}' > results/objrel_plural_singular_results.txt

        python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/process_ablation_accuracies.py plural_plural objrel_ablation | sort -nk4 | perl -ne 's/plural_plural//; s/_.*abl//; print' | awk '$4<1{print $1 "\t" $4}' > results/objrel_plural_plural_results.txt

fi


## objrel_that
if true
then

        perl ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/generate_relatives.pl 0 600 objrel_that | perl -F'\t' -ane 'print join "\t",(@F[0..1],"$F[2]_$F[3]",$F[4],$F[5])' | perl ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/post_process_stimuli_ending_with_verb_to_create_correct_wrong.pl > correct_wrong_objrel_that.txt

        perl -F'\t' -ane 'print $F[0],"\n"' correct_wrong_objrel_that.txt > objrel_that_prefixes.txt

        python ~/sentence-processing-MEG-LSTM/Code/LSTM/model-analysis/extract-activations.py $model_path -i objrel_that_prefixes.txt -v $vocab_path -o ./objrel_that_data --eos-separator "<eos>" --format pkl --cuda -g lstm --use-unk --unk-token "<unk>"

        python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/compute_accuracy.py objrel_that_data.pkl correct_wrong_objrel_that.txt 1 2 6

        python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/get_ALL_sentences_and_data.py objrel_that_data.pkl correct_wrong_objrel_that.txt 1 2 6 > temp_good_objrel_that.txt

        perl ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/convert_sentences_to_tal_format.pl objrel_that temp_good_objrel_that.txt

        mkdir objrel_that_ablation

        bash ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/generate_ablation_commands.sh ./objrel_that ./objrel_that_ablation $model_path $vocab_path do_split > temp_objrel_that_ablation_commands.txt

        bash ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/run_ablation.sh temp_objrel_that_ablation_commands.txt

        python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/process_ablation_accuracies.py singular_singular objrel_that_ablation | sort -nk4 | perl -ne 's/singular_singular//; s/_.*abl//; print' | awk '$4<1{print $1 "\t" $4}' > results/objrel_that_singular_singular_results.txt

        python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/process_ablation_accuracies.py singular_plural objrel_that_ablation | sort -nk4 | perl -ne 's/singular_plural//; s/_.*abl//; print' | awk '$4<1{print $1 "\t" $4}' > results/objrel_that_singular_plural_results.txt

        python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/process_ablation_accuracies.py plural_singular objrel_that_ablation | sort -nk4 | perl -ne 's/plural_singular//; s/_.*abl//; print' | awk '$4<1{print $1 "\t" $4}' > results/objrel_that_plural_singular_results.txt

        python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/process_ablation_accuracies.py plural_plural objrel_that_ablation | sort -nk4 | perl -ne 's/plural_plural//; s/_.*abl//; print' | awk '$4<1{print $1 "\t" $4}' > results/objrel_that_plural_plural_results.txt

fi

## subjrel_that
if true
then

        perl ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/generate_relatives.pl 0 600 subjrel_that | perl -F'\t' -ane 'print join "\t",(@F[0..1],"$F[2]_$F[3]",$F[4],$F[5])' | perl ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/post_process_stimuli_ending_with_verb_to_create_correct_wrong.pl > correct_wrong_subjrel_that.txt

        perl -F'\t' -ane 'print $F[0],"\n"' correct_wrong_subjrel_that.txt > subjrel_that_prefixes.txt

        python ~/sentence-processing-MEG-LSTM/Code/LSTM/model-analysis/extract-activations.py $model_path -i subjrel_that_prefixes.txt -v $vocab_path -o ./subjrel_that_data --eos-separator "<eos>" --format pkl --cuda -g lstm --use-unk --unk-token "<unk>"

        python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/compute_accuracy.py subjrel_that_data.pkl correct_wrong_subjrel_that.txt 1 2 6

        python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/get_ALL_sentences_and_data.py subjrel_that_data.pkl correct_wrong_subjrel_that.txt 1 2 6 > temp_good_subjrel_that.txt

        perl ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/convert_sentences_to_tal_format.pl subjrel_that temp_good_subjrel_that.txt

        mkdir subjrel_that_ablation

        bash ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/generate_ablation_commands.sh ./subjrel_that ./subjrel_that_ablation $model_path $vocab_path do_split > temp_subjrel_that_ablation_commands.txt

        bash ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/run_ablation.sh temp_subjrel_that_ablation_commands.txt


        python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/process_ablation_accuracies.py singular_singular subjrel_that_ablation | sort -nk4 | perl -ne 's/singular_singular//; s/_.*abl//; print' | awk '$4<1{print $1 "\t" $4}' > results/subjrel_that_singular_singular_results.txt

        python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/process_ablation_accuracies.py singular_plural subjrel_that_ablation | sort -nk4 | perl -ne 's/singular_plural//; s/_.*abl//; print' | awk '$4<1{print $1 "\t" $4}' > results/subjrel_that_singular_plural_results.txt

        python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/process_ablation_accuracies.py plural_singular subjrel_that_ablation | sort -nk4 | perl -ne 's/plural_singular//; s/_.*abl//; print' | awk '$4<1{print $1 "\t" $4}' > results/subjrel_that_plural_singular_results.txt

        python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/process_ablation_accuracies.py plural_plural subjrel_that_ablation | sort -nk4 | perl -ne 's/plural_plural//; s/_.*abl//; print' | awk '$4<1{print $1 "\t" $4}' > results/subjrel_that_plural_plural_results.txt
fi


## NOUNPP_that
if true
then

        #Generating sentences of the form "NP P NP V" ("the athlete beside the car avoids"). Note that in this case we have a distractor for both the singular and plural condition (athlete(s)/car(s)), so the analysis will be conducted in terms of the categories: singular_singular, singular_plural, plural_plural and plural_singular.
        #The extra command-line perl script in the following pipeline creates the composite number tags listed above:

        perl ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/generate_relatives.pl 0 600 nounpp_adv | perl -F'\t' -ane 'print join "\t",(@F[0..1],"$F[2]_$F[3]",$F[4])' | perl ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/post_process_stimuli_ending_with_verb_to_create_correct_wrong.pl > correct_wrong_nounpp_adv.txt


        perl -F'\t' -ane 'print $F[0],"\n"' correct_wrong_nounpp_adv.txt > nounpp_adv_prefixes.txt

        python ~/sentence-processing-MEG-LSTM/Code/LSTM/model-analysis/extract-activations.py $model_path -i nounpp_adv_prefixes.txt -v $vocab_path -o ./nounpp_adv_data --eos-separator "<eos>" --format pkl --cuda -g lstm --use-unk --unk-token "<unk>"

        python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/compute_accuracy.py nounpp_adv_data.pkl correct_wrong_nounpp_adv.txt 1 2 6

        python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/get_ALL_sentences_and_data.py nounpp_adv_data.pkl correct_wrong_nounpp_adv.txt 1 2 6 > temp_good_nounpp_adv.txt

        #Note that, in the following step, we now generate separate file sets for all possible singular/plural combinations:

        perl ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/convert_sentences_to_tal_format.pl nounpp_adv temp_good_nounpp_adv.txt

        mkdir nounpp_adv_ablation

        bash ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/generate_ablation_commands.sh ./nounpp_adv ./nounpp_adv_ablation $model_path $vocab_path do_split > temp_nounpp_adv_ablation_commands.txt

        bash ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/run_ablation.sh temp_nounpp_adv_ablation_commands.txt

        python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/process_ablation_accuracies.py singular_singular nounpp_adv_ablation | sort -nk4 | perl -ne 's/singular_singular//; s/_.*abl//; print' | awk '$4<1{print $1 "\t" $4}' > results/nounpp_adv_singular_singular_results.txt

        python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/process_ablation_accuracies.py singular_plural nounpp_adv_ablation | sort -nk4 | perl -ne 's/singular_plural//; s/_.*abl//; print' | awk '$4<1{print $1 "\t" $4}' > results/nounpp_adv_singular_plural_results.txt

        python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/process_ablation_accuracies.py plural_singular nounpp_adv_ablation | sort -nk4 | perl -ne 's/plural_singular//; s/_.*abl//; print' | awk '$4<1{print $1 "\t" $4}' > results/nounpp_adv_plural_singular_results.txt

        python ~/sentence-processing-MEG-LSTM/Code/Stimuli/English/NA_tasks/process_ablation_accuracies.py plural_plural nounpp_adv_ablation | sort -nk4 | perl -ne 's/plural_plural//; s/_.*abl//; print' | awk '$4<1{print $1 "\t" $4}' > results/nounpp_adv_plural_plural_results.txt

fi


echo ALL_DONE

echo "Checking the number of outputs ..."

echo adv_ablation
ls adv_ablation/ | wc -l

echo adv_conjunction_ablation
ls adv_conjunction_ablation/ | wc -l

echo nounpp_ablation
ls nounpp_ablation/ | wc -l

echo objrel_ablation
ls objrel_ablation/ | wc -l

echo subjrel_that_ablation
ls subjrel_that_ablation/ | wc -l

echo adv_adv_ablation
ls adv_adv_ablation/ | wc -l

echo namepp_ablation/
ls namepp_ablation/ | wc -l

echo nounpp_adv_ablation
ls nounpp_adv_ablation/ | wc -l

echo objrel_that_ablation
ls objrel_that_ablation/ | wc -l

echo simple_ablation
ls simple_ablation/ | wc -l

bash ./analyse_ablation_results.sh > results/final_results.txt

