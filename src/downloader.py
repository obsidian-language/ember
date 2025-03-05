import requests
import sys

def download_file(url, output):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(output, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Downloaded {output}")
    except requests.RequestException as e:
        print(f"Error downloading {url}: {e}")
        sys.exit(1)
