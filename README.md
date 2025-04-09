# dedupe-poc-customerb2c
This project uses Dedupe to complete a POC project 
to test the Dedupe library for adding ML-based 
matching, entity resolution, and record linkage using
Semarchy xDM's Customer B2C tutorial data.

## Set up
1. Follow dedupe's instructions to get the library
```
# Make sure Python and PIP are installed. 
python --version
pip install virtualenv virtualenvwrapper
```
- Environment variables
```
# Add to .zshrc
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=$(which python3)
export PROJECT_HOME=$HOME/Semarchy/semarchy-ml-match
source /usr/local/bin/virtualenvwrapper.sh
```
- Get started installing dedupe using virtual environment:
```
source ~/.zshrc # reload after previous step
mkvirtualenv entity_resolution
pip install dedupe
pip install dedupe-variable-datetime # B2C has date_of_birth
```
- Optional: Libraries
```
pip install -r requirements.txt
pip install pytest
```

2. Create a working version of the CustomerB2C
tutorial demo environment, up to the point of loading data.

Fork
Option A: Thomas's POC integrated with xDM & PostgreSQL
Option B: Minimal POC using CustomerB2C tutorial data
(No programmatic ETL, ETL is manual)

## Option A: Thomas's xDM + dedupe POC with Childcare Data

1. Set up Thomas's Dockerfile. These are my settings
modified for CustomerB2C 

- Tell docker to build: 
```
docker build -t xdm-ml-poc-customerb2c .
```
- Tell docker to run with db settings: 
```
docker run -e db_driver='postgresql' \
-e db='postgres' \
-e db_host='host.docker.internal' \
-e db_port='5432' \
-e db_usr='semarchy_customer_b2c_mdm' \
-e db_pw='semarchy_customer_b2c_mdm' \
-p 8089:80 \
--name xdm-ml-poc-customerb2c xdm-ml-poc-customerb2c
```
2. Set up xDM Job Notification
- Create an HTTP Job Notifications (under Configuration)
Name: FastAPIMLMatcher
Label: FastAPI ML Matcher
Plugin ID: HTTP
Base path: /matchers/person/cluster # TODO: Using xDM Entity name
Leave the remaining settings unpopulated

3. On the data location, add a Job Notification Policy.
Name: DedupeMLMatcher
Label: Dedupe ML Matcher
Notification Server: HTTP server configured in the previous step
Use Complex Condition: Unchecked
Job Name Pattern: CustomerB2C%

## Option B: Minimal set up with B2C Data

1. Take the CSV example and modify the script
https://github.com/dedupeio/dedupe-examples/blob/main/csv_example/csv_example.py
Changes include: 
- Removed pre-processing (as it's performed in xDM enrichers)
- Tweak input & output file names
- Tweak Read Data 
- Tweak fields for defining matching criteria
- Add a timer to figure out how long it takes to run dedupe
- See history of commits to see all the tweaks I made

2. Analyze the results in SQL 
- See database folder for scripts to understand the results

3. Initial impressions & areas for improvement
- The supervised training was straightforward on the 
command line but we'd need a better user interface for
non-technical users. 
- It's great the learned settings & training.json exist.
This makes it much faster to run after providing the initial
training data set and supervised learning inputs
- The training.json also means it's potentially possible to use
UM data to train the model. TODO: Area for future investigation
- I would like weighting in this model. member_id should have a 
much higher weighting than it currently does as this member_id is
one of the most trusted data values that the model should perform
an exact match on.  
- No manual or expert weighting possible. The ML model does the 
weighting based on supervised learning. This means there's a 
compelling purpose for xDM's current match engine. xDM's 
exact match can be useful for expert input and ML can be
used for probabilistic matching.
- There should be monitoring on the model over time, including
a test set with true matches.


## Credits
I'm basing this off Thomas's PoC on dedupe, which uses
childcare agency data. But I'm modifying it for the
CustomerB2C tutorial dataset. 

Thomas's code which connects to xDM is a thin
layer on top of the Python library dedupe by 
Forest Gregg and Derek Eder. 2022. 
Dedupe. https://github.com/dedupeio/dedupe.

which in turn is built on Mikhail Yuryevich Bilenko's 
Ph.D. dissertation: Learnable Similarity Functions and 
their Application to Record Linkage and Clustering.
http://www.cs.utexas.edu/~ml/papers/marlin-dissertation-06.pdf
