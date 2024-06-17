import random

import torch
import torchaudio
from pydub import AudioSegment

import ChatTTS
import numpy as np

import const

chat = ChatTTS.Chat()
chat.load_models(compile=False)
sample_rate = 24000


def generate_audio(text, temperature, top_P, top_K, audio_seed_input, text_seed_input):
    torch.manual_seed(audio_seed_input)
    rand_spk = chat.sample_random_speaker()
    params_infer_code = {
        'spk_emb': rand_spk,
        'temperature': temperature,
        'top_P': top_P,
        'top_K': top_K,
    }
    params_refine_text = {'prompt': '[oral_2][laugh_0][break_6]'}

    torch.manual_seed(text_seed_input)
    wav = chat.infer(text,
                     skip_refine_text=True,
                     params_refine_text=params_refine_text,
                     params_infer_code=params_infer_code
                     )

    audio_data = np.array(wav[0]).flatten()
    text_data = text[0] if isinstance(text, list) else text

    return [audio_data, text_data]


def generate_audio_array(inputs, audio_path):
    silence_duration = 2
    silence = np.zeros(sample_rate * silence_duration, dtype=np.float32)
    audio = np.array([], dtype=np.float32)
    for input in inputs:
        output = generate_audio(input, 0.3, 0.7, 20, random.choice(const.audio_seed), 42)
        if audio.size == 0:
            audio = output[0]
        else:
            audio = np.hstack((audio, silence))
            audio = np.hstack((audio, output[0]))

    # 确保音频数据是二维数组格式
    audio = audio.reshape(1, -1)
    # 将拼接好的音频数据保存到文件
    torchaudio.save(audio_path, torch.from_numpy(audio), sample_rate)

def gen_news_audio(news_audio_path,background_path,news_music_path):
    wav_audio = AudioSegment.from_wav(news_audio_path)
    mp3_audio = AudioSegment.from_mp3(background_path)
    # mp3_audio = mp3_audio - 10
    mp3_audio = mp3_audio * (len(wav_audio) // len(mp3_audio) + 1)

    if len(mp3_audio) > len(wav_audio):
        fade_duration = 5000  # 5秒渐弱
        mp3_audio = mp3_audio[:len(wav_audio)].fade_out(fade_duration)
    combined_audio = wav_audio.overlay(mp3_audio)
    combined_audio.export(news_music_path, format="mp3")
