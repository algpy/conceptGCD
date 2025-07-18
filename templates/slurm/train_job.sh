#!/bin/bash
#SBATCH --job-name=conceptGCD_train
#SBATCH --output=logs/train_%j.out
#SBATCH --error=logs/train_%j.err
#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:v100:1
#SBATCH --mem=32G
#SBATCH --partition=gpu

# =============================================================================
# ConceptGCD训练作业模板 (ConceptGCD Training Job Template)
# 
# 用途: 训练Concept-Driven GCD模型
# Purpose: Train Concept-Driven GCD model
# =============================================================================

echo "作业开始时间: $(date)"
echo "运行节点: $SLURMD_NODENAME"
echo "作业ID: $SLURM_JOB_ID"

# 环境设置 (Environment Setup)
echo "设置环境..."
module purge
module load python/3.8.5
module load cuda/11.2
module load cudnn/8.1.1

# 激活Python环境
source ~/.bashrc
conda activate conceptgcd

# 设置环境变量
export CUDA_VISIBLE_DEVICES=$SLURM_LOCALID
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# 创建必要的目录
mkdir -p logs
mkdir -p outputs/models
mkdir -p outputs/checkpoints

# 验证环境
echo "Python版本: $(python --version)"
echo "CUDA可用性: $(python -c 'import torch; print(torch.cuda.is_available())')"
echo "GPU数量: $(python -c 'import torch; print(torch.cuda.device_count())')"

# 主要训练任务 (Main Training Task)
echo "开始训练..."

# 阶段1: 数据预处理检查
echo "检查数据预处理状态..."
if [ ! -f "data/processed/train_features.pt" ]; then
    echo "运行数据预处理..."
    python scripts/preprocess.py \
        --config configs/preprocess.yaml \
        --output-dir data/processed
fi

# 阶段2: 模型训练
echo "开始模型训练..."
python scripts/train.py \
    --config configs/experiments/concept_gcd.yaml \
    --output-dir outputs/models \
    --checkpoint-dir outputs/checkpoints \
    --log-dir logs \
    --device cuda \
    --num-workers $SLURM_CPUS_PER_TASK

# 阶段3: 模型验证
echo "运行模型验证..."
python scripts/validate.py \
    --config configs/experiments/concept_gcd.yaml \
    --model-path outputs/models/best_model.pth \
    --output-dir outputs/validation

# 清理临时文件
echo "清理临时文件..."
find /tmp -name "*conceptgcd*" -user $USER -delete 2>/dev/null || true

echo "作业完成时间: $(date)"
echo "训练作业完成!"

# 作业统计信息
echo "=== 作业统计 ==="
echo "总运行时间: $SECONDS 秒"
echo "GPU使用情况:"
nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total --format=csv