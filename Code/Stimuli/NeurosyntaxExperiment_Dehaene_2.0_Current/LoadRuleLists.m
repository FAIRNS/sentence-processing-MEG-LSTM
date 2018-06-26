%LoadRuleLists.m

%adjust rules to a numeric array for easier searching for matches later 
nrules = length(r);
rmatchlist=cell(nrules,1);
rlablist=cell(nrules,1);
rwtlist=zeros(nrules,1);
istermword=zeros(nrules,1);
for irule = 1:nrules
    rmatchlist{irule}=r{irule}.match;   
    if isfield( r{irule},'lab' )
        rlablist{irule}=r{irule}.lab;
    else
        rlablist{irule}='';
    end
    rwtlist(irule)=r{irule}.wt;
    
    if ~strcmp(r{irule}.subst{1}(1),'_') && ~strcmp( r{irule}.subst{1},'#empty' ) % Note- this will exclude #empty, but will consider the verb tenses as 'words', for ease of balancing them       
        istermword(irule)=1;  %%% term word rules
    end
end  


