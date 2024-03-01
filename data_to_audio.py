# -*- coding: utf-8 -*-
# @Time      : 2024/2/29 15:31
# @Author    : RedHerring
# @FileName  : data_to_audio.py
# @微信公众号  : AI Freedom
# @知乎       : RedHerring

import os, requests, time
from xml.etree import ElementTree
import pandas as pd


subscription_key = "your ttskey"
fetch_token_url = "your url"
base_url = "your region"


class TextToSpeech(object):
    """
    A class that represents a Text-to-Speech converter.

    Args:
        subscription_key (str): The subscription key for accessing the Text-to-Speech service.
        fetch_token_url (str): The URL for fetching the access token.
        base_url (str): The base URL for the Text-to-Speech service.

    Attributes:
        subscription_key (str): The subscription key for accessing the Text-to-Speech service.
        fetch_token_url (str): The URL for fetching the access token.
        base_url (str): The base URL for the Text-to-Speech service.
        timestr (str): The current timestamp in the format "%Y%m%d-%H%M".
        access_token (str): The access token for authenticating requests.

    Methods:
        get_token(): Fetches the access token from the specified URL.
        save_audio(data, child_path): Saves the audio generated from the given data to the specified path.

    """

    def __init__(self, subscription_key, fetch_token_url, base_url):
        self.subscription_key = subscription_key
        self.fetch_token_url = fetch_token_url
        self.base_url = base_url
        self.timestr = time.strftime("%Y%m%d-%H%M")
        self.access_token = None

    def get_token(self):
        """
        Fetches the access token from the specified URL.

        This method sends a POST request to the fetch_token_url with the subscription key in the headers.
        The response contains the access token, which is then stored in the access_token attribute.

        """

        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key
        }
        response = requests.post(self.fetch_token_url, headers=headers)
        self.access_token = str(response.text)

    def save_audio(self, data, child_path):
        """
        Saves the audio generated from the given data to the specified path.

        Args:
            data (str): The text to be converted to audio.
            child_path (str): The path where the audio file will be saved.

        This method constructs the URL for the Text-to-Speech service and sets the necessary headers.
        It creates an XML body with the specified text and sends a POST request to the constructed URL.
        If the response status code is 200, the audio content is saved to the specified path.

        """

        path = 'cognitiveservices/v1'
        constructed_url = self.base_url + path
        headers = {
            'Authorization': 'Bearer ' + str(self.access_token),
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
            'User-Agent': 'TTSForPython'
        }
        xml_body = ElementTree.Element('speak', version='1.0')
        xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-us')
        voice = ElementTree.SubElement(xml_body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
        voice.set('name', 'zh-CN-XiaoxiaoNeural')
        # voice.set('name', 'zh-CN-YunxiNeural')
        # voice.set('name', 'zh-CN-sichuan-YunxiNeural')
        voice.set(' rate ', '1.4')
        voice.text = data
        body = ElementTree.tostring(xml_body)
        response = requests.post(constructed_url, headers=headers, data=body)
        if response.status_code == 200:
            with open(child_path+'.wav', 'wb') as audio:
                audio.write(response.content)
        else:
            print("\nStatus code: " + str(response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")
            print("Reason: " + str(response.reason) + "\n")


def load_source_data_text(path, tts_key, tts_url, region):
    """
    Loads the source data from a CSV file and converts the text to audio using the TextToSpeech API.

    Args:
        path (str): The path to the CSV file containing the source data.
        tts_key (str): The subscription key for the TextToSpeech API.
        tts_url (str): The URL for fetching the token for the TextToSpeech API.
        region (str): The region for the TextToSpeech API.

    Returns:
        str: The path to the directory where the audio files are saved.
    """
    subscription_key = tts_key
    fetch_token_url = tts_url
    base_url = 'https://'+region+'.tts.speech.microsoft.com/'
    app = TextToSpeech(subscription_key, fetch_token_url, base_url)
    app.get_token()
    df_temp = pd.read_csv(path)
    for index, row in df_temp.iterrows():
        new_path = path.split(".csv")[0].replace("data_split","data_audio")
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        path_child =os.path.join(new_path,str(index))
        app.save_audio(row['text'], path_child)
    return new_path


if __name__ == "__main__":
    tts_key = "xxxx"
    region = "japaneast"
    tts_url = "https://japaneast.api.cognitive.microsoft.com/sts/v1.0/issuetoken"
    load_source_data_text("data/data_split/黑白相间的.csv", tts_key, tts_url, region)