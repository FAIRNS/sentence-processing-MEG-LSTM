filebase = 'nounpp'
unit = 847 
condition = filebase
gates = ['gates.forget', 'hidden']
constraints = ['number_1 singular number_2 singular','number_1 singular number_2 plural','number_1 plural number_2 singular','number_1 plural number_2 plural']

cmd = 'python3 Code/LSTM/model-analysis/plot_units_activations.py -sentences Data/Stimuli/%s.text -meta Data/Stimuli/%s.info -activations Data/LSTM/%s.pkl -o Figures/%s_%s_%s.png' % (filebase, filebase, filebase, condition, unit, '_'.join(gates))
cmd = cmd + ' -c ' + condition
for constraint in constraints:
    for gate in gates:
        s = ' -g ' + str(unit) + ' ' + gate + ' ' + constraint
        cmd = cmd + s
print(cmd)


