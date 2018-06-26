DefGrammCats

nGrammCats=length(GrammCats);
TermWord.List={};
TypeCounts_Orig=zeros(1,nGrammCats);
for isent=1:nsentences
    nwords = length(wordlist{isent,1});
    for iword=1:nwords
        [tf,ind]=ismember( wordlist{isent,1}{iword},TermWord.List );
        if ~tf            
            ind=length( TermWord.List )+1;
            
            TermWord.List{ind}=wordlist{isent,1}{iword};                        
            parents=FindParents( surface{isent},nodelist{isent,1}{iword} );            
            TermWord.FirstParent{ind}=surface{isent}.node{parents(1)};
            TermWord.FirstParentType(ind)=find(strcmp(TermWord.FirstParent{ind},GrammCats));
        end
                        
        TypeCounts_Orig( TermWord.FirstParentType(ind) )=TypeCounts_Orig( TermWord.FirstParentType(ind) )+1;
    end
end
        
TypeCounts_Orig
totnwords=sum(TypeCounts_Orig)


% Disp the nExtraWords in each NP and VP   
Count.AllnWords=zeros(4,4);     % rows correpsonds to 0, 1, 2, and 3 extra words... column corresponds to the respective NP or VP    
for isent=1:nsentences
    for iP=1:4
        if ~isempty(SentInfo(isent).AllnWords{iP})
            curval=SentInfo(isent).AllnWords{iP};
            Count.AllnWords( curval+1,iP )=Count.AllnWords( curval+1,iP )+1;
        end
    end
end
            
Count.AllnWords            