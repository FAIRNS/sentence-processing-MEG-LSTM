
%%% below code no longer needed
% overwrite current patient text file   
% cd ..
% fid = fopen(['CurrentPatient.txt'],'w');
% fprintf(fid,subjectname);  % this does completely rewrite over whatever was in the original file, even if the new text is smaller    
% fclose(fid);
% cd(subjectname)

fname=[savedir filesep 'StimFileList_' subjectname '.txt'];
if exist(fname,'file')
    %StimFileList_fid=fopen(fname,'r+');
    %A=fscanf(StimFileList_fid,'%s');
    
    A=importdata(fname);  % this works better than scanf...     
    StimFileList_fid=fopen(fname,'w');  % this will erase the current file, so we can rewrite the whole thing later   
    
    %rewrite the old Loc blocks...   
    il=1;
    while ~strcmp(A{il},'MainFileList')
        fprintf(StimFileList_fid,[A{il} '\n']);
        il=il+1;
    end
    % add new Loc blocks  
    for ibl=1:length( outfile_Loc )
        fprintf(StimFileList_fid,[outfile_Loc{ibl}(1:end-4) '.csv\n']);
    end
    
    %rewrite the old Main blocks...   
    while ~strcmp(A{il},'JabFileList')
        fprintf(StimFileList_fid,[A{il} '\n']);
        il=il+1;
    end
    % add new Main blocks  
    for ibl=1:length( outfile_Main )
        fprintf(StimFileList_fid,[outfile_Main{ibl}(1:end-4) '.csv\n']);
    end
    
    %rewrite the old Jab blocks...   
    while il <= length(A)
        fprintf(StimFileList_fid,[A{il} '\n']);
        il=il+1;
    end
    % add new Jab blocks  
    for ibl=1:length( outfile_Jab )
        fprintf(StimFileList_fid,[outfile_Jab{ibl}(1:end-4) '.csv\n']);
    end   
else
    StimFileList_fid=fopen(fname,'w');
    fprintf(StimFileList_fid,'LocFileList\n');
    for ibl=1:length( outfile_Loc )
        fprintf(StimFileList_fid,[outfile_Loc{ibl}(1:end-4) '.csv\n']);
    end
    fprintf(StimFileList_fid,'MainFileList\n');
    for ibl=1:length( outfile_Main )
        fprintf(StimFileList_fid,[outfile_Main{ibl}(1:end-4) '.csv\n']);
    end
    fprintf(StimFileList_fid,'JabFileList\n');
    for ibl=1:length( outfile_Jab )
        fprintf(StimFileList_fid,[outfile_Jab{ibl}(1:end-4) '.csv\n']);
    end    
end
fclose(StimFileList_fid);

fname=[savedir filesep  'RestartInfo_' subjectname '.txt'];
if exist(fname,'file')
    % do nothing here
else
    RestartInfo_fid=fopen(fname,'w');
    fprintf(RestartInfo_fid,'NextLocBl=1\n');
    fprintf(RestartInfo_fid,'NextLocTr=1\n');
    fprintf(RestartInfo_fid,'NextMainBl=1\n');
    fprintf(RestartInfo_fid,'NextMainTr=1\n');
    fprintf(RestartInfo_fid,'NextJabBl=1\n');
    fprintf(RestartInfo_fid,'NextJabTr=1\n');
    fclose(RestartInfo_fid);
end

fname=[savedir filesep 'OvSessLog_' subjectname '.txt'];
if exist(fname,'file')
    % do nothing here
else
    OvSessLog_fid=fopen(fname,'w');
    fprintf(OvSessLog_fid,'Each line is one trial, except for lines showing session start and end times.\n');
    fprintf(OvSessLog_fid,'For each trial we record in this order: Date+time of trial completion, StimFile, TrialNum, response, RT (rel to the response screen).\n');
    fclose(OvSessLog_fid);
end


% save a diff csv file for each block below

%%%%%% not sure if it ultimately will be needed, but include it for now
% output the maximum number of words in the first position of the output file
maxNWords=13;
for ibl=1:nBlocksToGen
    for curBlockType=BlockOrder
        switch curBlockType
            case 1
                if ibl <= MaxNMemBlocks
                    curfile=[savedir filesep outfile_Loc{ibl}];                    
                end
            case 2
                curfile=[savedir filesep outfile_Main{ibl}];
            case 3
                curfile=[savedir filesep outfile_Jab{ibl}];
        end
        load(curfile);        
        
        fid = fopen([curfile(1:end-4) '.csv'],'w');
        
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
                for iword = 1:nwords
                    fprintf(fid,',%s',wordlist{isent,inum}{iword});
                end
                fprintf(fid,'\n');
            end
        end
    end
end


