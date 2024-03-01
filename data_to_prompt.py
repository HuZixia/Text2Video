# -*- coding: utf-8 -*-
# @Time      : 2024/2/29 13:46
# @Author    : RedHerring
# @FileName  : data_to_prompt.py
# @微信公众号  : AI Freedom
# @知乎       : RedHerring


import pandas as pd
import os


def split_data_process(data):
    """
    Split the given data into sentences and save each sentence in a separate CSV file.

    Args:
        data (str): The input data to be split.

    Returns:
        str: The file path of the saved CSV file.
    """
    content = data.split('。')
    content = [x.strip().replace("\n", "") for x in content if len(x.strip()) > 0]
    each_df = pd.DataFrame(content, columns=["text"])
    csv_save_path = os.path.join("data/data_split", data[:5] + ".csv")
    each_df.to_csv(csv_save_path, index=False)
    return csv_save_path


def load_data_text(path, api_key):
    """
    Load data from a CSV file and generate prompts based on the text.

    Args:
        path (str): The path to the CSV file.
        api_key (str): The API key for the LLM (Language Model) service.

    Returns:
        str: The path to the newly generated CSV file with prompts.
    """
    df = pd.DataFrame(columns=['text', 'index', 'prompt'])
    df_temp = pd.read_csv(path)
    for index, row in df_temp.iterrows():
        prompt_param = row['text']
        # Optional: Here you can regenerate prmpt according to text by LLM
        new_row = {'text': row['text'], 'index': index, 'prompt':  prompt_param}
        df = pd.concat([df, pd.DataFrame(new_row, index=[0])], ignore_index=True)
    new_path = path.replace("data_split", "data_prompt")
    df.to_csv(new_path, index=False, encoding='utf-8')
    return new_path







