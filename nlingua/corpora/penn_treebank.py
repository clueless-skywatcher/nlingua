import os
import re
import zipfile
from io import BytesIO

import requests

from nlingua.corpora._constants import *
from nlingua.corpora.base import TaggingCorpus

class PennTreebankCorpus(TaggingCorpus):
    PENN_TREEBANK_REGEX = r'[A-Za-z!.,]+/[A-Za-z!.,]+'
    def __init__(self, download = True, *args, **kwargs) -> None:
        super(PennTreebankCorpus, self).__init__(*args, **kwargs)
        if self._platform == "Windows":
            data_dir = LOCAL_CORPORA_DIR_WINDOWS
        elif self._platform == "Mac":
            data_dir = LOCAL_CORPORA_DIR_MAC
        else:
            data_dir = LOCAL_CORPORA_DIR_UNIX

        if download:
            response = requests.get(PENN_TREEBANK_SRC)
            print("Downloaded Penn Treebank Sample...")
            zip_file = zipfile.ZipFile(BytesIO(response.content))
            zip_file.extractall(f"{data_dir}/data")

        self._folder_path = PENN_TREEBANK_SRC.split("/")[-1].split(".")[0]
        self._folder_path = os.path.join(data_dir, "data", self._folder_path, "tagged")
        self._read()

    def files(self):
        return [x for x in os.listdir(self._folder_path) if x.startswith('wsj')]

    def _read(self):
        x = self.files()
        file_tags = {}
        for wsj in x:
            pos_tags = []
            path = os.path.join(self._folder_path, wsj)
            with open(path, 'r') as f:
                for line in f.readlines():
                    matches = re.findall(self.PENN_TREEBANK_REGEX, line)
                    if len(matches) > 0:
                        for m in matches:
                            pos_tags.append(tuple(m.split('/')))
            file_tags[wsj] = pos_tags

        self._data = file_tags

    def tagged_words(self, file_or_list):
        if isinstance(file_or_list, str):
            try:
                return self._data[file_or_list]
            except:
                print(f"File named: {file_or_list} was not found")
        elif isinstance(file_or_list, list):
            return_list = []
            for x in file_or_list:
                try:
                    return_list.append(self._data[x])
                except KeyError as e:
                    print(f"File named: {x} was not found")
            return return_list