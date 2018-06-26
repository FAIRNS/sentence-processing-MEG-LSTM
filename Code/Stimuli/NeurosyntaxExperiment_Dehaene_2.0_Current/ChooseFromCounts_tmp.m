function ChosenType=ChooseFromCounts( Counts,TypeFracs )
% note- this procedure will be approximately systematic (beyond the first choice) if a weird value (rather than an eays fraction) for FirstTypeFrac is chosen     

if length(Counts)==1
    ChosenType=1;
    return
end
    
Tol=1e-3;    % bc the adjusted counts might not be 100% eq if FirstTypeFrac is used   
nTypes=length(Counts);

if nargin<2 || isempty( FirstTypeFrac );    FirstTypeFrac=1/nTypes; 
end

RestFrac=(1-FirstTypeFrac)/(nTypes-1);

% divide the count of Counts(1) by the proper ratio, and then choose from there     
Counts(1)=Counts(1)/ ( FirstTypeFrac/RestFrac );     % will be more likely to be chosen if FirstTypeFrac > RestFrac 

Inds= find( abs(Counts-min( Counts ))<Tol );
ChosenType= Inds( randi( length(Inds) ) );
