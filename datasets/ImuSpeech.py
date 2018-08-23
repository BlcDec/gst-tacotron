from concurrent.futures import ProcessPoolExecutor
from functools import partial
import numpy as np
import os
from util import audio


def build_from_path(in_dir, out_dir, num_workers=1, tqdm=lambda x: x):

  executor = ProcessPoolExecutor(max_workers=num_workers)
  futures = []
  index = 1
  with open(os.path.join(in_dir, 'metadata.csv'), encoding='utf-8') as f:
      for line in f:
          parts = line.strip().split(',')
          tar_cd_path = os.path.join(in_dir, 'wly', '%s.wav' % parts[0])
          in_jd_path=os.path.join(in_dir,   'gky', '%s.wav' % parts[1])
          in_cg_path = os.path.join(in_dir,     'tts', '%s.wav' % parts[2])
          futures.append(executor.submit(partial(_process_utterance, out_dir, index, tar_cd_path,in_jd_path, in_cg_path)))
          index += 1
  return [future.result() for future in tqdm(futures)]


def _process_utterance(out_dir, index, tar_cd_path,in_jd_path, in_cg_path):
  '''Preprocesses a single utterance audio/text pair.

  This writes the mel and linear scale spectrograms to disk and returns a tuple to write
  to the train.txt file.

  Args:
    out_dir: The directory to write the spectrograms into
    index: The numeric index to use in the spectrogram filenames.
    wav_path: Path to the audio file containing the speech input
    text: The text spoken in the input audio file

  Returns:
    A (spectrogram_filename, mel_filename, n_frames, text) tuple to write to train.txt
  '''

  # Load the audio to a numpy array:
  tar_cd_wav = audio.load_wav(tar_cd_path)

  # Compute the linear-scale spectrogram from the wav:
  tar_cd_spectrogram = audio.spectrogram(tar_cd_wav).astype(np.float32)
  n_frames = tar_cd_spectrogram.shape[1]

  # Compute a mel-scale spectrogram from the wav:
  tar_cd_mel_spectrogram = audio.melspectrogram(tar_cd_wav).astype(np.float32)


  in_jd_wav = audio.load_wav(in_jd_path)
  in_cg_wav = audio.load_wav(in_cg_path)

  # Compute the linear-scale spectrogram from the wav:
  # Beacase of use voice traing,needless spectrogram.
  #in_spectrogram = audio.spectrogram(in_cg_wav).astype(np.float32)

  # Compute the mel-scale spectrogram from the wav:
  in_jd_mel_spectrogram = audio.melspectrogram(in_jd_wav).astype(np.float32)
  in_cg_mel_spectrogram = audio.melspectrogram(in_cg_wav).astype(np.float32)


  # Write the spectrograms to disk:
  in_jd_mel_spectrogram_filename = 'Imuspeech-in_jd_mel_spec-%05d.npy' % index
  in_cg_mel_spectrogram_filename = 'Imuspeech-in_cg_mel_spec-%05d.npy' % index
  tar_cd_spectrogram_filename    = 'Imuspeech-tar_cd_spec-%05d.npy'    % index
  tar_cd_mel_filename            = 'Imuspeech-tar_cd_mel-%05d.npy'     % index

  np.save(os.path.join(out_dir, in_jd_mel_spectrogram_filename), in_jd_mel_spectrogram.T, allow_pickle=False)
  np.save(os.path.join(out_dir, in_cg_mel_spectrogram_filename), in_cg_mel_spectrogram.T, allow_pickle=False)
  np.save(os.path.join(out_dir, tar_cd_spectrogram_filename), tar_cd_spectrogram.T, allow_pickle=False)
  np.save(os.path.join(out_dir, tar_cd_mel_filename), tar_cd_mel_spectrogram.T, allow_pickle=False)



  # Return a tuple describing this training example:
  return (tar_cd_spectrogram_filename, tar_cd_mel_filename, n_frames, in_jd_mel_spectrogram_filename,in_cg_mel_spectrogram_filename)
