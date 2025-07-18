#!/bin/bash
# =============================================================================
# ConceptGCD多阶段执行管理脚本
# ConceptGCD Multi-Stage Execution Management Script
# 
# 此脚本演示如何管理多阶段的机器学习流水线
# This script demonstrates how to manage multi-stage ML pipeline
# =============================================================================

set -e  # 遇到错误立即退出

echo "=== ConceptGCD多阶段执行开始 ==="
echo "执行时间: $(date)"

# 配置参数
PROJECT_ROOT="$(pwd)"
LOG_DIR="logs/pipeline"
OUTPUT_DIR="outputs/pipeline"

# 创建必要目录
mkdir -p $LOG_DIR
mkdir -p $OUTPUT_DIR

# =============================================================================
# 阶段1: 数据预处理 (Stage 1: Data Preprocessing)
# =============================================================================
echo "提交阶段1: 数据预处理作业..."

PREPROCESS_JOB=$(sbatch --parsable \
    --job-name=conceptGCD_preprocess \
    --output=$LOG_DIR/preprocess_%j.out \
    --error=$LOG_DIR/preprocess_%j.err \
    --time=02:00:00 \
    --nodes=1 \
    --cpus-per-task=8 \
    --mem=16G \
    --wrap="python scripts/preprocess.py --config configs/preprocess.yaml")

echo "数据预处理作业ID: $PREPROCESS_JOB"

# =============================================================================
# 阶段2: 特征提取 (Stage 2: Feature Extraction)
# =============================================================================
echo "提交阶段2: 特征提取作业..."

FEATURE_JOB=$(sbatch --parsable \
    --dependency=afterok:$PREPROCESS_JOB \
    --job-name=conceptGCD_features \
    --output=$LOG_DIR/features_%j.out \
    --error=$LOG_DIR/features_%j.err \
    --time=06:00:00 \
    --nodes=1 \
    --gres=gpu:1 \
    --cpus-per-task=4 \
    --mem=24G \
    --wrap="python scripts/extract_features.py --config configs/feature_extraction.yaml")

echo "特征提取作业ID: $FEATURE_JOB"

# =============================================================================
# 阶段3: 模型训练 (Stage 3: Model Training)
# =============================================================================
echo "提交阶段3: 模型训练作业..."

TRAIN_JOB=$(sbatch --parsable \
    --dependency=afterok:$FEATURE_JOB \
    --job-name=conceptGCD_train \
    --output=$LOG_DIR/train_%j.out \
    --error=$LOG_DIR/train_%j.err \
    --time=24:00:00 \
    --nodes=1 \
    --gres=gpu:v100:1 \
    --cpus-per-task=8 \
    --mem=32G \
    slurm/train_job.sh)

echo "模型训练作业ID: $TRAIN_JOB"

# =============================================================================
# 阶段4: 超参数优化 (Stage 4: Hyperparameter Optimization)
# =============================================================================
echo "提交阶段4: 超参数优化数组作业..."

HYPEROPT_JOB=$(sbatch --parsable \
    --dependency=afterok:$TRAIN_JOB \
    --job-name=conceptGCD_hyperopt \
    --output=$LOG_DIR/hyperopt_%A_%a.out \
    --error=$LOG_DIR/hyperopt_%A_%a.err \
    --array=1-20 \
    --time=12:00:00 \
    --nodes=1 \
    --gres=gpu:1 \
    --cpus-per-task=4 \
    --mem=16G \
    slurm/array_hyperopt.sh)

echo "超参数优化作业ID: $HYPEROPT_JOB"

# =============================================================================
# 阶段5: 最终评估 (Stage 5: Final Evaluation)
# =============================================================================
echo "提交阶段5: 最终评估作业..."

EVAL_JOB=$(sbatch --parsable \
    --dependency=afterok:$HYPEROPT_JOB \
    --job-name=conceptGCD_eval \
    --output=$LOG_DIR/eval_%j.out \
    --error=$LOG_DIR/eval_%j.err \
    --time=04:00:00 \
    --nodes=1 \
    --gres=gpu:1 \
    --cpus-per-task=4 \
    --mem=16G \
    --wrap="python scripts/final_evaluation.py --config configs/evaluation.yaml")

echo "最终评估作业ID: $EVAL_JOB"

# =============================================================================
# 阶段6: 结果汇总 (Stage 6: Results Summary)
# =============================================================================
echo "提交阶段6: 结果汇总作业..."

SUMMARY_JOB=$(sbatch --parsable \
    --dependency=afterok:$EVAL_JOB \
    --job-name=conceptGCD_summary \
    --output=$LOG_DIR/summary_%j.out \
    --error=$LOG_DIR/summary_%j.err \
    --time=01:00:00 \
    --nodes=1 \
    --cpus-per-task=2 \
    --mem=8G \
    --wrap="python tools/generate_report.py --pipeline-dir $OUTPUT_DIR")

echo "结果汇总作业ID: $SUMMARY_JOB"

# =============================================================================
# 作业监控 (Job Monitoring)
# =============================================================================
echo ""
echo "=== 已提交的作业链 ==="
echo "1. 数据预处理: $PREPROCESS_JOB"
echo "2. 特征提取: $FEATURE_JOB (依赖: $PREPROCESS_JOB)"
echo "3. 模型训练: $TRAIN_JOB (依赖: $FEATURE_JOB)"
echo "4. 超参数优化: $HYPEROPT_JOB (依赖: $TRAIN_JOB)"
echo "5. 最终评估: $EVAL_JOB (依赖: $HYPEROPT_JOB)"
echo "6. 结果汇总: $SUMMARY_JOB (依赖: $EVAL_JOB)"
echo ""

# 保存作业ID到文件
cat > $OUTPUT_DIR/job_ids.txt << EOF
PREPROCESS_JOB=$PREPROCESS_JOB
FEATURE_JOB=$FEATURE_JOB
TRAIN_JOB=$TRAIN_JOB
HYPEROPT_JOB=$HYPEROPT_JOB
EVAL_JOB=$EVAL_JOB
SUMMARY_JOB=$SUMMARY_JOB
EOF

echo "作业ID已保存到: $OUTPUT_DIR/job_ids.txt"

# 创建监控脚本
cat > $OUTPUT_DIR/monitor_jobs.sh << 'EOF'
#!/bin/bash
# 监控作业状态脚本

source outputs/pipeline/job_ids.txt

echo "=== ConceptGCD作业状态监控 ==="
echo "检查时间: $(date)"
echo ""

for job_name in PREPROCESS_JOB FEATURE_JOB TRAIN_JOB HYPEROPT_JOB EVAL_JOB SUMMARY_JOB; do
    job_id_var=${job_name}
    job_id=${!job_id_var}
    
    if [ ! -z "$job_id" ]; then
        status=$(squeue -j $job_id -h -o "%T" 2>/dev/null || echo "COMPLETED/FAILED")
        echo "$job_name ($job_id): $status"
    fi
done

echo ""
echo "详细状态:"
sacct -j $PREPROCESS_JOB,$FEATURE_JOB,$TRAIN_JOB,$HYPEROPT_JOB,$EVAL_JOB,$SUMMARY_JOB \
    --format=JobID,JobName,State,Elapsed,MaxRSS 2>/dev/null || echo "无法获取详细状态"
EOF

chmod +x $OUTPUT_DIR/monitor_jobs.sh

echo "监控脚本已创建: $OUTPUT_DIR/monitor_jobs.sh"
echo "使用以下命令监控作业状态:"
echo "  bash $OUTPUT_DIR/monitor_jobs.sh"
echo ""
echo "=== 多阶段执行管理完成 ==="