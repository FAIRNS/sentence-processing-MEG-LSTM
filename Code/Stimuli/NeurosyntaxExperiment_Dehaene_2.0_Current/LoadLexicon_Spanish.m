%%%%% additional knowledge of conjugation
past = {
    { 'dormir'   ,'cantar'  ,'llorar',  'gritar'  ,'trabajar'  ,'atacar'  ,'encontrar'  ,'besar'  ,'golpear'  ,'ayudar'  ,'disfrutar'  ,'preferir,'  ,'odiar'  ,'querer'   ,'ser','estar'},
    { 'durmi�'   ,'cant�'   ,'llor�'   ,'grit�'   ,'trabaj�'   ,'atac�'   ,'encontr�'   ,'bes�'   ,'golpe�'   ,'ayud�'   ,'disfrut�'   ,'prefiri�'   ,'odi�'   ,'quiso'    ,'fue','estuvo'},
    { 'durmieron','cantaron','lloraron','gritaron','trabajaron','atacaron','encontraron','besaron','golpearon','ayudaron','disfrutaron','prefirieron','odiaron','quisieron','fueron','estuvieron'}
    };

present = {
    { 'dormir' ,'cantar','llorar','gritar','trabajar','atacar','encontrar','besar','golpear','ayudar','disfrutar','preferir,','odiar','querer','ser','estar'},
    {'duerme' ,'canta','llora','grita','trabaja','ataca','encuentra','besa','golpea','ayuda','disfruta','prefiere','odia','quiere' ,'es','est�'}, % el/ ella
    {'duermen' ,'cantan','lloran','gritan','trabajan','atacan','encuentran','besan','golpean','ayudan','disfrutan','prefieren','odian','quieren','son','est�n'}  % ellos/ellas 
    };

future = {
    { 'dormir' ,'cantar','llorar','gritar','trabajar','atacar','encontrar','besar','golpear','ayudar','disfrutar','preferir,','odiar','querer','ser','estar'},
    {'dormir�','cantar�','llorar�','gritar�','trabajar�','atacar�','encontrar�','besar�','golpear�','ayudar�','disfutar�','preferir�','odiar�','querr�','ser�','estar�'},
    {'dormir�n','cantar�n','llorar�n','gritar�n','trabajar�n','atacar�n','encontrar�n','besar�n','golpear�n','ayudar�n','disfrutar�n','preferir�n','odiar�n','querr�n','ser�n','estar�n' }
    };

%pastparticiple = {
%    { 'dormir'   ,'courir', 'voir',   'vouloir' ,'?tre','faire'},
%    { 'dormi '   ,'couru' , 'vu'  ,   'voulu'   ,'?t?', 'fait'} 
%    };  %% not frequent in Spanish

 auxiliaries = {
     { 'poder',  'deber'   ,'ser','estar,' ,'haber'},
     { 'podr�a', 'deber�a' ,'es' ,'est�'   ,'ha'},
     { 'podr�an','deber�an','son','est�n'  ,'han'}
     };
 
 
plurals = {
    {'mujer','profesor','competidor'},
    {'mujeres','profesores','competidores'}
    };

feminine = {
    { 'triste','orgulloso' ,'contento','asustado' ,'preocupado','peque�o','gordo','alto','curioso','este','estos','un' ,'el','los' ,'algunos'},
    { 'triste','orgullosa' ,'contenta','asustada' ,'preocupada','peque�a','gorda','alta','curiosa','esta','estas','una','la','las','algunas'}
    };

pronouns = {  %%% in order  singular: masc fem  plural: masc fem; and then vertically, nominative, accusative, genitive
    { { '�l','ella'},{'ellos','ellas'} },
    { {'lo','la'},  {'los','las'} },
    { {'el','ella'},{'ellos','ellas'}}  %%% not used?
    };

deictic = {'all�'};
