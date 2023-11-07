import logging
import os
import json
import shared_code.dbHelper as dbHelper

from shared_code.Prompt import Prompt
from azure.functions import HttpRequest, HttpResponse
from azure.core.rest import HttpRequest as RestRequest
from azure.core.rest import HttpResponse as RestResponse
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem
from azure.cosmos import CosmosClient
from azure.cosmos.exceptions import CosmosHttpResponseError, CosmosResourceExistsError, CosmosResourceNotFoundError

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('prompt_create')
credentials = TranslatorCredential(os.environ['TranslationKey'], os.environ['AzureTextTranslationRegion'])
Translator = TextTranslationClient(endpoint=os.environ['TranslationEndpoint'], credential=credentials, logging_enable=False)
ThisCosmos = CosmosClient.from_connection_string(os.environ['AzureCosmosDBConnectionString'])
CwDB = ThisCosmos.get_database_client(os.environ['Database'])
PlayerContainer = CwDB.get_container_client(os.environ['PlayerContainer'])
PromotContainer = CwDB.get_container_client(os.environ['PromptContainer'])
target_lang = ["en", "es", "it", "sv", "ru", "id", "bg", "zh-Hans"]

def main(req: HttpRequest) -> HttpResponse:
    req_body = req.get_json()
    logger.info('New prompt creation request. %s', req_body)
    
    # validate user
    name = req_body.get('username')
    if (dbHelper.player_exist(PlayerContainer, name) == False):
        body = json.dumps({"result": False, "msg": "Player does not exist" })
        return HttpResponse(body=body, mimetype="application/json")

    text = req_body.get('text')
    
    # validate text
    if (len(text) > 80 or len(text) < 15):
        body = json.dumps({"result": False, "msg": "Prompt less than 15 characters or more than 80 characters"  })
        return HttpResponse(body=body, mimetype="application/json")
    
    # construct request
    get_src_lang_req = RestRequest(
        method='POST', 
        url='https://api.cognitive.microsofttranslator.com/detect?api-version=3.0', 
        headers= {"Content-Type": "application/json"},
        json= [{"Text": text}], # azure 你为什么非要加 [] 呢？？？？？
        )
    resp = Translator.send_request(request=get_src_lang_req)
    resp_json = resp.json()
    logger.info(resp_json)
    confidence = resp_json[0]["score"]
    src_lang = resp_json[0]["language"]
    logger.info("detected language %s of confidence %s", src_lang, confidence)
    
    if (confidence < 0.3) or (src_lang not in target_lang):
        logger.info("confidence is low: %s", confidence < 0.3)
        logger.info("src_lang is not in target_lang: %s", src_lang not in target_lang)
        body = json.dumps({"result": False, "msg": "Unsupported language"})
        return HttpResponse(body=body, mimetype="application/json")
    
    trans_langs = target_lang.copy()
    trans_langs.remove(src_lang)
    
    input_text = [InputTextItem(text=text)]
    response = Translator.translate(content=input_text, to=trans_langs, from_parameter=src_lang)
    
    this_prompt = Prompt(name, src_lang, text)
    this_prompt.from_json(response[0].get("translations"))
    
    PromotContainer.create_item(this_prompt.to_dict(), enable_automatic_id_generation=True)
    

    return HttpResponse(body=json.dumps({"result" : True, "msg": "OK" }), mimetype="application/json")    