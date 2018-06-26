function ChosenType=ChooseFromCounts( Counts,TypeFracs )
% note- this procedure will be approximately systematic (beyond the first choice) if a weird value (rather than an eays fraction) for FirstTypeFrac is chosen     

nTypes=length(Counts);
if nTypes==1
    ChosenType=1;
    return
end
    
Tol=1e-3;    % bc the adjusted counts might not be 100% eq if FirstTypeFrac is used   

if nargin<2 || isempty( TypeFracs );    TypeFracs=1/nTypes*ones(nTypes,1); 
end

if length(TypeFracs) <= nTypes
    RemFrac=1-sum(TypeFracs);
    nLeftTypes= nTypes - length(TypeFracs);
    TypeFracs(end+1:end+nLeftTypes)=RemFrac/nLeftTypes;
end

% make sure both are col vectors
[nr, nc]=size(Counts);
if nc>nr;   Counts=Counts';     end
[nr, nc]=size(TypeFracs);
if nc>nr;   TypeFracs=TypeFracs';     end

% divide Counts(1) by the Corresponding TypeFrac, and then choose from there     
Counts=Counts ./ ( TypeFracs );     % will be more likely to be chosen if FirstTypeFrac > RestFrac 

Inds= find( abs(Counts-min( Counts ))<Tol );
ChosenType= Inds( randi( length(Inds) ) );
