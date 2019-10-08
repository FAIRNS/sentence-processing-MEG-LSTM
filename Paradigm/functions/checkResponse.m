function [feedback_answer,correct_wrong] = checkResponse(correct_response, panel_response,subject_detected_viol)
%CHECKRESPONSE Summary of this function goes here
%   Detailed explanation goes here

if isempty(panel_response) % SUBJECT HASN'T CONFIRMED BY PRESSING ON THE PANEL
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%% DIDNT CONFIRM (DDC) %%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if subject_detected_viol % subject detected a violation but didn't confirm in panel
        if strcmp(correct_response, 'VIOLATION') % Indeed there was a violation
           feedback_answer = '';
           correct_wrong = 'CORRECT_DDC';
        elseif strcmp(correct_response, 'ACCEPTABLE') % But there was no violation
           feedback_answer = '';
           correct_wrong = 'WRONG_DDC';
       end
    else % Nothing was pressed (no detection and no confirmaiton on panel)
        
       if strcmp(correct_response, 'VIOLATION') % Indeed there was a violation
           feedback_answer = '';
           correct_wrong = 'WRONG_DDC';
        elseif strcmp(correct_response, 'ACCEPTABLE') % But there was no violation
           feedback_answer = '';
           correct_wrong = 'CORRECT_DDC';
       end          
    end
else % SOMETHING WAS PRESSED ON DECISION PANEL
    % %%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % PANEL-RESPONSE VIOLATION
    % %%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if strcmp(panel_response, 'VIOLATION')
        if subject_detected_viol % Subject was CONSISTENT
            if strcmp(correct_response, 'VIOLATION') % indeed violation
                feedback_answer = 'Bravo!';
                correct_wrong = 'CORRECT';
            elseif strcmp(correct_response, 'ACCEPTABLE') % there was no violation
               feedback_answer = 'Peccato..';
               correct_wrong = 'WRONG';
            end
        else % Subject was INCONSISTENT (CHANGED HER MIND or slow, or by mistke)
            if strcmp(correct_response, 'VIOLATION') % indeed violation
                feedback_answer = 'Bravo!';
                correct_wrong = 'CORRECT_INC';
            elseif strcmp(correct_response, 'ACCEPTABLE') % there was no violation
               feedback_answer = 'Peccato..';
               correct_wrong = 'WRONG_INC';
            end
        end
    % %%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % PANEL-RESPONSE ACCEPTABLE
    % %%%%%%%%%%%%%%%%%%%%%%%%%%%%
    elseif strcmp(panel_response, 'ACCEPTABLE') 
        if subject_detected_viol % subject was INCONSISTENT (CHANGED HER MIND)
           if strcmp(correct_response, 'VIOLATION') % but there was a violation (!PANEL CHOICE DETERMINES FEEDBACK!)
               feedback_answer = 'Peccato..';
               correct_wrong = 'WRONG_INC';
           elseif strcmp(correct_response, 'ACCEPTABLE') % Indeed, there was no violation
               feedback_answer = 'Bravo!';
               correct_wrong = 'CORRECT_INC';
            end
        else % subject was CONSISTENT and only pressed acceptable
           if strcmp(correct_response, 'VIOLATION') % but there was a violation
               feedback_answer = 'Peccato..';
               correct_wrong = 'WRONG';
            elseif strcmp(correct_response, 'ACCEPTABLE') % Indeed, there was no violation
               feedback_answer = 'Bravo!';
               correct_wrong = 'CORRECT';
            end
        end
    
    end

end

