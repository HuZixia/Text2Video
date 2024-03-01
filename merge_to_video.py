# -*- coding: utf-8 -*-
# @Time      : 2024/2/29 17:12
# @Author    : RedHerring
# @FileName  : data_to_video.py
# @微信公众号  : AI Freedom
# @知乎       : RedHerring


import os
from moviepy.editor import ImageSequenceClip, AudioFileClip, concatenate_videoclips, ImageClip
import numpy as np


def flFunc(gf, t):
    return frameScroll(gf(t), 2)


import numpy as np

def frameScroll(frame, x):
    """
    Scrolls the given frame vertically by the specified amount.

    Args:
        frame (numpy.ndarray): The input frame to be scrolled.
        x (int): The amount by which the frame should be scrolled.

    Returns:
        numpy.ndarray: The scrolled frame.

    """
    global framePos, clipHeight

    moveCount = framePos + x
    if moveCount > clipHeight:
        moveCount -= clipHeight
    framePos = moveCount
    remainFrame = frame[:moveCount]
    exceedFrame = frame[moveCount:]

    return np.vstack((exceedFrame, remainFrame))


def merge_video(image_dir_path, audio_dir_path):
    """
    Merges images and audio files into a single video file.

    Args:
        image_dir_path (str): The path to the directory containing the image files.
        audio_dir_path (str): The path to the directory containing the audio files.

    Returns:
        str: The path to the generated video file.

    Raises:
        FileNotFoundError: If the image or audio directories do not exist.
    """

    image_files = sorted(os.listdir(image_dir_path))
    audio_files = sorted(os.listdir(audio_dir_path))
    print(image_files)
    clips = []
    duration = 5
    speed = 10
    size = 700
    fps = 24
    for i in range(len(image_files)):
        image_path = os.path.join(image_dir_path, image_files[i])
        audio_path = os.path.join(audio_dir_path, audio_files[i])
        audio_clip = AudioFileClip(audio_path)

        img_clip = ImageSequenceClip([image_path], fps, duration)
        fl = lambda gf, t: gf(t)[int(speed * t):int(speed * t) + size,:]
        img_clip = img_clip.set_position(('center', 'center')).fl(fl,apply_to=['mask']).set_duration(audio_clip.duration)
        clip = img_clip.set_audio(audio_clip)
        clips.append(clip)
    final_clip = concatenate_videoclips(clips)
    new_parent = image_dir_path.replace("data_image","data_video").split("story")[0]
    if not os.path.exists(new_parent):
        os.makedirs(new_parent)
    new_path = image_dir_path.replace("data_image","data_video")
    final_clip.write_videofile(new_path+".mp4", fps=30.00, audio_codec="aac")
    return new_path+".mp4"

