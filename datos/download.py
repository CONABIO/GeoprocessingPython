import requests
import codecs
from io import BytesIO
# from zipfile import ZipFile
from os import path
import fire
import shutil


def _readUrlsFromFile(folder_path):
    with codecs.open(folder_path, encoding='utf-8') as f:
        urls = [url for url in f.readlines()]

    return [url.strip('\n') for url in urls]


def DownloadData(input_file, output_folder='./'):
    urls = _readUrlsFromFile(input_file)

    for url in urls:
        zip_name = url.split('/')[-1]
        r = requests.get(url)
        if r.ok:
            print(u'Escribiendo {}'.format(zip_name))
            with open(path.join(output_folder, zip_name), 'wb') as f:
                shutil.copyfileobj(BytesIO(r.content), f)
        else:
            print(u'Error en descarga de {}'.format(zip_name))


if __name__ == '__main__':
    fire.Fire(DownloadData)
