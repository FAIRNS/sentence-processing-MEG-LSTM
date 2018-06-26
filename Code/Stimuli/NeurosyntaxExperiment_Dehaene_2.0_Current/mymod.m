function out=mymod(A,B)
% function out=mymod(A,B)
%
% same as mod, but if mod(A,B)==0, then it outputs B instead of 0.

out=mod(A-1,B)+1;