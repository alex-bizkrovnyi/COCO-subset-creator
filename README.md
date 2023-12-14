1. Download the following files. There are COCO dataset:
- http://images.cocodataset.org/zips/train2017.zip
- http://images.cocodataset.org/zips/val2017.zip
- http://images.cocodataset.org/annotations/annotations_trainval2017.zip
3. Define subset of classes which are needed:
```python
    subset_classes = [
        ['person', 'bicycle'],
        ['person'],
        ['cat']
    ]
```
**Pay attention:** In case, if classes list contains more, than one class, for ex: **['person', 'bicycle']**, then images will 
be found for both **['person', 'bicycle']** classes on the same picture. If you want to include only one class, for ex. person,
then add list **['person']**, where only one class.

3. Application parameters:
   ```python
    params = {
        'train_source_annotations_path': 'path_to_annotation_file/instances_train2017.json',
        'valid_source_annotations_path': 'path_to_annotation_file/instances_val2017.json',
        'classes': subset_classes,
        'train_source_images_zip_path': coco_train_images_zip_file,
        'valid_source_images_zip_path': coco_valid_images_zip_file
    }
    ```
    | Name | Description |
   | -------- | ------- |
    | train_source_annotations_path | Path to file: **instances_train2017**. Which is placed under http://images.cocodataset.org/annotations/annotations_trainval2017.zip  |
    | valid_source_annotations_path | Path to file: **instances_val2017.json**. Which is placed under http://images.cocodataset.org/annotations/annotations_trainval2017.zip |
    | classes | List of Lists, where defined needed classes to subset.|
    | train_source_images_zip_path | Path to zip with train images from COCO dataset.|
    | valid_source_images_zip_path | path to zip with val images from COCO dataset. | 


### Converting COCO subset to YOLO format.
- The YOLO **\*.yaml** file contains mapping of COCO dataset categories ids to YOLO.yaml format based on annotations.json 
in COCO dataset.
- The following [link](https://github.com/ultralytics/ultralytics/blob/main/ultralytics/cfg/datasets/coco8.yaml) contains 
source page with definition of YOLO yaml file base on full COCO dataset.
  - There can be found the following:
```yaml
  # Classes
    names:
      0: person
      1: bicycle
      2: car
      3: motorcycle
      4: airplane
      5: bus
      6: train
      7: truck
      8: boat
      9: traffic light
      10: fire hydrant
      11: stop sign
      12: parking meter
      13: bench
      14: bird
      15: cat
      16: dog
      17: horse
      18: sheep
      19: cow
      20: elephant
      21: bear
      22: zebra
      23: giraffe
      24: backpack
      25: umbrella
      26: handbag
      27: tie
      28: suitcase
      29: frisbee
      30: skis
      31: snowboard
      32: sports ball
      33: kite
      34: baseball bat
      35: baseball glove
      36: skateboard
      37: surfboard
      38: tennis racket
      39: bottle
      40: wine glass
      41: cup
      42: fork
      43: knife
      44: spoon
      45: bowl
      46: banana
      47: apple
      48: sandwich
      49: orange
      50: broccoli
      51: carrot
      52: hot dog
      53: pizza
      54: donut
      55: cake
      56: chair
      57: couch
      58: potted plant
      59: bed
      60: dining table
      61: toilet
      62: tv
      63: laptop
      64: mouse
      65: remote
      66: keyboard
      67: cell phone
      68: microwave
      69: oven
      70: toaster
      71: sink
      72: refrigerator
      73: book
      74: clock
      75: vase
      76: scissors
      77: teddy bear
      78: hair drier
      79: toothbrush
```

Presented above classes and their ids corresponds to annotations of full coco dataset. If you would like to create a subset 
of **COCO** and then convert it to **YOLO** format, you need to remap original ids to subset ones. 
The following format will not work, because during training YOLO model does not accept it:
    
```yaml
    # Classes
    names:
      names:
      0: person
      1: bicycle
      15: cat
      16: dog
      17: horse
      18: sheep
      19: cow
      20: elephant
      21: bear
      22: zebra
      23: giraffe
      24: backpack
      25: umbrella
      26: handbag
      29: frisbee
      32: sports ball
      33: kite
      36: skateboard
``` 

The following error happened: 
`RuntimeError: Dataset '/content/yolo_format_dataset/coco.yaml' error ❌ '18-class dataset requires class indices 0-17, but you have invalid class indices 0-36 defined in your dataset YAML.'`

So, it is **required** to remap original categories ids and corresponding annotations to own subset ids.

===
**WIP** It is required to add additional link and modernisation of repo. Currently, only COCO subset creation is supported here.
===

### Example of tool USAGE:

```python
    subset_classes = [
        ['person', 'bicycle'],
        ['person', 'dog'],
        ['person', 'horse'],
        ['person', 'cow'],
        ['person', 'backpack'],
        ['person', 'umbrella'],
        ['person', 'handbag'],
        ['person', 'frisbee'],
        ['person', 'sports ball'],
        ['person', 'kite'],
        ['person', 'skateboard'],
        ['frisbee'],
        ['skateboard'],
        ['kite'],
        ['sports ball'],
        ['person'],
        ['bear'],
        ['zebra'],
        ['giraffe'],
        ['horse'],
        ['sheep'],
        ['cow'],
        ['elephant'],
        ['cat']
    ]
    coco_train_annotation_file = 'COCO_DATASET_FULL_2017/annotations_trainval2017/annotations/instances_train2017.json'
    coco_val_annotation_file = 'COCO_DATASET_FULL_2017/annotations_trainval2017/annotations/instances_val2017.json'
    coco_train_images_zip_file = 'COCO_DATASET_FULL_2017/train2017.zip'
    coco_valid_images_zip_file = 'COCO_DATASET_FULL_2017/val2017.zip'

    params = {
        'train_source_annotations_path': coco_train_annotation_file,
        'valid_source_annotations_path': coco_val_annotation_file,
        'classes': subset_classes,
        'train_source_images_zip_path': coco_train_images_zip_file,
        'valid_source_images_zip_path': coco_valid_images_zip_file
    }

    DatasetCreator().create_dataset_subset(params)
```
