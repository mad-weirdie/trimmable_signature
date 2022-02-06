# python implementation of watermarking algorithm by Wei Li and Xiangyang Xue
# "An Audio Watermarking Technique That Is Robust Against Random Cropping"
# (2003)

import numpy as np
from scipy.io import wavfile
import pywt
from statistics import mode
from PIL import Image
from tqdm import tqdm
import matplotlib.pyplot as plt


def make_watermark_from_image():
    im_frame = Image.open('433_watermark_image.png')
    np_frame = np.array(im_frame)
    # np_frame has rgba channels, we just want a single channel, so we take the
    # r channel.
    single_channel = np_frame[..., 0]
    # Channel is 8-bit (0-255), we want 1 bit instead.
    single_channel //= single_channel.max()
    return single_channel.shape, single_channel.flatten()


FRAME_SIZE = 2048
OVERLAP_SIZE = int(FRAME_SIZE * 0.75)


def hamming_window_mask(length):
    # The hamming window funciton is a cosine wave that starts at a bit more
    # than 0, grows to 1, and then returns to the starting value over the
    # course of the array.

    # length: length of the array to create.
    mask = np.arange(0, 2 * np.pi, 2 * np.pi / length)
    return 0.54 - 0.46 * np.cos(mask)


def repeat_mark(mark):
    new_mark = []
    for i in mark:
        for reapeat in range(5):
            new_mark.append(i)
    return new_mark


def insert_watermark(audio, mark):
    ALPHA = 100
    old_dtype = audio.dtype
    mark = repeat_mark(mark)
    audio = audio.astype(np.float64)
    watermarked_audio = audio.copy()
    watermarked_audio[:] = 0  # Zero out whole array, while preserving shape
    mark_index = 0
    for sample_start in tqdm(
            range(0, len(audio) - FRAME_SIZE, FRAME_SIZE - OVERLAP_SIZE)):
        frame = audio[sample_start:sample_start + FRAME_SIZE].copy()
        frame *= hamming_window_mask(len(frame))
        # We preform a 3-level wavelet decomposition using the db4 wavelet
        # basis...
        coeffs = pywt.wavedec(frame, 'db4', level=3)
        # and we only consider the data at the ca3 level (that is, the coarsest
        # (i.e. lowest frequencies) part of the segment.
        frame_ca3 = coeffs[0]
        ca3_coeffs_mean = frame_ca3.mean()
        for j in range(len(frame_ca3)):
            if mark[mark_index] == 1:
                frame_ca3[j] = frame_ca3[j] - ca3_coeffs_mean + ALPHA
            elif mark[mark_index] == 0:
                frame_ca3[j] = frame_ca3[j] - ca3_coeffs_mean - ALPHA
            else:
                raise ValueError("watermark must be an array of only 1 and 0")
        watermarked_frame = pywt.waverec(coeffs, 'db4')
        watermarked_audio[
        sample_start:sample_start + FRAME_SIZE] += watermarked_frame

        mark_index += 1
        if mark_index == len(mark):
            break
    print(f"amount of mark written: {mark_index}/{len(mark)}")
    watermarked_audio *= (max(audio) / max(watermarked_audio))
    print(max(watermarked_audio))
    return watermarked_audio.astype(old_dtype)


def blind_read_watermark(audio, watermark_dimensions):
    audio = audio.astype(np.float64)
    watermark_segment = []
    watermark = np.zeros(watermark_dimensions).flatten()
    index = 0
    for sample_start in tqdm(range(0, len(audio) - FRAME_SIZE,
                                   FRAME_SIZE - OVERLAP_SIZE)):
        frame = audio[sample_start:sample_start + FRAME_SIZE].copy()
        frame *= hamming_window_mask(len(frame))
        # We preform a 3-level wavelet decomposition using the db4 wavelet
        # basis...
        coeffs = pywt.wavedec(frame, 'db4', level=3)
        # and we only consider the data at the ca3 level (that is, the coarsest
        # (i.e. lowest frequencies) part of the segment.
        frame_ca3 = coeffs[0]
        ca3_coeffs_mean = frame_ca3.mean()
        watermark_segment.append(1 if ca3_coeffs_mean > 0 else 0)
        if len(watermark_segment) == 5:
            watermark[index] = mode(watermark_segment)
            watermark_segment = []
            index += 1
            if index == len(watermark):
                break
    watermark = watermark.reshape(watermark_dimensions)
    return watermark


dimensions, mark = make_watermark_from_image()

fs, raw_audio = wavfile.read('../audio_samples/monkeys_mono.wav')
watermarked_audio = insert_watermark(raw_audio, mark)
wavfile.write('out.wav', fs, watermarked_audio)

# Do some attacks to `out.wav`

fs, watermarked_audio = wavfile.read('out.wav')
recovered_watermark = blind_read_watermark(watermarked_audio, dimensions)
plt.imshow(recovered_watermark)
plt.show()
