function [Pattern,Counts]=AssignDetPatterns(Counts,NPPattern)

Pattern=zeros(3,1);

tmpType=ChooseFromCounts( Counts );
Counts( tmpType )=Counts( tmpType ) +1;

if length(Counts)==27
    Pattern(1)=mymod(tmpType,3);
    Pattern(2)=mymod(floor( (tmpType-1)/3 )+1,3);
    Pattern(3)=mymod(floor( (tmpType-1)/9 )+1,3);
elseif length(Counts)==9
    Pattern(1)=mymod(tmpType,3);
    if NPPattern==101
        Pattern(3)=mymod(floor( (tmpType-1)/3 )+1,3);
    elseif NPPattern==110
        Pattern(2)=mymod(floor( (tmpType-1)/3 )+1,3);
    end
elseif length(Counts)==8
    if tmpType>4;   Pattern(1)=2;      else    Pattern(1)=1;      end
    if iseven(tmpType);   Pattern(3)=2;      else    Pattern(3)=1;      end
    if ismember(tmpType,[1 2 5 6]);   Pattern(2)=2;      else    Pattern(2)=1;      end
elseif length(Counts)==4
    if tmpType>2;   Pattern(1)=2;      else    Pattern(1)=1;      end
    if NPPattern==101
        if iseven(tmpType);   Pattern(3)=2;      else    Pattern(3)=1;      end
    elseif NPPattern==110
        if iseven(tmpType);   Pattern(2)=2;      else    Pattern(2)=1;      end
    end
end
