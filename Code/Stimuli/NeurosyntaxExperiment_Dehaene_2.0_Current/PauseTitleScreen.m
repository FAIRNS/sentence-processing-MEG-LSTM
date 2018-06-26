%function PauseTitleScreen

GoodJobScreen
Screen(window,'Flip',window);
WaitSecs(1);

curTit='Take a break between tasks...';
DrawFormattedText(window, curTit, 'center','center',blue,wrapat,[],[],vSpacing);
Screen(window,'Flip',window);

WaitSecs(1.5);

DrawFormattedText(window, curTit, 'center','center',blue,wrapat,[],[],vSpacing);
DrawPressEnter2
Screen(window,'Flip');

WaitForEnter
