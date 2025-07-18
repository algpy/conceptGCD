#!/bin/bash
#SBATCH --job-name=conceptGCD_hyperopt
#SBATCH --output=logs/hyperopt_%A_%a.out
#SBATCH --error=logs/hyperopt_%A_%a.err
#SBATCH --array=1-50
#SBATCH --time=12:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:1
#SBATCH --mem=16G
#SBATCH --partition=gpu

# =============================================================================
# ConceptGCD超参数优化数组作业模板
# ConceptGCD Hyperparameter Optimization Array Job Template
# 
# 用途: 并行执行多个超参数配置的训练
# Purpose: Parallel execution of training with multiple hyperparameter configs
# =============================================================================

echo "数组作业开始: $(date)"
echo "数组任务ID: $SLURM_ARRAY_TASK_ID"
echo "总数组大小: $SLURM_ARRAY_TASK_COUNT"
echo "运行节点: $SLURMD_NODENAME"

# 环境设置
module purge
module load python/3.8.5
module load cuda/11.2

source ~/.bashrc
conda activate conceptgcd

export CUDA_VISIBLE_DEVICES=$SLURM_LOCALID
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

# 创建任务特定的目录
TASK_DIR="outputs/hyperopt/task_${SLURM_ARRAY_TASK_ID}"
mkdir -p $TASK_DIR
mkdir -p logs/hyperopt

# 获取该任务的超参数配置
CONFIG_FILE="configs/hyperparams/config_${SLURM_ARRAY_TASK_ID}.yaml"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "错误: 配置文件不存在: $CONFIG_FILE"
    exit 1
fi

echo "使用配置文件: $CONFIG_FILE"

# 运行训练
echo "开始超参数优化任务 $SLURM_ARRAY_TASK_ID..."

python scripts/train.py \
    --config $CONFIG_FILE \
    --output-dir $TASK_DIR \
    --task-id $SLURM_ARRAY_TASK_ID \
    --device cuda \
    --num-workers $SLURM_CPUS_PER_TASK \
    --hyperopt-mode

# 记录结果
echo "任务 $SLURM_ARRAY_TASK_ID 完成时间: $(date)"

# 检查是否是最后一个任务，如果是则汇总结果
if [ "$SLURM_ARRAY_TASK_ID" == "$SLURM_ARRAY_TASK_MAX" ]; then
    echo "等待其他任务完成..."
    sleep 30
    
    echo "汇总超参数优化结果..."
    python tools/summarize_hyperopt.py \
        --results-dir outputs/hyperopt \
        --output-file outputs/hyperopt_summary.json
fi