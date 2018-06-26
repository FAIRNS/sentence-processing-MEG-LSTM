function [Type, FromToCounts]= ChooseFromFromToCounts( FromToCounts, Type )

remOpts=1:length(FromToCounts);
remOpts(Type)=[];

curType = ChooseFromCounts( FromToCounts(Type,remOpts) );
FromToCounts( Type,remOpts(curType) )=FromToCounts( Type,remOpts(curType) )+1;
Type=remOpts(curType);
