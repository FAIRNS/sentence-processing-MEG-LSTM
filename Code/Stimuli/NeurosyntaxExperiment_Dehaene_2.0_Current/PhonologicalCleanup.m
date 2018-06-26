function d=PhonologicalCleanup(language,d)

%global language;

[wordseq,nodenumbers] = GenerateWordSequence(d,1,{},{});

if language == 1 % English
    %%%% change 'a' to 'an' if needed
    allk = find(strcmp('a',wordseq));
    for ik = 1:length(allk)
        k=allk(ik);
        if (~isempty(k))&&(k<length(wordseq))
            nextword = wordseq{k+1};
            firstletter = nextword(1);
            if ismember(firstletter,{'a','e','i','o','u'})
                d.terminalword{nodenumbers{k}} = 'an';
            end
        end
    end
end

if language == 2 % French
    %%%% shorten with apostrophy where appropriate
    allk = [];
    allk = [ allk  strmatch('le',wordseq,'exact')' ];
    allk = [ allk  strmatch('la',wordseq,'exact')' ];
    allk = [ allk  strmatch('de',wordseq,'exact')' ];
    for ik = 1:length(allk)
        k=allk(ik);
        if (~isempty(k))&&(k<length(wordseq))
            nextword = wordseq{k+1};
            firstletter = nextword(1);
            if ismember(firstletter,{'a','e','i','o','u','�','�','�','h'})   % 'h' added for the word "homme" in Neurosyntax 2.0 (even though it should not be used in the general sesne with all h words in French)    
                d.terminalword{nodenumbers{k}} = [ d.terminalword{nodenumbers{k}}(1:end-1) '''' ];
            end
        end
    end
end
