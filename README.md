# Demo

## Video Link

Please see [here](https://www.loom.com/share/6fbc69b7778c4c8c898862b1655d5992) to view the demo. See below for timestamps

## Timestamps

- 00:30 - Sending prompt to the backend
- 01:15 - Pptx file received from the backend
- 01:20 - Downloading .pptx file to the desktop
- 01:30 - Walkthrough of the AI generated presentation

\*note, this project is currently not hosted online given API costs

# Stack Information

### Frontend
- Next.js
    - Typescript
    - SCSS

### Backend
- Flask
    - Python

# Installation Instruction

## Client

### To Test Locally

1. change the `BASE_URL` variable located in the context folder to the correct backend URL.
2. run the following commands in the command line:

```
yarn
yarn run dev
```

## Server

### Setup: To run on your local machine run the following

1. Download virtual environment

    - run the following: `pip3 install virtualenv`

2. Setup the virtual environment

-   run the following:

```
python3 -m venv ./venv
source ./venv/bin/activate
pip3 install -r requirements.txt
```

3. Create a .env file

-   add the following code in a .env file, and fill in the API keys

```
OPENAI_API_KEY=KEY_STRING
GOOGLE_CREDS=KEY_JSON
```

4. Run the app

-   run the following: `python3 app.py`
