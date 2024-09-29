import gdown
import tarfile
import os
import glob
from pathlib import Path
import argparse


file_id = '12XoMqhANCWrnFFrl-3cDmd9Xx_hVkJrk'
url = f'https://drive.google.com/uc?/export=download&id={file_id}'
root_dir = Path(__file__).parent.parent
output = f'{root_dir}/BrainTumourRaw.tar'

old_folder_name = f'{root_dir}/Task01_BrainTumour'
new_folder_name = f'{root_dir}/BrainTumourData'

def download_dataset(url, output):
    gdown.download(url, output, quiet=False)


def extract_dataset(output):
    with tarfile.open(output, 'r') as tar:
        tar.extractall(f'{root_dir}')
        print("Extraction completed!")

def rename_folders(old_folder_name, new_folder_name):
    os.rename(old_folder_name, new_folder_name)
    print(f"Folder renamed from '{old_folder_name}' to '{new_folder_name}'")

def delete_hidden_files(folder_path):
    for file_path in glob.iglob(os.path.join(folder_path, '**', '._*'), recursive=True):
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")
    
    print(f"Every hidden file in '{folder_path}' has been deleted!")


def main():
    parser = argparse.ArgumentParser(description="Dataset management script")
    parser.add_argument('--manual', action='store_true', help='If set, skips the dataset download')
    args = parser.parse_args()

    if not args.manual:
        download_dataset(url, output)
    extract_dataset(output)
    rename_folders(old_folder_name, new_folder_name)
    delete_hidden_files(new_folder_name)

if __name__ == "__main__":
    main()