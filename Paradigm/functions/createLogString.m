function log_str = createLogString(varargin)
% create a tab-delimited string from a cell of input vars. 
log_str = '';
for i=1:length(varargin)
   if ~isstring(varargin{i})
       curr_arg_str = num2str(varargin{i});
   else
       curr_arg_str = varargin{i};
   end
   log_str = [log_str, curr_arg_str, '\t'];
end
log_str = [log_str, '\r\n'];
end

