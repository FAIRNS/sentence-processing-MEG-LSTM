function d= ReorderPronoun(d,i)
%%%% Specifically for French and Spanish, move the accusative pronoun relative to the verb

global language;
if language == 2 % French
    if ~isempty(i)
        if d.nchildren{i}>0
            ip = d.children{i}(1); %%% this is the actual node for the pronoun
        else
            ip=i;
        end
        pronoun = d.node{ip};
        labels = d.labels{ip};
        if strcmp(d.terminalword{ip}(1),'#') %%% adjective substitution
            newnode = sprintf('le_%s',d.terminalword{ip});
        else
            newnode = sprintf('%s_PRONOUN_MOV',pronoun);
            d.terminalword{ip} = '#emptypronoun';
        end
        
        parents = FindParents(d,i,[]);
        for k=1:length(parents)
            if strfind(d.node{parents(k)},'_T_P1')  %%% find the parent tense phrase
                tp1 = parents(k);
                break;
            end
            
        end
        if ~isempty( [ FindInChildren(d,tp1,[],'#might') FindInChildren(d,tp1,[],'#should') ])
            for k=1:length(parents)
                if strfind(d.node{parents(k)},'_V_P1')  %%% find the first parent VP1
                    vp1 = parents(k);
                    break;
                end
            end
            childnumber = find( d.children{parents(k+1)} == vp1);
            d=InsertNode(d,parents(k+1),childnumber,newnode,labels);
        else
            tp2=parents(k+1);
            d=InsertNode(d,tp2,2,newnode,labels);
            
            %%%% very special case of French past participle: need to
            %%%% agreement with the pronoun preceding it!
            if ~isempty(intersect(d.labels{tp1},'#perfect'))
                numberlabels = {'$SINGULAR','$PLURAL'};
                genderlabels = {'$MASC','$FEMI'};
                possiblelabels = union(numberlabels,genderlabels);
                %%% begin by removing any existing labels on the past
                %%% participle
                pp = FindInChildren(d,tp1,[],'_V_P0');
                if ~strcmp(d.node{pp},'_BE_V_P0')  %%% "�t�" ne s'accord pas
                    pp = d.children{pp(1)}(1); %% this is the node of the past participle
                    oldlabels = d.labels{pp};
                    newlabels = intersect(oldlabels,setxor(oldlabels,possiblelabels));
                    %% then add the labels of the pronoun
                    newlabels = union(newlabels, intersect(labels,possiblelabels));
                    d.labels{pp} = newlabels;
                    %%% then compute the proper agreement of the past
                    %%% participle
                    currentgender=intersect(newlabels,genderlabels);
                    ii = strmatch(currentgender,genderlabels);
                    if ii==2 % feminine
                        d.terminalword{pp}= [ d.terminalword{pp} 'e' ];
                    end
                    currentnumber=intersect(newlabels,numberlabels);
                    ii = strmatch(currentnumber,numberlabels);
                    if ii==2 % plural
                        d.terminalword{pp}= [ d.terminalword{pp} 's' ];
                    end
                end
            end
        end
    end
end

if language == 4 % Spanish
    if ~isempty(i)
        if d.nchildren{i}>0
            ip = d.children{i}(1); %%% this is the actual node for the pronoun
        else
            ip=i;
        end
        
        %%%% prepare the new node with the pronoun
        pronoun = d.node{ip};
        labels = d.labels{ip};
        if strcmp(d.terminalword{ip}(1),'#') %%% adjective substitution after ser or estar
            newnode = sprintf('lo_%s',d.terminalword{ip});
            newterminal = 'lo';
            flag_NP = 0;  %% it's a substitutive adjective, should go before the verb
        else
            newnode = sprintf('%s_PRONOUN_MOV',pronoun);
            newterminal = pronoun;
            flag_NP = 1;  %% it's a substituted NP, should go after and next to the verb
        end
        
        parents = FindParents(d,i,[]);
        for k=1:length(parents)
            if strfind(d.node{parents(k)},'_T_P1')  %%% find the first parent tense phrase
                tp1 = parents(k);
                break;
            end
        end
        tp2=parents(k+1);
        
        for k=1:length(parents)
            if strfind(d.node{parents(k)},'_V_P1')  %%% find the first parent VP1
                vp1 = parents(k);
                break;
            end
        end
        
        tp0=FindInChildren(d,tp1,[],'_V_P0');
        d.nchildren{tp0} = 1; %%% remove the particle 'a' if present
        verbnode = d.children{tp0};
        verbnode = verbnode(1);
        d.children{tp0} = verbnode; %% leave a single child

        if ~isempty( [ FindInChildren(d,tp1,[],'#might') FindInChildren(d,tp1,[],'#should') ])... %% these tenses require inserting the article after the infinitive verb
                ||  ~isempty(intersect(d.labels{tp1},'#inf'))  %%% this is an infinitive node
            %% dont move the pronoun, but label the verb as requiring fusion with the next pronoun
            
            % be sure to located the verb -- even infinitive can move to
            % TP0 position
            if strcmp(d.terminalword{d.children{tp0}},'#movedverb')
                verbnode = FindInChildren(d,tp1,[],d.node{d.children{tp0}});
                verbnode = verbnode(1);
            end
            d.labels{verbnode} = union(d.labels{verbnode},'#fusenext'); % mark it as requiring fusion with the next work if it is a pronoun (this is performed by function ListTerminals)
            if flag_NP == 0 %% the pronoun substitutes for an adjective, so insert it
                d.terminalword{ip} = newterminal;
                d.terminalnode{ip} = newnode;
            end
        else  %%% the verb has been moved to T_P0, therefore it is not infinitive -- move the pronoun
            d.terminalword{ip} = '#emptypronoun';
            d=InsertNode(d,tp2,2,newnode,labels);
            %%%% remove the 'a' from the verb if present
        end
    end
end

