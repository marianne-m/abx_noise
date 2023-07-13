import sys
import argparse
from pathlib import Path
import numpy as np
import librosa as lb
import librosa.display
import torch
from tqdm import tqdm



def parse_args(argv):
    parser = argparse.ArgumentParser(description='Extract MFCC features.')

    parser.add_argument('data', type=Path,
                        help="Path to the audio data.")
    parser.add_argument('output', type=Path,
                        help="Path to generated MFCC features.")
    parser.add_argument('--extension', type=str, default=".wav",
                        help="Extension of the audiofiles. Default : .wav")

    return parser.parse_args(argv)


def main(argv):
    args = parse_args(argv)

    for audio_file in tqdm(args.data.rglob(f"*{args.extension}")):
        filename = audio_file.stem
        data, sr = lb.load(audio_file)
        mfcc = librosa.feature.mfcc(y=data, sr=sr, n_mfcc=13)
        mfcc_delta = librosa.feature.delta(mfcc)
        mfcc_delta2 = librosa.feature.delta(mfcc, order=2)
        features = np.vstack([mfcc, mfcc_delta, mfcc_delta2])

        features_torch = torch.from_numpy(features)
        features_torch = torch.transpose(features_torch, 0, 1)
        torch.save(features_torch, args.output / f"{filename}.pt")


if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)