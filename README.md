# ABX on noise

This project objective is to evaluate models on a ABX task on noise.

We first evaluate the models on the Dcase Dataset.
We use the STARSS22 dataset to generate the `.item` files.

## DCASE dataset

The [Sony-TAu Realistic Spatial Soundscapes 2022 (STARSS22)](https://zenodo.org/record/6387880) dataset contains multichannel recordings of 
sound scenes in various rooms and environments, together with temporal and spatial annotations of 
prominent events belonging to a set of target classes.

The 13 sound classes are :

  0. Female speech, woman speaking
  1. Male speech, man speaking
  2. Clapping
  3. Telephone
  4. Laughter
  5. Domestic sounds
  6. Walk, footsteps
  7. Door, open or close
  8. Music
  9. Musical instrument
  10. Water tap, faucet
  11. Bell
  12. Knock

For each recording, the labels are provided in a CSV file :
`[frame number (int)], [active class index (int)], [source number index (int)], [azimuth (int)], [elevation (int)]`

A frame correspond to a temporal relolution of 100ms.

We removed the "Music" class (8), and keep the frames with only one class activated at a time to compute the ABX scores.


## DCASE + AusioSet

The results on Dcase only are promising, so we decided to keep only a few classes and to extend the dataset with noise 
segments from [AudioSet](https://research.google.com/audioset/).

The classes kept from Dcase are :
- Walk, footsteps
- Clapping
- Water tap
- Male speech
- Female speech
- Domestic sounds : seperated in two classes Vacuum cleaner and Air conditioning

To separate domestic sounds, we used two additional labels on Dcase:
  13. Vacuum Cleaner
  14. Air Conditioning

We added the following classes from AudioSet:
- Air conditioning
- Baby Cry
- Knock
- Purr
- Rain
- Vacuum cleaner
- Walk, footsteps
- Water tap


## Evaluation scripts

To compute the ABX score, use [CPC2](https://github.com/MarvinLvn/CPC2/tree/master).

You can use the launchers in `launchers`

The item files are in `./item_files/final_merged`

The audiofiles are on Jean Zay : `/gpfswork/rech/xdz/commun/abx_noise/audiofiles`


## Plot graphs

You can use `scripts/plot_abx.py` to plot the mean and std ABX error rate according to training duration.
