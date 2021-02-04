
from scisum.config import ITRANSLATE_K, URL_ITRANSLATE_API
import json
import requests

def translate_text(text, mode="forward", lang_src="en", lang_trsl="fr"):
  """ Translate text with itranslate API"""
  
  if mode == "forward":
    lang_in = lang_src
    lang_out = lang_trsl
  elif mode == "backward":
    lang_in = lang_trsl
    lang_out =  lang_src
  
  payload = {"source": 
             {
              "dialect": f"{lang_in}",
              "text": f"{text}"
              },
             "target": 
             {
              "dialect": f"{lang_out}"
              }
             }
  payload = json.dumps(payload)
  headers = {
      'content-type': "application/json",
      'api-key': ITRANSLATE_K,
      }
  response = request_translation(data=payload, headers=headers)
  trsl_text = json.loads(response.text)["target"]["text"]
  return trsl_text

def request_translation(data, headers):
  response = requests.request("POST", URL_ITRANSLATE_API, data=data, headers=headers)
  if response.status_code !=200:
    print(lang_trsl)
    print(response.text)
    #Retry connection once.
    time.sleep(1)
    response = request_translation(data, headers)
    if response.status_code !=200:
      raise ConnectionError("Impossible to connect to i-Translate API")

  return response
      
