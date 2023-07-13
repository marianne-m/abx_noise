# Creating a noise dataset

The aim is to create a dataset of noises, based on Audioset.
We want a clean dataset with only one class at a time, and noises
long enough to extract 1s of the noise. 
We want to use ABX test on this data.

### Data creation protocol

1/ First, we selected classes of domestic sounds : 
```
['Air conditioning',
 'Baby cry, infant cry',
 'Bark',
 'Bathtub (filling or washing)',
 'Car',
 'Crying, sobbing',
 'Howl',
 'Knock',
 'Meow',
 'Microwave oven',
 'Moo',
 'Purr',
 'Rain',
 'Subway, metro, underground',
 'Toilet flush',
 'Train',
 'Vacuum cleaner',
 'Walk, footsteps',
 'Water tap, faucet',
 'White noise']
 ```

 After listening to each class, we kept only these classes :
 ```
 ['Air conditioning',
 'Baby cry, infant cry',
 'Car',
 'Knock',
 'Purr',
 'Rain',
 'Vacuum cleaner',
 'Walk, footsteps',
 'Water tap, faucet + Bathtub (filling or washing)']
 ```

 2/ We then apply Brouhaha to find speech and removed the files with VAD.

 3/ We listen to all the remaining files and selected the ones where the sound was
 present and clean.

