import random
import sys

import const
from chain import Spider,llm,audio
from suno import suno

def normal_news():
    news_path = f"tmp/news.wav"
    background_path = f"tmp/background.mp3"
    news_music_path = f"tmp/news_music.mp3"
    ids = suno.make_music()
    news_list = Spider.get_news_content()
    kimi = llm.llm_api(const.kimi_api_key, const.kimi_base_url, const.kimi_model)
    summarizes = []
    for news in news_list:
        summarize = kimi.call(news)
        if summarize is not None:
            summarizes.append(summarize)

    audio.generate_audio_array(summarizes, news_path)
    suno.download_music(random.choice(ids), background_path)
    audio.gen_news_audio(news_path, background_path, news_music_path)


def news_36kr():
    news_path = f"tmp/news_36r.wav"
    background_path = f"tmp/background.mp3"
    news_music_path = f"tmp/news_music_36r.mp3"
    ids = suno.make_music()
    news_list = Spider.get_36r_content()
    kimi = llm.llm_api(const.kimi_api_key, const.kimi_base_url, const.kimi_model)
    summarizes = []
    for news in news_list:
        summarize = kimi.call(news)
        if summarize is not None:
            summarizes.append(summarize)

    audio.generate_audio_array(summarizes, news_path)
    suno.download_music(random.choice(ids), background_path)
    audio.gen_news_audio(news_path, background_path, news_music_path)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("usage:python main.py normal|36kr")
        sys.exit()
    param = sys.argv[1]
    if param == '36kr':
        news_36kr()
    else:
        normal_news()

