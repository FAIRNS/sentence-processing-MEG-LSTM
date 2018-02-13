'''
Epoching and averaging for each condition
To do:
- OK -- include subject's correct response and RT
- OK -- repeat for multiple speed conditions
- OK -- crop epochs to timelock on word positions
- Correction for head positions
- OK -- exact onset time with photodiode. Exact times are: 301, 167, 116 ms. Condition 80 ms is wrong at the moment.
- stim info for decoding word categories
'''

from __future__ import division
import mne
from mne.preprocessing import read_ica
import pickle
import numpy as np
import os.path as op
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d as mp3d
# import matplotlib as plt

def get_coordinates(fif_file):
	# fif_file is the fif file itself (not the path)
	# ax is an instance of 3D subplot, e.g. ax = fig.add_subplot(111, projection='3d')
	ntrial = len(fif_file.info['dig'])
	xyz = np.zeros((ntrial,3))
	# ys = np.zeros((ntrial))
	# zs = np.zeros((ntrial))
	for itrl in range(ntrial):
		xyz[itrl,0] = fif_file.info['dig'][itrl]['r'][0]
		xyz[itrl,1] = fif_file.info['dig'][itrl]['r'][1]
		xyz[itrl,2] = fif_file.info['dig'][itrl]['r'][2]
	return xyz

def plot_dig(xs, ys, zs, ax, facecolor, edgecolor):
	# fif_file is the fif file itself (not the path)
	# ax is an instance of 3D subplot, e.g. ax = fig.add_subplot(111, projection='3d')
	ax.scatter(xs[:2], ys[:2], zs[:2], c=facecolor, marker='+', s=70)
	ax.scatter(xs[3:7], ys[3:7], zs[3:7], c=facecolor, marker='o', s=140)
	f = ax.plot_trisurf(xs[8:],ys[8:],zs[8:], shade=True)
	alpha = 0.5
	f.set_facecolor((facecolor[0], facecolor[1], facecolor[2], alpha))
	f.set_edgecolor((edgecolor[0], edgecolor[1], edgecolor[2], alpha))
	ax.add_collection3d(f)

def get_stimulus_information(subj_num, subject, sessions, runs):

	''' ----- GET STIMULUS INFORMATION ------ '''
	# get RSVP speeds for each session
	speeds = [None]*2
	f = open('/neurospin/meg/meg_tmp/sentcomp_Marti_2016/' + subj_num + '-' + subject + '/Stim/speeds.p', 'r')
	speeds[0] = pickle.load(f)
	f.close()
	f = open('/neurospin/meg/meg_tmp/sentcomp_Marti_2016/' + subj_num + '-' + subject + '/Stim2/speeds.p', 'r')
	speeds[1] = pickle.load(f)
	f.close()

	# block_list = []
	# file_list = os.listdir('/neurospin/meg/meg_tmp/sentcomp_Marti_2016/' + subj_num + '-' + subject + '/Stim')
	# for files in file_list:
	# 	if files.startswith('block'):
	# 	    block_list.append(files)

	info_stim = [None]*len(sessions)
	info_stim[0] = [None]*len(runs)
	info_stim[1] = [None]*len(runs)
	print('-----> Loading stimulus information for session 1:')
	for irun in range(len(runs)):
		# f = open(op.join('/neurospin/meg/meg_tmp/sentcomp_Marti_2016/' + subj_num + '-' + subject + '/Stim/' + block_list[irun] + '/info_stim.p'), 'r')
		f = open(op.join('/neurospin/meg/meg_tmp/sentcomp_Marti_2016/' + subj_num + '-' + subject + '/Stim/block' + str(irun) + '_' + str(speeds[0][irun]) + 'ms/info_stim.p'), 'r')
		print(op.join('/neurospin/meg/meg_tmp/sentcomp_Marti_2016/' + subj_num + '-' + subject + '/Stim/block' + str(irun) + '_' + str(speeds[0][irun]) + 'ms/info_stim.p'))
		info_stim[0][irun] = pickle.load(f)
		f.close()

	# block_list = []
	# file_list = os.listdir('/neurospin/meg/meg_tmp/sentcomp_Marti_2016/' + subj_num + '-' + subject + '/Stim2')
	# for files in file_list:
	# 	if files.startswith('block'):
	# 	    block_list.append(files)
	print('-----> Loading stimulus information for session 2:')
	for irun in range(len(runs)):
		# f = open(op.join('/neurospin/meg/meg_tmp/sentcomp_Marti_2016/' + subj_num + '-' + subject + '/Stim/' + block_list[irun] + '/info_stim.p'), 'r')
		f = open(op.join('/neurospin/meg/meg_tmp/sentcomp_Marti_2016/' + subj_num + '-' + subject + '/Stim2/block' + str(irun) + '_' + str(speeds[1][irun]) + 'ms/info_stim.p'), 'r')
		print(op.join('/neurospin/meg/meg_tmp/sentcomp_Marti_2016/' + subj_num + '-' + subject + '/Stim2/block' + str(irun) + '_' + str(speeds[1][irun]) + 'ms/info_stim.p'))
		info_stim[1][irun] = pickle.load(f)
		f.close()

	# now build vectors for all trials
	nepochs = len(info_stim[0][0]) # number of trials for each block
	speeds_epochs = [None]*len(sessions)
	for isession in range(len(sessions)):
		speeds_epochs[isession] = [None]*len(runs)
		for irun in range(len(runs)):
			speeds_epochs[isession][irun] = [None]*nepochs
			if speeds[isession][irun]==80:
				for iepoch in range(nepochs):
					speeds_epochs[isession][irun][iepoch] = '1'
			if speeds[isession][irun]==120:
				for iepoch in range(nepochs):
					speeds_epochs[isession][irun][iepoch] = '2'
			if speeds[isession][irun]==160:
				for iepoch in range(nepochs):
					speeds_epochs[isession][irun][iepoch] = '3'
			if speeds[isession][irun]==300:
				for iepoch in range(nepochs):
					speeds_epochs[isession][irun][iepoch] = '4'

	anomalies_epochs = [None]*len(sessions)
	for isession in range(len(sessions)):
		anomalies_epochs[isession] = [None]*len(runs)
		for irun in range(len(runs)):
			anomalies_epochs[isession][irun] = [None]*nepochs
			for iepoch in range(nepochs):
				if info_stim[isession][irun][iepoch]['anomaly']=='correct':
					anomalies_epochs[isession][irun][iepoch] = str(int(0))
				elif info_stim[isession][irun][iepoch]['anomaly']=='string':
					anomalies_epochs[isession][irun][iepoch] = str(int(1))
				elif info_stim[isession][irun][iepoch]['anomaly']=='syntax':
					anomalies_epochs[isession][irun][iepoch] = str(int(2))
				elif info_stim[isession][irun][iepoch]['anomaly']=='semantic':
					anomalies_epochs[isession][irun][iepoch] = str(int(3))

	position_epochs = [None]*len(sessions)
	for isession in range(len(sessions)):
		position_epochs[isession] = [None]*len(runs)
		for irun in range(len(runs)):
			position_epochs[isession][irun] = [None]*nepochs
			for iepoch in range(nepochs):
				position_epochs[isession][irun][iepoch] = str(int(info_stim[isession][irun][iepoch]['anomaly_position']+1))
	structure_epochs = [None]*len(sessions)
	for isession in range(len(sessions)):
		structure_epochs[isession] = [None]*len(runs)
		for irun in range(len(runs)):
			structure_epochs[isession][irun] = [None]*nepochs
			for iepoch in range(nepochs):
				structure_epochs[isession][irun][iepoch] = str(int(info_stim[isession][irun][iepoch]['structure']))
	return speeds_epochs, anomalies_epochs, position_epochs, structure_epochs

# def set_new_triggers(events, anomalies_epochs, speeds_epochs, position_epochs, speed_oi):
def set_trial_info(events, anomalies_epochs, speeds_epochs, position_epochs, structure_epochs):
	# build new triggers for averaging
	iepoch=0
	acc, rt = [], []
	for itrl in range(len(events)):
		if events[itrl,2]==1: # this replace trigger for word 1 by a code specific to speed, anomaly, position and accuracy
			# if speeds_epochs[iepoch]==4:
			# 	real_speed=301 # in ms.
			# elif speeds_epochs[iepoch]==3:
			# 	real_speed=167
			# elif speeds_epochs[iepoch]==2:
			# 	real_speed=116
			# else:
			# 	real_speed=116 #CHANGE THIS once the presentation time for speed 1 will be actually 83 ms.
			rt_trial = 0
			acc_trial = '0'
			# events[itrl,2] = int(speeds_epochs[isession][irun][iepoch][0] + anomalies_epochs[isession][irun][iepoch][0] + position_epochs[isession][irun][iepoch][0])
			for i_event_trial in range(10): #range(9) because there are 8 word triggers and 1 response trigger
				if itrl+i_event_trial>=len(events):
					pass
				else:
					if events[itrl+i_event_trial,2]==2048 or events[itrl+i_event_trial,2]==16384:
						rt_trial = events[itrl+i_event_trial,0] - events[itrl,0]
					if events[itrl+i_event_trial,2]==2048 and int(anomalies_epochs[iepoch][0])>0: # correct detection of anomaly
						acc_trial = '1'
					elif events[itrl+i_event_trial,2]==16384 and int(anomalies_epochs[iepoch][0])==0: # correct detection of correct sentence
						acc_trial = '1'
					# else:
					# 	acc_trial = '0'
			events[itrl,2] = int(speeds_epochs[iepoch] + anomalies_epochs[iepoch] + position_epochs[iepoch] + structure_epochs[iepoch] + acc_trial)
			iepoch = iepoch+1
			acc.append(acc_trial)
			rt.append(rt_trial)
	return events, acc, rt

# def set_condition_dict(speed_oi):
# 	A = [0, 1, 2, 3]
# 	P = [4, 6, 8]
# 	R = [0, 1]
# 	key_names = []
# 	values = []
# 	# key_names = ['A0_R0']
# 	# key_names.append('A0_R1')

# 	# values = [int(str(speed_oi) + '000')]
# 	# values.append(int(str(speed_oi) + '001'))
# 	# for iA, iP, iR in map(A, P, R):
# 	# 	key_names.append('S' + str(speed_oi) + '_' + 'A' + str(iA) + '_' + 'P' + str(iP) + '_' + 'R' + str(iR))
# 	# 	values.append(int(str(speed_oi) + str(iA) + str(iP) + str(iR)))
# 	for iA in A:
# 		for iP in P:
# 			for iR in R:
# 				key_names.append('A' + str(iA) + '_' + 'P' + str(iP) + '_' + 'R' + str(iR))
# 				values.append(int(str(speed_oi) + str(iA) + str(iP) + str(iR)))
# 	event_id = dict(zip(key_names, values))
# 	return event_id

def set_condition_dict(speed_oi):
	A = [0, 1, 2, 3]
	P = [4, 6, 8]
	R = [0, 1]
	S = [1, 2, 3]
	key_names = []
	values = []
	# key_names = ['A0_R0']
	# key_names.append('A0_R1')

	# values = [int(str(speed_oi) + '000')]
	# values.append(int(str(speed_oi) + '001'))
	# for iA, iP, iR in map(A, P, R):
	# 	key_names.append('S' + str(speed_oi) + '_' + 'A' + str(iA) + '_' + 'P' + str(iP) + '_' + 'R' + str(iR))
	# 	values.append(int(str(speed_oi) + str(iA) + str(iP) + str(iR)))
	for iA in A:
		for iP in P:
			for iR in R:
				for iS in S:
					key_names.append('A' + str(iA) + '_' + 'P' + str(iP) + '_S' + str(iS) + '_' + 'R' + str(iR))
					values.append(int(str(speed_oi) + str(iA) + str(iP) + str(iS) + str(iR)))
	event_id = dict(zip(key_names, values))
	return event_id

def find_bad_epochs(epochs, plot):
	''' returns the index of epochs for which the variance across sensors exceeds 2 SD '''
	outlim = 2 # threshold for outlier definition. In SD.
	
	grad = np.concatenate([epochs._data[:,range(0,304,3),:], epochs._data[:,range(1,305,3),:]], axis=1)
	mag = epochs._data[:,range(2,306,3),:]

	grad_var = np.sum(np.var(grad,axis=1), axis=1)
	mag_var = np.sum(np.var(mag,axis=1), axis=1)
	trials = range(grad.shape[0])
	grad_outliers = np.where(1*(grad_var>np.median(grad_var)+2*np.std(grad_var)*outlim)==1)
	grad_outliers = grad_outliers[0]
	mag_outliers = np.where(1*(mag_var>np.median(mag_var)+2*np.std(mag_var)*outlim)==1)
	mag_outliers = mag_outliers[0]
	if plot==1:
		fig = plt.figure()
		# fig.title("Bad trials")
		ax1 = fig.add_subplot(211)
		ax1.scatter(trials,grad_var, c='k', edgecolors='k')
		ax1.set_ylim((0, np.max(grad_var)*1.2))
		ax1.set_xlabel("Trial #")
		ax1.set_ylabel("Sensor variance")
		ax2 = fig.add_subplot(212)
		ax2.scatter(trials,mag_var, c='k', edgecolors='k')
		ax2.set_ylim((0, np.max(mag_var)*1.2))
		ax2.set_xlabel("Trial #")
		ax2.set_ylabel("Sensor variance")
		ax1.scatter(grad_outliers, grad_var[grad_outliers], c='r', edgecolors='r')
		ax2.scatter(mag_outliers, mag_var[mag_outliers], c='r', edgecolors='r')
	outliers = np.unique(np.concatenate((grad_outliers, mag_outliers), axis=0))
	return outliers

def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return idx

# def get_condition(conditions,epochs,startTime, duration,real_speed):
# 	''' 
# 	selects conditions and time windows 
# 	Build a condition name from the "conditions" dictionnary

# 	'''
# 	# conditions = dict([
# 	# 		('Anomalies', [0, 1, 2, 3]), 
# 	# 		('Positions', [4, 6, 8]), 
# 	# 		('Responses', [0, 1])])

# 	''' Get conditions names '''
# 	values = []
# 	key_names = []
# 	# if 'Anomalies' in conditions:
# 	# 	if 0 in conditions['Anomalies']:
# 	# 		if 0 in conditions['Responses']:
# 	# 			key_names.append('A0_R0')
# 	# 		if 1 in conditions['Responses']:
# 	# 			key_names.append('A0_R1')

# 	for iA in conditions['Anomalies']:
# 		# if iA>0:
# 		for iP in conditions['Positions']:
# 			for iR in conditions['Responses']:
# 				key_names.append('A' + str(iA) + '_' + 'P' + str(iP) + '_' + 'R' + str(iR))
	
# 	''' Build epochs '''
# 	ep = []
# 	# time = np.arange(twin[0], twin[1], .005, dtype=float)
# 	for iA in conditions['Anomalies']:
# 		# if iA==0:
# 		# 	for p in conditions['Positions']:
# 		# 		k = []
# 		# 		for kname in key_names:
# 		# 			if kname[1]=='0':
# 		# 				k.append(kname)
# 		# 		tmin = real_speed*(p-1) + startTime # p-1 because time 0 is actually word 1
# 		# 		tmax = tmin + duration
# 		# 		ep.append(epochs[k].crop(tmin,tmax))
# 		# else:
# 		for p in conditions['Positions']:
# 			k = []
# 			for kname in key_names:
# 				if kname[4]==str(p):
# 					k.append(kname)
# 			tmin = real_speed*(p-1) + startTime
# 			tmax = tmin + duration
# 			ep.append(epochs[k].crop(tmin,tmax))
# 	for p in range(len(ep)):
# 		ltimes = ep[p]._data.shape[2]
# 		ep[p].times = epochs.times[find_nearest(epochs.times, startTime):find_nearest(epochs.times, startTime)+ltimes]
# 		# ep[p].baseline = (startTime, 0)
# 		ep[p].baseline = None
# 	ep = mne.concatenate_epochs(ep)
# 	# print('ding')
# 	return key_names, ep

def get_condition(conditions,epochs,startTime, duration,real_speed):
	''' 
	selects conditions and time windows 
	Build a condition name from the "conditions" dictionnary

	'''
	# conditions = dict([
	# 		('Anomalies', [0, 1, 2, 3]), 
	# 		('Positions', [4, 6, 8]), 
	# 		('Responses', [0, 1])])

	''' Get conditions names '''
	values = []
	key_names = []
	# if 'Anomalies' in conditions:
	# 	if 0 in conditions['Anomalies']:
	# 		if 0 in conditions['Responses']:
	# 			key_names.append('A0_R0')
	# 		if 1 in conditions['Responses']:
	# 			key_names.append('A0_R1')

	for iA in conditions['Anomalies']:
		# if iA>0:
		for iP in conditions['Positions']:
			for iS in conditions['Structure']:
				for iR in conditions['Responses']:
					key_names.append('A' + str(iA) + '_' + 'P' + str(iP) + '_S' + str(iS) + '_' + 'R' + str(iR))
	
	''' Build epochs '''
	ep = []
	# time = np.arange(twin[0], twin[1], .005, dtype=float)
	for iA in conditions['Anomalies']:
		# if iA==0:
		# 	for p in conditions['Positions']:
		# 		k = []
		# 		for kname in key_names:
		# 			if kname[1]=='0':
		# 				k.append(kname)
		# 		tmin = real_speed*(p-1) + startTime # p-1 because time 0 is actually word 1
		# 		tmax = tmin + duration
		# 		ep.append(epochs[k].crop(tmin,tmax))
		# else:
		for p in conditions['Positions']:
			k = []
			for kname in key_names:
				if kname[4]==str(p):
					k.append(kname)
			tmin = real_speed*(p-1) + startTime
			tmax = tmin + duration
			ep.append(epochs[k].crop(tmin,tmax))
	for p in range(len(ep)):
		ltimes = ep[p]._data.shape[2]
		ep[p].times = epochs.times[find_nearest(epochs.times, startTime):find_nearest(epochs.times, startTime)+ltimes]
		# ep[p].baseline = (startTime, 0)
		ep[p].baseline = None
		''' FIX HERE TO SELECT STRUCTURE CONDITIONS '''
	ep = mne.concatenate_epochs(ep)
	# print('ding')
	return key_names, ep

def sentcomp_epoch(subject, subj_num, runs, sessions, data_sss_path, speed_oi):
	# ''' ----- SUBJECT INFO ----- '''
	# subject = 'am150105'
	# subj_num = '1'
	# runs = range(1,9)
	# sessions = [1,2]
	# data_sss_path = '/neurospin/meg/meg_tmp/sentcomp_Marti_2016/Seb/data/sss/'
	# speed_oi = 4
	# real_speed = .301

	''' get stim info '''
	speeds_epochs, anomalies_epochs, position_epochs, structure_epochs = get_stimulus_information(subj_num, subject, sessions, runs)

	# ''' compare head position between sessions '''
	# sss = mne.io.Raw(data_sss_path + 'sentcomp_' + subject + '_' + subj_num + '_1_run1_raw_sss.fif', preload = True)
	# sss2 = mne.io.Raw(data_sss_path + 'sentcomp_' + subject + '_' + subj_num + '_2_run1_raw_sss.fif', preload = True)
	# xyz1 = get_coordinates(sss)
	# xyz2 = get_coordinates(sss2)
	# fig = plt.figure()
	# ax = fig.add_subplot(111, projection='3d')
	# plot_dig(xyz1[:,0], xyz1[:,1], xyz1[:,2], ax, [1, 0, 0], [1, .5, .5])
	# plot_dig(xyz2[:,0], xyz2[:,1], xyz2[:,2], ax, [0, 0, 1], [.5, .5, 1])
	# ax.axis('square')
	# del sss
	# del sss2

	''' ----- MAIN LOOP ACROSS RUNS AND SESSIONS ----- '''
	all_epochs, acc, rt = [], [], []
	for isession in range(len(sessions)):
		for irun in range(len(runs)):
			speed_of_this_run = int(np.unique(speeds_epochs[isession][irun])[0])
			if speed_of_this_run==speed_oi:
				data_sss_filename = 'sentcomp_' + subject + '_' + subj_num + '_' + str(sessions[isession]) + '_run' + str(runs[irun]) + '_raw_sss.fif'

				# Information status
				mne.set_log_level('INFO')

				# "Load raw data"
				sss_fname = data_sss_path + data_sss_filename
				print('Loading: ' + sss_fname)
				sss = mne.io.Raw(sss_fname, preload = True) 

				# find events
				events = mne.find_events(sss, stim_channel='STI101', consecutive=False, min_duration=0)

				# build new triggers 
				events, acc_session, rt_session = set_trial_info(events=events, anomalies_epochs=anomalies_epochs[isession][irun], speeds_epochs=speeds_epochs[isession][irun], position_epochs=position_epochs[isession][irun], structure_epochs=structure_epochs[isession][irun])
				acc.append(acc_session)
				rt.append(rt_session)
				# get real speed value
				# vals = np.unique(np.diff(events[:,0]))
				# x = np.zeros((1,2))
				# x[0] = vals[np.searchsorted(vals,speeds[isession][irun], side='right')]
				# x[1] = vals[np.searchsorted(vals,speeds[isession][irun], side='left')]
				# real_speed.append(vals[np.searchsorted(vals,speeds[isession][irun], side='left')]) ################### CHANGE THIS   ---- not optimal
				event_id = set_condition_dict(speed_oi)

				# define the default event channel
				mne.set_config('MNE_STIM_CHANNEL', 'STI101') 

				if any(np.in1d(events[:,2],event_id.values())):
					# all combinations of triggers (conditions and responses) are necessarily present
					print('top')
					event_id_subset = dict()
					sel_cond = np.in1d(events[:,2],event_id.values())
					sel_val = np.unique(events[sel_cond,2])
					for icond in range(len(sel_val)):
						event_id_subset[event_id.keys()[event_id.values().index(sel_val[icond])]] = sel_val[icond]

					# start with the entire epoch
					electronicDelay = .04
					tmin = -0.8 + electronicDelay  # start of each epoch 
					tmax = 4 + electronicDelay  # end of each epoch 
					sss.info['bads'] += [] # bad channels
					picks = mne.pick_types(sss.info, meg=True, eeg=False, eog=False, stim=False, exclude='bads')
					baseline = (-.8 + electronicDelay, -.3 + electronicDelay)  # means from the first instant to t = 0
					
					# reject = dict(grad=4000e-13, mag=4e-12) # criterion for bad trials
					tmp = mne.Epochs(sss, events, event_id_subset, tmin, tmax, proj=True, picks=picks, baseline=baseline, preload=True, decim=5)
					# apply ica
					if op.isfile('/neurospin/meg/meg_tmp/sentcomp_Marti_2016/Seb/data/result_ica/' + subject + '_' + 'session' + str(sessions[isession]) + '_run' + str(runs[irun]) + '_ica.fif'):
						ica = read_ica('/neurospin/meg/meg_tmp/sentcomp_Marti_2016/Seb/data/result_ica/' + subject + '_' + 'session' + str(sessions[isession]) + '_run' + str(runs[irun]) + '_ica.fif')
						ica.apply(tmp)
					else:
						print('No ICA found.')
					all_epochs.append(tmp)

	''' this changes the info field to gather all trials --- TODO: find a way to apply transformation necessary to make sessions comparable '''
	for iepoch in range(len(all_epochs)):
		all_epochs[iepoch].info = all_epochs[0].info
	epochs = mne.epochs.concatenate_epochs(all_epochs)
  
	outliers = find_bad_epochs(epochs,plot=0)
	epochs.drop(outliers) # remove outliers
	epochs.save(op.join('/neurospin/meg/meg_tmp/sentcomp_Marti_2016/Seb/data/epochs/' + subject + '_speed' + str(speed_oi) + '_V2-epo.fif'))

	# ''' build epochs timelocked on anomalies '''
	# np.set_printoptions(precision=3)
	# time = np.asarray(range(0,1501,5))/1000
	# tmin = real_speed*4
	# tmax = tmin + 1.5
	# epo = epochs['A0_R0','A1_P4_R0','A2_P4_R0','A3_P4_R0','A0_R1','A1_P4_R1','A2_P4_R1','A3_P4_R1'].crop(tmin,tmax)
	# epo.times = time
	# epo.save(op.join('/neurospin/meg/meg_tmp/sentcomp_Marti_2016/Seb/data/epochs/' + subject + '_S' + str(speed_oi) + '_P4-epo.fif'))

	# epo = epochs['A0_R0','A1_P6_R0','A2_P6_R0','A3_P6_R0','A0_R1','A1_P6_R1','A2_P6_R1','A3_P6_R1'].crop(tmin,tmax)
	# epo.times = time
	# epo.save(op.join('/neurospin/meg/meg_tmp/sentcomp_Marti_2016/Seb/data/epochs/' + subject + '_S' + str(speed_oi) + '_P6-epo.fif'))

	# epo = epochs['A0_R0','A1_P8_R0','A2_P8_R0','A3_P8_R0','A0_R1','A1_P8_R1','A2_P8_R1','A3_P8_R1'].crop(tmin,tmax)
	# epo.times = time
	# epo.save(op.join('/neurospin/meg/meg_tmp/sentcomp_Marti_2016/Seb/data/epochs/' + subject + '_S' + str(speed_oi) + '_P8-epo.fif'))


