% AddedGenCSVListScript.m

%  this was written to make the training .csv files  
setparameters_NYU

loadTrainLocStimuli

fid = fopen(['MemTrainingStim.csv'],'w');
for isent = 1:length(fbtext2)    
    for inum = 1:2
        nwords = length(wordlist{isent,inum});
        fprintf(fid,num2str(nwords));
        %fprintf(fid,',%s',num2str( fontsizes(fontused(isent)) ));
        fprintf(fid,',%s',num2str( fs_Stim ));
        fprintf(fid,[',' num2str(samestruct(isent))]);
        for iword = 1:nwords
            fprintf(fid,',%s',wordlist{isent,inum}{iword});
        end
        fprintf(fid,'\n');
    end    
    fprintf(fid,strrep(fbtext2{isent},'\n',','));
    fprintf(fid,'\n');
end
fclose(fid);


loadTrainMainStimuli

fid = fopen(['MainTrainingStim.csv'],'w');
for isent = 1:length(fbtext2)    
    for inum = 1:2
        nwords = length(wordlist{isent,inum});
        fprintf(fid,num2str(nwords));
        %fprintf(fid,',%s',num2str( fontsizes(fontused(isent)) ));
        fprintf(fid,',%s',num2str( fs_Stim ));
        fprintf(fid,[',' num2str(samestruct(isent))]);
        for iword = 1:nwords
            fprintf(fid,',%s',wordlist{isent,inum}{iword});
        end
        fprintf(fid,'\n');
    end    
    fprintf(fid,strrep(fbtext2{isent},'\n',','));
    fprintf(fid,'\n');
end
fclose(fid);


loadTrainJabStimuli

fid = fopen(['JabTrainingStim.csv'],'w');
for isent = 1:length(fbtext2)    
    for inum = 1:2
        nwords = length(wordlist{isent,inum});
        fprintf(fid,num2str(nwords));
        %fprintf(fid,',%s',num2str( fontsizes(fontused(isent)) ));
        fprintf(fid,',%s',num2str( fs_Stim ));
        fprintf(fid,[',' num2str(samestruct(isent))]);
        for iword = 1:nwords
            fprintf(fid,',%s',wordlist{isent,inum}{iword});
        end
        fprintf(fid,'\n');
    end    
    fprintf(fid,strrep(fbtext2{isent},'\n',','));
    fprintf(fid,'\n');
end
fclose(fid);