#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ConceptGCD训练脚本模板
ConceptGCD Training Script Template

此脚本展示了在Slurm环境下运行的典型训练流程
This script demonstrates typical training workflow under Slurm environment
"""

import os
import sys
import json
import argparse
import logging
from pathlib import Path
from typing import Dict, Any, Optional

import yaml
import torch
import torch.distributed as dist
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def setup_logging(log_dir: str, rank: int = 0) -> logging.Logger:
    """设置日志系统"""
    log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建logger
    logger = logging.getLogger("ConceptGCD")
    logger.setLevel(logging.INFO)
    
    # 只在主进程中添加handler
    if rank == 0:
        # 文件handler
        file_handler = logging.FileHandler(log_dir / "train.log")
        file_handler.setLevel(logging.INFO)
        
        # 控制台handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger


def load_config(config_path: str) -> Dict[str, Any]:
    """加载配置文件"""
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config


def setup_distributed(rank: int, world_size: int) -> None:
    """设置分布式训练"""
    if world_size > 1:
        # 初始化分布式进程组
        dist.init_process_group(
            backend='nccl',
            init_method='env://',
            world_size=world_size,
            rank=rank
        )
        torch.cuda.set_device(rank)


def cleanup_distributed() -> None:
    """清理分布式训练"""
    if dist.is_initialized():
        dist.destroy_process_group()


def get_slurm_info() -> Dict[str, Any]:
    """获取Slurm作业信息"""
    slurm_info = {}
    
    # 常见的Slurm环境变量
    slurm_vars = [
        'SLURM_JOB_ID', 'SLURM_JOB_NAME', 'SLURM_JOB_NODELIST',
        'SLURM_NTASKS', 'SLURM_NTASKS_PER_NODE', 'SLURM_CPUS_PER_TASK',
        'SLURM_MEM_PER_NODE', 'SLURM_ARRAY_TASK_ID', 'SLURM_LOCALID'
    ]
    
    for var in slurm_vars:
        value = os.environ.get(var)
        if value is not None:
            slurm_info[var] = value
    
    return slurm_info


def save_experiment_info(output_dir: str, config: Dict[str, Any], 
                        slurm_info: Dict[str, Any]) -> None:
    """保存实验信息"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 保存配置
    with open(output_dir / "config.yaml", 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
    
    # 保存Slurm信息
    with open(output_dir / "slurm_info.json", 'w', encoding='utf-8') as f:
        json.dump(slurm_info, f, indent=2, ensure_ascii=False)
    
    # 保存环境信息
    env_info = {
        'python_version': sys.version,
        'pytorch_version': torch.__version__,
        'cuda_version': torch.version.cuda if torch.cuda.is_available() else None,
        'gpu_count': torch.cuda.device_count(),
        'hostname': os.uname().nodename,
        'pwd': os.getcwd()
    }
    
    with open(output_dir / "environment.json", 'w', encoding='utf-8') as f:
        json.dump(env_info, f, indent=2, ensure_ascii=False)


class ConceptGCDTrainer:
    """ConceptGCD训练器"""
    
    def __init__(self, config: Dict[str, Any], logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.device = torch.device(config['system']['device'])
        
        # 设置随机种子
        self.set_seed(config['reproducibility']['seed'])
        
        # 初始化模型、数据、优化器等
        self.model = self.build_model()
        self.train_loader, self.val_loader = self.build_dataloaders()
        self.optimizer = self.build_optimizer()
        self.scheduler = self.build_scheduler()
        self.criterion = self.build_criterion()
        
        # Tensorboard写入器
        if config['logging']['tensorboard']:
            self.writer = SummaryWriter(config['checkpoint']['save_dir'] + '/tensorboard')
        else:
            self.writer = None
    
    def set_seed(self, seed: int) -> None:
        """设置随机种子"""
        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        
        if self.config['reproducibility']['deterministic']:
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False
        else:
            torch.backends.cudnn.benchmark = True
    
    def build_model(self):
        """构建模型"""
        # 这里应该实现具体的模型构建逻辑
        self.logger.info("构建ConceptGCD模型...")
        # return ConceptGCDModel(self.config['model'])
        pass
    
    def build_dataloaders(self):
        """构建数据加载器"""
        self.logger.info("构建数据加载器...")
        # 这里应该实现具体的数据加载逻辑
        # return train_loader, val_loader
        pass
    
    def build_optimizer(self):
        """构建优化器"""
        self.logger.info("构建优化器...")
        # 这里应该实现具体的优化器构建逻辑
        pass
    
    def build_scheduler(self):
        """构建学习率调度器"""
        self.logger.info("构建学习率调度器...")
        # 这里应该实现具体的调度器构建逻辑
        pass
    
    def build_criterion(self):
        """构建损失函数"""
        self.logger.info("构建损失函数...")
        # 这里应该实现具体的损失函数构建逻辑
        pass
    
    def train_epoch(self, epoch: int) -> Dict[str, float]:
        """训练一个epoch"""
        self.logger.info(f"开始训练epoch {epoch}")
        
        # 这里应该实现具体的训练逻辑
        metrics = {
            'loss': 0.0,
            'accuracy': 0.0,
            'concept_loss': 0.0,
            'discovery_loss': 0.0
        }
        
        return metrics
    
    def validate_epoch(self, epoch: int) -> Dict[str, float]:
        """验证一个epoch"""
        self.logger.info(f"开始验证epoch {epoch}")
        
        # 这里应该实现具体的验证逻辑
        metrics = {
            'val_loss': 0.0,
            'val_accuracy': 0.0,
            'novel_class_acc': 0.0,
            'nmi': 0.0,
            'ari': 0.0
        }
        
        return metrics
    
    def save_checkpoint(self, epoch: int, metrics: Dict[str, float], 
                       is_best: bool = False) -> None:
        """保存检查点"""
        checkpoint = {
            'epoch': epoch,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'scheduler_state_dict': self.scheduler.state_dict(),
            'metrics': metrics,
            'config': self.config
        }
        
        save_dir = Path(self.config['checkpoint']['save_dir'])
        save_dir.mkdir(parents=True, exist_ok=True)
        
        # 保存当前检查点
        torch.save(checkpoint, save_dir / f'checkpoint_epoch_{epoch}.pth')
        
        # 保存最佳检查点
        if is_best:
            torch.save(checkpoint, save_dir / 'best_model.pth')
            self.logger.info(f"保存最佳模型 (epoch {epoch})")
        
        # 保存最新检查点
        torch.save(checkpoint, save_dir / 'latest.pth')
    
    def train(self) -> None:
        """主训练循环"""
        self.logger.info("开始训练ConceptGCD模型")
        
        best_metric = 0.0
        
        for epoch in range(1, self.config['training']['epochs'] + 1):
            # 训练
            train_metrics = self.train_epoch(epoch)
            
            # 验证
            if epoch % self.config['training']['eval_freq'] == 0:
                val_metrics = self.validate_epoch(epoch)
            else:
                val_metrics = {}
            
            # 合并指标
            all_metrics = {**train_metrics, **val_metrics}
            
            # 记录日志
            self.log_metrics(epoch, all_metrics)
            
            # 保存检查点
            is_best = val_metrics.get('val_accuracy', 0.0) > best_metric
            if is_best:
                best_metric = val_metrics.get('val_accuracy', 0.0)
            
            if epoch % self.config['training']['save_freq'] == 0:
                self.save_checkpoint(epoch, all_metrics, is_best)
        
        self.logger.info("训练完成!")
        
        if self.writer:
            self.writer.close()
    
    def log_metrics(self, epoch: int, metrics: Dict[str, float]) -> None:
        """记录指标"""
        # 控制台和文件日志
        metric_str = " | ".join([f"{k}: {v:.4f}" for k, v in metrics.items()])
        self.logger.info(f"Epoch {epoch} | {metric_str}")
        
        # Tensorboard日志
        if self.writer:
            for key, value in metrics.items():
                self.writer.add_scalar(key, value, epoch)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='ConceptGCD训练脚本')
    parser.add_argument('--config', type=str, required=True, help='配置文件路径')
    parser.add_argument('--output-dir', type=str, default='outputs', help='输出目录')
    parser.add_argument('--device', type=str, default='cuda', help='设备类型')
    parser.add_argument('--num-workers', type=int, default=4, help='数据加载器工作进程数')
    parser.add_argument('--task-id', type=int, help='任务ID（用于数组作业）')
    parser.add_argument('--hyperopt-mode', action='store_true', help='超参数优化模式')
    
    args = parser.parse_args()
    
    # 获取分布式训练信息
    rank = int(os.environ.get('LOCAL_RANK', 0))
    world_size = int(os.environ.get('WORLD_SIZE', 1))
    
    # 设置分布式训练
    setup_distributed(rank, world_size)
    
    try:
        # 设置日志
        logger = setup_logging(args.output_dir, rank)
        
        if rank == 0:
            logger.info("=== ConceptGCD训练开始 ===")
            logger.info(f"配置文件: {args.config}")
            logger.info(f"输出目录: {args.output_dir}")
            logger.info(f"设备: {args.device}")
            logger.info(f"分布式: rank={rank}, world_size={world_size}")
        
        # 加载配置
        config = load_config(args.config)
        
        # 更新配置中的设备信息
        config['system']['device'] = args.device
        config['dataset']['dataloader']['num_workers'] = args.num_workers
        
        # 获取Slurm信息
        slurm_info = get_slurm_info()
        
        if rank == 0:
            logger.info("Slurm作业信息:")
            for key, value in slurm_info.items():
                logger.info(f"  {key}: {value}")
            
            # 保存实验信息
            save_experiment_info(args.output_dir, config, slurm_info)
        
        # 创建训练器并开始训练
        trainer = ConceptGCDTrainer(config, logger)
        trainer.train()
        
        if rank == 0:
            logger.info("=== 训练完成 ===")
    
    finally:
        # 清理分布式训练
        cleanup_distributed()


if __name__ == "__main__":
    main()