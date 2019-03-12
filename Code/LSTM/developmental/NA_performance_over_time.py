import os, pickle


# Collect performance results
batches = [0]
perf = [0.5]
for epoch in range(1,10):
    for batch in range(200, 123000, 200):
        print(epoch, batch)
        filename = 'Output/english_nounpp_epoch_%i_batch_%i.abl' % (epoch, batch)
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                results = pickle.load(f)
                perf.append(results['score_on_task']/results['num_sentences'])
                t = (epoch - 1) * 123000 + batch
                batches.append(t)
        else:
            print('File %s does not exist' % filename)

#print(batches, perf)
# Plot
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 10))
ax.plot(batches, perf)
ax.set_xlabel('Batch', fontsize=16)
ax.set_ylabel('Performance on the nounPP NA-task', fontsize=16)
fig.savefig(os.path.join('..', '..', '..', 'Figures', 'English_network_development_per_batch.png'))
print('Figure saved to: ' + os.path.join('Figures', 'English_network_development_per_batch.png'))
#plt.show()
