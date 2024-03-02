# Text2Video

## 1. 项目介绍

`这是一个文本转视频的项目，通过输入文本，一键直接生成对应的视频。`

本项目对应的知乎链接：https://zhuanlan.zhihu.com/p/684926869

### `技术栈：`
1. 文本处理，分割文本，生成 prompt
2. 语音合成，将文本转换为语音，azure speech
3. 图片生成，将文本转成图片，openai DALL·E
4. 视频合成，将图片和语音合成视频，moviepy



## 2. 效果展示

视频结果在目录 `data/data_video` 下，以下是一个例子。

https://github.com/HuZixia/Text2Video/assets/38995480/10a3b5ac-f762-4286-8c86-ce57c9a7eb40


## 3. 安装使用


### 3.1 环境准备

- python环境
```
python的3.10版本
```

- 安装依赖

```
pip install -r requirements.txt
```
- 具体依赖

```
fastapi==0.110.0
python-dotenv==1.0.0
pydantic~=1.10.7
pandas==1.5.3
moviepy==1.0.3
openai==0.27.8
```


### 3.2 key准备

项目路径配置 .env 文件，项目要求 openai key，用 DALL·E 生成图片；azure speech key，将文本转成语音。

```
OPENAI_API_KEY="XXXX"
AZURE_SPEECH_KEY="XXXX"
AZURE_SPEECH_LOCATION="XXXX"
AZURE_SPEECH_ENDPOINT="XXXX"
```


### 3.3 代码执行

在 `main.py` 中给定文本，执行 `main.py` 文件，即可一键生成视频，视频保存在 `data/data_video` 文件夹下。

```
python main.py
```


## 4. 作者信息

`@Author    : RedHerring`

`@微信公众号  : AI Freedom`

`@知乎       : RedHerring`

欢迎关注微信公众号，学习交流 🤓

<img src="./AI Freedom.jpg" style="margin-left: 0px">