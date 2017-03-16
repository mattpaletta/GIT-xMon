import fileinput
import os
import sys
import time
from sys import version_info
import PIL
from PIL import Image
import json
from pprint import pprint
from shutil import copyfile
import watchdog

# 1. Find all source material, languages, assets collections, graphics files, etc.
# 2. Check if any materials are not in the app, if not, create them and add it
# 3. Wait for any of them to be updated
# 4. Recreate files on change and copy to correct destination

class Watcher:
    projName = ""
    containspod = False

    # Keep track of source images and Xcode assets
    images = {}
    source = {}

    def writeJSON(filename, data):
        with open(filename, 'w') as outfile:
            json.dump(data, outfile)

    def resize(source, dest, width, height=0):
        img = Image.open(source)
        
        wpercent = width / float(img.size[0])
        if height > 0:
            hsize = int(height / float(img.size[1]))
        else:
            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((width, hsize), PIL.Image.ANTIALIAS)

        img.save(dest)

    def indexDir():
        
        print("Scanning Directory")
        # Search for project name
        for root, subFolders, files in os.walk("."):
            for file in files:
                if file.endswith('.xcodeproj'):
                    print("Found Project File!")
                    projName = os.path.splitext(file)[0] # Assume the name from the xcode project

                elif file == "Podfile":
                    print("Found PodFile!")
                    containspod = True

        if not os.path.exists(projName):
            print("Project not found.  Exiting!")
            return False
        
        print("Looking for image assets")
        for root, subFolders, files in os.walk(projName):
            for file in files:
                if file.endswith('.png') or file.endswith('.jpg'):
                    # Found an image!
                    filePath = os.path.join(root, file)
                    img = Image.open(source)
                    
                    # In height & width, assume 1x
                    image = {
                        "root": root,
                        "width": img.size[0],
                        "height": img.size[1]
                    }
                    
                    images[file] = image

        print("Looking for source assets")
        for root, subFolders, files in os.walk("Graphics"):
            for file in files:
                if file.endswith('.png') or file.endswith('.jpg') or file.endswith('.ai') or file.endswith('.psd'):
                    # Found an image!
                    filePath = os.path.join(root, file)
                    img = Image.open(source)
                    
                    # In height & width, assume 1x
                    image = {
                        "root": root,
                        "width": img.size[0],
                        "height": img.size[1]
                    }
                    
                    source[file] = image

        print("Looking for App Icon")
        if not 'AppIcon' in images.keys():
            print("AppIcon Not Found Exiting!")
            #return False
        else:
            print("App Icon Found!")


        print("Looking for languages")
        for root, subFolders, files in os.walk(projName):
            for file in files:
                if file.endswith('.lproj'):
                    print("Found language: "+file)


        return True # Successfully indexed app




def main():
    py3 = version_info[0] > 2
    overwrite = True
    over = ""
    
    print("\n\t Icon Creator by Matthew Paletta\n")

    while not os.path.exists("Graphics"):
        print("Creating images folder...")
        os.makedirs("Graphics")
        _ = input("It seems there was no images directory here.  We just created one for you!  Drag any images you would like to use in that folder, then press enter to continue.")

    #continue from while loop
    print("Graphics folder found")

    # HAVE A METHOD FOR ADDING A NEW IMAGE!
    # Eventually translate the app automatically?

    if indexDir == False:
        return


if __name__ == '__main__':
    main()
