function cc=CountTrueTerminals(s,i);

[ wordlist nodelist ] = ListTerminals(s,i,{},{});

cc= length(wordlist);

%
% function cc=CountTrueTerminals(s,i)
% %%%% this is a recursively called function
%
% if (s.nchildren{i}==0)
%     if (~strcmp(s.node{i}(1),'_'))  && (~strcmp(s.terminalword{i}(1),'#'))
%         %% definition of a true terminal node
%         cc = 1;
%     else
%         cc = 0;
%     end
% else
%    cc = 0;
%    for inode = s.children{i}
%        cc = cc + CountTrueTerminals(s,inode);
%    end
% end
