# -*- coding: utf-8 -*-
# @Time      : 2024/2/29 16:05
# @Author    : RedHerring
# @FileName  : data_to_image.py
# @微信公众号  : AI Freedom
# @知乎       : RedHerring


import os.path
import requests
import openai
import pandas as pd


def CreateImage(description, path, key):
    """
    Create an image based on the given description using the OpenAI DALL-E model.

    Args:
        description (str): The prompt or description for generating the image.
        path (str): The path to save the generated image.
        key (str): The API key for accessing the OpenAI service.

    Returns:
        str: The URLs of the generated images.

    Raises:
        Exception: If the specified size is not one of the valid sizes (256x256, 512x512, 1024x1024).
    """
    size = "1024x1024"
    if size not in ["256x256", "512x512", "1024x1024"]:
        raise Exception("Picture size does not match, only supported 256x256, 512x512, 1024x1024")
    openai.api_key = key
    # print("===description===" * 3)
    # print(description)
    image = openai.Image.create(
        prompt=description,
        n=1,
        size=size,
        model="dall-e-3",
        response_format="url",
    )
    numOfOutput = len(image.data)
    org_path = path
    urls = ""
    for i in range(numOfOutput):
        path = org_path
        url = image.data[i]["url"]
        urls += url + " "
        img_content = requests.get(url).content
        if i >= 1:
            path = path.split(".")[0] + "_" + str(i + 1) + "." + path.split(".")[1]
        with open(path, "wb") as f:
            f.write(img_content)
    urls = urls.rstrip(" ")
    return urls


def load_image_data(path,api_key):
    df = pd.read_csv(path)
    newpath = path.split(".csv")[0].replace("data_prompt", "data_image")
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    oldprompts_list = []
    oldurls_list = []
    instruction = "你是一个幽默的喜剧导演。你要根据历史的prompt、图片，以及这次的prompt，生成新的图片。要求图片里面的角色形象前后一致，情景根据prompt内容生成。图片风格幽默风趣，色彩明亮，画面生动，吸引人。"

    for index, row in df.iterrows():
        childpath = os.path.join(newpath,str(index)+".png")
        oldprompts = "。".join(oldprompts_list[-5:])
        oldurls = "。".join(oldurls_list[-5:])
        context = "历史的prompt是：" + oldprompts + " 历史的图片是：" + oldurls
        query = "要求你参考历史上下文信息，查看历史的图片内容。历史图片中出现过的角色，再次生成时，形象要保持一致。根据下面的内容描述，生成一副画面并用英文单词表示：" + row["prompt"]
        prompt = f"""{instruction} ### 上下文 {context} ### 问题：{query}"""
        urls = CreateImage(prompt, childpath, api_key)
        oldprompts_list.append(row["prompt"])
        oldurls_list.append(urls)

    return newpath


from data_to_prompt import split_data_process, load_data_text

if __name__ == '__main__':
    text = """在一条安静的马路上，两只小猫咪正在进行一场非同寻常的讨论。一只是黑白相间的小家伙，另一只则是橘色条纹的小可爱。它们站着，就像两位小绅士，准备展开一场有礼貌的社交。"""
    api_key = "xxxx"
    data_path = split_data_process(text)
    data_prompt_path = load_data_text(data_path,api_key)
    iamge_source = load_image_data(data_prompt_path,api_key)
    print(iamge_source)
    image_files = sorted(os.listdir(iamge_source))
    print(image_files)
    for i in range(len(image_files)):
        image_path = os.path.join(iamge_source, image_files[i])
        print(image_path)

    