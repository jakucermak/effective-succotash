import os
from typing import List
from requests import get, RequestException
from bs4 import BeautifulSoup
from multiprocessing import Pool

BASE_URL = "https://kojipkgs.fedoraproject.org/compose/branched/"

class Compose:
    def __init__(self, build_name: str, link:str):
        self.build_name = build_name
        self.link = link

class ComposeSet():

    def __init__(self, composes: List[Compose]):
        self.available_composes = composes

    @classmethod
    def fetch(cls):
        response = get(BASE_URL)
        soup = BeautifulSoup(response.text, "html.parser")
        versions: List[Compose] = []
        for link in soup.find_all("a"):
            href = link.get("href")
            if href and "Fedora" in href:

                build_name = href.strip("/")
                link = BASE_URL + href
                versions.append(Compose(build_name,link))

        return cls(versions)

    def download_rpms(self, compose: Compose):
        url = compose.link + "compose/metadata/rpms.json"
        try:
            # https://kojipkgs.fedoraproject.org/compose/branched/Fedora-41-20241011.n.0/compose/metadata/rpms.json
            filename = os.curdir + "/" + compose.link.split("/")[-2] + '-rpms.json'

            response = get(url, stream=True)
            response.raise_for_status()

            with open(filename, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print("File downloaded: {}".format(filename))
            return filename
        except RequestException as e:
            raise Exception("Error during download {}: {}".format(url, e))


    def download(self, composes: List[Compose]) -> List[str]:
        with Pool(2) as pool:
            file_paths = pool.map(self.download_rpms, composes)
            return file_paths
