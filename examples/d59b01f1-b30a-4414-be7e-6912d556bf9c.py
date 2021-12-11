# This program was generated by "Generative Art Synthesizer" 
# Generation date: 2021-11-28 04:17:38 UTC 
# GAS change date: 2021-11-28 03:58:45 UTC 
# GAS md5 hash: fa4b9db8bcdb760d7fde2be64723fca2 
# Python version: 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)] 
# For more information visit: https://github.com/volotat/GAS

#import python libraries 
import os #OS version: default 
import numpy as np #Numpy version: 1.19.5 
from PIL import Image #PIL version: 8.1.2 

#set initial params
SIZE = 768 
GRID_CHANNELS = 16 

def test_values(arr):
    if np.isnan(arr).any():
        raise Exception('Array has None elements!') 
        
    if np.amin(arr) < -1 or np.amax(arr) > 1:
        raise Exception('Values went to far! [ %.2f : %.2f ]'%(np.amin(arr), np.amax(arr)) ) 
           
    return arr

#define grid transformation methods

def transit(x, t_indx, s_indx, alphas):
    res = x.copy()
    res[:,:,t_indx] = np.sum(x[:,:,s_indx] * alphas, axis = -1)
    return test_values(res.clip(-1,1)) 

def sin(x, t_indx, s_indx, scale = 1, shift = 0): 
    res = x.copy()
    res[:,:,t_indx] = np.sin(x[:,:,s_indx] * 0.5 * np.pi * scale + shift)
    return test_values(res)     

def magnitude(x, t_indx, s_indx, ord = 2): 
    res = x.copy()
    res[:,:,t_indx] = np.linalg.norm(x[:,:,s_indx], axis = -1, ord = ord) / np.sqrt(len(s_indx))
    return test_values(res)   

def shift(x, t_indx, s_indx, shift):
    res = x.copy()
    if shift > 0: res[:,:,t_indx] = (-np.abs(((x[:,:,s_indx] + 1) / 2) ** (1 + shift) - 1) ** (1 / (1 + shift)) + 1) * 2 - 1
    if shift < 0: res[:,:,t_indx] = np.abs((1 - (x[:,:,s_indx] + 1) / 2) ** (1 - shift) - 1) ** (1 / (1 - shift)) * 2 - 1  
    return test_values(res) 

def inverse(x, t_indx, s_indx): 
    res = x.copy()
    res[:,:,t_indx] = -x[:,:,s_indx] 
    return test_values(res)   

def smooth_max(x, t_indx, s1_indx, s2_indx, p = 10): 
    res = x.copy()
    res[:,:,t_indx] = np.log((np.exp(x[:,:,s1_indx] * p) + np.exp(x[:,:,s2_indx] * p)) ** (1/p)) / 1.07
    return test_values(res)   

def smooth_min(x, t_indx, s1_indx, s2_indx, p = 10): 
    res = x.copy()
    res[:,:,t_indx] = -np.log((np.exp(-x[:,:,s1_indx] * p) + np.exp(-x[:,:,s2_indx] * p)) ** (1/p)) / 1.07
    return test_values(res)   

def shift_mod_abs(x, t_indx, s_indx, shift):
    res = x.copy()
    res[:,:,t_indx] = np.abs(np.mod((x[:,:,s_indx] + 3)/4 + shift/2, 1) * 2 - 1) * 2 - 1
    return test_values(res) 

#set initial grid
grid = np.zeros((SIZE, SIZE, GRID_CHANNELS))

x = ((np.arange(SIZE)/(SIZE-1) - 0.5) * 2).reshape((1, SIZE)).repeat(SIZE, 0)
y = ((np.arange(SIZE)/(SIZE-1) - 0.5) * 2).reshape((SIZE, 1)).repeat(SIZE, 1)

grid[:,:,0] = (x * 0.8643418060594885 + y * 0.6002740205725097) / 2 
grid[:,:,1] = (x * 0.01183721078650768 + y * -0.7074877558164501) / 2 
grid[:,:,2] = (x * -0.48643728170863887 + y * 0.7203274908191206) / 2 
grid[:,:,3] = (x * 0.7658582693960334 + y * 0.14941321785247208) / 2 
grid[:,:,4] = (x * 0.9210916218391232 + y * 0.37140846720931764) / 2 
grid[:,:,5] = (x * 0.39136156737873007 + y * -0.06549676689056216) / 2 
grid[:,:,6] = (x * 0.9324751771973863 + y * -0.19588844971222885) / 2 
grid[:,:,7] = (x * 0.06023978890473192 + y * -0.6815582001062757) / 2 
grid[:,:,8] = (x * -0.6993118954667219 + y * 0.961464040384854) / 2 
grid[:,:,9] = (x * 0.37138346094417707 + y * -0.7566733584213707) / 2 
grid[:,:,10] = (x * 0.3387057689135291 + y * 0.25721938764502617) / 2 
grid[:,:,11] = (x * 0.12753054557270316 + y * -0.3413646845394549) / 2 
grid[:,:,12] = (x * -0.21127520837749425 + y * -0.43789418122650203) / 2 
grid[:,:,13] = (x * -0.7360271671180054 + y * -0.5198570345042122) / 2 
grid[:,:,14] = (x * -0.2137488758947239 + y * 0.7151440164025549) / 2 
grid[:,:,15] = (x * 0.525452161570175 + y * 0.5170838810547953) / 2 

#apply transformations to the grid
grid = sin(grid, 2, 8, 0.25835015172321396, 21.926278243121033)
grid = sin(grid, 9, 2, -2.0587278631511223, -13.714042922610375)
grid = sin(grid, 2, 6, 1.7139745932070736, -4.643371114330151)
grid = transit(grid, 10, [5], [1.0])
grid = inverse(grid, 14, 4)
grid = transit(grid, 3, [15, 2, 4], [0.03247658803244306, 0.38545593380145043, 0.5820674781661065])
grid = magnitude(grid, 15, [15, 11], 2)
grid = sin(grid, 15, 15, -3.253602321442124, -3.0985528409208882)
grid = magnitude(grid, 6, [10, 11, 5, 0, 1, 6], 2)
grid = sin(grid, 3, 1, 1.1235142164006418, 1.51467460366068)
grid = sin(grid, 8, 11, -3.37504357213741, 44.68116651400874)
grid = sin(grid, 7, 14, 0.4447217762204615, 93.13418937590188)
grid = transit(grid, 6, [6, 12, 15, 3, 7, 4, 10], [0.06297423637167997, 0.03744988443931329, 0.3650503980527056, 0.09940753870849321, 0.1221871068090384, 0.1794107207938837, 0.13352011482488577])
grid = transit(grid, 6, [1, 8, 15, 10, 5], [0.10050817394019121, 0.040893968335904814, 0.47121559436798194, 0.12456955105829291, 0.2628127122976291])
grid = transit(grid, 11, [8, 9, 10, 1], [0.1741870817351788, 0.4296821339947654, 0.2592226287922774, 0.13690815547777838])
grid = sin(grid, 9, 11, 6.097916247045983, -70.8957881028912)
grid = sin(grid, 4, 15, -2.339002647277993, 41.615905892741296)
grid = sin(grid, 8, 11, 1.2434848286606566, 21.6237943811725)
grid = transit(grid, 11, [15, 9], [0.070251274216773, 0.9297487257832269])
grid = sin(grid, 15, 11, -0.8555545495423866, -79.31183209188053)
grid = transit(grid, 1, [2, 11, 5, 10, 1, 14, 0], [0.22879040917375634, 0.021771653373915942, 0.08945373188395699, 0.03139252269478689, 0.13974229914963618, 0.0006454380025782731, 0.48820394572136944])
grid = sin(grid, 13, 12, -1.0802856451916583, 72.77003783382975)
grid = shift_mod_abs(grid, 3, 1, -0.012532722033949506)
grid = shift(grid, 5, 12, -2.1150798109327225)
grid = transit(grid, 15, [8, 12, 9], [0.28436606994946934, 0.6885905502984891, 0.02704337975204158])
grid = smooth_max(grid, 10, 15, 6)
grid = transit(grid, 1, [10, 14, 4, 15, 1, 5, 6], [0.2495066295298203, 0.11468510633252497, 0.18785735489376995, 0.21136745589024844, 0.0964692952292473, 0.04260437960684226, 0.09750977851754668])
grid = sin(grid, 3, 1, -4.0560493416166175, 95.81416817425202)
grid = smooth_min(grid, 8, 11, 2)
grid = smooth_min(grid, 1, 4, 9)
grid = transit(grid, 8, [11], [1.0])
grid = sin(grid, 9, 15, -0.44933023328502564, -24.232082701600262)
grid = shift(grid, 5, 5, 0.32284439059108283)
grid = transit(grid, 6, [13, 7, 4, 15], [0.4974867376535544, 0.122001688608576, 0.264153347409728, 0.11635822632814159])
grid = smooth_max(grid, 5, 8, 11)
grid = sin(grid, 15, 1, 3.770783199305386, -43.59702742584115)
grid = shift(grid, 14, 4, 0.9626752538173012)
grid = shift(grid, 11, 4, 0.2986356924688961)
grid = transit(grid, 6, [6, 3, 9], [0.25337956571267745, 0.6686201014198824, 0.07800033286744022])
grid = sin(grid, 11, 4, -2.174418438809594, -54.49746971586607)
grid = sin(grid, 14, 5, 3.355412283064952, -96.00248310659103)
grid = transit(grid, 14, [12, 4], [0.20390434823030096, 0.7960956517696991])
grid = sin(grid, 0, 12, -3.2677897638310442, 90.64652490830457)
grid = transit(grid, 2, [5], [1.0])
grid = magnitude(grid, 5, [1, 3, 4], 2)
grid = shift_mod_abs(grid, 11, 11, 0.036778005118671686)
grid = smooth_max(grid, 13, 15, 6)
grid = shift(grid, 12, 3, -2.4651939565062495)
grid = shift(grid, 6, 14, -0.37870084323956843)
grid = sin(grid, 14, 0, -4.328018669612688, 83.36714104275745)
grid = transit(grid, 3, [13, 10, 8, 15, 14, 7, 11], [0.1944986624492616, 0.07486992256727688, 0.231134536265638, 0.10482295336029568, 0.23146487356687384, 0.15903518116768317, 0.004173870622970833])
grid = sin(grid, 4, 13, 1.752132294661211, 71.31434471438615)
grid = sin(grid, 6, 0, -0.9548000503320968, 40.365867704964245)
grid = sin(grid, 10, 10, -4.939739936965214, -67.4768415587308)
grid = sin(grid, 15, 5, 3.699809545048698, 29.060835724196096)
grid = transit(grid, 2, [6, 5, 11, 10], [0.18704063266917545, 0.40027016568536794, 0.38958390250734687, 0.023105299138109676])
grid = transit(grid, 13, [1, 12], [0.5856329592081684, 0.41436704079183173])
grid = transit(grid, 4, [11, 2], [0.6681946567337378, 0.3318053432662622])
grid = transit(grid, 7, [13], [1.0])
grid = transit(grid, 13, [7, 15, 14, 1, 4, 13, 8, 5], [0.0651212397067138, 0.08141617223168503, 0.16370117204908682, 0.05749699627211134, 0.040133892841632726, 0.23195806583657988, 0.1891085902638602, 0.17106387079833013])
grid = smooth_min(grid, 6, 1, 2)
grid = shift(grid, 0, 2, 1.7297995294615762)
grid = transit(grid, 10, [11, 10, 1, 7], [0.5051037285536154, 0.03972966200442982, 0.010248478752532954, 0.44491813068942176])
grid = sin(grid, 4, 15, 0.8114196615621545, 33.63335810627916)
grid = transit(grid, 12, [1, 4], [0.17812517814724027, 0.8218748218527597])
grid = magnitude(grid, 1, [5, 13, 9, 8, 4, 0, 1, 12], 2)
grid = sin(grid, 12, 15, 1.052413439431268, 36.85244986848153)
grid = sin(grid, 3, 14, 2.2265558341365272, 58.678344201412585)
grid = shift(grid, 10, 15, -1.191003896319024)
grid = transit(grid, 9, [0], [1.0])
grid = transit(grid, 8, [7], [1.0])
grid = transit(grid, 3, [14, 15, 0], [0.8324348548693109, 0.10090260553984436, 0.06666253959084477])
grid = transit(grid, 4, [1, 11, 6], [0.6951764313394179, 0.15807485986386538, 0.14674870879671675])
grid = sin(grid, 5, 8, -0.5388929584442547, -40.951045799188975)
grid = transit(grid, 0, [14, 12, 7, 15, 1, 5, 2], [0.0717952669114225, 0.18497158257756685, 0.18028069287744894, 0.040369480659820135, 0.2844136813127787, 0.029472127023213723, 0.20869716863774904])
grid = transit(grid, 3, [7, 0, 11, 5, 3, 10, 2, 12, 9, 14], [0.1532552642217957, 0.052082540513404836, 0.10456226084242329, 0.24222079213756853, 0.08192888875012067, 0.05087687641485665, 0.0593378546226986, 0.10434054332655823, 0.07649277311127953, 0.07490220605929412])
grid = sin(grid, 12, 11, 1.5813522349204758, -62.901105458887294)
grid = smooth_max(grid, 15, 5, 10)
grid = transit(grid, 9, [7, 1, 3, 13, 12, 15, 14, 9, 10, 4], [0.10962082360967332, 0.19053125615890631, 0.007498748298648956, 0.08816972127292766, 0.022108372600841662, 0.09155352349652587, 0.22688313608684876, 0.0990170623345669, 0.0399082096247022, 0.12470914651635842])
grid = sin(grid, 1, 12, -3.377197075812285, 91.81363199388284)
grid = sin(grid, 11, 4, 4.088354335292304, 17.471191356978437)
grid = sin(grid, 1, 9, 3.9750551181423828, -38.07369088660142)
grid = transit(grid, 9, [6, 4, 0, 14, 15, 7, 5, 9, 2], [0.15072414902669207, 0.016115151222039378, 0.21635379624035503, 0.09258664461187874, 0.07041863207187138, 0.18595251578398936, 0.08747389527715435, 0.15161056370630907, 0.028764652059710613])
grid = smooth_min(grid, 6, 10, 12)
grid = transit(grid, 6, [14, 12, 4, 0, 8], [0.019392835029131125, 0.052779084304161325, 0.6519161877101358, 0.1513185999987104, 0.12459329295786135])
grid = transit(grid, 4, [7, 3, 1], [0.14722074771812224, 0.4297314900167701, 0.4230477622651076])
grid = shift_mod_abs(grid, 1, 1, -0.6172636229141508)
grid = transit(grid, 15, [2, 3, 14, 7], [0.1845131860494681, 0.4988627618028293, 0.18005727801502275, 0.13656677413267973])
grid = sin(grid, 4, 3, 2.341721772936374, 93.14683704647129)
grid = transit(grid, 12, [3, 9, 6], [0.7994910272394715, 0.006846176789205516, 0.19366279597132302])
grid = sin(grid, 6, 14, -1.7929160237288677, 31.293746081333893)
grid = shift(grid, 12, 8, -1.9404984616312757)
grid = transit(grid, 14, [11], [1.0])
grid = transit(grid, 6, [6, 15], [0.5041461806949813, 0.49585381930501876])
grid = sin(grid, 0, 8, -2.266948121830639, -1.1518625113740057)
grid = transit(grid, 3, [10, 8, 14], [0.005914755244404283, 0.3474144230365773, 0.6466708217190185])
grid = sin(grid, 7, 7, -5.456915147396615, 85.27127765743711)
grid = transit(grid, 0, [11], [1.0])
grid = shift(grid, 13, 14, 2.7325419662813806)
grid = transit(grid, 7, [2, 7, 5, 0, 14, 8], [0.15042155054028075, 0.13210423196800344, 0.38072446016471123, 0.028952560227987104, 0.08423664460117544, 0.22356055249784204])
grid = sin(grid, 2, 4, -1.6480877840655301, 76.00607107062402)
grid = transit(grid, 10, [13, 1, 4], [0.2959827043708235, 0.6675905062669568, 0.0364267893622195])
grid = transit(grid, 5, [14], [1.0])
grid = smooth_min(grid, 11, 5, 12)
grid = transit(grid, 11, [4, 9], [0.0414241817853843, 0.9585758182146157])
grid = sin(grid, 7, 2, -5.131910581877072, -78.47100231216919)
grid = transit(grid, 0, [12, 4, 14, 7, 3, 13, 10], [0.17790933722356692, 0.16361663972063273, 0.055062694716432256, 0.03457850774889348, 0.17804031568953546, 0.37672133851192235, 0.014071166389016693])
grid = transit(grid, 8, [0, 13, 14, 8, 10], [0.1598266111835022, 0.12709196443400606, 0.3831321974706776, 0.2732362617687772, 0.056712965143037114])
grid = sin(grid, 14, 14, 2.827375960857153, -20.639387817820335)
grid = sin(grid, 14, 2, 1.4860061918580802, -42.78420050467888)
grid = sin(grid, 15, 14, 0.018329907799037693, -95.64144589957225)
grid = sin(grid, 9, 10, 4.112614360938578, 69.82339276605475)
grid = magnitude(grid, 5, [2, 11, 10, 5, 1], 2)
grid = sin(grid, 4, 14, 3.1210073945273855, 38.905295821442905)
grid = smooth_max(grid, 13, 14, 6)
grid = sin(grid, 6, 11, -3.037900911862603, -41.0210573164032)
grid = transit(grid, 13, [6, 10, 0, 3, 2, 5, 15, 1, 8, 13], [0.14458514805634057, 0.06277120423567376, 0.04501475076653843, 0.2686104020212368, 0.034997235626152125, 0.06538207662054918, 0.11842986397869752, 0.16490812357449247, 0.058322167537226376, 0.036979027583092815])
grid = sin(grid, 7, 11, 2.869626213337865, 74.40437688303828)
grid = sin(grid, 12, 15, 1.1174220644733124, 53.91153672547625)
grid = magnitude(grid, 10, [5, 10, 9, 15], 2)
grid = shift_mod_abs(grid, 13, 11, 0.8154777646703879)
grid = transit(grid, 1, [3, 1, 2], [0.09070339866389106, 0.11035232864788158, 0.7989442726882273])
grid = sin(grid, 8, 0, -1.9070787965881668, -27.79434470565772)
grid = transit(grid, 14, [13, 8, 5, 0, 3, 4, 1, 10, 6, 14, 15], [0.14822502205506907, 0.02300773844849466, 0.12691643624383514, 0.13647656943918957, 0.05676955927731482, 0.049161479697029754, 0.06655624850662041, 0.09125188322203971, 0.044386864366051035, 0.18829084764843304, 0.06895735109592303])
grid = sin(grid, 6, 3, 2.2897047356489, -53.45998887926924)
grid = magnitude(grid, 4, [7, 8, 11, 13, 14, 4, 5, 10, 1, 0, 6, 3, 15], 2)
grid = sin(grid, 11, 13, -0.1814613020335019, -2.8508454113726316)
grid = magnitude(grid, 0, [11, 0, 8, 13, 14, 4, 12, 3], 2)
grid = smooth_max(grid, 6, 2, 11)
grid = sin(grid, 9, 5, -0.18692398669078705, 85.3474252103604)
grid = shift(grid, 6, 6, -0.43484582555426854)
grid = sin(grid, 15, 11, -0.7837863833509879, 50.36233031416694)
grid = sin(grid, 8, 11, -1.9337995907751608, 21.163769561969346)
grid = transit(grid, 1, [8], [1.0])
grid = magnitude(grid, 9, [2, 10, 12, 11], 2)
grid = transit(grid, 14, [5], [1.0])
grid = transit(grid, 2, [8, 3, 4, 2, 13], [0.18498519947711267, 0.2302544048382734, 0.2086334555132189, 0.3225390759303082, 0.05358786424108684])
grid = magnitude(grid, 14, [14], 2)
grid = sin(grid, 8, 2, 5.076940832355406, 32.423288865905306)
grid = transit(grid, 9, [10, 2, 9, 12, 0, 7, 13], [0.12335535828902748, 0.08147455120491619, 0.2835136525720616, 0.11805389463803133, 0.0378112141423774, 0.059296312113284025, 0.296495017040302])
grid = transit(grid, 11, [4, 5, 10, 9], [0.02996345096592542, 0.48969977025851535, 0.42213340811300837, 0.05820337066255086])
grid = sin(grid, 2, 2, 2.2884523199401094, -27.726937767680553)
grid = sin(grid, 11, 0, 0.521768702657551, -36.14223206396525)
grid = transit(grid, 13, [4, 10, 12, 5, 0, 8], [0.2980635462987921, 0.17179733779951878, 0.09786381529303359, 0.24122469062670912, 0.08143600789808472, 0.10961460208386163])
grid = sin(grid, 10, 13, -0.7808301922947212, -56.925522550689855)
grid = sin(grid, 12, 8, -0.925860745567602, -19.750482963953715)
grid = sin(grid, 9, 6, 0.3475244586593385, 50.86089760282346)
grid = inverse(grid, 0, 9)
grid = sin(grid, 2, 12, 5.028535534609008, -54.43133346629676)
grid = transit(grid, 13, [0, 8, 15], [0.12565659207849286, 0.7129538168259533, 0.1613895910955539])
grid = sin(grid, 15, 15, 6.8822694780228275, -41.458924758553664)
grid = sin(grid, 2, 12, 7.07921736485995, -37.3282028950211)
grid = transit(grid, 2, [2, 6], [0.4961167548365782, 0.5038832451634218])
grid = sin(grid, 2, 9, -0.24890892305397372, 55.189675163034394)
grid = transit(grid, 7, [2], [1.0])
grid = smooth_max(grid, 8, 10, 14)
grid = smooth_min(grid, 13, 6, 14)
grid = smooth_min(grid, 10, 15, 5)
grid = sin(grid, 5, 14, -3.59787328637373, -4.6003362534814585)
grid = smooth_min(grid, 12, 9, 7)
grid = shift(grid, 15, 2, 5.183497681208784)
grid = transit(grid, 13, [2], [1.0])
grid = sin(grid, 13, 11, -0.804329014613692, -46.91284611395681)
grid = transit(grid, 0, [7, 3, 11, 1, 14], [0.03145191813181808, 0.09071377345604954, 0.09547112600182535, 0.726698465422093, 0.055664716988213944])
grid = sin(grid, 6, 0, 3.8685190352084877, 18.48968352998257)
grid = shift(grid, 10, 0, 1.0851721995280201)
grid = sin(grid, 10, 10, -0.9668205128176128, 76.20329901100277)
grid = transit(grid, 1, [10, 0, 3, 6, 14, 7], [0.20549491073638246, 0.08574509427186884, 0.14079815063964976, 0.25920977005745516, 0.21534948779848698, 0.09340258649615688])
grid = transit(grid, 1, [6, 2, 9], [0.23347264141429105, 0.06856874594440747, 0.6979586126413015])
grid = transit(grid, 10, [3, 2, 1, 14], [0.22007742709217595, 0.06231621565934076, 0.43619923427690077, 0.2814071229715825])
grid = transit(grid, 12, [11, 1, 14, 12, 6, 10], [0.3374943865594992, 0.22350558268536735, 0.14353397264572443, 0.08296470440224331, 0.008257687774290553, 0.20424366593287513])
grid = sin(grid, 9, 2, 1.0830299059228978, -77.74979102909612)
grid = smooth_max(grid, 0, 9, 13)
grid = transit(grid, 12, [8, 4, 11, 2, 13, 1, 14, 9, 3, 12], [0.035372198910961127, 0.02728831715545566, 0.07999987463180491, 0.038325806496588385, 0.16805977626186341, 0.1611280343306679, 0.20996326459408754, 0.060803673993692776, 0.1169179936754737, 0.10214105994940464])
grid = magnitude(grid, 2, [4, 2], 2)
grid = transit(grid, 3, [7], [1.0])
grid = smooth_max(grid, 5, 7, 7)
grid = transit(grid, 4, [14, 7, 1], [0.20823326496530067, 0.6788107794212056, 0.11295595561349375])
grid = sin(grid, 8, 6, -0.530789542928052, 64.54735922524384)
grid = transit(grid, 13, [13, 4], [0.7308590707137472, 0.2691409292862528])
grid = shift(grid, 1, 13, 1.4999684528302675)
grid = transit(grid, 11, [1, 12, 10], [0.12013853509276692, 0.849543204936108, 0.0303182599711251])
grid = transit(grid, 4, [1, 12], [0.6875857680991523, 0.3124142319008477])
grid = sin(grid, 4, 1, -3.363226773250937, 25.5343752054072)
grid = magnitude(grid, 0, [1, 3], 2)
grid = transit(grid, 3, [0, 11, 10, 14], [0.09841561254146537, 0.5674100590476, 0.11773837778094363, 0.216435950629991])
grid = shift(grid, 1, 3, 0.01661279567605323)
grid = shift_mod_abs(grid, 3, 2, -0.2133332440524478)
grid = sin(grid, 15, 0, -5.2272318986280615, -53.96578944083943)
grid = transit(grid, 6, [1, 12, 8, 9], [0.09213199280762226, 0.4910336047652721, 0.19210131195162689, 0.22473309047547882])
grid = sin(grid, 0, 15, -1.3179897820273345, -89.46947544983148)
grid = sin(grid, 1, 5, 3.9607874764176705, 96.06170319096557)
grid = smooth_min(grid, 9, 14, 9)
grid = transit(grid, 0, [14, 1], [0.34428647723613853, 0.6557135227638614])
grid = sin(grid, 9, 2, 3.306126522965714, 6.304127258578674)
grid = transit(grid, 0, [5], [1.0])
grid = sin(grid, 11, 9, 1.7706450796781383, -82.77411170538574)
grid = smooth_min(grid, 1, 7, 11)
grid = sin(grid, 2, 11, -0.7203008355220097, -61.794878694986096)
grid = sin(grid, 1, 3, -1.3852579257158861, 70.39932523840088)
grid = magnitude(grid, 10, [14, 8, 11], 2)
grid = transit(grid, 5, [2, 14, 8, 11, 10], [0.34629003014977483, 0.20697322274098853, 0.1697190192780604, 0.2744661411144167, 0.002551586716759634])
grid = smooth_max(grid, 13, 13, 13)
grid = sin(grid, 7, 7, -6.271142920686637, 6.17693903742564)
grid = magnitude(grid, 10, [3, 12], 2)
grid = transit(grid, 9, [10, 9, 8, 6, 15], [0.18043834954968205, 0.020353471497975763, 0.30145354183405304, 0.35221597982728914, 0.14553865729100013])
grid = smooth_max(grid, 3, 8, 14)
grid = sin(grid, 15, 15, -2.525502336973101, 17.598001537890923)
grid = transit(grid, 9, [9, 2, 8, 11, 5, 13], [0.2744797838047736, 0.24368188521775427, 0.09678712104547853, 0.056223222791167864, 0.20091882659532662, 0.12790916054549908])
grid = sin(grid, 13, 7, -6.92218269746812, -34.12441968918432)
grid = transit(grid, 8, [2, 3, 4, 15], [0.22994236448114524, 0.2820709490900832, 0.44201739393738093, 0.04596929249139073])
grid = transit(grid, 2, [0, 5, 6, 3], [0.03614323335547806, 0.1641470595904913, 0.4891505143646568, 0.3105591926893739])
grid = transit(grid, 6, [3, 1, 6, 2, 14, 7], [0.1994852509936342, 0.007843849882205234, 0.2462946588511506, 0.11138973783235838, 0.23018633587503146, 0.20480016656562033])
grid = shift(grid, 3, 14, 3.376567837033712)
grid = sin(grid, 7, 10, -0.46800156615938016, -65.81474725672227)
grid = smooth_max(grid, 12, 15, 15)
grid = sin(grid, 4, 5, 1.5605201423298307, 41.257060583287625)
grid = transit(grid, 10, [0, 4, 7], [0.8767866735738928, 0.10056650618889666, 0.022646820237210628])
grid = smooth_min(grid, 3, 13, 1)
grid = sin(grid, 0, 15, -2.3963170699361074, -93.13858100326142)
grid = sin(grid, 12, 13, 0.29594346639174257, 63.55851019939223)
grid = transit(grid, 10, [10, 6], [0.9723022461605464, 0.027697753839453502])
grid = sin(grid, 12, 5, 1.8907728163627338, 65.20958420244952)
grid = sin(grid, 4, 9, -1.006090982255747, -39.50983346190293)
grid = sin(grid, 8, 10, -3.150783570642279, 34.78200133754518)
grid = sin(grid, 0, 14, 5.032058303624256, -72.55400365793456)
grid = smooth_min(grid, 5, 13, 13)
grid = sin(grid, 0, 4, 4.2120558589601576, -22.168073827353282)
grid = smooth_max(grid, 8, 6, 11)
grid = sin(grid, 7, 0, -3.3710387114054736, 51.65233042745939)
grid = sin(grid, 3, 14, -3.828171624184156, 0.24088929185863606)
grid = sin(grid, 7, 0, -0.3925996355496973, 20.355897476026996)
grid = magnitude(grid, 13, [1, 7, 8, 14, 15, 2], 2)
grid = sin(grid, 14, 2, 1.2350070154005643, 37.818516321038175)
grid = sin(grid, 13, 15, -0.6470355376804856, 84.84663719027833)
grid = transit(grid, 10, [8, 10, 15, 7], [0.5046292600947969, 0.25534987589462593, 0.0028301273345001494, 0.2371907366760769])
grid = sin(grid, 14, 1, -3.5857841599782088, 73.19056294384069)
grid = transit(grid, 5, [2], [1.0])
grid = sin(grid, 11, 9, 0.09611404275583257, -93.75557402038382)
grid = transit(grid, 7, [8, 14, 4, 12, 13], [0.019814682351872896, 0.07726972684300765, 0.3598208110321618, 0.40441827399198005, 0.13867650578097765])
grid = transit(grid, 5, [13, 10], [0.4811921528927294, 0.5188078471072707])
grid = sin(grid, 14, 0, 2.051426169780874, 63.76246527159026)
grid = shift_mod_abs(grid, 6, 3, -0.4755431113627433)
grid = magnitude(grid, 6, [12, 8], 2)
grid = smooth_max(grid, 10, 11, 10)
grid = smooth_max(grid, 11, 8, 1)
grid = sin(grid, 9, 6, -5.630441048669049, -86.9465298420423)
grid = magnitude(grid, 6, [14, 4], 2)
grid = smooth_max(grid, 15, 14, 3)
grid = magnitude(grid, 7, [12, 2, 13, 5, 15], 2)
grid = sin(grid, 13, 5, 0.7180577239258917, -37.68450320125265)
grid = shift_mod_abs(grid, 15, 0, 0.39740628783756393)
grid = sin(grid, 3, 7, -2.881653747960443, -94.77525107179954)
grid = transit(grid, 5, [5, 7, 14, 6, 4], [0.005949232124648486, 0.5161432759242179, 0.09511905036065257, 0.16343482834023207, 0.21935361325024894])
grid = transit(grid, 3, [14, 9, 1, 7, 4, 2, 8, 5], [0.05585679808011971, 0.06674136180595235, 0.2137030916852326, 0.02559947287617969, 0.1956946752117402, 0.15675988536650867, 0.1800095813240246, 0.10563513365024214])
grid = sin(grid, 4, 2, -5.169611770787436, -44.95148680576768)
grid = transit(grid, 8, [3, 0, 14], [0.1566308589079141, 0.7970637677355046, 0.046305373356581254])
grid = transit(grid, 0, [8], [1.0])
grid = sin(grid, 5, 0, 4.638114296229324, -63.89290552408961)
grid = transit(grid, 3, [6, 5, 15, 10, 9, 8, 4, 7], [0.16960256336629126, 0.06864962307071441, 0.2158620377888371, 0.10901843462467302, 0.010434896725598823, 0.010169751774402854, 0.21059986384926022, 0.20566282880022224])
grid = transit(grid, 8, [10, 13, 12, 11, 15, 4], [0.4435802804003096, 0.07242751759704737, 0.021444958364808572, 0.1946574509998237, 0.029735516697332025, 0.23815427594067873])
grid = transit(grid, 8, [13, 1, 10], [0.10611200537562752, 0.2372006097404753, 0.6566873848838972])
grid = magnitude(grid, 7, [8, 5], 2)
grid = transit(grid, 7, [1, 15, 9, 12, 14, 13], [0.00044952045854961177, 0.048141123875975626, 0.3018330391335465, 0.2586521054236143, 0.22603082380374503, 0.164893387304569])
grid = shift(grid, 1, 14, 0.021266437525674597)
grid = sin(grid, 0, 11, 1.9798653884460715, 67.43517932958545)
grid = transit(grid, 0, [2, 14, 10, 9, 15, 0, 4, 13, 7, 11, 8, 5, 12, 3], [0.10467592362317106, 0.04951546823907811, 0.023540294958541385, 0.05473962503770174, 0.08641215885733243, 0.13050979276288038, 0.129145679319401, 0.09449095720988115, 0.04887414236750689, 0.07727784070060024, 0.07436487349092359, 0.01533190945217298, 0.020605028028148124, 0.09051630595266091])
grid = sin(grid, 2, 1, 0.7695685465372705, -69.89732340107402)
grid = smooth_max(grid, 2, 2, 0)
grid = sin(grid, 7, 9, 4.5894276567977235, 30.091535668201317)
grid = sin(grid, 14, 7, 7.17752751641597, -34.944651993686975)
grid = transit(grid, 15, [2], [1.0])
grid = sin(grid, 13, 10, -0.5138392230865213, -8.296600184086273)
grid = transit(grid, 2, [14, 0, 12, 1], [0.2451888160620973, 0.365448425773462, 0.22025822155063365, 0.1691045366138071])
grid = sin(grid, 14, 14, -0.6726555888607855, -21.091093780269603)
grid = transit(grid, 13, [1, 0, 3, 4, 15, 10, 13, 9, 7, 5, 8, 11], [0.14608526514904863, 0.020944804084935098, 0.09216879117058731, 0.10953739375783059, 0.055820452153338834, 0.11491241549210994, 0.10824017885860414, 0.10864201759636412, 0.053077483312846466, 0.07271493285596015, 0.10795392203849626, 0.009902343529878422])
grid = sin(grid, 8, 5, -0.5836489194167, 0.15143369187518374)
grid = shift(grid, 14, 8, 3.290480403699842)
grid = sin(grid, 2, 10, -0.9803255007144543, 58.51296497813692)
grid = magnitude(grid, 2, [8, 3, 14], 2)
grid = transit(grid, 10, [14, 6, 13, 12, 9, 2], [0.051345785750632554, 0.07450141282093097, 0.20375372721426818, 0.16081935101075182, 0.08256917443949278, 0.42701054876392364])
grid = transit(grid, 13, [1, 12], [0.6148308098174511, 0.38516919018254886])
grid = transit(grid, 2, [15, 7], [0.17419753869885962, 0.8258024613011403])
grid = sin(grid, 1, 9, -0.30841944164827667, -88.99318840002482)
grid = sin(grid, 8, 9, 1.3672667398837988, 80.26581078508241)
grid = sin(grid, 8, 10, -12.303390582494227, -51.014346141847525)
grid = shift(grid, 2, 9, -1.037982047475446)
grid = sin(grid, 11, 13, -3.421112814272899, -84.69633212781906)
grid = transit(grid, 9, [6, 3], [0.3057675990182092, 0.6942324009817907])
grid = shift_mod_abs(grid, 13, 8, -0.3326423690411051)
grid = smooth_max(grid, 3, 13, 8)
grid = smooth_max(grid, 0, 5, 7)
grid = magnitude(grid, 4, [2, 9], 2)
grid = sin(grid, 11, 0, -1.5579018776057265, -1.954556483139399)
grid = transit(grid, 9, [3, 9, 2, 4, 6], [0.10995575679803808, 0.46426804432023183, 0.0604444076660765, 0.32820573807710823, 0.03712605313854538])
grid = transit(grid, 1, [7, 3], [0.9403287956779426, 0.059671204322057386])
grid = sin(grid, 9, 6, 3.319747886522862, 72.47031470870365)
grid = sin(grid, 8, 15, 1.6585061250903068, -31.80271171290275)
grid = sin(grid, 15, 3, -2.9647600710162014, -8.123234032378491)
grid = sin(grid, 2, 12, 4.214209488676055, 20.72219281761059)
grid = sin(grid, 10, 10, -5.0365926976698745, -86.66890376959748)
grid = sin(grid, 5, 14, -2.853073739010866, -96.16514750314258)
grid = transit(grid, 2, [12], [1.0])
grid = shift(grid, 11, 15, -0.7693891099582622)

#create color space 
colors = np.zeros((5, 3)) 
colors[0] = [214, 253, 80] 
colors[1] = [71, 246, 91] 
colors[2] = [158, 120, 242] 
colors[3] = [19, 82, 205] 
colors[4] = [106, 100, 43] 

res = np.zeros((SIZE, SIZE, 3))  
res += (grid[:,:,0:0+1].repeat(3, -1) + 1) / 2 * colors[0] 
res += (grid[:,:,1:1+1].repeat(3, -1) + 1) / 2 * colors[1] 
res += (grid[:,:,2:2+1].repeat(3, -1) + 1) / 2 * colors[2] 
res += (grid[:,:,3:3+1].repeat(3, -1) + 1) / 2 * colors[3] 
res += (grid[:,:,4:4+1].repeat(3, -1) + 1) / 2 * colors[4] 

res = (res / 5 * 2.626527804403767).clip(0,255) 

#save results 
im = Image.fromarray(np.uint8(res))
im.save(os.path.basename(__file__) + '.png')

#save layers
img = np.zeros((SIZE * 4, SIZE * 4))
for j in range(GRID_CHANNELS):
    x = j % 4
    y = j // 4
    img[x*SIZE:(x + 1)*SIZE, y*SIZE:(y+1)*SIZE] = grid[:,:,j]

img = (img + 1) * 127.5 
im = Image.fromarray(np.uint8(img))
im.save(os.path.basename(__file__) + '_layers.png')
