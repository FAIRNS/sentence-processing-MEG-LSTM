toc

Priority(0);
Screen('closeall'); % this line deallocates the space pointed to by the buffers, and returns the screen to normal.
FlushEvents('keyDown'); % removed typed characters from queue.

%%% Don't need to save data at the end anymore because we're already saving it every trial        
% disp('saving data')
% outfile = [ 'ExperimentalRun' sprintf('_%d',fix(clock)) '.mat' ];
% save(outfile);  %%% save everything: the wordlist, the sentences, even the rules used to generate the sentences

cd(initdir)
