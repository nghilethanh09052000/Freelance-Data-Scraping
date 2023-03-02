# Insructions for creating virtual environment, intalling required dependencies and running scrapy project


1. Installing and running Splash docker: Which is needed for the script.
first Install docker: Linux or Macos
```
sudo docker pull scrapinghub/splash
sudo docker run -it -p 8050:8050 --rm scrapinghub/splash
```
https://splash.readthedocs.io/en/latest/install.html
 
2. Virtual environment and installing dependencies
```
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

3. Running
```
source venv/bin/activate
scrapy crawl flickr 
scrapy crawl flickr -O result.json

```

# Instructions for Pycharm in the video attached



- We want to make a large scale image dataset for Machine Learning. There will be few search tags like "landscape", "seascape", "nightscape", "cityscape", "long exposure", "waterfall", "forest", "mountain" etc. 

- Each tag we want to crawl around 50 - 100K images then filter out the best 25K Good-Images based on user statistics (likes, views etc). 

- Only images having EXIF metadata will be scrapped and metadata will be updated to DB (preferred MongoDB).Images can be called from Flickr.com, Pexels.com, Pixabay.com, Unsplash.com.