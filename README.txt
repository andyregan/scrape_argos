=Description=
Scrapes the Argos.ie site for catalogue items.

=Requirements=

Python 2.7.3.

See requirements.txt for Python requirements.

=Usage= 
To crawl the argos site and save catalogue items in JSON format run the following:

$scrapy crawl argos -o ~/catalogue-items.json -t json
