%%%%% additional knowledge of conjugation
past = {
    { 'dormir'   ,'cantar'  ,'llorar',  'gritar'  ,'trabajar'  ,'atacar'  ,'encontrar'  ,'besar'  ,'golpear'  ,'ayudar'  ,'disfrutar'  ,'preferir,'  ,'odiar'  ,'querer'   ,'ser','estar'},
    { 'durmió'   ,'cantó'   ,'lloró'   ,'gritó'   ,'trabajó'   ,'atacó'   ,'encontró'   ,'besó'   ,'golpeó'   ,'ayudó'   ,'disfrutó'   ,'prefirió'   ,'odió'   ,'quiso'    ,'fue','estuvo'},
    { 'durmieron','cantaron','lloraron','gritaron','trabajaron','atacaron','encontraron','besaron','golpearon','ayudaron','disfrutaron','prefirieron','odiaron','quisieron','fueron','estuvieron'}
    };

present = {
    { 'dormir' ,'cantar','llorar','gritar','trabajar','atacar','encontrar','besar','golpear','ayudar','disfrutar','preferir,','odiar','querer','ser','estar'},
    {'duerme' ,'canta','llora','grita','trabaja','ataca','encuentra','besa','golpea','ayuda','disfruta','prefiere','odia','quiere' ,'es','está'}, % el/ ella
    {'duermen' ,'cantan','lloran','gritan','trabajan','atacan','encuentran','besan','golpean','ayudan','disfrutan','prefieren','odian','quieren','son','están'}  % ellos/ellas 
    };

future = {
    { 'dormir' ,'cantar','llorar','gritar','trabajar','atacar','encontrar','besar','golpear','ayudar','disfrutar','preferir,','odiar','querer','ser','estar'},
    {'dormirá','cantará','llorará','gritará','trabajará','atacará','encontrará','besará','golpeará','ayudará','disfutará','preferirá','odiará','querrá','será','estará'},
    {'dormirán','cantarán','llorarán','gritarán','trabajarán','atacarán','encontrarán','besarán','golpearán','ayudarán','disfrutarán','preferirán','odiarán','querrán','serán','estarán' }
    };

%pastparticiple = {
%    { 'dormir'   ,'courir', 'voir',   'vouloir' ,'?tre','faire'},
%    { 'dormi '   ,'couru' , 'vu'  ,   'voulu'   ,'?t?', 'fait'} 
%    };  %% not frequent in Spanish

 auxiliaries = {
     { 'poder',  'deber'   ,'ser','estar,' ,'haber'},
     { 'podría', 'debería' ,'es' ,'está'   ,'ha'},
     { 'podrían','deberían','son','están'  ,'han'}
     };
 
 
plurals = {
    {'mujer','profesor','competidor'},
    {'mujeres','profesores','competidores'}
    };

feminine = {
    { 'triste','orgulloso' ,'contento','asustado' ,'preocupado','pequeño','gordo','alto','curioso','este','estos','un' ,'el','los' ,'algunos'},
    { 'triste','orgullosa' ,'contenta','asustada' ,'preocupada','pequeña','gorda','alta','curiosa','esta','estas','una','la','las','algunas'}
    };

pronouns = {  %%% in order  singular: masc fem  plural: masc fem; and then vertically, nominative, accusative, genitive
    { { 'él','ella'},{'ellos','ellas'} },
    { {'lo','la'},  {'los','las'} },
    { {'el','ella'},{'ellos','ellas'}}  %%% not used?
    };

deictic = {'allá'};
