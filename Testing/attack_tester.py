"""
-------------------------------------------------------------------------------
Title:			CIS 433 Project - Audio Watermarking System Robustness Tests
-------------------------------------------------------------------------------
Description:	This file contains definitions for a series of modules which
			  	are used to test the robustness various audio watermarking
			  	methods.
-------------------------------------------------------------------------------
Authors: 		Arden Butterfield, Ian Parish, and Madison Werries

Last edit by: 	Madison Werries
Last edit on:	2/6/2022
-------------------------------------------------------------------------------
Credits:

	While the Python implementation is our own, these tests were derived from
	the concepts described in "StirMark for Audio," which is part of the
	Stirmark Benchmark 4.0 system, linked below:
	(1) https://www.petitcolas.net/watermarking/stirmark/
	
	The concepts our code was structured around comes from Appendix C of the
	Appendices section of the Stirmark Benchmark System. The PDF document
	containing the specific standards and criteria for testing watermarking
	robustness can be found linked below:
	(2) https://link.springer.com/content/pdf/bbm%3A978-3-319-07974-5%2F1.pdf
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
	Below is the full copyright information for the two links provided above:
	
	Copyright:
		Fabien A. P. Petitcolas, Martin Steinebach, Frédéric Raynal, Jana
		Dittmann, Caroline Fontaine, Nazim Fatès. A public automated
		web-based evaluation service for watermarking schemes: StirMark
		Benchmark. In Ping Wah Wong and Edward J. Delp, editors,
		proceedings of electronic imaging, security and watermarking of
		multimedia contents III, vol. 4314, San Jose, California, U.S.A.,
		20-26 January 2001. The Society for imaging science and
		technology (I.S.&T.) and the international Society for optical
		engineering (SPIE). ISSN 0277-786X.
	and
		Fabien A. P. Petitcolas. Watermarking schemes
		evaluation. I.E.E.E. Signal Processing, vol. 17, no. 5,
		pp. 58-64, September 2000.
-------------------------------------------------------------------------------
"""
from scipy.io import wavfile

class AttackTester:
	""" This module runs attack tests given a specific watermarking method. """
	def __init__(self, insert_watermark, insert_args, read_watermark, read_args):
		self.InsertWatermark = insert_watermark
		self.insert_args = insert_args
		self.ReadWatermark = read_watermark
		self.read_args = read_args
		
		# A list of all the attacks to be performed on any given file
		self.attacks = {
			self.DoNothing,
			self.SmallCrop,
			self.BigCrop,
			self.CutSamples,
			self.PitchShift,
			self.Compress,
			self.Amplify,
			self.HighPass,
			self.LowPass,
			self.TimeScale,
			self.AddNoise}
	
	def RunAttackTest(self, filename, watermark, attack):
		""" Runs a singular attack on a file/watermark combo. """
		samplerate, raw_audio = wavfile.read(filename)
		watermarked_audio = self.InsertWatermark(raw_audio, watermark)
		damaged_audio = attack(watermarked_audio)
		recovered_watermark = self.ReadWatermark(damaged_audio, self.read_args)
		
		#TODO: verify accuracy/success of read_result somehow
		return 0  # Could return an accuracy/percent success? or just true/false?
		
	def TestAll(self, audio_files, watermarks):
		""" Runs every kind of attack against the set of audio files."""
		for attack in self.attacks:
			for file in audio_files:
				for watermark in watermarks:
					self.RunAttackTest(file, watermark, attack)
	
	def DoNothing(self, watermarked_audio):
		"""	This 'attack' does not damage the watermark at all, testing the watermarking method works as expected. """
		return watermarked_audio

	def CropEnds(self, watermarked_audio):
		""" This attack test will crop a small section out of start/end of the watermarked audio file. """
		damaged = watermarked_audio.copy()
		damaged = damaged[len(damaged) // 4:]
		damaged = damaged[:- (len(damaged) // 4)]
		return damaged
	
	def SmallCrop(self, watermarked_audio):
		""" This attack test will crop a small section out of the watermarked audio file randomly. """
		# TODO !!!
		return watermarked_audio
	
	def BigCrop(self, watermarked_audio):
		""" This attack test will crop a large section out of the watermarked audio file randomly. """
		# TODO !!!
		return watermarked_audio
	
	def CutSamples(self, watermarked_audio):
		""" This attack will crop several same-sized segments out of the watermarked audio file. """
		# TODO !!!
		return watermarked_audio
	
	def PitchShift(self, watermarked_audio):
		""" This attack will pitch-shift the watermarked audio by a specified amount. """
		# TODO !!!
		return watermarked_audio
	
	def Compress(self, watermarked_audio):
		""" This attack will compress the watermarked audio by a specified amount. """
		# TODO !!!
		return watermarked_audio
	
	def Amplify(self, watermarked_audio):
		""" This attack will increase or decrease the volume of the watermarked audio by a specified amount. """
		# TODO !!!
		return watermarked_audio
	
	def HighPass(self, watermarked_audio):
		""" This attack will attenuate low frequencies below a specified threshold in the watermarked audio. """
		# TODO !!!
		return watermarked_audio
	
	def LowPass(self, watermarked_audio):
		""" This attack will attenuate high frequencies above a specified threshold in the watermarked audio. """
		# TODO !!!
		return watermarked_audio
	
	def TimeScale(self, watermarked_audio):
		""" This attack will change the time scale in the watermarked audio by a specified amount. """
		# TODO !!!
		return watermarked_audio
	
	def AddNoise(self, watermarked_audio):
		""" This attack will add noise to the watermarked audio. """
		# TODO !!!
		return watermarked_audio
	
	# AddBrumm
	# AddDynNoise
	# AddFFTNoise
	# AddSinus
	# CopySample
	# Echo
	# ExtraStero
	# FFT_HLPassQuick
	# FFT_Invert
	# FFT_RealInverse
	# FFT_Stat1
	# FFT_test
	# FlippSample
	# Invert
	# LSBZero
	# Normalize
	# Smooth
	# Smooth2
	# Stat1
	# Stat2
	# VoiceRemove
	# ZeroCross
	# ZeroLength
	# ZeroRemove
	
	# Faking a signature that's not supposed to exist
	# Changing the number of samples per second
	# Adding noise
	# Time-scale modification
