%DefContentWords   

ContentWordMatches={'_VT_V_P0','VI_V_P0','_N_P0','_A_P0'}; %'_ADV_P0'  .....

LoadRules
ContentWords={};

for ir=1:length(r)
    if ismember(r{ir}.match,ContentWordMatches)
        ContentWords{end+1}=r{ir}.subst{1};
    end
end
        

