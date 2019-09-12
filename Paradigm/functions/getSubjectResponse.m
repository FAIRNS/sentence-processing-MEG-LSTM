function [key_press_name, key_press_time] = getSubjectResponse(handles, start_time, duration)
    key_press_time = start_time +  duration; % set to maximal time in case no key is pressed later
    key_press_name = ''; % Set to empty string if no key is pressed.
    
    % participant responds now:
     while (GetSecs <= start_time + duration)
         [pressed,~,key_code] = KbCheck;
         if pressed
             if ~isempty(key_code(handles.Key)) % RIGHT
                 key_press_time = GetSecs;
                 key_press_name = 'SPACE';
             elseif ~isempty(key_code(handles.escapeKey))
                 error('ESCAPE key was pressed')
             end
             break
         end
     end
end