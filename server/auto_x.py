import magic 
from uuid import uuid4
from typing import List, Dict, Optional
from api.model import AutoXMLBase
from PIL import Image

from ml.pipelines.lspr_pipeline import *

lspr_pipeline = LSPRPipeline()
class AutoSolution(AutoXMLBase):

    def setup(self):
        self.set("model_version", f'{self.__class__.__name__}-v0.0.1')
                        
    def predict(self, tasks: List[Dict], context: Optional[Dict] = None, **kwargs) -> List[Dict]:
        final_predictions = []
        lspr_tasks = []

        from_name_r, to_name = self.get_config_item('RectangleLabels')
        from_name_t, to_name = self.get_config_item('TextArea')
        
        for task in tasks:
            try:
                if 'lspr' in task['data']:
                    raw_img_path = task['data']['lspr']
               
                if raw_img_path is not None:
                    img_path = self.get_local_path(
                        raw_img_path,
                        task_id=task.get('id')
                    )
                    # printing the mime type of the file 
                    mime = magic.from_file(img_path, mime = True)
                    print(mime)

                    if 'image/' in mime:
                        if 'lspr' in task['data']:
                            lspr_tasks.append(img_path)
                       
                    elif 'video/' in mime:
                        pass
                    elif 'audio/' in mime:
                        pass
                    elif mime == 'application/pdf':
                        pass
            except Exception as e:
                logger.error(f"Error getting local path: {e}")

        if len(lspr_tasks) > 0:
            final_predictions.append(self.multiple_lspr_tasks(lspr_tasks, from_name_r, from_name_t, to_name))
       
        return final_predictions
    
    def multiple_lspr_tasks(self, image_paths, from_name_r, from_name_t, to_name):
        
        predictions = []

        all_boxes, all_labels, all_logits, all_lengths = lspr_pipeline.predict(image_paths)

        for boxes_xyxy, label, logits, (H, W) in zip(all_boxes, all_labels, all_logits, all_lengths):                 
            predictions.extend(self.get_lspr_results(boxes_xyxy, label, logits, (H, W), from_name_r, from_name_t, to_name))

        return {
            'result': predictions,
            'score': 0,
            'model_version': self.get('model_version')
        }

    def get_lspr_results(self, boxes_xyxy, labels, logits, lengths, from_name_r, from_name_t, to_name):
        results = []
        height, width = lengths
        for box, label, score in zip(boxes_xyxy, labels, logits):
            # random ID
            label_id = str(uuid4())[:9]
            # results.append({
            #     'id': label_id,
            #     'from_name': from_name_r,
            #     'to_name': to_name,
            #     'original_width': width,
            #     'original_height': height,
            #     'image_rotation': 0,
            #     'value': {
            #         "rectanglelabels": [label],
            #         'rotation': 0,
            #         'width': (box[2] - box[0]) / width * 100,
            #         'height': (box[3] - box[1]) / height * 100,
            #         'x': box[0] / width * 100,
            #         'y': box[1] / height * 100
            #     },
            #     'score': float(score),
            #     'type': 'rectanglelabels',
            #     'readonly': False
            # })
            results.append({
                "original_width": width,
                "original_height": height,
                "image_rotation": 0,
                "value": {
                    "rotation": 0,
                    'width': (box[2] - box[0]) / width * 100,
                    'height': (box[3] - box[1]) / height * 100,
                    'x': box[0] / width * 100,
                    'y': box[1] / height * 100,
                    "text": [
                        label
                    ]
                },
                "id": label_id,
                "from_name": from_name_t,
                "to_name": to_name,
                "type": "textarea",
                "origin": "manual"
            })

        return results
    
    def get_names(self):
        import xml.etree.ElementTree as ET
        current_label_config = self.get('label_config')    
        root = ET.fromstring(current_label_config)
        names = []
        for node in root.findall("Label"):
            value = node.get('value')
            names.append(value)
            
        return names
    
    def train(self, annotations, **kwargs):
        odvg_annos = []
        names = self.get_names()
        for annos in annotations:
            if 'lspr' in annos['data']:
                raw_img_path = annos['data']['lspr']
                img_path = self.get_local_path(
                        raw_img_path,
                        task_id=annos['id']
                )
                image_source = Image.open(img_path)
                width, height = image_source.size 
                
                for anno in annos['annotations']:
                    if len(anno['result']) > 0:
                        ret = {"im_file": img_path,
                            "shape": (height,width),
                            "bboxes":[],
                            "cls":[],
                            "bbox_format":"xyxy",
                            "normalized":True}
                        x1 = anno['result'][0]['value']['x']
                        y1 = anno['result'][0]['value']['y']
                        x2 = x1 + anno['result'][0]['value']['width']
                        y2 = y1 + anno['result'][0]['value']['height']
                        ret["bboxes"].append([x1*width/100, y1*height/100, 
                                            x2*width/100, y2*height/100])
                        label = anno['result'][0]['value']['rectanglelabels'][0]
                        ret["cls"].append([0])
                        odvg_annos.append(ret)

        lspr_pipeline.train(odvg_annos, names)