from dataset_creation.dataset_creator import DatasetCreator

if __name__ == '__main__':
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
