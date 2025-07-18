# ConceptGCD Code Analysis Framework

## Project Overview
**Composing Novel Classes: A Concept-Driven Approach to Generalized Category Discovery**

This document provides a comprehensive framework for analyzing code structure, logic, and implementation patterns in a Slurm-based machine learning project focused on Generalized Category Discovery (GCD).

## 1. Research Domain Context

### Generalized Category Discovery (GCD)
GCD is a machine learning paradigm that aims to:
- Discover novel categories in unlabeled data
- Leverage knowledge from labeled known categories
- Compose novel classes using concept-driven approaches
- Handle both supervised and unsupervised learning aspects

### Common Research Components
1. **Data Processing**: Dataset loading, preprocessing, augmentation
2. **Model Architecture**: Neural networks for feature extraction and classification
3. **Training Pipeline**: Supervised pretraining, unsupervised discovery
4. **Evaluation Metrics**: Clustering metrics, classification accuracy, novel class discovery
5. **Visualization**: t-SNE, UMAP, confusion matrices

## 2. Expected Code Structure for GCD Projects

### Typical Directory Organization
```
conceptGCD/
├── configs/              # Configuration files
│   ├── datasets/        # Dataset-specific configs
│   ├── models/          # Model architecture configs
│   └── experiments/     # Experiment configurations
├── data/                # Data handling
│   ├── datasets.py      # Dataset classes
│   ├── loaders.py       # Data loaders
│   └── transforms.py    # Data transformations
├── models/              # Model implementations
│   ├── backbones/       # Feature extractors
│   ├── heads/           # Classification/clustering heads
│   └── losses.py        # Loss functions
├── methods/             # GCD algorithms
│   ├── base.py          # Base method class
│   ├── concept_gcd.py   # Main concept-driven GCD
│   └── utils.py         # Method utilities
├── evaluation/          # Evaluation metrics and tools
├── scripts/             # Training and evaluation scripts
├── slurm/               # Slurm job management
└── utils/               # General utilities
```

## 3. Slurm Framework Integration Patterns

### Common Slurm Components in ML Projects
1. **Job Scripts**: SBATCH scripts for different experiments
2. **Array Jobs**: Parallel execution of hyperparameter sweeps
3. **Resource Management**: GPU/CPU allocation, memory management
4. **Environment Setup**: Module loading, conda environments
5. **Output Management**: Logging, checkpointing, results collection

### Expected Slurm Script Structure
```bash
#!/bin/bash
#SBATCH --job-name=conceptGCD
#SBATCH --output=logs/%j.out
#SBATCH --error=logs/%j.err
#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gres=gpu:1
#SBATCH --mem=32G

# Environment setup
module load python/3.8
source activate conceptgcd

# Main execution
python scripts/train.py --config configs/experiments/concept_gcd.yaml
```

## 4. Analysis Checklist for Multi-Stage Execution

### Stage 1: Code Structure Analysis
- [ ] Directory organization adherence to ML best practices
- [ ] Separation of concerns (data, models, methods, evaluation)
- [ ] Configuration management approach
- [ ] Import structure and dependencies

### Stage 2: Slurm Integration Analysis
- [ ] Job script organization and naming conventions
- [ ] Resource allocation patterns
- [ ] Environment management
- [ ] Output and logging strategies
- [ ] Array job implementations for hyperparameter tuning

### Stage 3: Algorithm Logic Analysis
- [ ] Data flow through the pipeline
- [ ] Model architecture design
- [ ] Training procedures (supervised + unsupervised)
- [ ] Novel class discovery mechanisms
- [ ] Concept composition strategies

### Stage 4: Experimental Framework Analysis
- [ ] Configuration management
- [ ] Hyperparameter handling
- [ ] Evaluation protocols
- [ ] Results aggregation and analysis
- [ ] Reproducibility measures

### Stage 5: Code Quality and Maintainability
- [ ] Code organization and modularity
- [ ] Documentation quality
- [ ] Testing framework
- [ ] Error handling and logging
- [ ] Performance optimization

## 5. Key Concepts to Identify

### Core GCD Concepts
1. **Known vs Novel Classes**: How the code distinguishes between categories
2. **Concept Representation**: How concepts are encoded and manipulated
3. **Composition Mechanisms**: How novel classes are formed from concepts
4. **Discovery Pipeline**: The process of identifying new categories

### Slurm-Specific Patterns
1. **Job Dependencies**: How experiments depend on each other
2. **Resource Scaling**: How resources are allocated based on experiment size
3. **Fault Tolerance**: Error handling and job restart mechanisms
4. **Data Management**: How data is shared across compute nodes

## 6. Expected File Types and Their Purposes

### Python Files
- **main.py**: Entry point for training/evaluation
- **train.py**: Training pipeline implementation
- **eval.py**: Evaluation pipeline
- **config.py**: Configuration handling utilities

### Configuration Files
- **YAML/JSON**: Experiment configurations
- **INI**: System-level configurations

### Slurm Files
- **submit_*.sh**: Job submission scripts
- **array_jobs.sh**: Array job definitions
- **env_setup.sh**: Environment preparation

### Data Files
- **requirements.txt**: Python dependencies
- **environment.yml**: Conda environment specification

This framework will be used to systematically analyze the conceptGCD codebase once it's implemented.