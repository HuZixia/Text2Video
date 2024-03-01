# -*- coding: utf-8 -*-
# @Time      : 2024/2/29 18:45
# @Author    : RedHerring
# @FileName  : main.py
# @微信公众号  : AI Freedom
# @知乎       : RedHerring


import os
from data_to_prompt import split_data_process, load_data_text
from data_to_audio import load_source_data_text
from data_to_image import load_image_data
from merge_to_video import merge_video
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

openai_api_key = os.getenv("OPENAI_API_KEY")
azure_speech_key = os.getenv("AZURE_SPEECH_KEY")
azure_speech_location = os.getenv("AZURE_SPEECH_LOCATION")
azure_speech_endpoint = os.getenv("AZURE_SPEECH_ENDPOINT")


def main(text):
    """
    Main function that processes the given text to generate a video.

    Args:
        text (str): The input text to be processed.

    Returns:
        str: The path to the generated video file.
    """
    data_path = split_data_process(text)
    data_prompt_path = load_data_text(data_path, openai_api_key)
    tts_data = load_source_data_text(data_path, azure_speech_key, azure_speech_endpoint, azure_speech_location)
    image_source = load_image_data(data_prompt_path, openai_api_key)
    path_video = merge_video(image_source, tts_data)
    print(path_video)


if __name__ == '__main__':

    text = (
        "测试一下下：黑白相间的猫咪站在路中间，自称是“斑马线的守护者”，橘色猫则耸耸肩，说它是过马路的“导盲犬”。"
        "小黑白得意地宣布它将开一家“猫咖啡馆”，地点选在橘猫的“领土”上，橘猫反击说它就喜欢在竞争中找乐子。"
    )

    # text = (
    #     "黑白相间的猫咪站在路中间，自称是“斑马线的守护者”，橘色猫则耸耸肩，说它是过马路的“导盲犬”。"
    #     "小黑白得意地宣布它将开一家“猫咖啡馆”，地点选在橘猫的“领土”上，橘猫反击说它就喜欢在竞争中找乐子。"
    #     "橘色小猫自称是“领地规划师”，指挥着一群小鸽子重新划分空中的领空。"
    #     "小黑白提出要进行一场“喵式辩论”，声称自己会用最锋利的逻辑“挠败”对方。"
    #     "橘色小猫摆出一副学者样，但却拿着一本倒过来的地图，自信地说这是最新版的“猫界地理”。"
    #     "两只猫为了争一个晒太阳的好位置，竟然决定用“摇尾巴比赛”来决胜负。"
    #     "小黑白举起爪子，庄严宣布自己愿意分享领地，但只限于“美食区”。"
    #     "橘色小猫声称自己的祖先是“猫派大将军”，领地自然是“遗产”。"
    #     "辩论结束时，两只猫决定合开一家“喵星人快乐俱乐部”，共同管理这块“争议领地”。"
    #     "最后，两只猫咪并肩而行，一边走一边计划如何把这场辩论写成一个“爆笑的剧本”。"
    # )

    main(text)






