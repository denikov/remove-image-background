'''
================================================================================
Semi-automated Background Removal of Profile Images

REQUIREMENTS:
    - A JSON file structured as shown here:
      [
        {
          "name": <Some Person>
        },
        {
          "name": <Another Person>
        },
        etc...
      ]

    - Run setup.py to install required resources.

    - Install the correct chromedriver specifically to your Chrome version.
    - - Make sure the PATH to your chromedriver executable is set in you environemnt

USAGE:
    python remove-image-background <path to your JSON file>

TEST (JSON file with 4 names):
    python remove-image-background tests/sample.json

HOW IT WORKS:
    You provide a file structured as shown above. The program opens two Chrome
tabs: google.com and remove.bg. On each name from your file, a Google search is
performed and the "Images" section is opened. You find an image and click on it,
bringing up the preview section. The program detects this, grabs the link to the
image and sends it to remove.bg.  The website removes the background, the
processed image is downloaded to your computer, a profile is cropped and saved.
The file you provided is modified to include the reference to the new image.
================================================================================
'''

from app import App

if __name__ == '__main__':
    print(__doc__)
    App().run()
