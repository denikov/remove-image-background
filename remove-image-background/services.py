'''
TODO: make this into a singleton class
'''

import sys
import os
import platform
import json
import glob


_name_list = []
_current_index = 0

#file path gets set from App
_file_path = None



def checkAllFound():
    global _name_list
    global _current_index
    if _current_index == len(_name_list):
        print('All found')
        return None
    else:
        try:
            return _name_list[_current_index]['name']
        except:
            return None



def getLastImage():
    return max(glob.iglob('./remove-image-background/temp/*'), key = os.path.getctime)



def removeFromTemp():
# remove from temp folder the latest downloaded image
    imgName = getLastImage()
    try:
        os.remove(imgName)
    except:
        pass
    return



def addToJSON(fileName):
    global _name_list
    global _current_index
    global _file_path

    _name_list[_current_index]['file'] = fileName
    with open(_file_path, 'w') as outfile:
        json.dump(_name_list, outfile, ensure_ascii=False, indent=2)

    _current_index += 1

    removeFromTemp()

# returns either a name or None
    return checkAllFound()



def loadList():
    global _name_list
    global _current_index
    global _file_path

    if len(_name_list) == 0:
        with open(_file_path) as p:
            _name_list = json.load(p)

    if platform.system() == 'Windows':
        for i, e in reversed(list(enumerate(_name_list))):
            if 'file' not in _name_list[i]:
                _current_index = i
                break
    else:
        for i in range(len(_name_list)):
            if 'file' not in _name_list[i]:
                _current_index = i
                break

# returns either a name or None
    return checkAllFound()

