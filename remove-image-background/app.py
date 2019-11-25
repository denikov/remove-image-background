#!/usr/local/bin python3

import os
import sys
import platform
import time

from browser import Browser
from opencv import OpenCV
import services


class App:

    def __init__(self):
        self._browser = Browser()



    def validateFile(self):
#validate that path to a file was provided
        try:
            file_path = sys.argv[1]
        except IndexError:
            return 'File path not provided for your search list.'
        else:
            if os.path.exists(file_path) == False:
                return 'File path does not exist.  Please provide a valid path to your search list file.'
            elif file_path.find('.json') == -1:
                return 'Your file does not have a valid JSON extension.'

        services._file_path = file_path
        return



    def startSearch(self):
        initialName = services.loadList()
        if initialName is None:
            self._browser.close()
        else:
            self._browser.search(initialName)
            self._browser.previewIsSelected()



    def run(self):

        validated = self.validateFile()
        if validated is not None:
            print(validated)
            self._browser.close()
            return

        cwd = os.getcwd()
        if not os.path.exists(os.path.join(cwd, 'remove-image-background/temp')):
            os.makedirs(os.path.join(cwd, 'remove-image-background/temp'))
        if not os.path.exists(os.path.join(cwd, 'remove-image-background/downloads')):
            os.makedirs(os.path.join(cwd, 'remove-image-background/downloads'))

        self.startSearch()



if __name__ == '__main__':
    App().run()
