import itertools
import json
import multiprocessing
import os
import shutil
import zipfile


class FileUtils:

    @staticmethod
    def save_json(data, file_name):
        with open(file_name, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    @staticmethod
    def unzip_to_folder(original_images_zip_location, temp_images_location):
        """
        This method is used to unzip source images zip to temp folder for further subset creation.
        :param original_images_zip_location: path to zip with source images.
        :param temp_images_location: Location where unzipped images will be stored
        :return:
        """
        os.mkdir(temp_images_location)
        print("Unzipping source images")
        with zipfile.ZipFile(original_images_zip_location, 'r') as zip_ref:
            zip_ref.extractall(temp_images_location)

    @staticmethod
    def save_files_in_parallel(files_location_map):
        """
        This method is used to copy files defined in files_location_map.
        In general, it is used for copying source images to destination folder in parallel.
        :param files_location_map:
        :return:
        """

        def copying(files_location: dict[str, str]):
            current_image_count = 0
            for source, dest in files_location.items():
                current_image_count = current_image_count + 1
                print(
                    f"Copying: {source} to {dest}. Copying {current_image_count} from chunk {len(files_location)}. Total {images_count}")
                shutil.copyfile(source, dest)

        images_count = len(files_location_map)
        paths_chunks = FileUtils.split_dict(files_location_map, os.cpu_count())
        jobs = []
        for chunk in paths_chunks:
            process = multiprocessing.Process(target=copying, args=(chunk,))
            process.start()
            jobs.append(process)

        for job in jobs:
            job.join()

    @staticmethod
    def split_dict(x, chunks):
        """
        Util method to divide the dictionary to equal-size chunks
        :param x:
        :param chunks:
        :return:
        """
        i = itertools.cycle(range(chunks))
        split = [dict() for _ in range(chunks)]
        for k, v in x.items():
            split[next(i)][k] = v
        return split
