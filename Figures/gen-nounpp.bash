# This file lives inside Figures
HOME_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"/..
UNIT=$1

if [ -z $1 ]
then 
    echo "Please, specify the unit."
    exit 1
fi

# Line width
LW=1.5

python3 $HOME_DIR/Code/LSTM/model-analysis/plot_units_activations.py \
    -sentences $HOME_DIR/Data/Stimuli/nounpp.text \
    -meta $HOME_DIR/Data/Stimuli/nounpp.info \
    -activations $HOME_DIR/Data/LSTM/nounpp.pkl \
    -o $HOME_DIR/Figures/nounpp_${UNIT}.pdf \
    -c nounpp \
    -g 4 r \- $LW ${UNIT} cell number_1 singular number_2 singular success correct "Singular-Singular"\
    -g 1 r \- $LW ${UNIT} gates.c_tilde number_1 singular number_2 singular success correct \
    -g 1 r "\-." $LW ${UNIT} gates.c_tilde number_1 singular number_2 plural success correct \
    -g 1 b "\-." $LW ${UNIT} gates.c_tilde number_1 plural number_2 singular success correct \
    -g 1 b \- $LW ${UNIT} gates.c_tilde number_1 plural number_2 plural success correct \
    -g 2 r \- $LW ${UNIT} gates.in number_1 singular number_2 singular success correct \
    -g 2 r "\-." $LW ${UNIT} gates.in number_1 singular number_2 plural success correct \
    -g 2 b "\-." $LW ${UNIT} gates.in number_1 plural number_2 singular success correct \
    -g 2 b \- $LW ${UNIT} gates.in number_1 plural number_2 plural success correct \
    -g 3 r \- $LW ${UNIT} gates.forget number_1 singular number_2 singular success correct \
    -g 3 r "\-." $LW ${UNIT} gates.forget number_1 singular number_2 plural success correct \
    -g 3 b "\-." $LW ${UNIT} gates.forget number_1 plural number_2 singular success correct \
    -g 3 b \- $LW ${UNIT} gates.forget number_1 plural number_2 plural success correct \
    -g 4 r "\-." $LW ${UNIT} cell number_1 singular number_2 plural success correct "\\textbf{Singular}-\\underline{Plural}"\
    -g 4 b "\-." $LW ${UNIT} cell number_1 plural number_2 singular success correct "\\textbf{Plural}-\\underline{Singular}"\
    -g 4 b \- $LW ${UNIT} cell number_1 plural number_2 plural success correct "\\textbf{Plural}-\\underline{Plural}"\
    -g 4 g "\-\-" $LW 1149 cell success correct "Syntax Unit 1150"\
    -g 5 r \- $LW ${UNIT} gates.out number_1 singular number_2 singular success correct \
    -g 5 r "\--" $LW ${UNIT} gates.out number_1 singular number_2 plural success correct \
    -g 5 b "\--" $LW ${UNIT} gates.out number_1 plural number_2 singular success correct \
    -g 5 b \- $LW ${UNIT} gates.out number_1 plural number_2 plural success correct \
    --ylabels "$\\tilde{C_t}$" '$i_t$' '$f_t$' '$C_t$' '$o_t$'\
    --use-tex \
    -r 1 -x "The" "\\textbf{boy(s)}" "near" "the" "\\underline{car(s)}" "\\textbf{greet(s)}" "the" \
    --no-legend

