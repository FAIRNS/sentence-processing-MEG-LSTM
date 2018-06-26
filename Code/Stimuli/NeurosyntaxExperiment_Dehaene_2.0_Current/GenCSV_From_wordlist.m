% GenCSV_From_wordlist.m

%%%%%% not sure if it ultimately will be needed, but include it for now
% output the maximum number of words in the first position of the output file
fprintf(fid,'%2d',maxNWords);
fprintf(fid,'\n');
%fprintf(fid,['new block,' outfile '\n']);

for isent = 1:nsentences  %% we just change the wordlists
    for inum = 1:2
        nwords = length(wordlist{isent,inum});
        fprintf(fid,'%2d',nwords);
        %fprintf(fid,',%s',num2str( fontsizes(fontused(isent)) ));
        fprintf(fid,',%s',num2str( fs_Stim ));
        if any( strcmp( wordlist{isent,inum},PressStr ))
            fprintf(fid,',%s','1');
        else
            fprintf(fid,',%s','0');
        end
        fprintf(fid,',%s',num2str( fs_Stim ));
        
        for iword = 1:nwords
            fprintf(fid,',%s',wordlist{isent,inum}{iword});
        end
        fprintf(fid,'\n');
    end
end

fclose(fid);

