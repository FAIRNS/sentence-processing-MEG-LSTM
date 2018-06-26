function d=AgreementNounAdjDet(language,d)

LoadLexicon;

%%%% PLURAL OF NOUNS
possiblelabels = {'$SINGULAR','$PLURAL'};
for i=FindInChildren(d,1,[],'_N_P0')
    i=i(1);
    b=d.children{i}(1); %%% this is the noun
    singularform = d.node{b};
    
    currentnumber=intersect(possiblelabels,d.labels{b});
    numberindex = strmatch(currentnumber,possiblelabels);
    
    % specific to English?...    
    if numberindex==2 % plural        
        if ismember( d.node{b}(end),{'s','x'} ) || ismember( d.node{b}(end-1:end),{'sh','ch'} )
            d.terminalword{b}= [ singularform, 'es' ];
        elseif ismember(singularform,plurals{1})            
            d.terminalword{b} = plurals{2}{ strcmp( singularform,plurals{1} ) };
        else
            d.terminalword{b}= [ singularform, 's' ];
        end
    end
end

%%%% AGREEMENT OF ADJECTIVE
if language == 2 %% French
    for i=FindInChildren(d,1,[],'_A_P0')
        i=i(1);
        b=d.children{i}(1); %%% this is the adjective

        singularform = d.terminalword{b};
        possiblelabels = {'$MASC','$FEMI'};
        currentnumber=intersect(possiblelabels,d.labels{b});
        numberindex = strmatch(currentnumber,possiblelabels);
        if numberindex==2 % feminine
            iadj = strmatch(singularform,feminine{1});
            if ~isempty(iadj)
                d.terminalword{b} = feminine{2}{iadj};
            else
                d.terminalword{b}= [ singularform, 'e' ];
            end
        end
        
        singularform = d.terminalword{b};
        possiblelabels = {'$SINGULAR','$PLURAL'};
        currentnumber=intersect(possiblelabels,d.labels{b});
        numberindex = strmatch(currentnumber,possiblelabels);
        if numberindex==2 % plural
            iadj = strmatch(singularform,plurals{1});
            if ~isempty(iadj)
                d.terminalword{b} = plurals{2}{iadj};
            else
                d.terminalword{b}= [ singularform, 's' ];
            end
        end
    end
end

if language == 4 %% Spanish
    for i=FindInChildren(d,1,[],'_A_P0')
        i=i(1);
        b=d.children{i}(1); %%% this is the adjective

        singularform = d.terminalword{b};
        possiblelabels = {'$MASC','$FEMI'};
        currentnumber=intersect(possiblelabels,d.labels{b});
        numberindex = strmatch(currentnumber,possiblelabels);
        if numberindex==2 % feminine
            iadj = strmatch(singularform,feminine{1});
            if ~isempty(iadj)
                d.terminalword{b} = feminine{2}{iadj};
            else
                if strcmp(singularform(end),'o')
                    d.terminalword{b}= [ singularform(1:end-1), 'a' ];
                else
                    d.terminalword{b}= singularform;
                end
            end
        end
        
        singularform = d.terminalword{b};
        possiblelabels = {'$SINGULAR','$PLURAL'};
        currentnumber=intersect(possiblelabels,d.labels{b});
        numberindex = strmatch(currentnumber,possiblelabels);
        if numberindex==2 % plural
            iadj = strmatch(singularform,plurals{1});
            if ~isempty(iadj)
                d.terminalword{b} = plurals{2}{iadj};
            else
                d.terminalword{b}= [ singularform, 's' ];
            end
        end
    end
end

%%%% ENFORCING GENDER AGREEMENT OF DETERMINER AND NUMERALS 
if (language == 2)||(language==4) %% French or Spanish
    tmplist=[ FindInChildren(d,1,[],'_DET') FindInChildren(d,1,[],'_D_P0') ];
    if language==4 % MJN: in French numerals (except 'un'   ) don't change based on gender or plural/singular
        tmplis=[tmplist FindInChildren(d,1,[],'_NUM') ];
    end        
    for i= tmplist
        i=i(1);
        if strcmp(d.node{i},'_NUM_D_P0')
            continue
        end
        
        if d.nchildren{i}>0
            b=d.children{i}(1); %%% this is the determiner
        else
            b=i;
        end
        singularform = d.terminalword{b};
        
        possiblelabels = {'$SINGULAR','$PLURAL'};
        currentnumber=intersect(possiblelabels,d.labels{b});
        numberindex = strmatch(currentnumber,possiblelabels);
        if numberindex==2 % plural
            iadj = strmatch(singularform,plurals{1});
            if ~isempty(iadj)
                d.terminalword{b} = plurals{2}{iadj};
            else
                d.terminalword{b}= [ singularform, 's' ];
            end
        end
        
        singularform = d.terminalword{b};
        possiblelabels = {'$MASC','$FEMI'};
        currentnumber=intersect(possiblelabels,d.labels{b});
        numberindex = strmatch(currentnumber,possiblelabels);
        if numberindex==2 % feminine
            iadj = strmatch(singularform,feminine{1});
            if ~isempty(iadj)
                d.terminalword{b} = feminine{2}{iadj};
            else
%                d.terminalword{b}= [ singularform, 'e' ];
            end
        end
    end
end

