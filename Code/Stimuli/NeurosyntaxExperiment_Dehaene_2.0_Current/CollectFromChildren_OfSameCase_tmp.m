function [labels,caseswitches] = CollectFromChildren_OfSameCase(d,i,labels,caseswitches,curcaselab)
%%% collect the labels from all the children until the case changes
%
% call without the curcaselab to use the case of the given node being input here...
%
% Also records the nodes when the case changes

DefCaseList     %sets the pre-dfined variable CaseList   
if nargin<3
    labels={};  %should only occur the first time through (potentially)
end
if nargin<4
    caseswitches=[];  %should only occur the first time through (potentially)
end
if nargin<5     
    curcaselab=intersect(CaseList,d.labels{i});     %should only occur the first time through (potentially)       
end
tmpcaselab=intersect(CaseList,d.labels{i});

if (isempty(curcaselab) && isempty(tmpcaselab)) || isequal( curcaselab,tmpcaselab )     % statement to decide blocking of propagation...   
    if i==67
        disp('stop')
    end
    
    for inode=1:d.nchildren{i}
        [labels,caseswitches] = CollectFromChildren_OfSameCase(d,d.children{i}(inode),labels,caseswitches,curcaselab);
    end
    
    % merge children and parent labels, having the children labels override if there are any conflicts       
    LoadLabConflicts
    nConf=size(LabConflicts,1);
    ToRem=[];
    
    if i==67
        disp('stop')
    end
    
    tmplabels = union(d.labels{i},labels);
    for il=1:length(tmplabels)
        [im,Ind]= ismember( tmplabels{il},LabConflicts );
        if im      
            ConfInd=mymod( Ind+nConf,nConf*2 );     % mymod( ind+nConf,nConf*2 ) gives the ind for the matching conflict label    
            if ismember( LabConflicts{ ConfInd },tmplabels ) 
                %conflict detected! Keep the one form the children, which is in labels    
                if ismember( LabConflicts{ ConfInd },labels )
                    % then remove Ind
                    ToRem=unique([ToRem il]);
                else
                    % then remove ConfInd
                    ToRem=unique([ToRem find(strcmp( LabConflicts{ ConfInd },tmplabels ))]);
                end
            end
        end
    end
    
    tmplabels(ToRem)=[];
    labels=tmplabels;
else
    caseswitches(end+1)= i;
end
