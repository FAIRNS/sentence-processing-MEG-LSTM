clear r
i=0;
JabberwockyWords_English;
Jr=r;
i=0;
ContentWords_English;

nr=length(r);
MatchList=cell(nr,1);
for ir=1:nr
    MatchList{ir}=r{ir}.subst;
end

for isent=1:nsentences
    inum=1;
    for iw=1:length(wordlist{isent,inum})
        % find matching English rule for all content words
        iw=3;
        
        curr=find( strcmp(MatchList,deepstructure{isent}.node{ nodelist{isent,1}{iw} }) )
        
                    
        
    end
    
    surface{isent} = DeepToSurface(language,deepstructure{isent});
end