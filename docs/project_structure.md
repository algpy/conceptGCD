# ConceptGCD项目结构指南
# ConceptGCD Project Structure Guide

## 完整项目目录结构 (Complete Project Directory Structure)

```
conceptGCD/
├── README.md                           # 项目说明文档
├── requirements.txt                    # Python依赖列表
├── environment.yml                     # Conda环境配置
├── setup.py                           # 项目安装脚本
├── .gitignore                         # Git忽略文件
├── .slurm_ignore                      # Slurm作业忽略文件
│
├── configs/                           # 配置文件目录
│   ├── datasets/                      # 数据集配置
│   │   ├── cifar100.yaml
│   │   ├── imagenet.yaml
│   │   └── cub200.yaml
│   ├── models/                        # 模型配置
│   │   ├── resnet.yaml
│   │   ├── vit.yaml
│   │   └── concept_encoder.yaml
│   ├── experiments/                   # 实验配置
│   │   ├── concept_gcd.yaml
│   │   ├── baseline.yaml
│   │   └── ablation_study.yaml
│   └── hyperparams/                   # 超参数配置
│       ├── config_1.yaml
│       ├── config_2.yaml
│       └── ...
│
├── data/                              # 数据相关
│   ├── __init__.py
│   ├── datasets.py                    # 数据集类定义
│   ├── loaders.py                     # 数据加载器
│   ├── transforms.py                  # 数据变换
│   ├── preprocessing.py               # 数据预处理
│   └── utils.py                       # 数据工具函数
│
├── models/                            # 模型定义
│   ├── __init__.py
│   ├── backbones/                     # 主干网络
│   │   ├── __init__.py
│   │   ├── resnet.py
│   │   ├── vit.py
│   │   └── efficientnet.py
│   ├── heads/                         # 分类/聚类头
│   │   ├── __init__.py
│   │   ├── classification_head.py
│   │   ├── clustering_head.py
│   │   └── concept_head.py
│   ├── concept_encoder.py             # 概念编码器
│   ├── concept_gcd.py                 # 主要ConceptGCD模型
│   ├── losses.py                      # 损失函数
│   └── utils.py                       # 模型工具函数
│
├── methods/                           # GCD方法实现
│   ├── __init__.py
│   ├── base.py                        # 基础方法类
│   ├── concept_gcd.py                 # Concept-driven GCD
│   ├── novel_discovery.py             # 新类发现算法
│   ├── concept_composition.py         # 概念组合机制
│   └── utils.py                       # 方法工具函数
│
├── evaluation/                        # 评估模块
│   ├── __init__.py
│   ├── metrics.py                     # 评估指标
│   ├── clustering.py                  # 聚类评估
│   ├── visualization.py              # 可视化工具
│   └── analysis.py                    # 结果分析
│
├── utils/                             # 通用工具
│   ├── __init__.py
│   ├── config.py                      # 配置处理
│   ├── logger.py                      # 日志系统
│   ├── checkpoint.py                  # 检查点管理
│   ├── distributed.py                # 分布式训练工具
│   ├── reproducibility.py            # 可复现性工具
│   └── misc.py                        # 其他工具函数
│
├── scripts/                           # 执行脚本
│   ├── train.py                       # 训练脚本
│   ├── eval.py                        # 评估脚本
│   ├── preprocess.py                  # 数据预处理脚本
│   ├── extract_features.py           # 特征提取脚本
│   ├── final_evaluation.py           # 最终评估脚本
│   └── hyperparameter_search.py      # 超参数搜索脚本
│
├── slurm/                             # Slurm作业管理
│   ├── submit_pipeline.sh             # 多阶段流水线提交
│   ├── train_job.sh                   # 训练作业脚本
│   ├── array_hyperopt.sh              # 超参数优化数组作业
│   ├── distributed_train.sh           # 分布式训练作业
│   ├── evaluation_job.sh              # 评估作业脚本
│   ├── preprocess_job.sh              # 预处理作业脚本
│   └── monitor_jobs.sh                # 作业监控脚本
│
├── tools/                             # 工具脚本
│   ├── analyze_code.py                # 代码分析工具
│   ├── generate_report.py             # 报告生成工具
│   ├── summarize_hyperopt.py          # 超参数优化结果汇总
│   ├── visualize_results.py           # 结果可视化工具
│   └── benchmark_performance.py       # 性能基准测试
│
├── docs/                              # 文档目录
│   ├── analysis_framework.md          # 分析框架文档
│   ├── slurm_analysis_guide.md        # Slurm分析指南
│   ├── project_structure.md           # 项目结构说明
│   ├── api_reference.md               # API参考文档
│   └── tutorials/                     # 教程目录
│       ├── getting_started.md
│       ├── slurm_usage.md
│       └── advanced_usage.md
│
├── tests/                             # 测试代码
│   ├── __init__.py
│   ├── test_data.py                   # 数据相关测试
│   ├── test_models.py                 # 模型相关测试
│   ├── test_methods.py                # 方法相关测试
│   ├── test_evaluation.py             # 评估相关测试
│   └── test_utils.py                  # 工具相关测试
│
├── templates/                         # 模板文件
│   ├── slurm/                         # Slurm脚本模板
│   │   ├── train_job.sh
│   │   ├── array_hyperopt.sh
│   │   └── submit_pipeline.sh
│   ├── configs/                       # 配置模板
│   │   └── experiment_config.yaml
│   └── scripts/                       # 脚本模板
│       └── train.py
│
├── logs/                              # 日志目录
│   ├── slurm_logs/                    # Slurm作业日志
│   ├── experiment_logs/               # 实验日志
│   └── pipeline/                      # 流水线日志
│
├── outputs/                           # 输出目录
│   ├── models/                        # 保存的模型
│   ├── checkpoints/                   # 检查点文件
│   ├── results/                       # 实验结果
│   ├── hyperopt/                      # 超参数优化结果
│   ├── pipeline/                      # 流水线输出
│   └── visualization/                 # 可视化结果
│
└── experiments/                       # 实验记录
    ├── experiment_1/                  # 实验1
    │   ├── config.yaml
    │   ├── results.json
    │   └── plots/
    ├── experiment_2/                  # 实验2
    └── ...
```

## 关键文件说明 (Key File Descriptions)

### 1. 配置文件 (Configuration Files)
- `configs/`: 存放所有配置文件，按功能分类
- `experiment_config.yaml`: 主要实验配置模板
- 支持YAML格式，便于版本控制和修改

### 2. 核心代码模块 (Core Code Modules)

#### 数据处理 (Data Processing)
- `data/datasets.py`: 定义各种数据集类
- `data/loaders.py`: 数据加载和批处理逻辑
- `data/transforms.py`: 数据增强和预处理变换

#### 模型定义 (Model Definitions)
- `models/concept_gcd.py`: 主要的ConceptGCD模型
- `models/concept_encoder.py`: 概念编码器实现
- `models/backbones/`: 各种主干网络实现

#### 方法实现 (Method Implementations)
- `methods/concept_gcd.py`: Concept-driven GCD算法
- `methods/novel_discovery.py`: 新类发现机制
- `methods/concept_composition.py`: 概念组合策略

### 3. Slurm作业管理 (Slurm Job Management)

#### 核心作业脚本
- `slurm/submit_pipeline.sh`: 多阶段流水线管理
- `slurm/train_job.sh`: 标准训练作业
- `slurm/array_hyperopt.sh`: 并行超参数优化

#### 作业模式
- **单作业模式**: 独立的训练或评估任务
- **数组作业模式**: 并行超参数搜索
- **流水线模式**: 多阶段依赖执行
- **分布式模式**: 多节点并行训练

### 4. 工具和脚本 (Tools and Scripts)

#### 分析工具
- `tools/analyze_code.py`: 自动化代码结构分析
- `tools/generate_report.py`: 实验报告生成
- `tools/visualize_results.py`: 结果可视化

#### 执行脚本
- `scripts/train.py`: 主训练脚本
- `scripts/eval.py`: 评估脚本
- `scripts/preprocess.py`: 数据预处理脚本

## 代码组织原则 (Code Organization Principles)

### 1. 模块化设计
- 每个功能模块独立成包
- 清晰的接口定义
- 最小化模块间依赖

### 2. 配置驱动
- 所有实验参数通过配置文件管理
- 支持配置继承和覆盖
- 便于实验复现和比较

### 3. Slurm集成
- 原生支持Slurm集群环境
- 自动化作业依赖管理
- 资源优化配置

### 4. 可扩展性
- 易于添加新的数据集和模型
- 支持插件式的算法扩展
- 标准化的评估接口

### 5. 可复现性
- 完整的环境和依赖管理
- 自动化的实验记录
- 版本控制友好的项目结构

## 开发工作流 (Development Workflow)

### 1. 本地开发
```bash
# 设置环境
conda env create -f environment.yml
conda activate conceptgcd

# 安装项目
pip install -e .

# 运行测试
python -m pytest tests/
```

### 2. 集群部署
```bash
# 数据预处理
sbatch slurm/preprocess_job.sh

# 训练模型
sbatch slurm/train_job.sh

# 超参数优化
sbatch slurm/array_hyperopt.sh

# 完整流水线
bash slurm/submit_pipeline.sh
```

### 3. 结果分析
```bash
# 生成分析报告
python tools/analyze_code.py .

# 可视化结果
python tools/visualize_results.py outputs/results/

# 生成最终报告
python tools/generate_report.py outputs/
```

此结构设计支持大规模机器学习研究项目的开发、部署和维护需求。