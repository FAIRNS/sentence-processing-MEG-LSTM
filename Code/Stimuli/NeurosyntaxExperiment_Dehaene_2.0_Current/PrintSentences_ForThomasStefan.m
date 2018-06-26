% load AggData and Experimental run first

ReparseFlag=1;

icmt=1;
is=10;   % Stanford_subject1 for the file I had loaded         
iw=[1041 280];   %To change block numbers, change iw, but nothing else to: [1 1] [521 200] [1041 280] one for each inum, for block 1 2 or 3, respectively
[EachnOpNpdes,EachnNodeClose]=deal( cell(2,1) ); 
for isent = 1:80
    %PrintReadableSentence(surface{isent});
    %PrintShortenedType(SentInfo(isent).Probe);
    %PrintReadableSentence(shortened{isent});
    
    for inum=1:2
        curStr='';
        curNums=[];
        
        % for getting histograms of nOpNodes and nNodeClose                   
        while iw(inum) <= length(AggData.subj(is).data.SentNum{inum}) && AggData.subj(is).data.SentNum{inum}(iw(inum))==isent
            if ~isempty(curStr)    curStr=[curStr ' '];     end
            curStr=[curStr AggData.subj(is).data.word{inum}{iw(inum)}];
            if ReparseFlag
                curNums=[curNums AggData.subj(is).data.NbOpenNodes_Reparse{icmt,inum}(iw(inum))];
                
                EachnOpNpdes{inum}=[EachnOpNpdes{inum}; AggData.subj(is).data.NbOpenNodes_Reparse{icmt,inum}(iw(inum))];
                
                EachnNodeClose{inum}=[EachnNodeClose{inum}; AggData.subj(is).data.NbNodeClosings_Reparse{icmt,inum}(iw(inum))];
            else
                curNums=[curNums AggData.subj(is).data.NbOpenNodes_NoEmpty{icmt,inum}(iw(inum))];
                
                EachnOpNpdes{inum}=[EachnOpNpdes{inum}; AggData.subj(is).data.NbOpenNodes_NoEmpty{icmt,inum}(iw(inum))];
                
                EachnNodeClose{inum}=[EachnNodeClose{inum}; AggData.subj(is).data.NbNodeClosings_NoEmpty{icmt,inum}(iw(inum))];
            end
            iw(inum)=iw(inum)+1;
        end
        disp(curStr)
        disp(num2str(curNums))
    end                         
            
    disp('************************************');
end

return

MainPrb={'Main','Probe'};
TypeStrs={'nOpNodes','nNodesClosing'};
figure
for inum=1:2
    for iType=1:2
        subplot(2,2,iType+(inum-1)*2)
        if iType==1
            myHist(EachnOpNpdes{inum},[],[],[],1)
        else
            myHist(EachnNodeClose{inum},[],[],[],1)
        end
        title([MainPrb{inum} TypeStrs{iType}])
    end
end

 