#!/usr/bin/python3

# Build .qrc files from SVG files


import os.path
import re

CURRENT_PATH=os.path.realpath(os.path.dirname(__file__))

CONFIG={
        'LINKS':{
                '32dp':          'ch/images/normal',
                '32dp-disabled': 'ch/images/disabled',
            },

        'TARGETS':{
                'FILES': {
                        'dark': 'dark_icons.qrc',
                        'light': 'light_icons.qrc',
                    },
                'PATH': CURRENT_PATH
            }
    }


def main():
    """main process"""

    for fileKey in CONFIG['TARGETS']['FILES']:
        fileContent=['<!DOCTYPE RCC><RCC version="1.0">']


        for srcLink in CONFIG['LINKS']:
            for srcFormat in ['svg']:
                directoryToProcess=os.path.join(CURRENT_PATH, srcFormat, fileKey, srcLink)

                if os.path.isdir(directoryToProcess):
                    fileContent.append(f'''  <qresource prefix="{CONFIG['LINKS'][srcLink]}">''')

                    directoryContent=os.listdir(directoryToProcess)

                    fileList=[]

                    for fileName in directoryContent:
                        fullPathFileName=os.path.join(directoryToProcess, fileName)

                        if os.path.isfile(fullPathFileName):
                            fName=re.search("(.*)\.(svg|png)$", fileName)

                            if fName:
                                fileList.append(fileName)

                    for fileName in sorted(fileList):
                        fName=re.search("(.*)\.(svg|png)$", fileName)
                        fileContent.append(f'    <file alias="{fName.groups()[0]}">{srcFormat}/{fileKey}/{srcLink}/{fileName}</file>')

                    fileContent.append(f'  </qresource>')

        fileContent.append('</RCC>')

        targetFileName=os.path.join(CONFIG['TARGETS']['PATH'], CONFIG['TARGETS']['FILES'][fileKey])
        print("Target: ", targetFileName)
        with open(targetFileName, 'w') as fHandle:
            fHandle.write("\n".join(fileContent))



if __name__ == "__main__":
    main()
