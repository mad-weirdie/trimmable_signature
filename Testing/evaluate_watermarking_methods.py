"""
-------------------------------------------------------------------------------
Title:			CIS 433 Project - Watermarking Evaluation Module
-------------------------------------------------------------------------------
Description:	This file controls the evaluation for a battery of robustness
				tests on all of the watermarking methods implemented in the
				system. The tests performed are described in attack_tester.py,
				tested against the files listed in audio_files_to_test.txt
-------------------------------------------------------------------------------
Authors: 		Arden Butterfield, Ian Parish, and Madison Werries

Last edit by: 	Madison Werries
Last edit on:	2/6/2022
-------------------------------------------------------------------------------
"""

from attack_tester import *
from wavlet_method.quiling_wu_2018_implementation import *

def EvaluateWatermarkMethods():
	""" This module tests the watermarking methods using a variety of attacks defined in AttackTester."""
	
	audio_file_names = open("audio_files_to_test.txt")
	watermark_names = open("watermarks_to_test.txt")
	audio_file_names.readline()  # Skip the file header
	audio_files = audio_file_names.readlines()
	watermarks = watermark_names.readlines()
	
	for i in range(len(audio_files)):
		audio_files[i] = "../audio_samples/" + audio_files[i].strip()
	for i in range(len(watermarks)):
		watermarks[i] = "../watermarks/" + watermarks[i].strip()
	
	# TODO: HERE LIES THE PART WHERE WE CREATE NEW INSTANCES OF AttackTester() FOR EACH OF THE DIFFERENT
	# 	WATERMARKING METHODS AND THEN TRY TO BREAK THEM
	
	print("Testing the Wu-Wavelet-Method...")
	Wavelet_Method = AttackTester(insert_watermark, [], blind_read_watermark, [])
	Wavelet_Method.TestAll(audio_files, watermarks)
	print("--------------------------------------")
	print("Testing the Li-Wavelet-Method...")
	#
	#
	print("--------------------------------------")

	audio_file_names.close()
	watermark_names.close()


if __name__ == '__main__':
	EvaluateWatermarkMethods()
