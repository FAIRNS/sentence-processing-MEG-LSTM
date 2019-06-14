# Instructions:
-------------
-------------

The steps described below will help you to replicate the figures presented in the [paper](https://arxiv.org/abs/1903.07435): 

Part 1 describes the scripts that: 
- Organize the stimuli in the required format.
- Extract gate and variable activations from the LSTM network and save them in a pkl file. 

Note that this part describes the required steps for the *Nounpp* number-agreement task (NA-task) only, but the step should be easily repeated for all other NA-tasks provided in the dataset folder. 

Part 2 describes the scripts required for regenerating figures 1-4 in the paper. Specifically,
- [plot_units_activations.py](plot_units_activations.py)
- [extract_embeddings_from_rnn.py](extract_embeddings_from_rnn.py)
- [extract_weights_from_rnn.py](extract_weights_from_rnn.py)



Part 1 - data organization and extraction of LSTM activations:
-------------------------------------------------------------
-------------------------------------------------------------
TBC

data organization
-----------------
TBC


extracting gate, cell and unit activations from the LSTM network
----------------------------------------------------------------
TBC


Part 2 - re-generate figures 1-4 in the paper:
----------------------------------------------
----------------------------------------------

- The scripts in this part require that the stimuus and metadata files for the *Nounpp* NA-task are in the *Data/Stimuli/* folder: *nounpp.text* and *nounpp.info*, correspondly, and that the LSTM activations for this task are in *Data/LSTM/nounpp.pkl*.

Launch the following commands from the root folder of the project and make sure that the paths specified in the arguments are indeed according to your local data organization.


FIGURE 1: dynamics of cell-suggestion, input and forget gates for units 776 and 988 and their efferent weights
--------------------------------------------------

### Unit 776 - nounpp
python3 Code/LSTM/model-analysis/plot_units_activations.py -sentences Data/Stimuli/nounpp.text -meta Data/Stimuli/nounpp.info -activations Data/LSTM/nounpp.pkl -o Figures/nounpp_775.pdf -c nounpp -g 4 r \- 6 775 cell number_1 singular number_2 singular success correct -g 1 r \- 6 775 gates.c_tilde number_1 singular number_2 singular success correct -g 1 r "\--" 6 775 gates.c_tilde number_1 singular number_2 plural success correct -g 1 b "\--" 6 775 gates.c_tilde number_1 plural number_2 singular success correct -g 1 b \- 6 775 gates.c_tilde number_1 plural number_2 plural success correct -g 2 r \- 6 775 gates.in number_1 singular number_2 singular success correct -g 2 r "\--" 6 775 gates.in number_1 singular number_2 plural success correct -g 2 b "\--" 6 775 gates.in number_1 plural number_2 singular success correct -g 2 b \- 6 775 gates.in number_1 plural number_2 plural success correct -g 3 r \- 6 775 gates.forget number_1 singular number_2 singular success correct -g 3 r "\--" 6 775 gates.forget number_1 singular number_2 plural success correct -g 3 b "\--" 6 775 gates.forget number_1 plural number_2 singular success correct -g 3 b \- 6 775 gates.forget number_1 plural number_2 plural success correct -g 4 r "\--" 6 775 cell number_1 singular number_2 plural success correct -g 4 b "\--" 6 775 cell number_1 plural number_2 singular success correct -g 4 b \- 6 775 cell number_1 plural number_2 plural success correct -g 4 g \- 6 1149 cell success correct -g 5 r \- 6 775 gates.out number_1 singular number_2 singular success correct -g 5 r "\--" 6 775 gates.out number_1 singular number_2 plural success correct -g 5 b "\--" 6 775 gates.out number_1 plural number_2 singular success correct -g 5 b \- 6 775 gates.out number_1 plural number_2 plural success correct -r 1 -x "The" "boy(s)" "near" "the" "car(s)" "greet(s)" "the" --no-legend

![alt_text](https://github.com/FAIRNS/sentence-processing-MEG-LSTM/blob/master/Figures_paper/nounpp_775.pdf)

### Unit 988 - nounpp
python3 Code/LSTM/model-analysis/plot_units_activations.py -sentences Data/Stimuli/nounpp.text -meta Data/Stimuli/nounpp.info -activations Data/LSTM/nounpp.pkl -o Figures/nounpp_987.pdf -c nounpp -g 4 r \- 6 987 cell number_1 singular number_2 singular success correct -g 4 r "\--" 6 987 cell number_1 singular number_2 plural success correct -g 4 b "\--" 6 987 cell number_1 plural number_2 singular success correct -g 4 b \- 6 987 cell number_1 plural number_2 plural success correct -g 3 r \- 6 987 gates.forget number_1 singular number_2 singular success correct -g 3 r "\--" 6 987 gates.forget number_1 singular number_2 plural success correct -g 3 b "\--" 6 987 gates.forget number_1 plural number_2 singular success correct -g 3 b \- 6 987 gates.forget number_1 plural number_2 plural success correct -g 2 r \- 6 987 gates.in number_1 singular number_2 singular success correct -g 2 r "\--" 6 987 gates.in number_1 singular number_2 plural success correct -g 2 b "\--" 6 987 gates.in number_1 plural number_2 singular success correct -g 2 b \- 6 987 gates.in number_1 plural number_2 plural success correct -g 1 r \- 6 987 gates.c_tilde number_1 singular number_2 singular success correct -g 1 r "\--" 6 987 gates.c_tilde number_1 singular number_2 plural success correct -g 1 b "\--" 6 987 gates.c_tilde number_1 plural number_2 singular success correct -g 1 b \- 6 987 gates.c_tilde number_1 plural number_2 plural success correct -g 4 g \- 6 1149 cell success correct -g 5 r \- 6 987 gates.out number_1 singular number_2 singular success correct -g 5 r "\--" 6 987 gates.out number_1 singular number_2 plural success correct -g 5 b "\--" 6 987 gates.out number_1 plural number_2 singular success correct -g 5 b \- 6 987 gates.out number_1 plural number_2 plural success correct -r 1 -x "The" "boy(s)" "near" "the" "car(s)" "greet(s)" "the"


(YLABELS:-y "$\tilde{C_t}$" "\$i\_t\$" "\$f\_t\$" "\$C\_t\$" "\$o\_t\$")

![alt_text](https://github.com/FAIRNS/sentence-processing-MEG-LSTM/blob/master/Figures_paper/nounpp_987.pdf)

### Effernt weights
python3 Code/LSTM/model-analysis/extract_embeddings_from_rnn.py -model Data/LSTM/hidden650_batch128_dropout0.2_lr20.0.cpu.pt -v Data/LSTM/english_vocab.txt -i Data/Stimuli/singular_plural_verbs.txt -u 775 987 1149 650 1299 -c b r m c c c g k k

![alt_text](https://github.com/FAIRNS/sentence-processing-MEG-LSTM/blob/master/Figures_paper/weight_dists_verbs.png)

FIGURE 2: generalization across time (GAT)
--------------------------------------------------

python SR_vs_LR_units.py -s ../../../Data/Stimuli/nounpp.text -m ../../../Data/Stimuli/nounpp.info -a ../../../Data/LSTM/activations/english/nounpp.pkl -g cell -o ../../../Figures/GAT1d_cell_.png

![alt_text](https://github.com/FAIRNS/sentence-processing-MEG-LSTM/blob/master/Figures_paper/GAT1d_cell_.png)

FIGURE 3: Cell activity of the syntax unit 1150
-----------------------------------------------------

python3 Code/LSTM/model-analysis/plot_units_activations.py -sentences Data/Stimuli/adv_conjunction.text -meta Data/Stimuli/adv_conjunction.info -activations Data/LSTM/adv_conjunction.pkl -o Figures/adv_conjunction_1149_cell.png -c adv_conjunction -g 1 g \- 6 1149 cell -y "\$C_t$" -x "The" "boy" "gently" "and" "kindly" "greets" "the" -r 1 --no-legend

python3 Code/LSTM/model-analysis/plot_units_activations.py -sentences Data/Stimuli/nounpp.text -meta Data/Stimuli/nounpp.info -activations Data/LSTM/nounpp.pkl -o Figures/nounpp_1149_cell.png -c nounpp -g 1 g \- 6 1149 cell -y "\$C_t$" -x "The" "boy" "near" "the" "car" "greets" "the" -r 1 --no-legend

python3 Code/LSTM/model-analysis/plot_units_activations.py -sentences Data/Stimuli/subjrel_that.text -meta Data/Stimuli/subjrel_that.info -activations Data/LSTM/subjrel_that.pkl -o Figures/subjrel_that_1149_cell.png -c subjrel_that -g 1 g \- 6 1149 cell -y "\$C_t$" -x "The" "boy" "that" "watches" "the" "dog" "greets" "the" -r 1 --no-legend

python3 Code/LSTM/model-analysis/plot_units_activations.py -sentences Data/Stimuli/double_subjrel_that.text -meta Data/Stimuli/double_subjrel_that.info -activations Data/LSTM/double_subjrel_that.pkl -o Figures/double_subjrel_that_1149_cell.png -c double_subjrel_that -g 1 g \- 6 1149 cell -y "\$C_t$" -x "The" "boy" "that" "watches" "the" "dog" "that" "watches" "the" "cat" "greets" "the" -r 1 --no-legend

* note that to successfully generate all figures you should prepare the stimuli and activations also for the other NA-tasks (adv_conjunction, subjrel_that and double_subjrel_that)

![alt_text](https://github.com/FAIRNS/sentence-processing-MEG-LSTM/blob/master/Figures_paper/nounpp_1149_cell.png)

FIGURE 4: connectivity among the syntax (1150) and the LR-number units (776 and 988)
-----------------------------------------------------------------------------------------------

python3 Code/LSTM/model-analysis/extract_weights_from_rnn.py -model Data/LSTM/models/hidden650_batch128_dropout0.2_lr20.0.cpu.pt -fu 775 987 1149 -tu 775 987 -o Figures/interactions.png --no-mds -activations Data/LSTM/activations/english/nounpp.pkl

![alt_text](https://github.com/FAIRNS/sentence-processing-MEG-LSTM/blob/master/Figures_paper/gate_Forget_afferent_interactions.png)


