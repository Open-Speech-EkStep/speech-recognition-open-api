import torch
import numpy as np
from pydub import AudioSegment
from fairseq import utils
from fairseq.data import Dictionary

from src.monitoring import monitor
from src.srt.timestamp_generator import extract_time_stamps
from tqdm import tqdm
from src.lib.inference_lib import W2lViterbiDecoder, get_feature_for_bytes, post_process


def get_results_from_chunks(wav_data, dict_path, generator, use_cuda=False, w2v_path=None, model=None, half=False):
    sample = dict()
    net_input = dict()
    feature = wav_data
    target_dict = Dictionary.load(dict_path)

    model.eval()

    if half:
        net_input["source"] = feature.unsqueeze(0).half()
    else:
        net_input["source"] = feature.unsqueeze(0)

    padding_mask = torch.BoolTensor(net_input["source"].size(1)).fill_(False).unsqueeze(0)

    net_input["padding_mask"] = padding_mask
    sample["net_input"] = net_input
    sample = utils.move_to_cuda(sample) if use_cuda else sample

    with torch.no_grad():
        hypo = generator.generate(model, sample, prefix_tokens=None)
    hyp_pieces = target_dict.string(hypo[0][0]["tokens"].int().cpu())
    text = post_process(hyp_pieces, 'letter')

    return text


def formatSrtTime(secTime):
    sec, micro = str(secTime).split('.')
    m, s = divmod(int(sec), 60)
    h, m = divmod(m, 60)
    return "{:02}:{:02}:{:02},{}".format(h, m, s, micro[:2])


def response_alignment(response, num_words_per_line=25):
    aligned_response = []

    if len(response.split(' ')) < 25:
        aligned_response.append(response)
    else:

        num_lines = len(response.split(' ')) // 25
        for line in range(num_lines):
            aligned_response.append(' '.join(response.split(' ')[25 * line: 25 * (line + 1)]))
        aligned_response.append(' '.join(response.split(' ')[(line + 1) * 25:]))
    return aligned_response


@monitor
def generate_srt(wav_path, language, model, generator, cuda, dict_path, half=False):
    start_time, end_time = extract_time_stamps(wav_path)
    original_file_path = wav_path.replace('clipped_audio_enhanced', 'clipped_audio')
    original_chunk = AudioSegment.from_wav(original_file_path)
    rst = ''
    result_obj = []
    for i in tqdm(range(len(start_time))):
        result = ''
        if end_time[i] - start_time[i] > 80:
            result += str(i + 1)
            result += '\n'
            result += str(formatSrtTime(start_time[i]))
            result += ' --> '
            result += str(formatSrtTime(end_time[i]))
            result += '\n'
            result += 'speech is not clear in this segment'
            result += '\n\n'
            continue
        chunk = original_chunk[start_time[i] * 1000: end_time[i] * 1000]
        float_wav = np.array(chunk.get_array_of_samples()).astype('float64')
        features = get_feature_for_bytes(float_wav, 16000)
        result += (str(i + 1))
        result += '\n'
        result += str(formatSrtTime(start_time[i]))
        result += ' --> '
        result += str(formatSrtTime(end_time[i]))
        result += '\n'

        response = get_results_from_chunks(wav_data=features, dict_path=dict_path, generator=generator, use_cuda=cuda,
                                           model=model, half=half)
        if language == 'en-IN':
            response = response.lower()

        # aligned_response = response_alignment(response, num_words_per_line=25)
        # result_end+='\n'.join(aligned_response)
        valid = True
        if len(response.rstrip().lstrip()) == 0:
            response = "[ Voice is not clearly audible ]"
            valid = False
        result_end = '\n\n'
        result_obj.append([result, response, result_end, valid])
    return result_obj
