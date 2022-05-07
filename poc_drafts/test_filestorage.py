import requests
from http import HTTPStatus

file_upload_url = 'http://39.98.50.209:5145/un/file'
file_download_url = 'http://39.98.50.209:5145/dn/file'


def upload_file(file_path, days=999, error_on_exists=False):
    file = {
        'file': open(file_path, 'rb'),
        'days': days
    }
    request = requests.post(file_upload_url, files=file)
    if request.status_code == HTTPStatus.OK:
        response = request.json()['data']
        file_id = response['afid']
        is_exist = response['is_exist']
        if error_on_exists and is_exist:
            raise Exception('File already exists.')
        return file_id


def download(file_id, download_path):
    with requests.get('/'.join(s.strip('/') for s in [file_download_url, file_id])) as request:
        request.raise_for_status()
        with open(download_path, 'wb') as f:
            for chunk in request.iter_content(chunk_size=8192):
                f.write(chunk)


if __name__ == '__main__':
    file_path = '../compiled_contracts/storage_bytecode.txt'
    file_id = upload_file(file_path)
    print(file_id)
    download(file_id, './test_download_file_from_endpoint.txt')
