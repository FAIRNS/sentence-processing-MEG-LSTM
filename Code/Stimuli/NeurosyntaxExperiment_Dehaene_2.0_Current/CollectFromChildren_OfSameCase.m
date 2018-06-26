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
    for inode=1:d.nchildren{i}
        [labels,caseswitches] = CollectFromChildren_OfSameCase(d,d.children{i}(inode),labels,caseswitches,curcaselab);
    end
    
    labels = union(d.labels{i},labels);
else
    caseswitches(end+1)= i;
end
