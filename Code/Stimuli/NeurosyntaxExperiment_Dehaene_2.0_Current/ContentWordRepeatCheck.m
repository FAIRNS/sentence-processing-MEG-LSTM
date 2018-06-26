function repeat=ContentWordRepeatCheck( language,d1,d2,d3,JabberFlag )

if nargin<5 || isempty(JabberFlag);     JabberFlag=0;       end
if nargin<4      d3=[];       end

if JabberFlag
    DefContentWords_Jabber;
else
    DefContentWords;
end

[term1, nlist1]=ListTerminals(d1,1,{},{});    
[term2, nlist2]=ListTerminals(d2,1,{},{});    

cw1=intersect( ContentWords,term1 );
cw2=intersect( ContentWords,term2 );

repeat=true;
if isempty(intersect(cw1,cw2))
    if ~isempty(d3)
        %check for s3 copmatibility if it was input
        term3=ListTerminals(d3,1,{},{}); 
        cw3=intersect( ContentWords,term3 );
        if isempty(intersect(cw1,cw3))
            repeat=false;
        end
    else
        repeat=false;
    end
end

