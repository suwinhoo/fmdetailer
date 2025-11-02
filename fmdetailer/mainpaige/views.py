import os
import csv
import io
import pandas as pd
import numpy as np 
from django.shortcuts import render, redirect

ROLES_WEIGHT = {'Advanced Forward': {'key': {'Dribbling': 0.821656915999922, 'Finishing': 1.0}, 'normal': {'Acceleration': 0.42411674176307385, 'Agility': 0.27824206533179685, 'Composure': 0.2820283224535919, 'First Touch': 0.5631667603516651, 'Flair': 0.6364564978448449, 'Heading': 0.5297160731951838, 'Long Shots': 0.226088810931474, 'Off the Ball': 0.5814500080015825, 'Pace': 0.3775911247476301, 'Penalty Taking': 0.37755944078528864, 'Technique': 0.5017944834890333}}, 'Advanced Playmaker': {'key': {'Flair': 0.8720324189766947, 'Technique': 0.7171884576893093, 'Vision': 1.0}, 'normal': {'Agility': 0.20779564272434795, 'Composure': 0.431876485790877, 'Corners': 0.639689830695903, 'Crossing': 0.3518839492129113, 'Dribbling': 0.5751697468565774, 'Finishing': 0.3851307074284766, 'First Touch': 0.58722659295324, 'Free Kick Taking': 0.6125264629799589, 'Long Shots': 0.5392763053292653, 'Off the Ball': 0.42390394839195356, 'Passing': 0.577180381597649, 'Penalty Taking': 0.40622147916007967, 'Teamwork': 0.4479199286748124}}, 'Anchor': {'key': {'Anticipation': 0.7216194931446324, 'Decisions': 0.7427415171518856, 'Marking': 1.0, 'Positioning': 0.9241064853730077, 'Tackling': 0.8970315396452874}, 'normal': {'Balance': 0.37505145437115545, 'Bravery': 0.260771462973125, 'Composure': 0.4746518357634653, 'Concentration': 0.6092983032520527, 'Corners': 0.22978638107807728, 'First Touch': 0.27150402670806517, 'Free Kick Taking': 0.37038642701317104, 'Heading': 0.344910135348403, 'Leadership': 0.3528709370156586, 'Long Shots': 0.5685717557751288, 'Passing': 0.3953280189203, 'Strength': 0.6334458897968582, 'Teamwork': 0.393737496414712, 'Technique': 0.23766441051950907, 'Vision': 0.46471809678745585, 'Work Rate': 0.4342770123089766}}, 'Attacking Midfielder': {'key': {'Flair': 1.0, 'Long Shots': 0.949199364788631, 'Technique': 0.7635976224840565, 'Vision': 0.7319622349303557}, 'normal': {'Corners': 0.5230748319836522, 'Crossing': 0.2385450609680666, 'Dribbling': 0.5139116791755503, 'Finishing': 0.4946472668875343, 'First Touch': 0.621619710224589, 'Free Kick Taking': 0.5528649070113782, 'Off the Ball': 0.41795513488622343, 'Passing': 0.5689912424102624, 'Penalty Taking': 0.2877937422338519}}, 'Ball Playing Defender': {'key': {'Anticipation': 0.7466456388285033, 'Balance': 0.7911857193086692, 'Bravery': 0.7409875035857774, 'Composure': 1.0, 'Concentration': 0.7327886161727859, 'Heading': 0.8929197886916445, 'Jumping Reach': 0.7893383196757885, 'Marking': 0.9811939495198433, 'Passing': 0.8169725896448404, 'Positioning': 0.9181464617912457, 'Strength': 0.9020317168489045, 'Tackling': 0.8574212949248919, 'Teamwork': 0.7826936874813764}, 'normal': {'Aggression': 0.32601891396090227, 'Crossing': 0.2029196196219701, 'Decisions': 0.22288198770264214, 'Determination': 0.27374819605870393, 'Dribbling': 0.27259672012222896, 'First Touch': 0.42446139514057096, 'Leadership': 0.47018285241452895, 'Long Shots': 0.24659779710301782, 'Long Throws': 0.6571244842709496, 'Penalty Taking': 0.45373503654240516, 'Stamina': 0.5306946736870637, 'Technique': 0.5621962413669555, 'Vision': 0.6935955462309594, 'Work Rate': 0.5496288309073737}}, 'Ball Winning Midfielder': {'key': {'Aggression': 0.8632318638976099, 'Stamina': 0.7504559729230909, 'Tackling': 0.798604925159274, 'Teamwork': 0.870199985721879, 'Work Rate': 1.0}, 'normal': {'Anticipation': 0.4929267988033261, 'Balance': 0.4865638111759215, 'Bravery': 0.6365275724343864, 'Composure': 0.30734504544531677, 'Concentration': 0.4023852699461287, 'Corners': 0.3305290310531092, 'Determination': 0.22431248993458514, 'First Touch': 0.20952402719916352, 'Free Kick Taking': 0.4090985035870243, 'Leadership': 0.29574509612958116, 'Long Shots': 0.5903827086116002, 'Long Throws': 0.2700202161126672, 'Marking': 0.6939088998851265, 'Passing': 0.4072226664579688, 'Penalty Taking': 0.3123959253462963, 'Positioning': 0.529654925686711, 'Strength': 0.5566628001455716, 'Technique': 0.2596320689714644, 'Vision': 0.4751055959301713}}, 'Box To Box Midfielder': {'key': {'Long Shots': 0.8041840460757239, 'Off the Ball': 0.7073789317055263, 'Passing': 0.7509711066963107, 'Stamina': 0.8469494087273648, 'Teamwork': 1.0, 'Work Rate': 0.9250334651679204}, 'normal': {'Anticipation': 0.2525889273826912, 'Balance': 0.6167517651354344, 'Bravery': 0.34604875909140054, 'Composure': 0.4660260021161761, 'Concentration': 0.4376060672480334, 'Corners': 0.6842585996749059, 'Crossing': 0.47792815955850504, 'Dribbling': 0.4096720518796468, 'Finishing': 0.35901014181764024, 'First Touch': 0.2954292676798691, 'Flair': 0.2361543608607406, 'Free Kick Taking': 0.6942442478068054, 'Long Throws': 0.30267628644515293, 'Marking': 0.455214110354414, 'Penalty Taking': 0.5750555519361923, 'Positioning': 0.429610922990928, 'Strength': 0.5059000487167242, 'Tackling': 0.5681686790421283, 'Technique': 0.41867646460398256, 'Vision': 0.6336776015551122}}, 'Carrilero': {'key': {'Passing': 0.7559600303939548, 'Positioning': 0.9733243582110327, 'Stamina': 1.0, 'Tackling': 0.723492287325683, 'Vision': 0.8472582321555131}, 'normal': {'Anticipation': 0.3114600059682872, 'Balance': 0.2678520007369856, 'Composure': 0.3475902516754734, 'Concentration': 0.3827903728322487, 'Corners': 0.5241971076546659, 'Crossing': 0.27283790720656315, 'Decisions': 0.2871045974810782, 'First Touch': 0.6082908264901083, 'Free Kick Taking': 0.5447334845904306, 'Leadership': 0.23726517427509086, 'Long Shots': 0.6651811910666391, 'Marking': 0.5370093102725165, 'Off the Ball': 0.2375909335878863, 'Penalty Taking': 0.278891008593418, 'Strength': 0.32083343336416253, 'Teamwork': 0.5032236893412708, 'Technique': 0.49457721174695635, 'Work Rate': 0.5976797143179563}}, 'Central Defender': {'key': {'Heading': 0.7750234109629633, 'Marking': 1.0, 'Positioning': 0.7882365568183031, 'Tackling': 0.7919649092387033}, 'normal': {'Decisions': 0.39575268928420454, 'Jumping Reach': 0.49001697173857284, 'Strength': 0.26565815860041203}}, 'Central Midfielder': {'key': {'Decisions': 0.7022062437695175, 'First Touch': 0.9891253552814548, 'Passing': 1.0, 'Vision': 0.8124078273821731}, 'normal': {'Long Shots': 0.6034781204732056, 'Marking': 0.29420353883999173, 'Tackling': 0.3878628571455951, 'Technique': 0.40143598212306536, 'Work Rate': 0.4612389615217764}}, 'Complete Forward': {'key': {'Balance': 0.7461737412704038, 'Finishing': 0.8879232235315874, 'Heading': 0.812262975693012, 'Long Shots': 0.7412018015498678, 'Penalty Taking': 1.0, 'Strength': 0.8977841611855463}, 'normal': {'Acceleration': 0.2753787962003133, 'Agility': 0.3797865328782236, 'Anticipation': 0.694934207446602, 'Bravery': 0.47489508025176336, 'Composure': 0.666525280450194, 'Concentration': 0.5466241775503576, 'Corners': 0.25952300039539344, 'Crossing': 0.35335891594974234, 'Decisions': 0.22236418552123616, 'Determination': 0.21916045855957053, 'Dribbling': 0.5716775854467258, 'First Touch': 0.4658336668155993, 'Flair': 0.6112854939419653, 'Free Kick Taking': 0.5319792350441302, 'Jumping Reach': 0.5637708360382614, 'Long Throws': 0.27711330027794173, 'Off the Ball': 0.6323518349268918, 'Pace': 0.3655272665635348, 'Passing': 0.3501598540141712, 'Stamina': 0.46654403310255477, 'Teamwork': 0.4181727993938142, 'Technique': 0.5516345504248822, 'Vision': 0.5296696463920605, 'Work Rate': 0.3455110887183891}}, 'Complete Wing-Back': {'key': {'Corners': 0.7593868270976064, 'Crossing': 0.9259055639136539, 'Dribbling': 0.7073853619465984, 'Long Throws': 1.0}, 'normal': {'Acceleration': 0.5219901832302591, 'Agility': 0.5564341015233939, 'Anticipation': 0.2597034605479925, 'Balance': 0.6822148957209426, 'Bravery': 0.3534813502290493, 'Composure': 0.6130342272162078, 'Concentration': 0.3001391704480801, 'Decisions': 0.289589162306947, 'First Touch': 0.5835222141109325, 'Flair': 0.5877324562760007, 'Free Kick Taking': 0.43453821437529044, 'Long Shots': 0.43916202314135183, 'Marking': 0.2868846492084315, 'Off the Ball': 0.5496510327062005, 'Pace': 0.5547109396455873, 'Passing': 0.6085391654654271, 'Penalty Taking': 0.45616969727418927, 'Stamina': 0.5296746083675302, 'Strength': 0.22826112674665938, 'Tackling': 0.3888220306269344, 'Teamwork': 0.62421604873492, 'Technique': 0.6534660688997449, 'Vision': 0.520548450965551, 'Work Rate': 0.4631829676276779}}, 'Deep Lying Forward': {'key': {'Balance': 0.7650570851814985, 'Composure': 0.7851478790493696, 'Finishing': 0.930410981094351, 'Flair': 0.7776049912748852, 'Off the Ball': 0.7741315316351663, 'Penalty Taking': 1.0, 'Teamwork': 0.8224191841240608}, 'normal': {'Anticipation': 0.5415259646884402, 'Bravery': 0.22345840292516983, 'Concentration': 0.4558769125164863, 'Corners': 0.45730133464418227, 'Crossing': 0.4464277924485694, 'Decisions': 0.4172828015765861, 'Dribbling': 0.5235262326885283, 'First Touch': 0.6444053601513957, 'Free Kick Taking': 0.6197963834990342, 'Heading': 0.5569926843370671, 'Jumping Reach': 0.28422361915731265, 'Leadership': 0.2390945275397899, 'Long Shots': 0.6971051108717534, 'Passing': 0.6250953556521615, 'Strength': 0.6038736030244243, 'Technique': 0.6683799533384814, 'Vision': 0.685744930500608, 'Work Rate': 0.26662140248994765}}, 'Deep Lying Playmaker': {'key': {'Passing': 0.7769878052255386, 'Technique': 0.7515549190412175, 'Vision': 1.0}, 'normal': {'Anticipation': 0.34031937076015895, 'Balance': 0.4596818403679966, 'Composure': 0.618714890178633, 'Concentration': 0.2307233939665479, 'Corners': 0.6106721421058069, 'Crossing': 0.2905834056461907, 'Decisions': 0.37482174747830943, 'First Touch': 0.6549693231449146, 'Free Kick Taking': 0.6069726961176368, 'Long Shots': 0.6823432616685181, 'Marking': 0.3660984630059446, 'Penalty Taking': 0.3542626558660902, 'Positioning': 0.46064183415095056, 'Tackling': 0.4195856559540471, 'Teamwork': 0.5968656669953177, 'Work Rate': 0.35497896059278783}}, 'Defensive Midfielder': {'key': {'Positioning': 0.8224952482947201, 'Tackling': 1.0}, 'normal': {'Anticipation': 0.3410247920878474, 'Concentration': 0.21300435867548848, 'Decisions': 0.24604649146719848, 'Long Shots': 0.3353476953617011, 'Marking': 0.47192172879952393, 'Passing': 0.21938516474292763, 'Teamwork': 0.23995336590538166, 'Work Rate': 0.5001799808529308}}, 'Defensive Winger': {'key': {'Crossing': 0.9428891750475209, 'Teamwork': 0.9005050367796978, 'Work Rate': 1.0}, 'normal': {'Corners': 0.6591493266012911, 'Dribbling': 0.26895631288108707, 'Free Kick Taking': 0.579253410229308, 'Long Shots': 0.3805488159090799, 'Long Throws': 0.6430280603805943, 'Off the Ball': 0.4269547224314694, 'Stamina': 0.6472343362038188, 'Technique': 0.35992894366104433}}, 'Enganche': {'key': {'First Touch': 0.7186820028965981, 'Flair': 0.8333379462208634, 'Free Kick Taking': 0.714106374976542, 'Passing': 0.7559589929492098, 'Technique': 0.8198356141674591, 'Vision': 1.0}, 'normal': {'Agility': 0.25393736510992665, 'Composure': 0.49978657171108853, 'Corners': 0.6965602363462289, 'Crossing': 0.3865820187516114, 'Decisions': 0.3825803219732778, 'Dribbling': 0.5710484965389372, 'Finishing': 0.5504426960449448, 'Long Shots': 0.6485829802889169, 'Off the Ball': 0.3845352179456165, 'Penalty Taking': 0.4460948795203382}}, 'False Nine': {'key': {'Dribbling': 0.861042410664244, 'Finishing': 1.0, 'Flair': 0.9526615726010141, 'Technique': 0.7604581021702443, 'Vision': 0.8397668312983498}, 'normal': {'Acceleration': 0.5159854042064385, 'Agility': 0.6570677012213713, 'Balance': 0.21743089250628736, 'Composure': 0.40240628790511207, 'Corners': 0.6183597887585007, 'Crossing': 0.40115999462072527, 'Decisions': 0.22437139269375667, 'First Touch': 0.5943565382137852, 'Free Kick Taking': 0.5899688211689627, 'Long Shots': 0.6044997232847806, 'Off the Ball': 0.6615362508332814, 'Pace': 0.4766945589036897, 'Passing': 0.6579150997660548, 'Penalty Taking': 0.47743322644082065, 'Stamina': 0.2745392280329401}}, 'Full-Back': {'key': {'Tackling': 1.0}, 'normal': {'Acceleration': 0.2842216862053159, 'Agility': 0.21909487713426928, 'Concentration': 0.42224339808037803, 'Decisions': 0.3524593426509021, 'Long Throws': 0.6547374779985907, 'Marking': 0.6286470803752848, 'Pace': 0.30961029725560313, 'Positioning': 0.35351485811275446, 'Stamina': 0.2652851885173583}}, 'Goalkeeper': {'key': {'Aerial Reach': 0.9835970935513371, 'Command of Area': 0.8739828065687891, 'Communication': 0.8670689253148726, 'Eccentricity': 0.7782548709443468, 'Handling': 1.0, 'Kicking': 0.8705183025099135, 'One on Ones': 0.7710791345643447, 'Punching': 0.8781172266482801, 'Reflexes': 0.9441503723523842, 'Throwing': 0.7743472205585}, 'normal': {'Bravery': 0.2882385182784699, 'Jumping Reach': 0.21849378826247473}}, 'Half Back': {'key': {'Composure': 1.0, 'Concentration': 0.7989410755908665, 'Marking': 0.9286359513520137, 'Positioning': 0.7958895857393652, 'Teamwork': 0.8997812985183861}, 'normal': {'Aggression': 0.2902908342494054, 'Anticipation': 0.6695430754004139, 'Balance': 0.6116342985498875, 'Bravery': 0.681164699707445, 'Corners': 0.4074475644790179, 'Crossing': 0.2963177722246063, 'Decisions': 0.43141898741376355, 'First Touch': 0.39488551488792717, 'Free Kick Taking': 0.563845438093789, 'Heading': 0.6705075606700935, 'Jumping Reach': 0.6789080462134233, 'Leadership': 0.39098492093478565, 'Long Shots': 0.6031133762851911, 'Long Throws': 0.4723002073480152, 'Off the Ball': 0.30112117369671587, 'Passing': 0.5771458448874132, 'Penalty Taking': 0.5580827156090256, 'Stamina': 0.4206893877189369, 'Strength': 0.6854248960495897, 'Tackling': 0.6372299260115966, 'Technique': 0.30832852716075637, 'Vision': 0.5302961847601249, 'Work Rate': 0.5959798752576523}}, 'Inside Forward': {'key': {'Balance': 1.0, 'Finishing': 0.8830539132357959, 'Flair': 0.7860689812983492}, 'normal': {'Acceleration': 0.3039110653816904, 'Agility': 0.38999616073557586, 'Anticipation': 0.21795798324355892, 'Composure': 0.46041408037359993, 'Corners': 0.4007763824521409, 'Crossing': 0.4257568111940918, 'Dribbling': 0.6692752226023251, 'First Touch': 0.58629526858671, 'Free Kick Taking': 0.4879692697578368, 'Long Shots': 0.6521807173026735, 'Off the Ball': 0.525083857519685, 'Pace': 0.3705546888188956, 'Penalty Taking': 0.6337274652206157, 'Technique': 0.47891126188295896, 'Vision': 0.24672216976916025}}, 'Inverted Wing-Back': {'key': {'Long Throws': 0.9200983088967949, 'Tackling': 1.0}, 'normal': {'Acceleration': 0.363094103811204, 'Agility': 0.26225507041260765, 'Marking': 0.6582949844691263, 'Pace': 0.3015847918118984, 'Positioning': 0.2201439331968717, 'Stamina': 0.46636665845133174, 'Teamwork': 0.22911318378523787}}, 'Inverted Winger': {'key': {'Corners': 0.8359768722052128, 'Crossing': 0.9197138275122314, 'Dribbling': 1.0, 'Flair': 0.9964066040646132, 'Free Kick Taking': 0.7242747170613328, 'Off the Ball': 0.7636125573502647, 'Technique': 0.75320759942032}, 'normal': {'Acceleration': 0.46782596507499896, 'Agility': 0.4018989646979325, 'Balance': 0.2696032357199374, 'Composure': 0.3608876634043415, 'Finishing': 0.6867795105287346, 'First Touch': 0.5470280320683677, 'Long Shots': 0.6918883612191659, 'Long Throws': 0.2114543482257865, 'Pace': 0.42070745585329644, 'Passing': 0.5581707442588362, 'Penalty Taking': 0.62149909583457, 'Stamina': 0.2500445319332133, 'Teamwork': 0.21993298647307297, 'Vision': 0.5718591095417231, 'Work Rate': 0.24786159755808007}}, 'Libero': {'key': {'Balance': 0.7759009519556731, 'Composure': 0.7654068215653171, 'Concentration': 0.758214673433776, 'Long Throws': 0.7619328681234795, 'Teamwork': 1.0, 'Vision': 0.8456852052190382}, 'normal': {'Anticipation': 0.5265370559849867, 'Bravery': 0.6061469915149152, 'Corners': 0.34681032419512453, 'Crossing': 0.31169535893761446, 'Dribbling': 0.5088925559745516, 'First Touch': 0.4830603817083382, 'Flair': 0.2894941988392857, 'Free Kick Taking': 0.4385723095801909, 'Heading': 0.5117408529555445, 'Jumping Reach': 0.42440941592638426, 'Leadership': 0.4262189822608872, 'Long Shots': 0.5271806151457294, 'Marking': 0.6861763112266281, 'Off the Ball': 0.31051326164603116, 'Passing': 0.6702664773896552, 'Penalty Taking': 0.6094110901651004, 'Positioning': 0.595340627562716, 'Stamina': 0.5531600974775726, 'Strength': 0.5941434527760322, 'Tackling': 0.483301522890906, 'Technique': 0.5037724466658703, 'Work Rate': 0.5770553449690605}}, 'Mezzala': {'key': {'Technique': 0.8120896221704059, 'Vision': 1.0, 'Work Rate': 0.7996739620393426}, 'normal': {'Acceleration': 0.6272037817404937, 'Agility': 0.28852998019044207, 'First Touch': 0.37217220706396004, 'Long Shots': 0.628879726148404, 'Pace': 0.3462816853582398, 'Passing': 0.6827081796680216}}, 'No-Nonsense Centre-Back': {'key': {'Heading': 0.840239990223303, 'Jumping Reach': 0.7239983018023828, 'Marking': 1.0, 'Positioning': 0.7642751658886436, 'Tackling': 0.7888499197866733}, 'normal': {'Aggression': 0.5232349824321194, 'Anticipation': 0.2561431212869097, 'Balance': 0.23167304520923443, 'Bravery': 0.5012172564334875, 'Concentration': 0.23635599825033743, 'Leadership': 0.22849490696735997, 'Strength': 0.6366518737870988}}, 'No-Nonsense Full-Back': {'key': {'Long Throws': 1.0, 'Marking': 0.9266727094852679, 'Strength': 0.9619488237408168, 'Tackling': 0.8752257681045025}, 'normal': {'Aggression': 0.5784464092746514, 'Anticipation': 0.29387665206180413, 'Balance': 0.5084206067306505, 'Bravery': 0.6604457361057252, 'Concentration': 0.25193223571263473, 'Heading': 0.6545614415929665, 'Jumping Reach': 0.5015516956797662, 'Leadership': 0.29578688716928764, 'Positioning': 0.6507881252320905, 'Stamina': 0.35033129411620484, 'Teamwork': 0.47958610751960873, 'Work Rate': 0.2790281999155527}}, 'Poacher': {'key': {'Finishing': 1.0}, 'normal': {'Composure': 0.280948068431519, 'Dribbling': 0.4160721525623608, 'First Touch': 0.23304137572125602, 'Flair': 0.3870731402275918, 'Heading': 0.5998290939544968, 'Off the Ball': 0.5823192032885135}}, 'Pressing Forward': {'key': {'Finishing': 1.0, 'Off the Ball': 0.7579805820306506, 'Penalty Taking': 0.9649902712765912, 'Work Rate': 0.7825577531974992}, 'normal': {'Acceleration': 0.3072568948411612, 'Aggression': 0.5866382903897985, 'Anticipation': 0.41557702537252866, 'Balance': 0.684167014441947, 'Bravery': 0.6599063907850781, 'Composure': 0.3943052532828373, 'Concentration': 0.3333579130297736, 'Crossing': 0.2401179836128624, 'Determination': 0.23294214742500824, 'Dribbling': 0.5199201356659464, 'First Touch': 0.21022855966653714, 'Flair': 0.6385644326329195, 'Free Kick Taking': 0.39703371121345654, 'Heading': 0.5724721992006949, 'Jumping Reach': 0.26529724759832485, 'Long Shots': 0.5811209303497409, 'Pace': 0.48106254401844745, 'Stamina': 0.6483082440193247, 'Strength': 0.6679313745949632, 'Teamwork': 0.677727160532064, 'Technique': 0.26333951260851796, 'Vision': 0.2902328240131502}}, 'Raumdeuter': {'key': {'Anticipation': 0.8763730842360247, 'Balance': 0.8572303278380711, 'Composure': 0.942201692633598, 'Concentration': 0.9467519488691731, 'Finishing': 1.0, 'Off the Ball': 0.7632517331212589, 'Penalty Taking': 0.9169175440421102, 'Teamwork': 0.7442950901573008, 'Work Rate': 0.7500776299008024}, 'normal': {'Acceleration': 0.20026414332745512, 'Agility': 0.3172497315027354, 'Bravery': 0.5345469950378268, 'Corners': 0.6067808839092007, 'Crossing': 0.5295523408990693, 'Decisions': 0.49574380053110795, 'Determination': 0.24136861477628713, 'Dribbling': 0.5080336813465178, 'First Touch': 0.4247747817865459, 'Flair': 0.438091038368162, 'Free Kick Taking': 0.5006404512379418, 'Heading': 0.6234991598302109, 'Jumping Reach': 0.5190853512318513, 'Long Shots': 0.6312745043478925, 'Long Throws': 0.29483990812363975, 'Pace': 0.2425436958015974, 'Passing': 0.41744072964108997, 'Stamina': 0.44966309142631283, 'Strength': 0.6095618069109802, 'Technique': 0.5467102746622186, 'Vision': 0.5725228882317112}}, 'Regista': {'key': {'Corners': 0.9566904392448964, 'Flair': 0.7757582201258315, 'Free Kick Taking': 1.0, 'Long Shots': 0.8223203861742016, 'Penalty Taking': 0.7739006832112106, 'Vision': 0.8192246018024527}, 'normal': {'Agility': 0.20633521854440057, 'Anticipation': 0.4577366365896617, 'Balance': 0.5014807557922115, 'Bravery': 0.29913351704394614, 'Composure': 0.6327503787517357, 'Concentration': 0.4262010122514119, 'Crossing': 0.6382998749444254, 'Dribbling': 0.6560555490900143, 'Finishing': 0.34409887641181114, 'First Touch': 0.5269040745320177, 'Off the Ball': 0.3977559392405798, 'Passing': 0.6160374429833628, 'Stamina': 0.2577970646832643, 'Strength': 0.3053072666419902, 'Teamwork': 0.5423353309527091, 'Technique': 0.6839348126248058, 'Work Rate': 0.244413621108833}}, 'Roaming Playmaker': {'key': {'Composure': 0.7082135830916353, 'Corners': 0.9930052945790776, 'Free Kick Taking': 1.0, 'Long Shots': 0.8491807638614464, 'Penalty Taking': 0.7904451026054871, 'Teamwork': 0.7449499067123632, 'Vision': 0.7578238978779823}, 'normal': {'Acceleration': 0.23839753984150305, 'Agility': 0.3962560426516467, 'Anticipation': 0.5591060872682043, 'Balance': 0.6162417938366931, 'Bravery': 0.3298721176311701, 'Concentration': 0.6783476705206487, 'Crossing': 0.6717537829472707, 'Dribbling': 0.5971493933279314, 'Finishing': 0.49685666098685255, 'First Touch': 0.4745892654901525, 'Flair': 0.6267962069412629, 'Off the Ball': 0.5813994474975915, 'Pace': 0.28543172620052537, 'Passing': 0.6466925480456401, 'Positioning': 0.28889860549397955, 'Stamina': 0.5944095623123294, 'Strength': 0.33741268773644506, 'Technique': 0.5938631668757401, 'Work Rate': 0.6133402719805142}}, 'Segundo Volante': {'key': {'Long Shots': 0.721155266433764, 'Marking': 0.8039033185196431, 'Passing': 0.7401438157047582, 'Positioning': 0.8313201620569328, 'Tackling': 1.0, 'Work Rate': 0.7615533759929987}, 'normal': {'Acceleration': 0.4817906346225551, 'Agility': 0.3941590171733612, 'First Touch': 0.3836842765341825, 'Free Kick Taking': 0.31555056232453993, 'Pace': 0.5960772474691656, 'Stamina': 0.5379534882412248, 'Technique': 0.23600753537189464, 'Vision': 0.4382701482596025}}, 'Shadow Striker': {'key': {'Dribbling': 0.7363192970940071, 'Finishing': 1.0}, 'normal': {'Acceleration': 0.564949834214364, 'Agility': 0.33596022203177794, 'Composure': 0.3400276564603119, 'Corners': 0.23161617221684688, 'First Touch': 0.6509554572569254, 'Flair': 0.6416714125994452, 'Free Kick Taking': 0.2766995701456801, 'Long Shots': 0.4112958975865404, 'Off the Ball': 0.533873420073048, 'Pace': 0.4447103759530486, 'Technique': 0.3759425244904911, 'Vision': 0.47385870848640116}}, 'Sweeper Keeper': {'key': {'Aerial Reach': 0.841465694053063, 'Command of Area': 0.9316931538164355, 'Communication': 0.8740183932417253, 'Eccentricity': 0.7228618079852775, 'Handling': 0.8692008790411215, 'Kicking': 0.9382055376333968, 'One on Ones': 1.0, 'Punching': 0.8985506803200892, 'Reflexes': 0.9689270712387903, 'Throwing': 0.886299295108467}, 'normal': {'Bravery': 0.307399261357657, 'Jumping Reach': 0.22292797372174575}}, 'Target Forward': {'key': {'Balance': 0.8626803117645949, 'Finishing': 0.7916566065915424, 'Heading': 0.8602838741728257, 'Jumping Reach': 0.8121959871869346, 'Penalty Taking': 0.8623464675600534, 'Strength': 1.0}, 'normal': {'Anticipation': 0.34265897896321124, 'Bravery': 0.5796432435849294, 'Composure': 0.4254612128395665, 'Concentration': 0.33546379948996763, 'Dribbling': 0.3009514228752778, 'Free Kick Taking': 0.32355083423231007, 'Long Shots': 0.492196478204319, 'Off the Ball': 0.513962725474587, 'Stamina': 0.29351920521642655, 'Teamwork': 0.4840205730759351, 'Vision': 0.21706055700923416, 'Work Rate': 0.3417913378052922}}, 'Trequartista': {'key': {'Balance': 0.7767478674115305, 'Corners': 0.7343571875113589, 'Dribbling': 0.774500192941238, 'Finishing': 0.7693221618589532, 'Flair': 0.8771084757269614, 'Free Kick Taking': 0.7618327686221932, 'Long Shots': 0.7557119821735929, 'Penalty Taking': 1.0, 'Technique': 0.740072516259401, 'Vision': 0.7824721975439989}, 'normal': {'Acceleration': 0.28352928203215805, 'Agility': 0.38992674842782127, 'Anticipation': 0.5780621227325476, 'Composure': 0.649038506944419, 'Crossing': 0.6300569529986999, 'First Touch': 0.5813895183426432, 'Heading': 0.40934592793781116, 'Off the Ball': 0.566828623964076, 'Pace': 0.2798081565323918, 'Passing': 0.5762755740575526, 'Stamina': 0.30752807315821956, 'Strength': 0.5554245204331161}}, 'Wide Centre-Back': {'key': {'Balance': 0.7581181078191432, 'Crossing': 0.7711631862615137, 'Heading': 0.8511795649599334, 'Jumping Reach': 0.733009636249727, 'Long Throws': 0.8816142351452464, 'Marking': 0.9023885844727448, 'Positioning': 0.7316112634724954, 'Stamina': 0.8128786004589278, 'Strength': 1.0, 'Tackling': 0.7457969593095882, 'Teamwork': 0.7163468299945003}, 'normal': {'Aggression': 0.30730186649746666, 'Anticipation': 0.6044049838602019, 'Bravery': 0.6819063088335542, 'Composure': 0.5780897321741174, 'Concentration': 0.5887572604661169, 'Corners': 0.2912080035461647, 'Determination': 0.2137370963370792, 'Dribbling': 0.4360002778171413, 'First Touch': 0.2715156122363842, 'Flair': 0.2015930718390826, 'Free Kick Taking': 0.3388302826176563, 'Leadership': 0.4265427591770235, 'Long Shots': 0.34619194413617704, 'Off the Ball': 0.3423568983057376, 'Pace': 0.21953144390169574, 'Passing': 0.41115336553794796, 'Penalty Taking': 0.46953305468227446, 'Technique': 0.3700064383527651, 'Vision': 0.46549908458437866, 'Work Rate': 0.6198202778889922}}, 'Wide Midfielder': {'key': {'Decisions': 0.7413492008002746, 'Passing': 0.7074466402606334, 'Teamwork': 0.8684961979926145, 'Work Rate': 1.0}, 'normal': {'Crossing': 0.4479936148579287, 'Long Throws': 0.31968650142417937, 'Stamina': 0.2672697752107242, 'Tackling': 0.47494160082304737, 'Vision': 0.24189497690562878}}, 'Wide Playmaker': {'key': {'Composure': 0.7671366808263143, 'Corners': 1.0, 'Crossing': 0.7815902893281343, 'Free Kick Taking': 0.9061772696892473, 'Penalty Taking': 0.7608016163525626, 'Teamwork': 0.7659829843163333, 'Vision': 0.8985000658626286}, 'normal': {'Anticipation': 0.5014406780390435, 'Balance': 0.49681281242376746, 'Concentration': 0.5382292618022295, 'Decisions': 0.47937721187681265, 'Dribbling': 0.6067388874313702, 'Finishing': 0.45820346039454185, 'First Touch': 0.6074332492521043, 'Flair': 0.6009827141247347, 'Leadership': 0.25629062137523984, 'Long Shots': 0.6710371167694966, 'Long Throws': 0.34424863976010434, 'Off the Ball': 0.5282382474083032, 'Passing': 0.699609091615721, 'Stamina': 0.21721466311365042, 'Strength': 0.24074766334209227, 'Technique': 0.6814896801102301, 'Work Rate': 0.3620736093736802}}, 'Wide Target Forward': {'key': {'Heading': 0.7175462986671572, 'Jumping Reach': 0.8311755449679133, 'Penalty Taking': 0.7361527927920805, 'Strength': 1.0}, 'normal': {'Balance': 0.5984416326492019, 'Bravery': 0.6577281513500574, 'Composure': 0.20743644236024372, 'Concentration': 0.21870807442628074, 'Crossing': 0.3728074954247613, 'Dribbling': 0.2216165814005176, 'Finishing': 0.5971973188323533, 'Flair': 0.27023539725499657, 'Free Kick Taking': 0.2587298941023734, 'Long Shots': 0.45757942284568903, 'Long Throws': 0.33479526186772984, 'Off the Ball': 0.47787046221463975, 'Stamina': 0.3767241736498674, 'Teamwork': 0.5143460385133521, 'Work Rate': 0.5077414875214131}}, 'Wing-Back': {'key': {'Long Throws': 1.0}, 'normal': {'Acceleration': 0.5521703182572522, 'Agility': 0.336782323317464, 'Anticipation': 0.2093138846753566, 'Balance': 0.36525027499120855, 'Bravery': 0.36606600816793167, 'Composure': 0.20075509974802583, 'Concentration': 0.31232593325105473, 'Corners': 0.3688064927438776, 'Crossing': 0.6548815919050556, 'Dribbling': 0.39760897629855235, 'Marking': 0.5528120389013897, 'Off the Ball': 0.3386798327582568, 'Pace': 0.4654333010953049, 'Passing': 0.24370190319853707, 'Positioning': 0.31815781274098043, 'Stamina': 0.6762503918456342, 'Strength': 0.22897423726415012, 'Tackling': 0.5993961767143947, 'Teamwork': 0.6930446289351614, 'Technique': 0.3093556260062465, 'Vision': 0.2077213094285797, 'Work Rate': 0.6173120282462075}}, 'Winger': {'key': {'Crossing': 1.0, 'Dribbling': 0.8416849292040979, 'Flair': 0.8012365887085868}, 'normal': {'Acceleration': 0.6183815953511931, 'Agility': 0.37926588294400004, 'Corners': 0.5360974154829397, 'Finishing': 0.32224483718748453, 'First Touch': 0.3912066912591298, 'Free Kick Taking': 0.28435469261965335, 'Off the Ball': 0.5068150066115477, 'Pace': 0.611540522319051, 'Technique': 0.48896857760596807}}}

ROLE_GROUPS = {
    'GK': [
        'Goalkeeper', 'Sweeper Keeper'
    ],
    'Defender': [
        'Ball Playing Defender', 'Central Defender', 'Libero', 'No-Nonsense Centre-Back', 
        'Wide Centre-Back', 'Complete Wing-Back', 'Full-Back', 'Inverted Wing-Back', 
        'No-Nonsense Full-Back', 'Wing-Back', 'Anchor', 'Defensive Midfielder', 'Half Back' # DM role są często grane przez DMs
    ],
    'Midfielder': [
        'Advanced Playmaker', 'Anchor', 'Attacking Midfielder', 'Ball Winning Midfielder', 
        'Box To Box Midfielder', 'Carrilero', 'Central Midfielder', 'Deep Lying Playmaker', 
        'Defensive Midfielder', 'Defensive Winger', 'Enganche', 'Half Back', 'Inside Forward', 
        'Inverted Winger', 'Mezzala', 'Raumdeuter', 'Regista', 'Roaming Playmaker', 
        'Segundo Volante', 'Shadow Striker', 'Trequartista', 'Wide Midfielder', 'Wide Playmaker', 
        'Winger'
    ],
    'Striker': [
        'Advanced Forward', 'Complete Forward', 'Deep Lying Forward', 'False Nine', 
        'Poacher', 'Pressing Forward', 'Target Forward', 'Wide Target Forward', 'Inside Forward', 'Shadow Striker', 'Trequartista', 'Raumdeuter' # Role AM/Winger, które są też ST
    ]
}

def get_position_group(position_string):

    if not isinstance(position_string, str):
        return None
        
    pos = position_string.upper()
    
    if 'ST' in pos:
        return 'Striker'
    if 'AM' in pos or 'M (' in pos:
        return 'Midfielder'
    if 'DM' in pos:

        if 'D (C)' in pos:
             return 'Defender' 
        return 'Midfielder'
    if 'D (' in pos or 'WB' in pos:
        return 'Defender'
    if 'GK' in pos:
        return 'GK'
        
    return None

def convert_attr_name(attr):

    special_cases = {
        'Free Kick Taking': 'free_kicks',
        'Jumping Reach': 'jump',
        'Aerial Reach': 'aerial_reach',
        'Command of Area': 'command_of_area',
        'Communication': 'communication',
        'Eccentricity': 'eccentricity',
        'One on Ones': 'one_on_ones',
        'Punching': 'punching',
        'Reflexes': 'reflexes',
        'Throwing': 'throwing',
        'Handling': 'handling',
        'Kicking': 'kicking'
    }
    
    if attr in special_cases:
        return special_cases[attr]
    
    return attr.lower().replace(' ', '_')

def fit_player(player, role, roles_weight):
    
    MAX_ATTRIBUTE_VALUE = 20
    
    if role not in roles_weight:
        return 0 

    key_stats = roles_weight[role]['key']
    normal_stats = roles_weight[role]['normal']

    num = 0
    for attr, weight in key_stats.items():
        converted_attr = convert_attr_name(attr)
        value = player.get(converted_attr, 0)
        num += float(value) * weight
    
    for attr, weight in normal_stats.items():
        converted_attr = convert_attr_name(attr)
        value = player.get(converted_attr, 0)
        num += float(value) * weight
    
    divider = sum(MAX_ATTRIBUTE_VALUE * weight for weight in key_stats.values())
    divider += sum(MAX_ATTRIBUTE_VALUE * weight for weight in normal_stats.values())
    
    if divider == 0:
        return 0 

    score = (num / divider) * 100
    return score

CSV_HEADER = [
    'name', 'position', 'best_role', 'corners', 'crossing', 'dribbling', 'finishing',
    'first_touch', 'free_kicks', 'heading', 'long_shots', 'long_throws',
    'marking', 'passing', 'penalty_taking', 'tackling', 'technique',
    'aggression', 'anticipation', 'bravery', 'composure', 'concentration',
    'decisions', 'determination', 'flair', 'leadership', 'off_the_ball',
    'positioning', 'teamwork', 'vision', 'work_rate', 'acceleration',
    'pace', 'agility', 'balance', 'jump', 'stamina', 'strength',
    'natural_fitness', 
    'aerial_reach', 'command_of_area', 
    'communication', 'eccentricity', 'handling', 'kicking', 'one_on_ones', 
    'punching', 'reflexes', 'throwing'
]



def index(request):
    return render(request, 'index.html')

def player_analysis(request):
    return render(request, 'player_analysis.html')


def add_player(request):
    if request.method == "POST":
        player_data_for_csv = []
        temp_player_for_calc = {}
        
        for field in CSV_HEADER:
            if field == 'best_role':
                continue 
            
            value = request.POST.get(field, 0)
            
            if field not in ['name', 'position']:
                if value == '' or value is None:
                    value = 0
                try:
                    numeric_value = float(value)
                except ValueError:
                    numeric_value = 0.0
                
                player_data_for_csv.append(numeric_value)
                temp_player_for_calc[field] = numeric_value
            else:
                player_data_for_csv.append(value)
                if field == 'position':
                    temp_player_for_calc[field] = value
                
        
        best_role_name = "Unknown"
        best_score = 0
        
        player_series = pd.Series(temp_player_for_calc) 
        
        player_position_str = temp_player_for_calc.get('position', '') 
        player_group = get_position_group(player_position_str)

        if player_group and player_group in ROLE_GROUPS:
            roles_to_check = ROLE_GROUPS[player_group]
        else:
            roles_to_check = ROLES_WEIGHT.keys() 
        
        for role in roles_to_check:
            if role in ROLES_WEIGHT: 
                score = fit_player(player_series, role, ROLES_WEIGHT)
                if score > best_score:
                    best_score = score
                    best_role_name = role
        
        player_data_for_csv.insert(2, best_role_name) 
        
        file_exists = os.path.exists("players.csv")
        with open("players.csv", "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(CSV_HEADER)
            writer.writerow(player_data_for_csv)

        player_name = player_data_for_csv[0] 
        return redirect('player_detail', player_name=player_name)
    
    return redirect('player_analysis')


def import_player(request):
    if request.method == "POST":
        if not request.FILES.get("player_file"):
            return render(request, "player_analysis.html", {
                "error": "Nie wybrano pliku.",
                "show_error": True
            })

        player_file = request.FILES["player_file"]
        
        try:
            if not player_file.name.endswith('.csv'):
                return render(request, "player_analysis.html", {
                    "error": "Nieprawidłowy format pliku. Tylko pliki CSV są obsługiwane.",
                    "show_error": True
                })
            
            decoded_file = io.TextIOWrapper(player_file.file, encoding='utf-8')
            reader = csv.reader(decoded_file)
            
            imported_header = next(reader)
            

            player_file.file.seek(0)
            decoded_file_dict = io.TextIOWrapper(player_file.file, encoding='utf-8')
            dict_reader = csv.DictReader(decoded_file_dict)
            
            try:
                player_data_dict = next(dict_reader)
            except StopIteration:
                return render(request, "player_analysis.html", {
                    "error": "Plik CSV jest pusty (nie zawiera danych).",
                    "show_error": True
                })

            if 'name' not in player_data_dict or 'position' not in player_data_dict:
                 return render(request, "player_analysis.html", {
                    "error": "Plik CSV nie zawiera wymaganych kolumn 'name' i 'position'.",
                    "show_error": True
                })

            temp_player_for_calc = {}
            for field in CSV_HEADER:
                if field not in ['name', 'position', 'best_role']:
                    value = player_data_dict.get(field, 0)
                    if value == '' or value is None:
                        value = 0
                    try:
                        numeric_value = float(value)
                    except ValueError:
                        numeric_value = 0.0
                    temp_player_for_calc[field] = numeric_value
                elif field == 'position':
                    temp_player_for_calc[field] = player_data_dict.get(field, '')

            player_series = pd.Series(temp_player_for_calc)
            best_role_name = "Unknown"
            best_score = 0
            
            player_position_str = temp_player_for_calc.get('position', '')
            player_group = get_position_group(player_position_str)

            if player_group and player_group in ROLE_GROUPS:
                roles_to_check = ROLE_GROUPS[player_group]
            else:
                roles_to_check = ROLES_WEIGHT.keys()

            for role in roles_to_check:
                if role in ROLES_WEIGHT:
                    score = fit_player(player_series, role, ROLES_WEIGHT)
                    if score > best_score:
                        best_score = score
                        best_role_name = role
            
            final_player_data = []
            for field in CSV_HEADER:
                if field == 'best_role':
                    final_player_data.append(best_role_name)
                else:
                    final_player_data.append(player_data_dict.get(field, 0))

            file_exists = os.path.exists("players.csv")
            with open("players.csv", "a", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                if not file_exists:
                    writer.writerow(CSV_HEADER)
                writer.writerow(final_player_data)
            
            player_name = final_player_data[0] 
            return redirect('player_detail', player_name=player_name)

            
        except Exception as e:
            return render(request, "player_analysis.html", {
                "error": f"Błąd podczas odczytu pliku: {str(e)}",
                "show_error": True
            })

    return redirect('player_analysis')


def player_detail(request, player_name):
    csv_file = 'players.csv' 
    if not os.path.exists(csv_file):
        return render(request, 'player_detail.html', {
            'error': 'Brak danych do analizy. Najpierw dodaj zawodnika.'
        })
    
    try:
        df_players = pd.read_csv(csv_file)
    except pd.errors.EmptyDataError:
        return render(request, 'player_detail.html', {
            'error': 'Plik z danymi jest pusty. Dodaj zawodnika.'
        })

    for col in CSV_HEADER:
        if col not in ['name', 'position', 'best_role']:
            if col in df_players.columns:
                df_players[col] = pd.to_numeric(df_players[col], errors='coerce').fillna(0)
            else:
                df_players[col] = 0

    player_row_series = df_players[df_players['name'] == player_name]
    
    if player_row_series.empty:
        if not df_players.empty:
            player_series = df_players.iloc[-1]
            player_name_found = player_series.get('name', 'Nieznany')
            error_msg = f'Nie znaleziono zawodnika "{player_name}". Wyświetlam ostatnio dodanego: "{player_name_found}"'
        else:
            return render(request, 'player_detail.html', {
                'error': f'Nie znaleziono zawodnika {player_name} ani żadnego innego.'
            })
    else:
        player_series = player_row_series.iloc[0]
        error_msg = None
    
    player_data = player_series.to_dict()
    
    if not ROLES_WEIGHT:
        return render(request, 'player_detail.html', {
            'player': player_data,
            'error': "BŁĄD: Wagi ról nie są zdefiniowane."
        })


    all_fit_scores_position = {}
    player_position_str = player_data.get('position', '')
    player_group = get_position_group(player_position_str)
    
    if player_group and player_group in ROLE_GROUPS:
        roles_to_check = ROLE_GROUPS[player_group]
    else:
        roles_to_check = ROLES_WEIGHT.keys() # Fallback

    for role in roles_to_check:
        if role in ROLES_WEIGHT:
            score = fit_player(player_series, role, ROLES_WEIGHT)
            all_fit_scores_position[role] = round(score, 2)
            
    sorted_scores_position = sorted(all_fit_scores_position.items(), key=lambda item: item[1], reverse=True)

    all_fit_scores_overall = {}
    for role in ROLES_WEIGHT.keys():
        score = fit_player(player_series, role, ROLES_WEIGHT)
        all_fit_scores_overall[role] = round(score, 2)
        
    sorted_scores_overall = sorted(all_fit_scores_overall.items(), key=lambda item: item[1], reverse=True)

    context = {
        'player': player_data,
        'sorted_scores': sorted_scores_position, # <-- Główna lista do wyświetlenia
        'sorted_scores_overall': sorted_scores_overall, # <-- Opcjonalna lista
        'error': error_msg
    }

    return render(request, 'player_detail.html', context)

