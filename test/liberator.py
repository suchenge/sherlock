import os
import zipfile
import pyzipper
import concurrent.futures


zip_folder = r'E:\Download\dsqn'
password = str.encode('dsqn', encoding="utf-8")

def zipfile_extract(zip_file_path):
    zip_file = zipfile.ZipFile(zip_file_path)
    files = zip_file.filelist

    worker = [{'executor': zip_file, 'file': item} for item in files if is_pic(item.filename)]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(zipfile_extract_work, worker)

    zip_file.close()

def is_pic(file_path):
    file_types = ['.jpg', '.gif']
    for file_type in file_types:
        if file_path.endswith(file_type) is True:
            return True
    return False

def zipfile_extract_work(work):
    file = work['file']
    executor = work['executor']
    executor.extract(file.filename, path=zip_folder, pwd=password)

def zipfile_extractall(zip_file_path):
    zip_file = zipfile.ZipFile(zip_file_path)
    zip_file.extractall(zip_folder, pwd=password)
    zip_file.close()

def zipper_extract(zip_file_path):
    try:
        with pyzipper.AESZipFile(zip_file_path, 'r', compression=pyzipper.ZIP_DEFLATED) as zf:
            zf.setpassword(password)
            zf.extractall(path=zip_folder, pwd=password)
    except Exception as e:
        print(str(e))


for path in os.listdir(zip_folder):
    if path is not None and path != '':
        zipfile_extract(os.path.join(zip_folder, path))

print("Done")


