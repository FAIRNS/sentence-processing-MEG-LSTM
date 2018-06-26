% CalcBigTermWordList.m    

DefGrammCats
nGrammCats=length(GrammCats);

AllLen=cellfun('length',wordlist);
ntotwords=sum(AllLen(:,1),1);

TermWord.OrigList_Inds=zeros(ntotwords,1);
TermWord.OrigList_Types=zeros(ntotwords,1);
TermWord.List={};
TermWord.Count=[];
TermWord.FirstParent={};
TermWord.FirstParentType=[];
TermWord.Root={};
itotw=0;
TypeCounts_Orig=zeros(1,nGrammCats);
for isent=1:nsentences
    nwords = length(wordlist{isent,1});
    for iword=1:nwords        
        itotw=itotw+1;

        rootlist{isent,1}{iword}=surface{isent}.node{ nodelist{isent,1}{iword} };
        [tf,ind]=ismember( wordlist{isent,1}{iword},TermWord.List );
        if tf
            TermWord.Count(ind)=TermWord.Count(ind)+1;
        else
            ind=length( TermWord.List )+1;
            
            TermWord.List{ind}=wordlist{isent,1}{iword};            
            parents=FindParents( surface{isent},nodelist{isent,1}{iword} );            
            TermWord.FirstParent{ind}=surface{isent}.node{parents(1)};
            TermWord.FirstParentType(ind)=find(strcmp(TermWord.FirstParent{ind},GrammCats));
            TermWord.Count(ind)=1;
            TermWord.Root{ind}=surface{isent}.node{ nodelist{isent,1}{iword} }; 
            if ismember(TermWord.Root{ind},DemonRootAdjust)
                TermWord.Root{ind}='this';
            end
        end

        TermWord.OrigList_Inds(itotw)=ind; % store all the overall inds: useful when chosing a word for the diff struc trials     
        TermWord.OrigList_Types(itotw)= TermWord.FirstParentType(ind);
        TypeCounts_Orig( TermWord.FirstParentType(ind) )=TypeCounts_Orig( TermWord.FirstParentType(ind) )+1;
    end
end

ntw=length(TermWord.Count);
TermWord.CommonRootInds=cell(ntw,1);
for itw=1:ntw
    TermWord.CommonRootInds{itw}= find(strcmp( TermWord.Root{itw},TermWord.Root ));    
end