import xml.etree.ElementTree as gfg
import colorsys 
 
def rgb2hex(r,g,b):
    return "#{:02x}{:02x}{:02x}".format(r,g,b)

def HSVToRGB(h, s, v): 
    (r, g, b) = colorsys.hsv_to_rgb(h, s, v) 
    return rgb2hex(int(255*r), int(255*g), int(255*b)) 
 
def getDistinctColors(n): 
    huePartition = 1.0 / (n + 1) 
    return HSVToRGB(huePartition * n, 1.0, 1.0)

person = {"keypoints":['nose', 'left eye', 'right eye', 'left ear', 'right ear', 'left shoulder', 'right shoulder', 'left elbow', 'right elbow', 'left wrist', 'right wrist', 'left hip', 'right hip', 'left knee', 'right knee', 'left ankle', 'right ankle'],"skeleton": [[16,14],[14,12],[17,15],[15,13],[12,13],[6,12],[7,13],[6,7],[6,8],[7,9],[8,10],[9,11],[2,3],[1,2],[1,3],[2,4],[3,5],[4,6],[5,7]]}

face = {"keypoints": ['right cheekbone 1', 'right cheekbone 2', 'right cheek 1', 'right cheek 2', 'right cheek 3', 'right cheek 4', 'right cheek 5', 'right chin', 'chin center', 'left chin', 'left cheek 5', 'left cheek 4', 'left cheek 3', 'left cheek 2', 'left cheek 1', 'left cheekbone 2', 'left cheekbone 1', 'right eyebrow 1', 'right eyebrow 2', 'right eyebrow 3', 'right eyebrow 4', 'right eyebrow 5', 'left eyebrow 1', 'left eyebrow 2', 'left eyebrow 3', 'left eyebrow 4', 'left eyebrow 5', 'nasal bridge 1', 'nasal bridge 2', 'nasal bridge 3', 'nasal bridge 4', 'right nasal wing 1', 'right nasal wing 2', 'nasal wing center', 'left nasal wing 1', 'left nasal wing 2', 'right eye eye corner 1', 'right eye upper eyelid 1', 'right eye upper eyelid 2', 'right eye eye corner 2', 'right eye lower eyelid 2', 'right eye lower eyelid 1', 'left eye eye corner 1', 'left eye upper eyelid 1', 'left eye upper eyelid 2', 'left eye eye corner 2', 'left eye lower eyelid 2', 'left eye lower eyelid 1', 'right mouth corner', 'upper lip outer edge 1', 'upper lip outer edge 2', 'upper lip outer edge 3', 'upper lip outer edge 4', 'upper lip outer edge 5', 'left mouth corner', 'lower lip outer edge 5', 'lower lip outer edge 4', 'lower lip outer edge 3', 'lower lip outer edge 2', 'lower lip outer edge 1', 'upper lip inter edge 1', 'upper lip inter edge 2', 'upper lip inter edge 3', 'upper lip inter edge 4', 'upper lip inter edge 5', 'lower lip inter edge 3', 'lower lip inter edge 2', 'lower lip inter edge 1'], "skeleton": []}

hand = {"keypoints":['wrist', 'thumb root', "thumb's third knuckle", "thumb's second knuckle", 'thumb’s first knuckle', "forefinger's root", "forefinger's third knuckle", "forefinger's second knuckle", "forefinger's first knuckle", "middle finger's root", "middle finger's third knuckle", "middle finger's second knuckle", "middle finger's first knuckle", "ring finger's root", "ring finger's third knuckle", "ring finger's second knuckle", "ring finger's first knuckle", "pinky finger's root", "pinky finger's third knuckle", "pinky finger's second knuckle", "pinky finger's first knuckle"],"skeleton": []}

animal_in_AnimalKindom = {"keypoints":['head mid top', 'eye left', 'eye right', 'mouth front top', 'mouth back left', 'mouth back right', 'mouth front bottom', 'shoulder left', 'shoulder right', 'elbow left', 'elbow right', 'wrist left', 'wrist right', 'torso mid back', 'hip left', 'hip right', 'knee left', 'knee right', 'ankle left ', 'ankle right', 'tail top back', 'tail mid back', 'tail end back'],"skeleton": [[1, 0], [2, 0], [3, 4], [3, 5], [4, 6], [5, 6], [0, 7], [0, 8], [7, 9], [8, 10], [9, 11], [10, 12], [0, 13], [13, 20], [20, 14], [20, 15], [14, 16], [15, 17], [16, 18], [17, 19], [20, 21], [21, 22]]}

animal_in_AP10K = {"keypoints": ['left eye', 'right eye', 'nose', 'neck', 'root of tail', 'left shoulder', 'left elbow', 'left front paw', 'right shoulder', 'right elbow', 'right front paw', 'left hip', 'left knee', 'left back paw', 'right hip', 'right knee', 'right back paw'], "skeleton": [[1, 2], [1, 3], [2, 3], [3, 4], [4, 5], [4, 6], [6, 7], [7, 8], [4, 9], [9, 10], [10, 11], [5, 12], [12, 13], [13, 14], [5, 15], [15, 16], [16, 17]]}

animal= {"keypoints": ['left eye', 'right eye', 'nose', 'neck', 'root of tail', 'left shoulder', 'left elbow', 'left front paw', 'right shoulder', 'right elbow', 'right front paw', 'left hip', 'left knee', 'left back paw', 'right hip', 'right knee', 'right back paw'], "skeleton": [[1, 2], [1, 3], [2, 3], [3, 4], [4, 5], [4, 6], [6, 7], [7, 8], [4, 9], [9, 10], [10, 11], [5, 12], [12, 13], [13, 14], [5, 15], [15, 16], [16, 17]]}

animal_face = {"keypoints": ['right eye right', 'right eye left', 'left eye right', 'left eye left', 'nose tip', 'lip right', 'lip left', 'upper lip', 'lower lip'], "skeleton": []}

fly = {"keypoints": ['head', 'eye left', 'eye right', 'neck', 'thorax', 'abdomen', 'foreleg right base', 'foreleg right first segment', 'foreleg right second segment', 'foreleg right tip', 'midleg right base', 'midleg right first segment', 'midleg right second segment', 'midleg right tip', 'hindleg right base', 'hindleg right first segment', 'hindleg right second segment', 'hindleg right tip', 'foreleg left base', 'foreleg left first segment', 'foreleg left second segment', 'foreleg left tip', 'midleg left base', 'midleg left first segment', 'midleg left second segment', 'midleg left tip', 'hindleg left base', 'hindleg left first segment', 'hindleg left second segment', 'hindleg left tip', 'wing left', 'wing right'], "skeleton": [[2, 1], [3, 1], [4, 1], [5, 4], [6, 5], [8, 7], [9, 8], [10, 9], [12, 11], [13, 12], [14, 13], [16, 15], [17, 16], [18, 17], [20, 19], [21, 20], [22, 21], [24, 23], [25, 24], [26, 25], [28, 27], [29, 28], [30, 29], [31, 4], [32, 4]]}

locust = {"keypoints": ['head', 'neck', 'thorax', 'abdomen1', 'abdomen2', 'anttip left', 'antbase left', 'eye left', 'foreleg left base', 'foreleg left first segment', 'foreleg left second segment', 'foreleg left tip', 'midleg left base', 'midleg left first segment', 'midleg left second segment', 'midleg left tip', 'hindleg left base', 'hindleg left first segment', 'hindleg left second segment', 'hindleg left tip', 'anttip right', 'antbase right', 'eye right', 'foreleg right base', 'foreleg right first segment', 'foreleg right second segment', 'foreleg right tip', 'midleg right base', 'midleg right first segment', 'midleg right second segment', 'midleg right tip', 'hindleg right base', 'hindleg right first segment', 'hindleg right second segment', 'hindleg right tip'],"skeleton": [[2, 1], [3, 2], [4, 3], [5, 4], [7, 6], [8, 7], [10, 9], [11, 10], [12, 11], [14, 13], [15, 14],[16, 15], [18, 17], [19, 18], [20, 19], [22, 21], [23, 22], [25, 24], [26, 25], [27, 26],[29, 28], [30, 29], [31, 30], [33, 32], [34, 33], [35, 34]]}

car ={"keypoints": ['right front wheel center', 'left front wheel center', 'right rear wheel center', 'left rear wheel center', 'front right', 'front left', 'back right', 'back left', 'none', 'roof front right', 'roof front left', 'roof back right', 'roof back left', 'none'],"skeleton": [[0, 2], [1, 3], [0, 1], [2, 3], [9, 11], [10, 12], [9, 10], [11, 12], [4, 0], [4, 9], [4, 5], [5, 1], [5, 10], [6, 2], [6, 11], [7, 3], [7, 12], [6, 7]]}

short_sleeved_shirt = {'keypoints': ['upper center neckline', 'upper right neckline', 'lower right neckline', 'lower center neckline', 'lower left neckline', 'upper left neckline', 'right sleeve outside 1', 'right sleeve outside 2', 'right cuff outside', 'right cuff inside', 'right sleeve inside 2', 'right sleeve inside 1', 'right side 1', 'right side 2', 'right side 3', 'center hem', 'left side 3', 'left side 2', 'left side 1', 'left sleeve inside 1', 'left sleeve inside 2', 'left cuff inside', 'left cuff outside', 'left sleeve outside 2', 'left sleeve outside 1'], 'skeleton': []}

long_sleeved_outwear={'keypoints': ['upper center neckline', 'lower right center neckline', 'lower right neckline', 'upper right neckline', 'lower left neckline', 'upper left neckline', 'right sleeve outside 1', 'right sleeve outside 2', 'right sleeve outside 3', 'right sleeve outside 4', 'right cuff outside', 'right cuff inside', 'right sleeve inside 1', 'right sleeve inside 2', 'right sleeve inside 3', 'right sleeve inside 4', 'right side outside 1', 'right side outside 2', 'right side outside 3', 'right side inside 3', 'left side outside 3', 'left side outside 2', 'left side outside 1', 'left sleeve inside 4', 'left sleeve inside 3', 'left sleeve inside 2', 'left sleeve inside 1', 'left cuff inside', 'left cuff outside', 'left sleeve outside 4', 'left sleeve outside 3', 'left sleeve outside 2', 'left sleeve outside 1', 'lower left center neckline', 'left side inside 1', 'left side inside 2', 'left side inside 3', 'right side inside 1', 'right side inside 2'], 'skeleton': []}

short_sleeved_outwear={'keypoints': ['upper center neckline', 'lower right center neckline', 'lower right neckline', 'upper right neckline', 'lower left neckline', 'upper left neckline', 'right sleeve outside 1', 'right sleeve outside 2', 'right cuff outside', 'right cuff inside', 'right sleeve inside 2', 'right sleeve inside 1', 'right side outside 1', 'right side outside 2', 'right side outside 3', 'right side inside 3', 'left side outside 3', 'left side outside 2', 'left side outside 1', 'left sleeve inside 1', 'left sleeve inside 2', 'left cuff inside', 'left cuff outside', 'left sleeve outside 2', 'left sleeve outside 1', 'lower left center neckline', 'left side inside 1', 'left side inside 2', 'left side inside 3', 'right side inside 1', 'right side inside 2'], 'skeleton': []}

sling={'keypoints': ['upper center neckline', 'upper right neckline', 'lower right neckline', 'lower center neckline', 'lower left neckline', 'upper left neckline', 'right sleeve', 'right side 1', 'right side 2', 'right side 3', 'center hem', 'left side 3', 'left side 2', 'left side 1', 'left sleeve'], 'skeleton': []}

vest = {'keypoints': ['upper center neckline', 'upper right neckline', 'lower right neckline', 'lower center neckline', 'lower left neckline', 'upper left neckline', 'right sleeve', 'right side 1', 'right side 2', 'right side 3', 'center hem', 'left side 3', 'left side 2', 'left side 1', 'left sleeve'], 'skeleton': []}

long_sleeved_dress={'keypoints': ['upper center neckline', 'upper right neckline', 'lower right neckline', 'lower center neckline', 'lower left neckline', 'upper left neckline', 'right sleeve outside 1', 'right sleeve outside 2', 'right sleeve outside 3', 'right sleeve outside 4', 'right cuff outside', 'right cuff inside', 'right sleeve inside 4', 'right sleeve inside 3', 'right sleeve inside 2', 'right sleeve inside 1', 'right side 1', 'right side 2', 'right side 3', 'right side 4', 'right side 5', 'center hem', 'left side 5', 'left side 4', 'left side 3', 'left side 2', 'left side 1', 'left sleeve inside 1', 'left sleeve inside 2', 'left sleeve inside 3', 'left sleeve inside 4', 'left cuff inside', 'left cuff outside', 'left sleeve outside 4', 'left sleeve outside 3', 'left sleeve outside 2', 'left sleeve outside 1'], 'skeleton': []}

long_sleeved_shirt = {'keypoints': ['upper center neckline', 'upper right neckline', 'lower right neckline', 'lower center neckline', 'lower left neckline', 'upper left neckline', 'right sleeve outside 1', 'right sleeve outside 2', 'right sleeve outside 3', 'right sleeve outside 4', 'right cuff outside', 'right cuff inside', 'right sleeve inside 4', 'right sleeve inside 3', 'right sleeve inside 2', 'right sleeve inside 1', 'right side 1', 'right side 2', 'right side 3', 'center hem', 'left side 3', 'left side 2', 'left side 1', 'left sleeve inside 1', 'left sleeve inside 2', 'left sleeve inside 3', 'left sleeve inside 4', 'left cuff inside', 'left cuff outside', 'left sleeve outside 4', 'left sleeve outside 3', 'left sleeve outside 2', 'left sleeve outside 1'], 'skeleton': []}

trousers = {'keypoints': ['right side outside 1', 'upper center', 'left side outside 1', 'right side outside 2', 'right side outside 3', 'right cuff outside', 'right cuff inside', 'right side inside 1', 'crotch', 'left side inside 1', 'left cuff inside', 'left cuff outside', 'left side outside 3', 'left side outside 2'], 'skeleton': []}

sling_dress = {'keypoints': ['upper center neckline', 'upper right neckline', 'lower right neckline', 'lower center neckline', 'lower left neckline', 'upper left neckline', 'right side 1', 'right side 2', 'right side 3', 'right side 4', 'right side 5', 'right side 6', 'center hem', 'left side 6', 'left side 5', 'left side 4', 'left side 3', 'left side 2', 'left side 1'], 'skeleton': []}

vest_dress = {'keypoints': ['upper center neckline', 'upper right neckline', 'lower right neckline', 'lower center neckline', 'lower left neckline', 'upper left neckline', 'right side 1', 'right side 2', 'right side 3', 'right side 4', 'right side 5', 'right side 6', 'center hem', 'left side 6', 'left side 5', 'left side 4', 'left side 3', 'left side 2', 'left side 1'], 'skeleton': []}

skirt = {'keypoints': ['right side 1', 'upper center', 'left side 1', 'right side 2', 'right side 3', 'center hem', 'left side 3', 'left side 2'], 'skeleton': []}

short_sleeved_dress = {'keypoints': ['upper center neckline', 'upper right neckline', 'lower right neckline', 'lower center neckline', 'lower left neckline', 'upper left neckline', 'right sleeve outside 1', 'right sleeve outside 2', 'right cuff outside', 'right cuff inside', 'right sleeve inside 1', 'right sleeve inside 2', 'left side 1', 'left side 2', 'left side 3', 'left side 4', 'left side 5', 'center hem', 'right side 5', 'right side 4', 'right side 3', 'right side 2', 'right side 1', 'left sleeve inside 2', 'left sleeve inside 1', 'left cuff inside', 'left cuff outside', 'left sleeve outside 2', 'left sleeve outside 1'], 'skeleton': []}

shorts = {'keypoints': ['right side outside 1', 'upper center', 'left side outside 1', 'right side outside 2', 'right cuff outside', 'right cuff inside', 'crotch', 'left cuff inside', 'left cuff outside', 'left side outside 2'], 'skeleton': []}

table = {'keypoints': ['desktop corner 1', 'desktop corner 2', 'desktop corner 3', 'desktop corner 4', 'table leg 1', 'table leg 2', 'table leg 3', 'table leg 4'], 'skeleton': []}

chair = {'keypoints': ['legs righttopcorner', 'legs lefttopcorner', 'legs leftbottomcorner', 'legs rightbottomcorner', 'base righttop', 'base lefttop', 'base leftbottom', 'base rightbottom', 'headboard righttop', 'headboard lefttop'], 'skeleton': []}

bed = {'keypoints': ['legs rightbottomcorner', 'legs righttopcorner', 'base rightbottom', 'base righttop', 'backrest righttop', 'legs leftbottomcorner', 'legs lefttopcorner', 'base leftbottom', 'base lefttop', 'backrest lefttop'], 'skeleton': []}

sofa = {'keypoints': ['legs rightbottomcorner', 'legs righttopcorner', 'base rightbottom', 'base righttop', 'armrests rightbottomcorner', 'armrests righttopcorner', 'backrest righttop', 'legs leftbottomcorner', 'legs lefttopcorner', 'base leftbottom', 'base lefttop', 'armrests leftbottomcorner', 'armrests lefttopcorner', 'backrest lefttop'], 'skeleton': []}

swivelchair = {'keypoints': ['rotatingbase 1', 'rotatingbase 2', 'rotatingbase 3', 'rotatingbase 4', 'rotatingbase 5', 'rotatingbase center', 'base center', 'base righttop', 'base lefttop', 'base leftbottom', 'base rightbottom', 'backrest righttop', 'backrest lefttop'], 'skeleton': []}

predefined_keypoints = ['person','face','hand','animal_in_AnimalKindom','animal_in_AP10K','animal',
                        'animal_face','fly','locust','car','short_sleeved_shirt','long_sleeved_outwear',
                        'short_sleeved_outwear','sling','vest','long_sleeved_dress','long_sleeved_shirt',
                        'trousers','sling_dress','vest_dress','skirt','short_sleeved_dress','shorts',
                        'table','chair','bed','sofa','swivelchair']

fo = open("ram_tag_list.txt", "r")
predefined_detection = fo.readlines()

def generate_detection_labels(fileName):
    root = gfg.Element("View") 
      
    m1 = gfg.Element("Image") 
    m1.set('name','image')
    m1.set('value','$dec')
    root.append (m1) 

    m1= gfg.Element("RectangleLabels") 
    m1.set('name','label')
    m1.set('toName','image')
 
    for i, pred in enumerate(predefined_detection):
        b1 = gfg.SubElement(m1, "Label") 
        b1.set('value',pred)
        b1.set('background',getDistinctColors(i))

    root.append (m1)
    tree = gfg.ElementTree(root) 

    gfg.indent(tree)
      
    with open (fileName, "wb") as files : 
        tree.write(files) 

def generate_kp_labels(fileName):
    root = gfg.Element("View") 
    m1 = gfg.Element("Image") 
    m1.set('name','image')
    m1.set('value','$kp')
    root.append (m1) 

    m1= gfg.Element("RectangleLabels") 
    m1.set('name','label')
    m1.set('toName','image')
 
    for i, pred in enumerate(predefined_keypoints):
        b1 = gfg.SubElement(m1, "Label") 
        b1.set('value',pred)
        b1.set('background',getDistinctColors(i))
    root.append (m1)

    m1 = gfg.Element("KeyPointLabels") 
    m1.set('name','keypoint')
    m1.set('toName','image')

    kp_labels = []
    for kp in predefined_keypoints:
        keypoint_dict = globals()[kp]
        keypoint_text_prompt = keypoint_dict.get("keypoints")
        kp_labels.extend(keypoint_text_prompt)

    kp_labels = set(kp_labels)

    for i, pred in enumerate(kp_labels):
        b1 = gfg.SubElement(m1, "Label") 
        b1.set('value',pred)
        b1.set('background',getDistinctColors(i))

    root.append (m1) 
      
    tree = gfg.ElementTree(root) 
    gfg.indent(tree)
    with open (fileName, "wb") as files : 
        tree.write(files) 

generate_detection_labels("detection.xml")
generate_kp_labels("keypoints.xml")