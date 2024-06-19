import shapely

from jord.geometric_analysis.principal_axis import buffer_principal_axis

door_wkt = "Polygon ((259011.2008620563428849 6251827.04947430267930031, 259011.20086663446272723 6251827.04948555119335651, 259011.20086754151270725 6251827.04949766211211681, 259011.20145621645497158 6251827.05093419179320335, 259011.20204146348987706 6251827.05237218085676432, 259011.20204929384635761 6251827.05238146428018808, 259011.20205389865441248 6251827.05239270161837339, 259011.20305759049369954 6251827.05357691366225481, 259011.20405863982159644 6251827.05476376973092556, 259011.20406895683845505 6251827.05477018002420664, 259011.20407680771313608 6251827.05477944295853376, 259011.20539733109762892 6251827.05559554696083069, 259011.20671613005106337 6251827.05641496367752552, 259011.20672792129334994 6251827.05641787126660347, 259011.20673825228004716 6251827.05642425641417503, 259011.20824659307254478 6251827.05679241567850113, 259011.20975380053278059 6251827.05716413259506226, 259012.49798140628263354 6251827.166566276922822, 259012.49581052322173491 6251827.18181540630757809, 259012.49134677735855803 6251827.2100857961922884, 259012.4859886730555445 6251827.23826545663177967, 259012.480230700050015 6251827.26645966898649931, 259012.47368412165087648 6251827.29443141259253025, 259012.46664068909012713 6251827.32220833003520966, 259012.45880033716093749 6251827.34989767428487539, 259012.45056006757658906 6251827.37729905266314745, 259012.4415285756404046 6251827.40479051694273949, 259012.43210207196534611 6251827.43178008589893579, 259012.42188198870280758 6251827.45876904297620058, 259012.41125336897675879 6251827.48529092594981194, 259012.40004198666429147 6251827.51178153790533543, 259012.38814420369453728 6251827.53795666061341763, 259012.37564151707920246 6251827.56385508272796869, 259012.36264662889880128 6251827.58934887032955885, 259012.34894596549565904 6251827.61466531362384558, 259012.33484175134799443 6251827.63969532772898674, 259012.32025951860123314 6251827.66429664567112923, 259012.30498217724380083 6251827.68870071042329073, 259012.28919521856005304 6251827.7127286596223712, 259012.27302798433811404 6251827.73633480630815029, 259012.25614624217269011 6251827.75957202725112438, 259012.23897862725425512 6251827.78259449359029531, 259012.22114685355336405 6251827.80498327594250441, 259012.20277303122566082 6251827.82703186292201281, 259012.18400163733167574 6251827.84878284297883511, 259012.16475741608883254 6251827.87011020164936781, 259012.14500863870489411 6251827.89095062017440796, 259012.12487146502826363 6251827.91138538718223572, 259012.10413068495108746 6251827.93133226223289967, 259012.083174443396274 6251827.95079872384667397, 259012.06175581950810738 6251827.96983750071376562, 259012.039743963687215 6251827.98837901838123798, 259012.01739941840060055 6251828.00635396409779787, 259011.9947553405945655 6251828.02393291890621185, 259011.97174470039317384 6251828.04099253192543983, 259011.948345076845726 6251828.05745158903300762, 259011.9244252699718345 6251828.07343121059238911, 259011.90040229063015431 6251828.08881782926619053, 259011.87577561527723446 6251828.10381229687482119, 259011.85117503019864671 6251828.11819570325314999, 259011.82597417145734653 6251828.13198672514408827, 259011.80046581628266722 6251828.14538605511188507, 259011.77488067653030157 6251828.15798029117286205, 259011.74887747815228067 6251828.17008865065872669, 259011.72266886656871065 6251828.18160455580800772, 259011.69618274521781132 6251828.19261563941836357, 259011.66940204610000364 6251828.20293116848915815, 259011.64249230074346997 6251828.21266236808151007, 259011.61528449898469262 6251828.22189713269472122, 259011.58802445937180892 6251828.23052121791988611, 259011.56043512854375876 6251828.23836135119199753, 259011.53273792596883141 6251828.24580683559179306, 259011.50496259756619111 6251828.25245307479053736, 259011.47697537372005172 6251828.25860629510134459, 259011.44879905835841782 6251828.2640629755333066, 259011.42062316570081748 6251828.26892430987209082, 259011.39223414156003855 6251828.27309332694858313, 259011.36374070183956064 6251828.2767666969448328, 259011.33526486085611396 6251828.2797432653605938, 259011.3067072625271976 6251828.28212306555360556, 259011.27811379209742881 6251828.28371159173548222, 259011.24962210320518352 6251828.28490288183093071, 259011.2208657430310268 6251828.28529952187091112, 259011.19227358553325757 6251828.28510096482932568, 259011.16369804699206725 6251828.28430719953030348, 259011.13502163629163988 6251828.2828188044950366, 259011.10622473285184242 6251828.2807262958958745, 259011.10312100933515467 6251828.2809871006757021, 259011.10024807453737594 6251828.28219016548246145, 259011.09788463526638225 6251828.28421877883374691, 259011.09625997158582322 6251828.28687614388763905, 259011.09553169400896877 6251828.28990446496754885, 259011.09577045359765179 6251828.29300996195524931, 259011.0969530880684033 6251828.29589136689901352, 259011.09896486857905984 6251828.29826915170997381, 259011.10161062993574888 6251828.2999126436188817, 259011.10463370371144265 6251828.30066240578889847, 259011.11594629724277183 6251828.30164610967040062, 259011.12688481312943622 6251828.30301342438906431, 259011.13811839141999371 6251828.30459006689488888, 259011.14919169354834594 6251828.30635395552963018, 259011.16012151818722486 6251828.30840329825878143, 259011.1710125754470937 6251828.31075812131166458, 259011.18203567806631327 6251828.31331705581396818, 259011.19278368676896207 6251828.31605291273444891, 259011.21433528795023449 6251828.32225268799811602, 259011.22482011478859931 6251828.32574763055890799, 259011.23545085225487128 6251828.32958650775253773, 259011.24593113004812039 6251828.33350436855107546, 259011.25635079349740408 6251828.33782951161265373, 259011.26667098491452634 6251828.34215416293591261, 259011.27682081301463768 6251828.3468386996537447, 259011.28701573831494898 6251828.35178769193589687, 259011.2969870546949096 6251828.356675592251122, 259011.30669510987354442 6251828.36201502289623022, 259011.3164584168989677 6251828.36763632111251354, 259011.32609069391037337 6251828.37333705555647612, 259011.33560518588637933 6251828.37932039704173803, 259011.34486285818275064 6251828.38536224607378244, 259011.35409581582644023 6251828.39194318372756243, 259011.35411252995254472 6251828.39195507112890482, 259011.36323368747252971 6251828.39842815045267344, 259011.37203923080232926 6251828.40527690667659044, 259011.38081111313658766 6251828.41217614058405161, 259011.38953812193358317 6251828.41943230479955673, 259011.39805718665593304 6251828.42677632626146078, 259011.40617447227123193 6251828.43420902173966169, 259011.41441515131737106 6251828.44205728638917208, 259011.42226386687252671 6251828.44990600273013115, 259011.43011309119174257 6251828.45804957300424576, 259011.43764477921649814 6251828.46626595966517925, 259011.44500073819654062 6251828.47470079269260168, 259011.45220360610983334 6251828.48328503221273422, 259011.45934703917009756 6251828.49199414905160666, 259011.46607905134442262 6251828.50087260082364082, 259011.47278588067274541 6251828.51004517637193203, 259011.47928870155010372 6251828.51920824218541384, 259011.48553161000018008 6251828.52837751340121031, 259011.49147105749580078 6251828.53782220836728811, 259011.49727130029350519 6251828.54755481984466314, 259011.50288497805013321 6251828.55730489175766706, 259011.5082906334719155 6251828.56713335588574409, 259011.51345400890568271 6251828.57697299495339394, 259011.52309543828596361 6251828.59723967406898737, 259011.52759472018806264 6251828.60760758351534605, 259011.53191734626307152 6251828.61802118271589279, 259011.53593272209400311 6251828.62840239889919758, 259011.53973817051155493 6251828.63894056435674429, 259011.54318707349011675 6251828.64958289265632629, 259011.54319602870964445 6251828.64961038995534182, 259011.54671819839859381 6251828.66037257481366396, 259011.54964936512988061 6251828.67112018633633852, 259011.55260479875141755 6251828.68205529171973467, 259011.55514398828381673 6251828.69279801659286022, 259011.55750402566627599 6251828.70381152350455523, 259011.55966795992571861 6251828.71482791658490896, 259011.56162939130445011 6251828.72600807528942823, 259011.56329189575626515 6251828.73705883976072073, 259011.56466990016633645 6251828.74818130489438772, 259011.56593975482974201 6251828.7593169528990984, 259011.56672128909849562 6251828.77045381627976894, 259011.56717940728412941 6251828.77798004355281591, 259011.0680453177774325 6251828.73563579190522432, 259011.06648936128476635 6251828.73574871383607388, 259011.06493287751800381 6251828.735860382206738, 259011.06492900400189683 6251828.73586195521056652, 259011.06492483543115668 6251828.73586225789040327, 259011.06348000830621459 6251828.7364504374563694, 259011.06203413096955046 6251828.73703765217214823, 259011.06203093286603689 6251828.73704034555703402, 259011.06202706202748232 6251828.73704192135483027, 259011.06083465626579709 6251828.73804783169180155, 259011.0596410556754563 6251828.73905306495726109, 259011.05963884672382846 6251828.73905661422759295, 259011.05963565185084008 6251828.73905930947512388, 259011.05881241141469218 6251828.74038452282547951, 259011.05798790248809382 6251828.74170933663845062, 259011.05798689840594307 6251828.7417133953422308, 259011.0579846927721519 6251828.74171694554388523, 259011.05761124094715342 6251828.7432317640632391, 259011.05723649359424599 6251828.74474645406007767, 259011.05288927798392251 6251828.79549183696508408, 259010.98734465290908702 6251828.78993573598563671, 259010.98422353691421449 6251828.79016256146132946, 259010.98132535073091276 6251828.79134295601397753, 259010.97893390836543404 6251828.79336132574826479, 259010.97728339934838004 6251828.7960200160741806, 259010.97653545497450978 6251828.79905866645276546, 259010.97013545496156439 6251828.87485866621136665, 259010.97036316810408607 6251828.87797905784100294, 259010.97154399022110738 6251828.88087635952979326, 259010.97356233416940086 6251828.88326696213334799, 259010.97622063040034845 6251828.88491685874760151, 259010.97925866636796854 6251828.88566454499959946, 259010.98237905791029334 6251828.8854368319734931, 259010.98527635939535685 6251828.88425600994378328, 259010.98766696275561117 6251828.88223766535520554, 259010.98931685907882638 6251828.87957936897873878, 259010.9900645450106822 6251828.87654133327305317, 259010.9956229311064817 6251828.81070919800549746, 259011.05119440160342492 6251828.81541989278048277, 259011.04563545496785082 6251828.88125866651535034, 259011.0458631681103725 6251828.88437905814498663, 259011.04704399022739381 6251828.88727635983377695, 259011.04906233417568728 6251828.88966696243733168, 259011.05172063040663488 6251828.8913168590515852, 259011.05475866637425497 6251828.89206454530358315, 259011.05787905791657977 6251828.89183683227747679, 259011.06077635940164328 6251828.89065601024776697, 259011.06316696276189759 6251828.88863766565918922, 259011.06481685908511281 6251828.88597936928272247, 259011.06556454501696862 6251828.88294133357703686, 259011.07112289752694778 6251828.8171095959842205, 259011.57525494953733869 6251828.85986423026770353, 259011.57840374385705218 6251828.8596310205757618, 259011.58132287123589776 6251828.85842769686132669, 259011.58372131528449245 6251828.85637422185391188, 259011.58535996812861413 6251828.85367531329393387, 259011.58607546761049889 6251828.85060003213584423, 259011.58687546759028919 6251828.83920003194361925, 259011.58688641712069511 6251828.83902102988213301, 259011.58748641714919358 6251828.82752102985978127, 259011.5874938499473501 6251828.82735066115856171, 259011.58789384993724525 6251828.8159506618976593, 259011.58789962195442058 6251828.81568695325404406, 259011.58799962195917033 6251828.80418695323169231, 259011.58799846141482703 6251828.80392458848655224, 259011.58779846140532754 6251828.79252458829432726, 259011.5877938499324955 6251828.79234933853149414, 259011.58739384994260035 6251828.78094933833926916, 259011.58738152580917813 6251828.78069242835044861, 259011.58668152580503374 6251828.76919242832809687, 259011.58667546760989353 6251828.76909996662288904, 259011.5858754676009994 6251828.75769996643066406, 259011.58583560731494799 6251828.7572669917717576, 259011.58453560731140897 6251828.7458669925108552, 259011.58452412401675247 6251828.74577046278864145, 259011.58312412403756753 6251828.73447046242654324, 259011.58308872074121609 6251828.73421231657266617, 259011.58138872071867809 6251828.72291231621056795, 259011.58134957021684386 6251828.72267200518399477, 259011.57934957023826428 6251828.71127200592309237, 259011.5793124882329721 6251828.71107254736125469, 259011.5771124882157892 6251828.69987254682928324, 259011.57707802412915044 6251828.69970470853149891, 259011.57467802413157187 6251828.68850470893085003, 259011.57463184613152407 6251828.6882997453212738, 259011.57203184612444602 6251828.67729974538087845, 259011.57195363397477195 6251828.67699091043323278, 259011.56895363397779875 6251828.66589090973138809, 259011.56894763821037486 6251828.66586882527917624, 259011.56594763821340166 6251828.65486882533878088, 259011.56580397128709592 6251828.65438960958272219, 259011.5622084790666122 6251828.64340338297188282, 259011.55871292651863769 6251828.6326171075925231, 259011.55860553903039545 6251828.63230355549603701, 259011.55470553901977837 6251828.62150355521589518, 259011.55462663623620756 6251828.62129252776503563, 259011.55052663624519482 6251828.61069252714514732, 259011.55043591660796665 6251828.61046622227877378, 259011.54603591660270467 6251828.59986622259020805, 259011.54597345006186515 6251828.59971906896680593, 259011.54137345004710369 6251828.5891190692782402, 259011.54123022512067109 6251828.58880406804382801, 259011.53143022512085736 6251828.56820406764745712, 259011.53125488082878292 6251828.56785337906330824, 259011.5259548808389809 6251828.55775337945669889, 259011.52586215903284028 6251828.55758081283420324, 259011.52036215903353877 6251828.54758081305772066, 259011.52026622454286553 6251828.54741035588085651, 259011.51456622453406453 6251828.53751035593450069, 259011.51449020378640853 6251828.53738058637827635, 259011.50859020379721187 6251828.52748058550059795, 259011.50846524169901386 6251828.52727649640291929, 259011.50236524170031771 6251828.51757649704813957, 259011.50216599242412485 6251828.5172720905393362, 259011.49576599241117947 6251828.50787209067493677, 259011.49565507145598531 6251828.50771252997219563, 259011.48905507146264426 6251828.49841252993792295, 259011.48897232059971429 6251828.49829765874892473, 259011.48217232059687376 6251828.48899765871465206, 259011.4820683664875105 6251828.48885805252939463, 259011.47516836650902405 6251828.47975805215537548, 259011.47493182585458271 6251828.47945816535502672, 259011.46763182582799345 6251828.47055816557258368, 259011.46756051678676158 6251828.47047221008688211, 259011.46026051678927615 6251828.46177220996469259, 259011.46013661427423358 6251828.46162737160921097, 259011.45263661429635249 6251828.45302737131714821, 259011.45247154129901901 6251828.45284275338053703, 259011.4447715412825346 6251828.44444275368005037, 259011.44459999073296785 6251828.44426024984568357, 259011.43659999073133804 6251828.43596024997532368, 259011.43647106798016466 6251828.43582893256098032, 259011.42847106797853485 6251828.42782893218100071, 259011.42829655145760626 6251828.4276586202904582, 259011.41989655146608129 6251828.41965862084180117, 259011.41975322159123607 6251828.41952477116137743, 259011.41145322160446085 6251828.41192477103322744, 259011.41122939638444223 6251828.41172590106725693, 259011.40252939637866803 6251828.4042259007692337, 259011.40239334182115272 6251828.40411071013659239, 259011.39349334180587903 6251828.3967107106000185, 259011.39328211525571533 6251828.39653988275676966, 259011.38438211526954547 6251828.38953988254070282, 259011.38433940624236129 6251828.38950647786259651, 259011.37533940622233786 6251828.38250647764652967, 259011.37498747004428878 6251828.38224492873996496, 259011.36569584248354658 6251828.3756508706137538, 259011.35630418418440968 6251828.36895681638270617, 259011.3559653662960045 6251828.36872564814984798, 259011.34646536628133617 6251828.3625256484374404, 259011.34632350312313065 6251828.36243475880473852, 259011.33662350312806666 6251828.35633475799113512, 259011.33639320859219879 6251828.35619423259049654, 259011.32659320859238505 6251828.35039423312991858, 259011.32648964479449205 6251828.35033377539366484, 259011.31658964478992857 6251828.34463377483189106, 259011.31641918746754527 6251828.34453784022480249, 259011.30641918748733588 6251828.33903784025460482, 259011.30600157208391465 6251828.33882079273462296, 259011.29580157206510194 6251828.33382079284638166, 259011.29576702031772584 6251828.33380393777042627, 259011.28546702032326721 6251828.32880393788218498, 259011.2852905819308944 6251828.32872040569782257, 259011.27489058193168603 6251828.3239204054698348, 259011.27456485689617693 6251828.32377704605460167, 259011.26406485689221881 6251828.31937704607844353, 259011.26403377670794725 6251828.31936408299952745, 259011.25343377672834322 6251828.31496408302336931, 259011.25310163883841597 6251828.31483311485499144, 259011.24240163882495835 6251828.31083311513066292, 259011.24229644454317167 6251828.3107944605872035, 259011.23149644455406815 6251828.30689446069300175, 259011.23126227798638865 6251828.30681316740810871, 259011.22649414881016128 6251828.30522379092872143, 259011.25003791798371822 6251828.30489904899150133, 259011.2503177534090355 6251828.30489127058535814, 259011.27901775340433232 6251828.30369127076119184, 259011.27915470022708178 6251828.30368460342288017, 259011.30795470022712834 6251828.30208460334688425, 259011.30823045497527346 6251828.30206545814871788, 259011.33703045497532003 6251828.29966545756906271, 259011.33723963171360083 6251828.2996458113193512, 259011.36593963170889765 6251828.29664581175893545, 259011.36617861693957821 6251828.29661792051047087, 259011.39487861696397886 6251828.29291792027652264, 259011.39505294780246913 6251828.29289388377219439, 259011.42365294779301621 6251828.28869388438761234, 259011.42390023113694042 6251828.28865440096706152, 259011.45230023114709184 6251828.28375440090894699, 259011.45250129391206428 6251828.28371759038418531, 259011.48090129389311187 6251828.27821759041398764, 259011.48114729661028832 6251828.27816673554480076, 259011.50934729661094025 6251828.27196673490107059, 259011.50952716049505398 6251828.27192544657737017, 259011.53752716051531024 6251828.26522544678300619, 259011.53779601072892547 6251828.26515715941786766, 259011.56569601071532816 6251828.25765715911984444, 259011.56583349843276665 6251828.25761914625763893, 259011.59363349844352342 6251828.24971914663910866, 259011.59391629113815725 6251828.24963425379246473, 259011.62141629113466479 6251828.24093425367027521, 259011.62161407031817362 6251828.24086941126734018, 259011.64901407030993141 6251828.23156941123306751, 259011.64920070793596096 6251828.23150399792939425, 259011.67630070794257335 6251828.22170399781316519, 259011.67649442233960144 6251828.2216316731646657, 259011.70349442234146409 6251828.21123167313635349, 259011.70373878563987091 6251828.21113383583724499, 259011.73043878562748432 6251828.20003383606672287, 259011.73062273694085889 6251828.19995519425719976, 259011.75702273694332689 6251828.18835519440472126, 259011.75722127631888725 6251828.1882653646171093, 259011.78342127631185576 6251828.17606536485254765, 259011.78361640981165692 6251828.17597191873937845, 259011.80941640981473029 6251828.16327191796153784, 259011.80965036401175894 6251828.16315291542559862, 259011.83535036401008256 6251828.14965291600674391, 259011.83550061579444446 6251828.1495723482221365, 259011.86090061580762267 6251828.13567234762012959, 259011.86114736489253119 6251828.13553273398429155, 259011.88594736487721093 6251828.12103273440152407, 259011.8861005621147342 6251828.12094132043421268, 259011.91090056212851778 6251828.10584132000803947, 259011.91109349884209223 6251828.10572081711143255, 259011.93529349882737733 6251828.09022081736475229, 259011.93545496152364649 6251828.0901151904836297, 259011.95955496153328568 6251828.07401519082486629, 259011.95975321688456461 6251828.07387927267700434, 259011.9833532168995589 6251828.05727927293628454, 259011.98355558741604909 6251828.05713311769068241, 259012.00675558741204441 6251828.03993311710655689, 259012.00693220799439587 6251828.03979911562055349, 259012.0297322079713922 6251828.02209911588579416, 259012.02986804352258332 6251828.02199176698923111, 259012.05236804354353808 6251828.00389176700264215, 259012.05254241827060468 6251828.00374821852892637, 259012.07474241827731021 6251827.98504821863025427, 259012.07494363840669394 6251827.98487409297376871, 259012.09654363838490099 6251827.96567409299314022, 259012.09670584279228933 6251827.96552669815719128, 259012.11780584280495532 6251827.94592669792473316, 259012.11793177638901398 6251827.94580766744911671, 259012.13883177639218047 6251827.92570766713470221, 259012.13902274213614874 6251827.92551901284605265, 259012.15932274213992059 6251827.90491901338100433, 259012.15945861861109734 6251827.90477840509265661, 259012.17935861859587021 6251827.8837784044444561, 259012.17952435003826395 6251827.8835991807281971, 259012.19892435002839193 6251827.86209918092936277, 259012.19907056144438684 6251827.86193349771201611, 259012.21797056146897376 6251827.84003349766135216, 259012.2180822127556894 6251827.83990184403955936, 259012.2365822127321735 6251827.81770184449851513, 259012.23672217669081874 6251827.81753005273640156, 259012.25472217670176178 6251827.7949300529435277, 259012.25491655548103154 6251827.7946778628975153, 259012.27221655548783019 6251827.77147786226123571, 259012.27229034993797541 6251827.77137760445475578, 259012.28929034993052483 6251827.74797760508954525, 259012.28945052094059065 6251827.74775056727230549, 259012.30575052092899568 6251827.72395056672394276, 259012.30585750759928487 6251827.72379108984023333, 259012.32175750762689859 6251827.69959108997136354, 259012.32187610937398858 6251827.69940618239343166, 259012.33727610934874974 6251827.67480618227273226, 259012.33740235181176104 6251827.67459897417575121, 259012.35210235181148164 6251827.64979897439479828, 259012.35221205977723002 6251827.64960917644202709, 259012.36641205978230573 6251827.62440917640924454, 259012.36649472452700138 6251827.62425949797034264, 259012.38029472454218194 6251827.59875949751585722, 259012.38040933644515462 6251827.59854133427143097, 259012.39350933642708696 6251827.5728413350880146, 259012.39360551637946628 6251827.57264749146997929, 259012.40620551639585756 6251827.54654749110341072, 259012.40630366478580981 6251827.5463380292057991, 259012.41830366477370262 6251827.51993802934885025, 259012.41840919639798813 6251827.51969752553850412, 259012.42970919641084038 6251827.49299752525985241, 259012.42978236736962572 6251827.49281989969313145, 259012.4404823673539795 6251827.46611989941447973, 259012.44055193950771354 6251827.4659413592889905, 259012.45085193950217217 6251827.43874135985970497, 259012.45094074599910527 6251827.43849731981754303, 259012.46044074601377361 6251827.41129731945693493, 259012.46050046276650392 6251827.41112109087407589, 259012.46960046276217327 6251827.38342109136283398, 259012.46967635082546622 6251827.38317984528839588, 259012.47797635084134527 6251827.35557984467595816, 259012.47802171940566041 6251827.35542442928999662, 259012.48592171940254048 6251827.32752442918717861, 259012.48599322472000495 6251827.32725792471319437, 259012.49309322470799088 6251827.2992579247802496, 259012.49313688179245219 6251827.29907884448766708, 259012.49973688178579323 6251827.27087884489446878, 259012.49979776461259462 6251827.27060095220804214, 259012.50559776462614536 6251827.24220095202326775, 259012.50562399069895037 6251827.24206794146448374, 259012.51102399069350213 6251827.21366794127970934, 259012.51107762966421433 6251827.21335962507873774, 259012.51557762967422605 6251827.18485962506383657, 259012.51560018127202056 6251827.18470940086990595, 259012.51933845205348916 6251827.15845032874494791, 259012.51936413301154971 6251827.1583461994305253, 259012.51936047006165609 6251827.15829566586762667, 259012.5197001812630333 6251827.1559094013646245, 259012.5197349927329924 6251827.15563838463276625, 259012.52303499274421483 6251827.12683838419616222, 259012.52304968546377495 6251827.12670187745243311, 259012.52594968545599841 6251827.09790187794715166, 259012.52576558326836675 6251827.09474747069180012, 259012.52460646774852648 6251827.09180797543376684, 259012.52258806710597128 6251827.08937687799334526, 259012.51991190205444582 6251827.08769690152257681, 259012.51684516575187445 6251827.08693577907979488, 259011.21645013199304231 6251826.9766362002119422, 259011.15080458816373721 6251826.97099207248538733, 259011.15552191901952028 6251826.91512118466198444, 259011.22114337206585333 6251826.92076324112713337, 259011.22426410947809927 6251826.92054031882435083, 259011.22716322005726397 6251826.91936394479125738, 259011.22955691872630268 6251826.91734927333891392, 259011.23121089351479895 6251826.91469351202249527, 259011.23196324188029394 6251826.91165662743151188, 259011.23174031870439649 6251826.90853589028120041, 259011.23056394528248347 6251826.90563677996397018, 259011.22854927321895957 6251826.90324308071285486, 259011.22589351265924051 6251826.9015891058370471, 259011.2228566279518418 6251826.9008367583155632, 259011.14725662794080563 6251826.89433675818145275, 259011.14413290043012239 6251826.89456037618219852, 259011.14123152272077277 6251826.8957392256706953, 259011.13883705268381163 6251826.89775768853724003, 259011.13718433224130422 6251826.90041780099272728, 259011.13643545497325249 6251826.90345866605639458, 259011.13003545498941094 6251826.97925866674631834, 259011.13026246894150972 6251826.98237606883049011, 259011.13144081365317106 6251826.98527110554277897, 259011.13345536793349311 6251826.98766093887388706, 259011.13610931523726322 6251826.98931208904832602, 259011.1391433720709756 6251826.99006324168294668, 259011.2048144057916943 6251826.99570956081151962, 259011.20063386522815563 6251827.04637771192938089, 259011.2007498191378545 6251827.04792588111013174, 259011.2008620563428849 6251827.04947430267930031),(259011.56799923727521673 6251828.804144237190485, 259011.5679015249479562 6251828.81538115441799164, 259011.56750914009171538 6251828.82656412292271852, 259011.56691825497546233 6251828.83788942079991102, 259011.56683482223888859 6251828.83907833695411682, 259011.07281778031028807 6251828.79718154110014439, 259011.0763106650847476 6251828.75640882831066847, 259011.56789341659168713 6251828.79811245854943991, 259011.56799923727521673 6251828.804144237190485),(259012.50503254286013544 6251827.10600564815104008, 259012.50315719246282242 6251827.12462981697171926, 259012.5006261530215852 6251827.1467188885435462, 259011.2213864523509983 6251827.03808003850281239, 259011.22474195642280392 6251826.99741133023053408, 259012.50503254286013544 6251827.10600564815104008))"

print(buffer_principal_axis(shapely.from_wkt(door_wkt).buffer(0).simplify(0)).wkt)