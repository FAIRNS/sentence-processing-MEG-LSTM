% SetLexSwitchTargs.m

DefContentCatList
if ProbeElideAdv
    ContentCatList( strcmp(ContentCatList,'_ADV_P0') )=[];
end

nCat=length(ContentCatList);
CatMatches=cell( nCat,1 );
for ir=1:length(r)
    [ia, iCat]=ismember( r{ir}.match,ContentCatList );        
      
    if ~strcmp( r{ir}.match,'_NUM' ) %it dn make sense, but matlab seems not to like the output when '_NUM' is input into ismember    
        if ia        
            % the below fixes the artificial introduction of _EMOTION_A_P0 and _PHYSICAL_A_P0 types needed t be introduced for French, and considers them all to be just adjectives for this purpose      
            if ismember(ContentCatList{iCat},{'_EMOTION_A_P0','_PHYSICAL_A_P0'});        iCat=3;     end     
            
            CatMatches{iCat}(end+1)=ir;
        elseif strcmp( r{ir}.match(end-4:end),ContentCatList{2} );     % check for verbmatch, which is different
            CatMatches{2}(end+1)=ir;
        end
    end
end

for iCat=1:nCat
    for im=1:length( CatMatches{iCat} )
        cur_addi=r{ CatMatches{iCat}(im) }.addi{1};
        r{ CatMatches{iCat}(im) }.LexSwitchTargs=[];
        for iim=1:length( CatMatches{iCat} )
            if iim~=im
                switch iCat
                    case {1,3}  % nouns and adj  
                        if LexSwitchAcrossMajorCat      % then we can choose anything that dn exactly match
                            if ~isequal( cur_addi,r{ CatMatches{iCat}(iim) }.addi{1} )
                                r{ CatMatches{iCat}(im) }.LexSwitchTargs(end+1)= CatMatches{iCat}(iim);
                            end
                        else        % then we want to only chose items off by one dimension in addi
                            if sum( strcmp( cur_addi,r{ CatMatches{iCat}(iim) }.addi{1} ) )==1
                                r{ CatMatches{iCat}(im) }.LexSwitchTargs(end+1)= CatMatches{iCat}(iim);
                            end                            
                        end
                    case 2      % verbs   
                        if LexSwitchAcrossMajorCat      % then we can choose anything that dn exactly match... while keeping the major clas sof transitive vs intransitive the same
                            if strcmp( r{ CatMatches{iCat}(im) }.match,r{ CatMatches{iCat}(iim) }.match ) && ~isequal( cur_addi,r{ CatMatches{iCat}(iim) }.addi{1} )
                                r{ CatMatches{iCat}(im) }.LexSwitchTargs(end+1)= CatMatches{iCat}(iim);
                            end
                        else        % then we want to only chose items off by one dimension in addi
                            if length( cur_addi )==2 % need to process the inanimate_subj inanimate_obj nouns differently   
                                if all(strcmp( r{ CatMatches{iCat}(iim) }.addi{1}(1:2),{'$INANIMATE_SUB','$ANIMATE_OBJ'} ))
                                    r{ CatMatches{iCat}(im) }.LexSwitchTargs(end+1)= CatMatches{iCat}(iim);
                                end
                            elseif all(strcmp( cur_addi(1:2),r{ CatMatches{iCat}(iim) }.addi{1}(1:2) )) && length( r{ CatMatches{iCat}(iim) }.addi{1} )==3 && ~strcmp( cur_addi(3),r{ CatMatches{iCat}(iim) }.addi{1}(3) )      
                                r{ CatMatches{iCat}(im) }.LexSwitchTargs(end+1)= CatMatches{iCat}(iim);
                            end                            
                        end                                                                        
                    case 4      % adverbs
                        if ~strcmp( cur_addi,r{ CatMatches{iCat}(iim) }.addi{1} )
                            r{ CatMatches{iCat}(im) }.LexSwitchTargs(end+1)= CatMatches{iCat}(iim);
                        end
                end
            end
        end
    end
end

