function [d, ProbeFromToCounts]=SubsNode(language,d,inode,SubsType,curCase, SwitchInfo, r, ProbeFromToCounts)

if nargin<5 || isempty(curCase);    curCase=0;      end

totnode=length(d.node);

% create first child, a node of 'SubType'
totnode=totnode+1;
if curCase==3 && strcmp('_PRONOUN_SUB',SubsType)
    SubsType='_Elided';     % locative: elide the PP    
end

if ismember(SubsType,{'_T_P0','Lex_Switch'})
    CreateSecondChild=0;    % for these substitutions we don't want to create an intermediate node      
    if strcmp(SubsType,'Lex_Switch')
        oldstem=d.node{ d.children{inode} };        % node should have the stem in it...    
    end
else
    CreateSecondChild=1;    
end

% change where this current node is pointing to   
oldchildren=d.children{inode};
d.children{inode}=totnode;
d.nchildren{inode}=1;
d.labels{totnode}=d.labels{inode};

%disp( ['Redirecting node: ' num2str(inode)] )   

if CreateSecondChild
    d.node{totnode}=SubsType;
    
    % create second child
    totnode=totnode+1;

    d.children{totnode-1}=totnode;
    d.nchildren{totnode-1}=1;

    % copy labels 
    d.labels{totnode}=d.labels{inode};
end

% the last new node is terminal
d.nchildren{totnode}=0;

%Subs for the new terminal node
switch SubsType
    case '_Elided'
        d.node{totnode}='#empty';
    case '_PRONOUN_SUB'
        LoadLexicon
        
        % Get Sing Or Plur
        [~,SingOrPlur]=intersect(LexList.SingPlur,d.labels{inode});
        
        % find gender
        [~,GenType]=intersect(LexList.Gender,d.labels{inode});
        
        if SwitchInfo.Switch && SwitchInfo.GrammOrLex==1    % make a grammatical switch      
            switch SwitchInfo.GrammSwitchType
                case 1      % gender
                    if isfield(ProbeFromToCounts,'Gender')
                        % AllowAnimacySwitch must be turned on   
                        % chose from the specific items from ProbeFromToCounts     
                        [GenType, ProbeFromToCounts.Gender]= ChooseFromFromToCounts( ProbeFromToCounts.Gender, GenType );
                    else
                        % AllowAnimacySwitch must be turned off... so we can just flip between Masc or Fem   
                        GenType=mymod( GenType+1,2 );                                                
                    end                        
                case 2      % number
                    SingOrPlur=mymod( SingOrPlur+1,2 );     % flip between SingOrPlur                                        
            end
        end
                
        d.node{totnode}=pronouns{curCase}{SingOrPlur}{GenType};
                
        d.labels{totnode}= AddLabClearConflicts( d.labels{totnode},{LexList.Gender{GenType}; LexList.SingPlur{SingOrPlur}} );        
        
        % need to adjust the number for the verb if we changed the subject's number
        if SwitchInfo.Switch && SwitchInfo.GrammOrLex==1 && SwitchInfo.GrammSwitchType==2 && curCase==1 
            b=FindInChildren(d,1,[],'_V_P0');
            b=d.children{b(1)}(1); %%% this is the infinitive form of the verb
            d.labels{b}= AddLabClearConflicts( d.labels{b},{ LexList.SingPlur{SingOrPlur} } );
        end
    case '_T_P0'
        DefTenseList
        
        %get current tense and choose new tense
        [~,Tense]=intersect( TenseList,d.labels{inode} );
        [Tense, ProbeFromToCounts.Tense]= ChooseFromFromToCounts( ProbeFromToCounts.Tense, Tense );
        
        d.node{totnode}=TenseList{ Tense };
        
        d=ReplaceTenseLabs( d,1,TenseList{ Tense } );   
    case 'Lex_Switch'
        % find the rulenumber corresponding to oldstem   
        % start searching from the last rule bc the terminal words are the last rules   
        nr=length(r);
        for ir=nr:-1:1            
            if strcmp( r{ir}.match,d.node{inode} ) && strcmp( r{ir}.subst{1},oldstem ) && all( ismember(r{ir}.addi{1},d.labels{oldchildren}) ) %  the last part of the statement is needed because presently appear shows up twice in the word list                   
                newr=r{ir}.LexSwitchTargs( randi(length(r{ir}.LexSwitchTargs)) );                
                d.node{totnode}=r{newr}.subst{1};
                d.labels{totnode}=unique([r{newr}.addi{1}'; d.labels{inode}(:)]);                                    
                break
            end
        end        
end
d.terminalword{totnode}=d.node{totnode};


