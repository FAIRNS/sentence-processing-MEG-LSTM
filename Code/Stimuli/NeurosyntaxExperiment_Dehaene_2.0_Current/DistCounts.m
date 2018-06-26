function counts = DistCounts(n,nTypes,TypeFracs)

if nargin<3 || isempty( TypeFracs );    TypeFracs=1/nTypes*ones(nTypes,1);  
end

if length(TypeFracs) <= nTypes
    RemFrac=1-sum(TypeFracs);
    nLeftTypes= nTypes - length(TypeFracs);
    TypeFracs(end+1:end+nLeftTypes)=RemFrac/nLeftTypes;
end

counts=floor(n*TypeFracs);
rem=counts-floor(n*TypeFracs);

remn=n-sum(counts);

for irem=1:remn
    maxCountInds= find( rem==max(rem) );    
    maxCountInds=maxCountInds( randi(length(maxCountInds)) );
    counts(maxCountInds)=counts(maxCountInds)+1;
    rem(maxCountInds)=0; 
end
    
    
    