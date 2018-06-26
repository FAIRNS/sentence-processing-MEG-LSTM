function [ wordlist nodelist ] = ListTerminals(s,i,wordlist,nodelist,IncEmpties)
%%%% this is a recursively called function that counts the terminal
%%%% node values and labels

if nargin<5 || isempty(IncEmpties)    IncEmpties=false;    end
if nargin<4;    nodelist={};    end
if nargin<3;    wordlist={};    end

global language;

if (s.nchildren{i}==0)
    if IncEmpties
        isterm=~strcmp(s.node{i}(1),'_');   %% definition of a terminal node
    else
        isterm=~strcmp(s.node{i}(1),'_') && ~strcmp(s.terminalword{i}(1),'#');   %% definition of a terminal node
    end
    
    if isterm
        iprev = length(wordlist);
        
        %%% detect if two consecutive words need to be compounded:
        
        compound = false;
        fuseditem = '';
        
        if (iprev>0)
            if (language == 2)
                %%% case of French
                if strcmp(wordlist{iprev}(end),'''') %%% apostrophy in French
                    compound = true;
                end
            end
            
            if (language == 4)
                %%% case of Spanish
                
                %%% check fusion of verb and pronoun in Spanish
                % is the current item a pronoun?
                parents = FindParents(s,i,[]);
                if ~isempty(strfind(s.node{parents(1)},'_PRONOUN_')) || ~isempty(strfind(s.node{parents(1)},'_ADJ_SUB'))
                    %%% is the previous item a verb that requires fusion?
                    prevnode = nodelist{iprev};
                    if ~isempty(intersect(s.labels{prevnode},'#fusenext'))
                        compound = true;
                    end
                end
                
                %%% check for de+el = del , a+el = al
                if strcmp(s.terminalword{i},'el')
                    if strcmp(wordlist{iprev},'de')
                        compound = true;
                        fuseditem = 'del';
                    end
                    if strcmp(wordlist{iprev},'a')
                        compound = true;
                        fuseditem = 'al';
                    end
                end
            end
        end
        
        if compound
            %%%% special case of words with an apostrophy: group them
            if isempty(fuseditem)
                wordlist{iprev} = [wordlist{iprev} s.terminalword{i} ];
            else
                wordlist{iprev} = fuseditem;
            end
            nodelist{iprev} = [ nodelist{iprev} ,  i ] ;
        else
            wordlist{iprev+1} = s.terminalword{i};
            nodelist{iprev+1} = i ;
        end
    end
else
    for inode = s.children{i}
        [ wordlist nodelist] = ListTerminals(s,inode,wordlist,nodelist,IncEmpties);
    end
end