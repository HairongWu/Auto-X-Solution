import logging
import magic 
import yaml
import glob
from uuid import uuid4
from typing import List, Dict, Optional
from api.model import AutoXMLBase

from ml.pipelines.ram_pipeline import *
from ml.pipelines.detection_pipeline import *
from ml.pipelines.keypoint_pipeline import *
from ml.pipelines.document_pipeline import *

logger = logging.getLogger(__name__)

ram_pipeline = RamPipeline()
dec_pipeline = DetectionPipeline()
kp_pipeline = KeypointPipeline()
ocr_pipeline = OCRPipeline()

class AutoSolution(AutoXMLBase):

    def setup(self):
        self.set("model_version", f'{self.__class__.__name__}-v0.0.1')
        self.projects = []

    def generate(self) -> List[Dict]:
        for f in glob.glob('./ls_project_templates/**/*.yml', recursive=True):
            with open(f, 'r') as file:
                config = yaml.safe_load(file)

            project = self.label_studio.projects.create(
                title=config['title'],
                label_config=config['config']
            )
            self.projects.append(project)
                        
    def predict(self, tasks: List[Dict], context: Optional[Dict] = None, **kwargs) -> List[Dict]:
        final_predictions = []
        image_dec_tasks = []
        image_kp_tasks = []
        image_ocr_tasks = []
        video_tasks = []

        from_name_k, to_name_k = self.get_config_item('KeyPointLabels')
        from_name_r, to_name_r = self.get_config_item('RectangleLabels')
        from_name_rect, to_name_rect = self.get_config_item('Rectangle')
        from_name_l, to_name_l = self.get_config_item('Labels')
        from_name_ta, to_name_ta = self.get_config_item('TextArea')
        
        for task in tasks:
            try:
                if 'ocr' in task['data']:
                    raw_img_path = task['data']['ocr']
                if 'dec' in task['data']:
                    raw_img_path = task['data']['dec']
                if 'kp' in task['data']:
                    raw_img_path = task['data']['kp']

                if raw_img_path is not None:
                    img_path = self.get_local_path(
                        raw_img_path,
                        task_id=task.get('id')
                    )
                    # printing the mime type of the file 
                    mime = magic.from_file(img_path, mime = True)
                    print(mime)

                    if 'image/' in mime:
                        if 'dec' in task['data']:
                            image_dec_tasks.append(img_path)
                        elif 'kp' in task['data']:
                            image_kp_tasks.append(img_path)
                        elif 'ocr' in task['data']:
                            image_ocr_tasks.append(img_path)

                    elif 'video/' in mime:
                        video_tasks.append(img_path)
                    elif 'audio/' in mime:
                        pass
                    elif mime == 'application/pdf':
                        image_ocr_tasks.append(img_path)
            except Exception as e:
                logger.error(f"Error getting local path: {e}")

        if len(image_dec_tasks) > 0:
            final_predictions.append(self.multiple_dec_tasks(image_dec_tasks, from_name_r, to_name_r))
        if len(image_kp_tasks) > 0:
            final_predictions.append(self.multiple_kp_tasks(image_kp_tasks, from_name_r, to_name_r, from_name_k, to_name_k))
        if len(image_ocr_tasks) > 0:
            final_predictions.append(self.multiple_ocr_tasks(image_ocr_tasks, from_name_rect, to_name_rect, from_name_l, to_name_l, to_name_ta))
        return final_predictions
    
    def multiple_dec_tasks(self, image_paths, from_name_r, to_name_r):
        
        predictions = []

        all_boxes, all_labels, all_logits, all_lengths = dec_pipeline.run_detection(image_paths, ram_pipeline.run_ram(image_paths))

        for boxes_xyxy, label, logits, (H, W) in zip(all_boxes, all_labels, all_logits, all_lengths):                 
            predictions.extend(self.get_detection_results(boxes_xyxy, label, logits, (H, W), from_name_r, to_name_r))

        return {
            'result': predictions,
            'score': 0,
            'model_version': self.get('model_version')
        }
    def multiple_kp_tasks(self, image_paths, from_name_r, to_name_r, from_name_k, to_name_k):
        
        predictions = []

        all_keypoints, all_boxes, all_labels, all_logits, all_lengths = kp_pipeline.run_keypoints(image_paths)
        
        for points, (H, W) in zip(all_keypoints, all_lengths):            
            predictions.extend(self.get_keypoint_results(points, (H, W), from_name_k, to_name_k))

        for boxes_xyxy, label, logits, (H, W) in zip(all_boxes, all_labels, all_logits, all_lengths):                 
            predictions.extend(self.get_detection_results(boxes_xyxy, label, logits, (H, W), from_name_r, to_name_r))

        return {
            'result': predictions,
            'score': 0,
            'model_version': self.get('model_version')
        }
    
    def multiple_ocr_tasks(self, image_paths, from_name_r, to_name_r, from_name_l, to_name_l, textarea_tag):
        
        predictions = []

        res_list = ocr_pipeline.run_ocr(image_paths)
        
        for res in res_list:                 
            predictions.extend(self.get_ocr_results(res, from_name_r, to_name_r, from_name_l, to_name_l,textarea_tag))

        return {
            'result': predictions,
            'score': 0,
            'model_version': self.get('model_version')
        }
    
    def get_detection_results(self, all_points, all_labels, all_scores, all_lengths, from_name_r, to_name_r):
        

        results = []
        height, width = all_lengths
        for points, score, label in zip(all_points, all_scores, all_labels):
            # random ID
            label_id = str(uuid4())[:9]
            results.append({
                'id': label_id,
                'from_name': from_name_r,
                'to_name': to_name_r,
                'original_width': width,
                'original_height': height,
                'image_rotation': 0,
                'value': {
                    "rectanglelabels": [label],
                    'rotation': 0,
                    'width': (points[2] - points[0]) / width * 100,
                    'height': (points[3] - points[1]) / height * 100,
                    'x': points[0] / width * 100,
                    'y': points[1] / height * 100
                },
                'score': float(score),
                'type': 'rectanglelabels',
                'readonly': False
            })

        return results
    
    def get_keypoint_results(self, points, lengths, from_name_k, to_name_k):
        
        results = []
        height, width = lengths

        for point in points:
            
            # creates a random ID for your label everytime so no chance for errors
            label_id = str(uuid4())[:9]

            results.append({
                'id': label_id,
                'from_name': from_name_k,
                'to_name': to_name_k,
                'original_width': width,
                'original_height': height,
                'image_rotation': 0,
                'value': {
                    'x': point[0] / width * 100,
                    'y': point[1]/ height * 100,
                    'width': 0.1,
                    'labels': [point[2]],
                    'keypointlabels': [point[2]]
                },
                'score': 1.0,
                'readonly': False,
                'type': 'keypointlabels'
            })
        
        return results
    
    def get_ocr_results(self, res, from_name_r, to_name_r, from_name_l, to_name_l,textarea_tag):
        results = []
        height, width = res[1]
        angle = int(res[2])
        for rs in res[0]:
            for r in rs['res']:
                # random ID
                label_id = str(uuid4())[:9]
                points = [r['text_region'][0][0],r['text_region'][0][1],r['text_region'][2][0],r['text_region'][2][1]]
                results.append({
                    'id': label_id,
                    'from_name': from_name_r,
                    'to_name': to_name_r,
                    'original_width': width,
                    'original_height': height,
                    'image_rotation': angle,
                    'value': {
                        'rotation': 0,
                        'width': (points[2] - points[0]) / width * 100,
                        'height': (points[3] - points[1]) / height * 100,
                        'x': points[0] / width * 100,
                        'y': points[1] / height * 100
                    },
                    'score': float(r['confidence']),
                    'type': 'rectangle',
                    'readonly': False
                })

        return results
    
    def train(self, annotations, **kwargs):
        odvg_annos = []
        ram_annos = []
        for annos in annotations:
            if 'dec' in annos['data']:
                raw_img_path = annos['data']['dec']
                img_path = self.get_local_path(
                        raw_img_path,
                        ls_access_token=self.LABEL_STUDIO_ACCESS_TOKEN,
                        ls_host=self.LABEL_STUDIO_URL,
                        task_id=annos['id']
                )
                ret = {"filename": img_path,
                        "height": annos['originalHeight'],
                        "width": annos['originalWidth'],
                        'detection':{}}
                
                instances = []
                for anno in annos['annotations']:
                    instances.append({'bbox':[anno['result'][0]['value']['x'], anno['result'][0]['value']['y'], 
                                        anno['result'][0]['value']['width'], anno['result'][0]['value']['height']], 
                                'category':anno['result'][0]['value']['rectanglelabels'][0], 'label':0})
                ret['detection']['instances'] = instances
                odvg_annos.append(ret)

        dec_pipeline.train_detection(odvg_annos)