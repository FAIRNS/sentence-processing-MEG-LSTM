%DefContentWords_Jabber 

ContentWordMatches={'_VT_V_P0','VI_V_P0','_N_P0','_A_P0'}; %'_ADV_P0'  

i=0;
JabberwockyWords_English;
ContentWords={};

for ir=1:length(r)
    if ismember(r{ir}.match,ContentWordMatches)
        ContentWords{end+1}=r{ir}.subst{1};
    end
end
        

