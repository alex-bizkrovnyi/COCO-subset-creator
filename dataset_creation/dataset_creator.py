import os.path
import shutil

from pycocotools.coco import COCO

from utils.file_utils import FileUtils


class DatasetCreator:

    @classmethod
    def __create_annotations_file(cls, source_annotations_path, list_subset_classes: list[list]):
        """
        This method is used to create a subset of original COCO annotations file based on defined classes.
        This method uses COCO API

        :param source_annotations_path: path to original annotations json file
        :param list_subset_classes: list of defined classes which are needed in subset
        :return: JSON in dict form
        """
        coco = COCO(source_annotations_path)
        subset_annotations = []
        subset_images = []
        subset_cat_ids = set()

        total_image_ids_set = set()

        for classes in list_subset_classes:
            cat_ids = coco.getCatIds(catNms=classes)
            subset_cat_ids.update(cat_ids)
            img_ids_for_classes = set(coco.getImgIds(catIds=cat_ids))

            required_images = img_ids_for_classes - total_image_ids_set
            total_image_ids_set.update(required_images)

            for img_id in required_images:
                ann_ids = coco.getAnnIds(imgIds=img_id, catIds=cat_ids)
                annotations = coco.loadAnns(ann_ids)
                subset_annotations.extend(annotations)

            subset_images.extend(coco.loadImgs(img_ids_for_classes))

        # Create a subset dataset dictionary

        return {
            "info": coco.dataset['info'],
            "licenses": coco.dataset['licenses'],
            "images": subset_images,
            "annotations": subset_annotations,
            "categories": [coco.cats[cat_id] for cat_id in subset_cat_ids]
        }

    @staticmethod
    def __generate_source_images_path_dict(images_location):
        """
        This method is used to create a dict where {file_name -> absolute path to image}.
        This action is a performance improvement.
        :param images_location:
        :return: dict {file_name -> absolute path to image}
        """
        file_paths_dict = {}
        for dir_path, dirs, files in os.walk(images_location):
            for file in files:
                file_paths_dict.update({file: os.path.join(dir_path, file)})

        return file_paths_dict

    def __generate_source_dest_images_paths(self,
                                            original_images_zip_location,
                                            temp_images_location,
                                            subset_annotations,
                                            destination_folder):
        """
        This method is used to create a dictionary with paths to required for subset source images and
        their destination location.
        :param original_images_zip_location: path to source images zip location
        :param temp_images_location: path where source images will be saved temporary
        :param subset_annotations: created json for COCO subset
        :param destination_folder: path to store subset images
        :return: dict where {source_path_to_image: destination_path}
        """
        FileUtils.unzip_to_folder(original_images_zip_location, temp_images_location)
        images_location_paths = self.__generate_source_images_path_dict(temp_images_location)
        images_count = len(subset_annotations['images'])
        current_image_count = 0
        images_paths = {}
        for image in subset_annotations['images']:
            current_image_count = current_image_count + 1
            images_paths.update({
                images_location_paths[image['file_name']]: os.path.join(destination_folder, image['file_name'])
            })
            print(f"Preparing: {image['file_name']} to {destination_folder}. "
                  f"Prepare {current_image_count} from {images_count}")
        return images_paths

    def create_dataset_subset(self, params):
        """
        Main method for subset creation. Currently, only train and valid subset creation is supported.
        :param params:
        :return:
        """
        train_subset_output_path = 'coco_subset/train/'
        valid_subset_output_path = 'coco_subset/valid/'
        temp_images_location = 'temp_images'

        print("Creation of training annotations")
        train_subset_annotations = self.__create_annotations_file(params['train_source_annotations_path'],
                                                                  params['classes'])
        print("Creation of valid annotations")
        valid_subset_annotations = self.__create_annotations_file(params['valid_source_annotations_path'],
                                                                  params['classes'])

        print("Saving created annotations files")
        if not os.path.exists(train_subset_output_path):
            os.makedirs(train_subset_output_path)
        if not os.path.exists(valid_subset_output_path):
            os.makedirs(valid_subset_output_path)

        print("Saving training annotations files")
        FileUtils.save_json(train_subset_annotations, f'{train_subset_output_path}_annotations.coco.json')
        print("Saving valid annotations files")
        FileUtils.save_json(valid_subset_annotations, f'{valid_subset_output_path}_annotations.coco.json')

        print("Saving train images")
        train_images_paths = self.__generate_source_dest_images_paths(params['train_source_images_zip_path'],
                                                                      temp_images_location,
                                                                      train_subset_annotations,
                                                                      train_subset_output_path)
        FileUtils.save_files_in_parallel(train_images_paths)
        shutil.rmtree(temp_images_location)
        print("Saving valid images")
        valid_images_paths = self.__generate_source_dest_images_paths(params['valid_source_images_zip_path'],
                                                                      temp_images_location,
                                                                      valid_subset_annotations,
                                                                      valid_subset_output_path)
        FileUtils.save_files_in_parallel(valid_images_paths)
        shutil.rmtree(temp_images_location)
