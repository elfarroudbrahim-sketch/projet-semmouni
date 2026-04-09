import requests
from PyPDF2 import PdfReader
import io

def extract_pdf_meta(url):
    print(f'\n[+] Extracting Metadata from: {url}')
    try:
        response = requests.get(url, timeout=10)
        with io.BytesIO(response.content) as f:
            reader = PdfReader(f)
            info = reader.metadata
            if info:
                for key, value in info.items():
                    print(f'  |-- {key.replace("/", "")}: {value}')
            else:
                print('  [-] No metadata found.')
    except Exception as e:
        print(f'  [!] Error: {e}')
