% overwrite current patient text file   

cd ..
fid = fopen(['CurrentPatient.txt'],'w');
fprintf(fid,'%s',subjectname);  % this does completely rewrite over whatever was in the original file, even if the new text is smaller    
cd(subjectname)
disp('sdf')
return

% do a diff file for each block

fid = fopen([csvfilename '.csv'],'w');

%%%%%% not sure if it ultimately will be needed, but include it for now
% output the maximum number of words in the first position of the output file
maxNWords=13;
fprintf(fid,'%2d',maxNWords);
fprintf(fid,'\n');

for ibl=1:nBlocksToGen
    for curBlockType=BlockOrder
        switch curBlockType
            case 1
                if ibl <= MaxNMemBlocks
                    curfile=outfile_Loc{ibl}
                    
                end
            case 2
                load( outfile_Main{ibl} );
            case 3
                load( outfile_Jab{ibl} );
        end
        load(  );
        
        
        
        fprintf(fid,['new block,' outfile '\n']);
        
        for isent = 1:nsentences  %% we just change the wordlists            
            
            for inum = 1:2
                nwords = length(wordlist{isent,inum});
                fprintf(fid,'%2d',nwords);
                %fprintf(fid,',%s',num2str( fontsizes(fontused(isent)) ));
                fprintf(fid,',%s',num2str( fs_Stim ));
                for iword = 1:nwords
                    fprintf(fid,',%s',wordlist{isent,inum}{iword});
                end
                fprintf(fid,'\n');
            end
        end
    end
end


