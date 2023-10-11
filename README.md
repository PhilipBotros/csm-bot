# CSM bot 

CSM bot is an application that helps CSMs navigate the large amount of information inside companies.
This is done by ingesting company specific information and giving the CSMs an interface to chat to the language model.

Currently, there are two ways of interacting with it:
1. Invoke it on Slack and chat directly to the bot
2. Use the web UI to chat to the model

## Configure environment
Create a virtual environment in python and install requirements.txt

```bash
$ python -m virtualenv .venv
$ pip install -r requirements.txt
```

You might get an error concerning sqlite3-binary.

This is due to 
```
pysqlite3-binary==0.5.0
```
in requirements.txt, which is needed on Azure because it comes with an old version of sqlite3.

## Secrets
Secrets are currently stored in a .env file, you'll need this before being able to run the application.

## Build the UI
The web-ui is built using [vue.js](https://vuejs.org).

To serve it, you need to a create bundle
```bash
$ cd webui
$ npm install
$ npm run build
```

## Run the web page

```bash
$ python -m flask run -p 3000
```


## Slack Bot
You basically need a tunnel to connect your local dev environment with slack infra. This can be achieved by running _ngrok_.

Installing it might be as easy as running

```bash
$ brew install ngrok
```

Then run it as

```bash
ngrok http 3000
```

