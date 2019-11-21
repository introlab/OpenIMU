import glob
import os


class FileManager:

    @staticmethod
    def get_file_list(from_path: str) -> dict:
        # Build file list
        file_list = {}  # Dictionary: file and base_data_folder (data participant ID)

        # Add files to list
        files = glob.glob(from_path + "/**/*.*", recursive=True)  # Files in sub folders
        for file in files:
            file_name = file.replace("/", os.sep)
            data_name = file.replace(from_path, "")
            data_name = data_name.replace("/", os.sep)
            # data_name = os.path.split(data_name)[0].replace(os.sep, "")
            data_name = data_name.split(os.sep)
            index = 0
            if data_name[index] == '':
                index = 1
            data_name = data_name[index]

            if file_name not in file_list:
                file_list[file_name] = data_name

        return file_list

    @staticmethod
    def merge_folders(root_src_dir: str, root_dst_dir: str):
        import os
        import shutil

        for src_dir, dirs, files in os.walk(root_src_dir):
            dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            for file_ in files:
                src_file = os.path.join(src_dir, file_)
                dst_file = os.path.join(dst_dir, file_)
                if os.path.exists(dst_file):
                    # in case of the src and dst are the same file
                    if os.path.samefile(src_file, dst_file):
                        continue
                    os.remove(dst_file)
                shutil.move(src_file, dst_dir)
