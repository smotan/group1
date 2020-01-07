# Song search
This programme allows you to search for songs by their lyrics or their themes. 

## Prerequisites
## [Install Flask](http://flask.pocoo.org/docs/1.0/installation/)
We will install Flask in a virtual environment to contain it.

Create a project directory:

```
mkdir myproject
cd myproject
```
And a virtual environment `demoenv`:

```
python3 -m venv demoenv
```

On Windows:

```
py -3 -m venv demoenv
```

Activate the environment:

```
. demoenv/bin/activate
```

On Windows:

```
demoenv/Scripts/activate
```

Install Flask:

```
pip install Flask
```
## Install [pke](https://github.com/boudinfl/pke)
```
pip install git+https://github.com/boudinfl/pke.git
```
You might also need the following resources:
```
python -m nltk.downloader stopwords
python -m nltk.downloader universal_tagset
python -m spacy download en # download the english model
```
## Install [spaCy](https://spacy.io/)

```
pip install -U spacy
```
## Install [scikit-learn](https://scikit-learn.org/stable/index.html)

```
pip install -U scikit-learn
```

## Run this Flask example application

Make sure you are in your `myproject` directory.

Clone the git repository and move to `final_project` directory:

```
git clone https://github.com/smotan/group1.git
cd group1/final_project
```
Set the following environment variables:

Show flask which file to run:

```
export FLASK_APP=ui.py
```

Enable development environment to activate interactive debugger and reloader:

```
export FLASK_ENV=development
```

Set the port in which to run the application, e.g.:

```
export FLASK_RUN_PORT=8000
```

On Windows command line, you can the environment variables with:

```
set FLASK_APP=ui.py
set FLASK_ENV=development
set FLASK_RUN_PORT=8000
```

And on Windows PowerShell:

```
$env:FLASK_APP = "ui.py"
$env:FLASK_ENV = "development"
$env:FLASK_RUN_PORT = "8000"
```
Run the app:

```
flask run
```

Go to `localhost:8000/search` in your browser to see the website.
