function ChosenType=ChooseFromRemCounts( RemCounts )

Inds= find( RemCounts==max( RemCounts ) );
ChosenType= Inds( randi( length(Inds) ) );