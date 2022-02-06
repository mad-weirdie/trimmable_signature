# python implementation of watermarking algorithm by Qiuling Wu 1,2 and Meng Wu
# "A Novel Robust Audio Watermarking Algorithm by Modifying the Average
# Amplitude in Transform Domain"
# (2018)

import numpy as np
from scipy.io import wavfile
import pywt
from PIL import Image
from tqdm import tqdm
import matplotlib.pyplot as plt
from scipy.fftpack import dct, idct

R_DWT_LEVEL = 4
N_SEGMENT_LENGTH = 1024
LAMBDA_EMBEDDING_DEPTH = 0.9

def make_watermark_from_image():
    im_frame = Image.open('433_watermark_image.png')
    np_frame = np.array(im_frame)
    # np_frame has rgba channels, we just want a single channel, so we take the
    # r channel.
    single_channel = np_frame[..., 0]
    # Channel is 8-bit (0-255), we want 1 bit instead.
    single_channel //= single_channel.max()
    return single_channel.shape, single_channel.flatten()

def insert_watermark(audio, mark):
    old_dtype = audio.dtype
    audio = audio.astype(np.float64)
    watermarked_audio = audio.copy()
    mark_index = 0
    for sample_start in tqdm(range(0, len(audio) - N_SEGMENT_LENGTH, N_SEGMENT_LENGTH)):
        segment = audio[sample_start:sample_start + N_SEGMENT_LENGTH].copy()
        coeffs = pywt.wavedec(segment, 'db4', level=R_DWT_LEVEL)
        coeff_to_use = coeffs[1] # First detail level coefficient
        assert(len(coeff_to_use) % 2 == 0)
        midpoint = len(coeff_to_use) // 2
        d_e1 = coeff_to_use[:midpoint]
        d_e2 = coeff_to_use[midpoint:]
        c1 = dct(d_e1, norm='ortho')
        c2 = dct(d_e2, norm='ortho')
        c = np.append(c1, c2)
        amp_c = np.mean(abs(c))
        amp_c1 = np.mean(abs(c1))
        amp_c2 = np.mean(abs(c2))
        # print(amp_c, amp_c1, amp_c2)
        if amp_c1 == 0 or amp_c2 == 0:
            continue
        if mark[mark_index] == 1:
            new_c1 = c1 * (1 + LAMBDA_EMBEDDING_DEPTH) * amp_c / amp_c1
            new_c2 = c2 * (1 - LAMBDA_EMBEDDING_DEPTH) * amp_c / amp_c2
        elif mark[mark_index] == 0:
            new_c1 = c1 * (1 - LAMBDA_EMBEDDING_DEPTH) * amp_c / amp_c1
            new_c2 = c2 * (1 + LAMBDA_EMBEDDING_DEPTH) * amp_c / amp_c2
        else:
            raise ValueError(f"unrecognized symbol in watermark, {mark[mark_index]} at index {mark_index}")
        new_d_e1 = idct(new_c1, norm='ortho')
        new_d_e2 = idct(new_c2, norm='ortho')
        new_d_e = np.append(new_d_e1, new_d_e2)
        coeffs[1] = new_d_e
        watermarked_segment = pywt.waverec(coeffs, 'db4')
        watermarked_audio[sample_start:sample_start + N_SEGMENT_LENGTH] = watermarked_segment
        mark_index += 1
        if mark_index == len(mark):
            break
    print(f"amount of mark written: {mark_index}/{len(mark)}")
    watermarked_audio *= (max(audio) / max(watermarked_audio))
    return watermarked_audio.astype(old_dtype)


def blind_read_watermark(audio, watermark_dimensions):
    audio = audio.astype(np.float64)
    watermark = np.zeros(watermark_dimensions).flatten()
    mark_index = 0
    for sample_start in tqdm(range(0, len(audio) - N_SEGMENT_LENGTH, N_SEGMENT_LENGTH)):
        segment = audio[sample_start:sample_start + N_SEGMENT_LENGTH].copy()
        coeffs = pywt.wavedec(segment, 'db4', level=R_DWT_LEVEL)
        coeff_to_use = coeffs[1]  # First detail level coefficient
        assert (len(coeff_to_use) % 2 == 0)
        midpoint = len(coeff_to_use) // 2
        d_e1 = coeff_to_use[:midpoint]
        d_e2 = coeff_to_use[midpoint:]
        c1 = dct(d_e1, norm='ortho')
        c2 = dct(d_e2, norm='ortho')
        amp_c1 = np.mean(abs(c1))
        amp_c2 = np.mean(abs(c2))
        if amp_c1 == 0 or amp_c2 == 0:
            continue
        if amp_c1 >= amp_c2:
            watermark[mark_index] = 1
        else:
            watermark[mark_index] = 0
        mark_index += 1
        if mark_index == len(mark):
            break
    return watermark.reshape(watermark_dimensions)

dimensions, mark = make_watermark_from_image()

fs, raw_audio = wavfile.read('../audio_samples/monkeys_mono.wav')
watermarked_audio = insert_watermark(raw_audio, mark)
wavfile.write('out.wav', fs, watermarked_audio)

# Do some attacks to `out.wav`

fs, watermarked_audio = wavfile.read('out.wav')
recovered_watermark = blind_read_watermark(watermarked_audio, dimensions)
plt.imshow(recovered_watermark)
plt.show()
