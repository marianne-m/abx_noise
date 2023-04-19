import pandas as pd
from pathlib import Path
import argparse
import logging
import sys
import json
import matplotlib.pyplot as plt
from collections import defaultdict

NOISE_DURATIONS = [300, 500, 1000]

logger = logging.getLogger(__name__)


def retreive_abx_scores(folder_path: str) -> pd.DataFrame:
    all_values = []
    for file in Path(folder_path).glob("**/ABX_scores.json"):
        parent = file.parent.name
        train_duration, exp_id, corpus, noise_duration = str(parent).split("_")
        train_duration = train_duration.replace("h", "")
        with open(file, "r") as abx_file:
            abx_dict = json.load(abx_file)
            abx = abx_dict["within"]
        all_values.append([train_duration, exp_id, corpus, noise_duration, abx])

    abx_df = pd.DataFrame(all_values, columns=["train_dur", "exp_id", "corpus", "noise_dur", "abx"])
    return abx_df


def compute_mean_std(abx_df):
    abx_df = abx_df.groupby(["train_dur", "corpus", "noise_dur"]).agg(['mean', 'std']).reset_index()
    return abx_df


def plot_figures(abx_df, fig_name):
    fig, ax = plt.subplots()

    for noise_duration in NOISE_DURATIONS:
        abx_by_noise = abx_df[abx_df['noise_dur'] == noise_duration]
        abx_by_noise = abx_by_noise[abx_by_noise['train_dur'] != 0]

        ax.errorbar(
            abx_by_noise["train_dur"],
            abx_by_noise[("abx", "mean")],
            yerr=abx_by_noise[("abx", "std")],
            label=f"Noise duration = {noise_duration} ms",
            alpha=0.7
        )
    
    ax.legend()
    ax.set_xlabel("Training duration in hours")
    ax.set_ylabel("ABX error rate")
    ax.set_xscale("log")
    ax.set_xticks([8, 16, 32, 64, 128, 256, 512, 1024])
    ax.set_xticklabels([8, 16, 32, 64, 128, 256, 512, 1024])
    ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())

    plt.savefig(fig_name)



def parse_args(argv):
    parser = argparse.ArgumentParser(description='Plot all abx scores by training duration')
    parser.add_argument("figure_name", type=str,
                        help="Name of the plot")

    subparsers = parser.add_subparsers(dest="load")
    parser_file = subparsers.add_parser("from_file")
    parser_file.add_argument('csv_file', type=str, 
                       help='Path to the csv file where all the abx scores have been recopied')

    parser_file = subparsers.add_parser("from_data")
    parser_file.add_argument('abx_score_path', type=str, 
                       help='Retreive all the abx scores in this folder')
    parser_file.add_argument('--path_abx', type=str, default="./abx.csv",
                             help='Where to save abx csv')


    return parser.parse_args(argv)


def main(argv):
    args = parse_args(argv)

    if args.load == "from_data":
        logger.info(f"Retreiving the abx scores from {args.abx_score_path}")
        abx_scores = retreive_abx_scores(args.abx_score_path)
        abx_scores.to_csv(args.path_abx)
        logger.info(f"Abx scores are save in this csv file : {args.abx_score_path}")

    elif args.load == "from_file":
        logger.info(f"Reading the abx scores from {args.csv_file}")
        abx_scores = pd.read_csv(args.csv_file, index_col=0).drop(labels="exp_id", axis=1)

    abx_scores = compute_mean_std(abx_scores)
    plot_figures(abx_scores, args.figure_name)


if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)