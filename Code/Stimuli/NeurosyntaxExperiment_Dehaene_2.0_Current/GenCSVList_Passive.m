
%%% below code no longer needed
% overwrite current patient text file   
% cd ..
% fid = fopen(['CurrentPatient.txt'],'w');
% fprintf(fid,subjectname);  % this does completely rewrite over whatever was in the original file, even if the new text is smaller    
% fclose(fid);
% cd(subjectname)

fname=[savedir filesep 'StimFileList_' subjectname '.txt'];
StimFileList_fid=fopen(fname,'w');
fprintf(StimFileList_fid,'LocFileList\n');
for ibl=1:length( outfile_Loc )
    fprintf(StimFileList_fid,[outfile_Loc{ibl}(1:end-4) '.csv\n']);
end
fprintf(StimFileList_fid,'MainJabFileList\n');
for ibl=1:length( outfile_Main )
    pos=strfind(outfile_Main{ibl},'Main');
    outfile_MainJab{ibl}=[outfile_Main{ibl}(1:pos+3) 'Jab' outfile_Main{ibl}(pos+4:end)];
    fprintf(StimFileList_fid,[outfile_MainJab{ibl}(1:end-4) '.csv\n']);
    fprintf(StimFileList_fid,[outfile_MainJab{ibl}(1:end-4) '_2.csv\n']);
end
fclose(StimFileList_fid);

fname=[savedir filesep  'RestartInfo_' subjectname '.txt'];
if exist(fname,'file')
    % do nothing here
else
    RestartInfo_fid=fopen(fname,'w');
    fprintf(RestartInfo_fid,'NextLocBl=1\n');
    fprintf(RestartInfo_fid,'NextLocTr=1\n');
    fprintf(RestartInfo_fid,'NextMainJabBl=1\n');
    fprintf(RestartInfo_fid,'NextMainJabTr=1\n');
    fclose(RestartInfo_fid);
end

fname=[savedir filesep 'OvSessLog_' subjectname '.txt'];
if exist(fname,'file')
    % do nothing here
else
    OvSessLog_fid=fopen(fname,'w');
    fprintf(OvSessLog_fid,'Each line is one trial, except for lines showing session start and end times.\n');
    fprintf(OvSessLog_fid,'For each trial we record in this order: Date+time of trial completion, StimFile, TrialNum, PressTrFlag, Response.\n');
    fclose(OvSessLog_fid);
end


% save a diff csv file for each block below

%%%%%% not sure if it ultimately will be needed, but include it for now
% output the maximum number of words in the first position of the output file
maxNWords=13;
for ibl=1:nBlocksToGen
    for curBlockType=1:2
        switch curBlockType
            case 1
                if ibl <= MaxNMemBlocks
                    curfile=[savedir filesep outfile_Loc{ibl}];
                    
                    load(curfile);
                    fid = fopen([curfile(1:end-4) '.csv'],'w');

                    GenCSV_From_wordlist
                end
            case 2
                curfile=[savedir filesep outfile_Jab{ibl}];
                load(curfile);
                wordlistJab=wordlist;
                
                curfile=[savedir filesep outfile_Main{ibl}];
                load(curfile);
                wordlistMain=wordlist;

                % now mix the two wordlists into a final wordlist, and then we're good      
                for ibl2=1:2  
                    inds=randperm(40)';                                      
                    
                    curfile=[savedir filesep outfile_MainJab{ibl}];
                    if ibl2==1
                        fid = fopen([curfile(1:end-4) '.csv'],'w');
                    else
                        fid = fopen([curfile(1:end-4) '_2.csv'],'w');
                    end
                    
                    wordlist(inds<=nsentences/2,:)=wordlistMain(1+nsentences/2*(ibl2==2) : nsentences/2*ibl2,:);
                    wordlist(inds>nsentences/2,:)=wordlistJab(1+nsentences/2*(ibl2==2) : nsentences/2*ibl2,:);
                    
                    GenCSV_From_wordlist
                end
        end               
    end
end


