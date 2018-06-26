function [NbOpenNodes, WordList, EmptyTermList]= ComputeSyntacticProperties_NotEmpty_rec(s,i,NbOpenNodes,NbOfRightNodes,WordList,EmptyTermList)

if nargin <  6;         EmptyTermList=[];       end
if nargin <  5;         WordList={};            end
if nargin <  4;         NbOfRightNodes=0;       end
if nargin <  3;         NbOpenNodes=[];         end
if nargin <  2;         i=1;                    end


%%%% this is a recursively called function that compute some properties of
%%%% the syntactic complexity at each word in the sentence:
%%%% NbOpenNodes is the nb of words or treelets that haven't been unified
%%%% yet
%%%% NbNodeClosings is the nb of binary nodes that are being closed after
%%%% each word


if (s.nchildren{i}==0)
    if (~strcmp(s.node{i}(1),'_')) && (~strcmp(s.terminalword{i}(1),'#'))   %% definition of a terminal node
        EmptyTermList(end+1)=false; 
        
        %%% we found a terminal word!
        iprev = length(NbOpenNodes);
        
        compound = false;
        if (iprev>0)
            if strcmp(WordList{iprev}(end),'''')
                compound = true;
            end
        end
        
        if compound
            %%%% special case of words with an apostrophy: group them
            WordList{iprev} = [WordList{iprev} s.terminalword{i} ];

            %nodelist{iprev} = [ nodelist{iprev} ,  i ] ;
            NbOpenNodes(iprev) = NbOfRightNodes +1 ; %%%  store the number of right branches up to that word
            
        else
            WordList{iprev+1} = s.terminalword{i};
            %nodelist{iprev+1} = i ;
            NbOpenNodes(iprev+1) = NbOfRightNodes +1 ; %%%  store the number of right branches up to that word
        end
    else
        % then we have an Empty Term
        EmptyTermList(end+1)=true;        
    end
    
else
    for iinode = 1:s.nchildren{i}
        inode = s.children{i}(iinode);
        if iinode==2
            %%% we are entering a right node
            NbOfRightNodes = NbOfRightNodes +1;
        end
        [ NbOpenNodes, WordList,EmptyTermList] = ComputeSyntacticProperties_NotEmpty_rec(s,inode,NbOpenNodes,NbOfRightNodes,WordList,EmptyTermList);
        if EmptyTermList(end)
            NbOfRightNodes = NbOfRightNodes -1;
        end
    end
end