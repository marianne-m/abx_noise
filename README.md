# ABX on noise

This project objective is to evaluate models on a ABX task on noise.

We use the STARSS22 dataset to generate the `.item` files.

The **Sony-TAu Realistic Spatial Soundscapes 2022 (STARSS22)** dataset contains multichannel recordings of 
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

We remove the "Music" class (8), and keep the frames with only one class activated at a time.


For each recording, the labels are provided in a CSV file :
`[frame number (int)], [active class index (int)], [source number index (int)], [azimuth (int)], [elevation (int)]`

A frame correspond to a temporal relolution of 100ms.