# Creating virtual environment and installing dependancies
```
cd project
python -m venv venv
source venv/bin/activate
python -m pip install -r fullRequirements.txt
```

# Running the script: (First activate virtual env)
```
source venv/bin/activate
scrapy crawl user_crawl -o result.json
```


# Parameters can be mopdified in crawler.cfg
1. flickr_url : search input (Default landscape)

2. mongoDb credentials

3. Group crawler parameters:

    * flickr_user 
    * flickr_pass 
    * flickr_message