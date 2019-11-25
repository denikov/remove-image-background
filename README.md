# remove-image-background
Semi Automated program which takes a user provided list of names, finds images, removes the background, crops and saves the resulting images, creating a transparent profile image.

## Install
`git clone https://github.com/denikov/remove-image-background.git`

`pip install -r requirements.txt`

## Test
`pytest` or `pytest --verbose`

## End to End Test with Sample File
`python remove-image-background tests/sample.json`

## Run
`python remove-image-background <path-to-your-file>`

## How It Works
*View `tests/sample.json` for the format required by the program in order to provide your own file.*

The program uses `Selenium` to control your Chrome browser, opening `google.com` and `remove.bg`. Going through your list of names, it does a search and brings up the `Images` section.  The program waits for you to scroll through the images or alter the search. Once you find a proper image, click on it, bringing up the preview section. This triggers the program to get the URL of that image and sends it to `remove.bg`. That platform removes the background of the image, the processed image is downloaded, `OpenCV` is used for detecting a face, cropping the ROI and saving the result. Then the next name in your list is searched and the process starts all over.

## Requirements
- Download [ChromeDriver - WebDriver for Chrome](https://chromedriver.chromium.org/downloads) from this page. The major version downloaded needs to be the same as your current Chrome version (if your Chrome version is **78**.93..., chromedriver needs to be version **78**...)
- Python3
- Python Virtual Environment is recommended

## Important
This program was created for a specific need so it is written to process images with a single person in them. Selecting an image from Google with more than one person will result in a warning message and you will have to select another. The program relies on OpenCV and Cascade Classifiers to find faces in an image. If the person's face is not very visible (turned away, side view, etc.), OpenCV will not detect it and you will receive a warning message to select another image. Quite large (~ >2500px) images also do not play well with OpenCV's `detectMultiScale()` method so be aware.
