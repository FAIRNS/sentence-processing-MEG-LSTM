function counts = DistCounts(n,nTypes,FirstTypeFrac)

if nargin<3 || isempty( FirstTypeFrac );    FirstTypeFrac=1/nTypes; 
end

nPerT=floor(n/nTypes);

counts=nPerT*ones(nTypes,1);
rem=n-sum(counts);

tmplist=randperm(nTypes);
counts(tmplist(1:rem))=counts(tmplist(1:rem))+1;
