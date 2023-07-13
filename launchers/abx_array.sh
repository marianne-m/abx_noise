#!/bin/bash
#SBATCH --job-name=job-array   # nom du job
#SBATCH --cpus-per-task=10
#SBATCH --account=xdz@v100
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
#SBATCH --ntasks-per-node=1    # Nombre de processus MPI par noeud
#SBATCH --hint=nomultithread   # 1 processus MPI par coeur physique (pas d'hyperthreading)
#SBATCH --time=01:00:00        # Temps d’exécution maximum demande (HH:MM:SS)
#SBATCH --output=logs/%x_%A_%a.out  # Nom du fichier de sortie contenant l'ID et l'indice
#SBATCH --error=logs/%x_%A_%a.out   # Nom du fichier d'erreur (ici commun avec la sortie)
#SBATCH --array=1-160%30
 

CORPUS="librivox"
# CORPUS="seedlings"
PATH_CHECKPOINT=$(sed -n "$SLURM_ARRAY_TASK_ID"p ./launchers/$CORPUS.txt)

DATASET_PATH="/gpfswork/rech/xdz/commun/abx_noise/audiofiles"
CPC_PATH="/gpfswork/rech/xdz/uzm31mf/CPC2"
ITEM_PATH="/gpfswork/rech/xdz/commun/abx_noise/final_item_files/item_files_merged"

BEST=$(python $CPC_PATH/utils/best_val_epoch.py --model_path $PATH_CHECKPOINT)
EPOCH=$(echo "$BEST" | awk '{print $NF}')
CHECKPOINT="checkpoint_${EPOCH}.pt"

EXP_ID=$(echo $PATH_CHECKPOINT | rev | cut -f 2,3 -d "/" | rev)
_EXP_ID=$(echo $PATH_CHECKPOINT | rev | cut -f 2,3 -d "/" | rev | tr / _)

echo "no seq_norm, max_size_seq 128000"
echo "path_checkpoint : $PATH_CHECKPOINT"
echo "exp_id : $EXP_ID"
echo "_exp_id : $_EXP_ID"
echo "checkpoint : $CHECKPOINT"


for DURATION in 300 500 1000
do
  	PATH_OUT="/gpfswork/rech/xdz/commun/abx_noise/cpc_abx_scores_with_speech/$CORPUS/$EXP_ID/${_EXP_ID}_${CORPUS}_${DURATION}"
        mkdir -p $PATH_OUT
        PATH_ITEM_FILE="${ITEM_PATH}/final_${DURATION}ms.item"
        echo "compution abx score for $CORPUS corpus and $DURATION ms"
        # Execution du code
        python $CPC_PATH/cpc/eval/eval_ABX.py from_checkpoint $PATH_CHECKPOINT/$CHECKPOINT $PATH_ITEM_FILE $DATASET_PATH \
        --out $PATH_OUT --cuda --strict --file_extension .wav --mode within --max_size_seq 128000
done
