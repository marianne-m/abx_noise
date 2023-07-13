#!/bin/bash
#SBATCH --account=xdz@v100
#SBATCH --nodes=1                    # on demande un noeud
#SBATCH --ntasks-per-node=1          # avec une tache par noeud (= nombre de GPU ici)
#SBATCH --gres=gpu:1                 # nombre de GPU par noeud (max 8 avec gpu_p2, gpu_p4, gpu_p5)
#SBATCH --cpus-per-task=10           # nombre de CPU par tache (1/4 des CPU du noeud 4-GPU)
#SBATCH --hint=nomultithread         # hyperthreading desactive
#SBATCH --time=01:00:00              # temps maximum d'execution demande (HH:MM:SS)


CORPUS="librivox"
#CORPUS="seedlings"

PATH_CHECKPOINT="/gpfsscratch/rech/xdz/commun/audiobooks_vs_longforms/librivox_training/English_LibriVox_extracted_full_random/1024h/00/cpc_small"
#PATH_CHECKPOINT="/gpfsscratch/rech/xdz/commun/audiobooks_vs_longforms/seedlings_training/EN/1024h/00/cpc_small"

DATASET_PATH="/gpfswork/rech/xdz/commun/abx_noise/audiofiles"
CPC_PATH="/gpfswork/rech/xdz/uzm31mf/CPC2"
ITEM_PATH="/gpfswork/rech/xdz/commun/abx_noise/final_item_files/item_files_merged"

BEST=$(python $CPC_PATH/utils/best_val_epoch.py --model_path $PATH_CHECKPOINT)
EPOCH=$(echo "$BEST" | awk '{print $NF}')
CHECKPOINT="checkpoint_${EPOCH}.pt"

echo "no seq_norm, max_size_seq 128000"

for DURATION in 300 500 1000
do
	PATH_OUT="/gpfswork/rech/xdz/commun/abx_noise/out_with_speech/${CORPUS}/${DURATION}"
        mkdir -p $PATH_OUT
	PATH_ITEM_FILE="${ITEM_PATH}/final_${DURATION}ms.item"
	echo "compution abx score for $CORPUS corpus and $DURATION ms"
	# Execution du code
	python $CPC_PATH/cpc/eval/eval_ABX.py from_checkpoint $PATH_CHECKPOINT/$CHECKPOINT $PATH_ITEM_FILE $DATASET_PATH \
	--out $PATH_OUT --cuda --strict --file_extension .wav --mode within --max_size_seq 128000
done

