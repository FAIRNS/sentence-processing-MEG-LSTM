function out = isdigit(input)
%function out = isdigit(input)
%
% Takes in a character, and outputs a one if it is a charater of a digit, 
% i.e. 0 through 9

a=strfind('0123456789',input);
if ~isempty(a)   out=1;
else    out=0;  end