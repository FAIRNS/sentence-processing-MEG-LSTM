function curCase=CalcCurCase(labels)

if ismember( '$NOMINATIVE',labels );       curCase=1;
elseif ismember( '$ACCUSATIVE',labels );       curCase=2;
elseif ismember( '$LOCATIVE',labels );       curCase=3;
else curCase=0;
end