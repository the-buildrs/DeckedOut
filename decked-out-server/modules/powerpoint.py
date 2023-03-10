from __future__ import print_function

import json
import os.path
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from shutil import copyfileobj
from io import BytesIO

SCOPES = ['https://www.googleapis.com/auth/presentations',
          'https://www.googleapis.com/auth/drive.file']

'''
----------------------------- FUNCTIONS -----------------------------
'''
'''
Authorizes credentials for your Google Account. This step is needed at the start
of every function call, since it checks whether the company (us) is authorized 
to edit the user's account
'''


def authorize_creds():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            local_creds = json.loads(os.getenv("GOOGLE_CREDS"))
            flow = InstalledAppFlow.from_client_config(local_creds, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds


'''Creates a Google Slide presentation. Takes title as input.'''


def create_presentation(title):
    creds = authorize_creds()
    try:
        service = build('slides', 'v1', credentials=creds)
        body = {
            'title': title
        }

        presentation = service.presentations().create(body=body).execute()
        presentation_id = presentation.get('presentationId')
        print(f"Created presentation with ID: {presentation_id}")

        return presentation_id

    except HttpError as error:
        print(f"An error occurred: {error}")
        print("Presentation not created")
        return error


'''
Fills the title page that was created when create_presentation() was called. As
of now, it only inserts the given title_text as the title.
'''


def fill_title_page(presentation_id: str, title_text: str):
    creds = authorize_creds()
    service = build('slides', 'v1', credentials=creds)
    title_slide = service.presentations().get(presentationId=presentation_id,
                                              fields='slides').execute().get('slides', [])[0]
    title_id = title_slide.get('pageElements', [])[0].get('objectId', 0)

    try:
        requests = [
            {
                'insertText': {
                    'objectId': title_id,
                    'text': title_text
                }
            }
        ]

        body = {
            'requests': requests
        }

        response = service.presentations() \
            .batchUpdate(presentationId=presentation_id, body=body).execute()
        create_slide_response = response.get('replies')[0].get('createSlide')
        print("Edited title slide")

    except HttpError as error:
        print(f"An error occurred: {error}")
        print("Title slide not edited")
        return error

    return response


'''
Creates a new slide and fills it with a slide title, an image correlated to the
title, and bullet points
Inputs:
    - presentation_id: the associated id of the presentation that is outputted
        after running create_presentation()
    - page_id: the associated id of the page that is generated in app.py as
        'Page1', 'Page2', etc
    - insertion_index: at what index in the presentation is the new slide going
        to be placed
    - slide_name: title of the slide generated by GPT-3
    - text: bullet points associated with the slide title generated by GPT-3
    - img: image associated with the slide title generated by DALL-E
'''


def fill_presentation(presentation_id: str, page_id: str, insertion_index: int,
                      slide_name: str, text: str, img: str):
    creds = authorize_creds()
    service = build('slides', 'v1', credentials=creds)
    pt350 = {'magnitude': 350, 'unit': 'PT'}

    try:
        requests = [
            {
                'createSlide': {
                    'objectId': page_id,
                    'insertionIndex': insertion_index,
                    'slideLayoutReference': {
                        'predefinedLayout': 'TITLE_AND_TWO_COLUMNS'
                    }
                }
            }
        ]

        # Execute the request.
        body = {
            'requests': requests
        }
        response = service.presentations() \
            .batchUpdate(presentationId=presentation_id, body=body).execute()
        create_slide_response = response.get('replies')[0].get('createSlide')
        print(f"Created slide with ID:"
              f"{(create_slide_response.get('objectId'))}")

        curr_slide = service.presentations().get(presentationId=presentation_id,
                                                 fields='slides').execute().get('slides', [])[-1]
        title_id = curr_slide.get('pageElements', [])[0].get('objectId', 0)
        text_id = curr_slide.get('pageElements', [])[2].get('objectId', 0)

        requests = [
            {
                'insertText': {
                    'objectId': title_id,
                    'text': slide_name
                }
            },

            {
                'insertText': {
                    'objectId': text_id,
                    'text': text
                }
            },

            {
                'createImage': {
                    'objectId': 'Image'+str(insertion_index),
                    'url': img,
                    'elementProperties': {
                        'pageObjectId': page_id,
                        'size': {
                            'height': {'magnitude': 3500000, 'unit': 'EMU'},
                            'width': {'magnitude': 3500000, 'unit': 'EMU'}
                        },
                        'transform': {
                            'scaleX': 1,
                            'scaleY': 1,
                            'translateX': 400000,
                            'translateY': 1100000,
                            'unit': 'EMU'
                        }
                    }
                }
            }
        ]

        # Execute the request.
        body = {
            'requests': requests
        }
        response = service.presentations() \
            .batchUpdate(presentationId=presentation_id, body=body).execute()
    except HttpError as error:
        print(f"An error occurred: {error}")
        print("Slides not created")
        return error

    return response


'''Exports Google Slides as a Microsoft PowerPoint (.pptx) that is returned to
the user'''


def download_ppt(presentation_id: str, presentation_name: str):
    creds = authorize_creds()
    service = build('drive', 'v3', credentials=creds)

    request = service.files().export_media(fileId=presentation_id,
                                           mimeType='application/vnd.openxmlformats-officedocument.presentationml.presentation')

    fh = BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%" % int(status.progress() * 100))

    # The file has been downloaded into RAM, now save it in a file
    fh.seek(0)
    with open(presentation_name + '.pptx', 'wb') as f:
        copyfileobj(fh, f, length=131072)


'''Deletes Google Slides version of presentation to clear up space'''


def delete_slides(presentation_id: str):
    creds = authorize_creds()
    try:
        service = build('drive', 'v3', credentials=creds)
        service.files().delete(fileId=presentation_id).execute()
        print("Successfully deleted slides")
    except HttpError as error:
        print(f"An error occurred: {error}")
        print("Slides not deleted")



