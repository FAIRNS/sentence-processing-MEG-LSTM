with open('objrel_that_acceptable.txt', 'r') as f:
    sents = f.readlines()

sent_type = 'objrel_that'
cond = 'SP'
viol_on_slide = 0

sents = sents[1::]
sents = [s.split('\t')[1] for s in sents]
print(sents)

with open('subj_00.txt', 'w') as f:
    for s in sents:
        s = s.split(' ')
        new_s = ' '.join(['_'.join([s[0], s[1]]), s[2], '_'.join([s[3], s[4]]), s[5], s[6], '_'.join([s[7], s[8]])])
        f.write('%s\t%s\t%s\t%i\n' % (new_s, sent_type, cond, viol_on_slide))