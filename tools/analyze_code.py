#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ConceptGCD代码分析工具
Code Analysis Tool for ConceptGCD Project

此工具用于分析Slurm框架下的机器学习项目代码结构、逻辑和组织方式。
This tool analyzes code structure, logic, and organization of ML projects under Slurm framework.
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import yaml


@dataclass
class CodeAnalysisResult:
    """代码分析结果数据结构"""
    project_name: str
    total_files: int
    python_files: int
    slurm_scripts: int
    config_files: int
    directory_structure: Dict[str, Any]
    slurm_patterns: List[str]
    dependencies: List[str]
    analysis_summary: Dict[str, Any]


class ConceptGCDAnalyzer:
    """ConceptGCD项目代码分析器"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.analysis_result = CodeAnalysisResult(
            project_name=self.project_root.name,
            total_files=0,
            python_files=0,
            slurm_scripts=0,
            config_files=0,
            directory_structure={},
            slurm_patterns=[],
            dependencies=[],
            analysis_summary={}
        )
    
    def analyze_project_structure(self) -> Dict[str, Any]:
        """分析项目整体结构"""
        print("🔍 分析项目结构 (Analyzing project structure)...")
        
        structure = {}
        for root, dirs, files in os.walk(self.project_root):
            # 跳过隐藏目录和常见的忽略目录
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules']]
            
            rel_path = os.path.relpath(root, self.project_root)
            if rel_path == '.':
                rel_path = 'root'
            
            structure[rel_path] = {
                'directories': dirs,
                'files': files,
                'file_count': len(files)
            }
            
            self.analysis_result.total_files += len(files)
            
            # 分类文件类型
            for file in files:
                if file.endswith('.py'):
                    self.analysis_result.python_files += 1
                elif file.endswith(('.sh', '.slurm', '.sbatch')):
                    self.analysis_result.slurm_scripts += 1
                elif file.endswith(('.yaml', '.yml', '.json', '.cfg', '.ini')):
                    self.analysis_result.config_files += 1
        
        self.analysis_result.directory_structure = structure
        return structure
    
    def analyze_slurm_scripts(self) -> List[Dict[str, Any]]:
        """分析Slurm脚本"""
        print("⚡ 分析Slurm脚本 (Analyzing Slurm scripts)...")
        
        slurm_files = []
        slurm_patterns = set()
        
        for root, dirs, files in os.walk(self.project_root):
            for file in files:
                if file.endswith(('.sh', '.slurm', '.sbatch')):
                    file_path = Path(root) / file
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        analysis = self._analyze_slurm_script_content(content, file_path)
                        slurm_files.append(analysis)
                        
                        # 收集常见模式
                        if 'array' in content.lower():
                            slurm_patterns.add('array_jobs')
                        if 'dependency' in content.lower():
                            slurm_patterns.add('job_dependencies')
                        if 'gres=gpu' in content:
                            slurm_patterns.add('gpu_usage')
                        if 'nodes=' in content and 'nodes=1' not in content:
                            slurm_patterns.add('multi_node')
                            
                    except Exception as e:
                        print(f"警告: 无法读取文件 {file_path}: {e}")
        
        self.analysis_result.slurm_patterns = list(slurm_patterns)
        return slurm_files
    
    def _analyze_slurm_script_content(self, content: str, file_path: Path) -> Dict[str, Any]:
        """分析单个Slurm脚本内容"""
        sbatch_params = {}
        
        # 提取SBATCH参数
        sbatch_pattern = r'#SBATCH\s+--(\S+)(?:=(\S+))?'
        matches = re.findall(sbatch_pattern, content)
        
        for param, value in matches:
            sbatch_params[param] = value if value else True
        
        # 分析资源配置
        resource_analysis = {
            'cpu_request': sbatch_params.get('cpus-per-task', 'not_specified'),
            'memory_request': sbatch_params.get('mem', 'not_specified'),
            'gpu_request': sbatch_params.get('gres', 'not_specified'),
            'time_limit': sbatch_params.get('time', 'not_specified'),
            'node_count': sbatch_params.get('nodes', 'not_specified')
        }
        
        # 检查环境设置
        has_module_load = 'module load' in content
        has_conda_activate = 'conda activate' in content or 'source activate' in content
        has_env_vars = 'export' in content
        
        return {
            'file_path': str(file_path),
            'file_name': file_path.name,
            'sbatch_parameters': sbatch_params,
            'resource_analysis': resource_analysis,
            'environment_setup': {
                'module_loading': has_module_load,
                'conda_environment': has_conda_activate,
                'environment_variables': has_env_vars
            },
            'script_type': self._classify_slurm_script(content, file_path.name)
        }
    
    def _classify_slurm_script(self, content: str, filename: str) -> str:
        """分类Slurm脚本类型"""
        content_lower = content.lower()
        filename_lower = filename.lower()
        
        if 'array' in content_lower or 'array' in filename_lower:
            return 'array_job'
        elif 'train' in content_lower or 'train' in filename_lower:
            return 'training_job'
        elif 'eval' in content_lower or 'test' in filename_lower:
            return 'evaluation_job'
        elif 'preprocess' in content_lower or 'preprocess' in filename_lower:
            return 'preprocessing_job'
        elif 'submit' in filename_lower:
            return 'job_submission'
        else:
            return 'general_job'
    
    def analyze_python_code(self) -> List[Dict[str, Any]]:
        """分析Python代码"""
        print("🐍 分析Python代码 (Analyzing Python code)...")
        
        python_files = []
        all_imports = set()
        
        for root, dirs, files in os.walk(self.project_root):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__']]
            
            for file in files:
                if file.endswith('.py'):
                    file_path = Path(root) / file
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        analysis = self._analyze_python_file(content, file_path)
                        python_files.append(analysis)
                        all_imports.update(analysis['imports'])
                        
                    except Exception as e:
                        print(f"警告: 无法读取Python文件 {file_path}: {e}")
        
        self.analysis_result.dependencies = list(all_imports)
        return python_files
    
    def _analyze_python_file(self, content: str, file_path: Path) -> Dict[str, Any]:
        """分析单个Python文件"""
        # 提取导入语句
        import_pattern = r'(?:from\s+(\S+)\s+import|import\s+(\S+))'
        matches = re.findall(import_pattern, content)
        imports = []
        for match in matches:
            module = match[0] if match[0] else match[1]
            imports.append(module.split('.')[0])  # 只取顶级模块名
        
        # 分析文件类型和用途
        file_type = self._classify_python_file(content, file_path.name)
        
        # 代码复杂度简单评估
        lines = content.split('\n')
        code_lines = [line for line in lines if line.strip() and not line.strip().startswith('#')]
        
        return {
            'file_path': str(file_path),
            'file_name': file_path.name,
            'file_type': file_type,
            'imports': list(set(imports)),
            'line_count': len(lines),
            'code_line_count': len(code_lines),
            'has_main': 'if __name__ == "__main__"' in content,
            'has_argparse': 'argparse' in content,
            'has_config': any(word in content.lower() for word in ['config', 'yaml', 'json'])
        }
    
    def _classify_python_file(self, content: str, filename: str) -> str:
        """分类Python文件类型"""
        content_lower = content.lower()
        filename_lower = filename.lower()
        
        # 基于文件名判断
        if filename_lower in ['train.py', 'training.py']:
            return 'training_script'
        elif filename_lower in ['eval.py', 'evaluate.py', 'test.py']:
            return 'evaluation_script'
        elif filename_lower in ['config.py', 'configs.py']:
            return 'configuration'
        elif filename_lower in ['main.py', '__main__.py']:
            return 'main_entry'
        elif 'model' in filename_lower:
            return 'model_definition'
        elif 'dataset' in filename_lower or 'data' in filename_lower:
            return 'data_handling'
        elif 'util' in filename_lower or 'helper' in filename_lower:
            return 'utility'
        
        # 基于内容判断
        if 'class' in content and 'torch.nn' in content:
            return 'model_definition'
        elif 'dataset' in content_lower and 'torch.utils.data' in content:
            return 'data_handling'
        elif 'def train' in content_lower or 'def main' in content_lower:
            return 'script'
        else:
            return 'general'
    
    def analyze_configuration_files(self) -> List[Dict[str, Any]]:
        """分析配置文件"""
        print("⚙️ 分析配置文件 (Analyzing configuration files)...")
        
        config_files = []
        
        for root, dirs, files in os.walk(self.project_root):
            for file in files:
                if file.endswith(('.yaml', '.yml', '.json', '.cfg', '.ini', 'requirements.txt')):
                    file_path = Path(root) / file
                    try:
                        analysis = self._analyze_config_file(file_path)
                        config_files.append(analysis)
                    except Exception as e:
                        print(f"警告: 无法分析配置文件 {file_path}: {e}")
        
        return config_files
    
    def _analyze_config_file(self, file_path: Path) -> Dict[str, Any]:
        """分析单个配置文件"""
        config_type = 'unknown'
        content_summary = {}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if file_path.suffix in ['.yaml', '.yml']:
                config_type = 'yaml'
                try:
                    data = yaml.safe_load(content)
                    if isinstance(data, dict):
                        content_summary = {
                            'keys': list(data.keys()),
                            'nested_structure': len([k for k, v in data.items() if isinstance(v, dict)]) > 0
                        }
                except:
                    content_summary = {'parse_error': True}
            
            elif file_path.suffix == '.json':
                config_type = 'json'
                try:
                    data = json.loads(content)
                    if isinstance(data, dict):
                        content_summary = {
                            'keys': list(data.keys()),
                            'nested_structure': len([k for k, v in data.items() if isinstance(v, dict)]) > 0
                        }
                except:
                    content_summary = {'parse_error': True}
            
            elif file_path.name == 'requirements.txt':
                config_type = 'requirements'
                packages = [line.strip().split('==')[0].split('>=')[0].split('<=')[0] 
                           for line in content.split('\n') if line.strip() and not line.startswith('#')]
                content_summary = {
                    'package_count': len(packages),
                    'packages': packages[:10]  # 只显示前10个
                }
        
        except Exception as e:
            content_summary = {'read_error': str(e)}
        
        return {
            'file_path': str(file_path),
            'file_name': file_path.name,
            'config_type': config_type,
            'content_summary': content_summary
        }
    
    def generate_analysis_summary(self) -> Dict[str, Any]:
        """生成分析总结"""
        print("📊 生成分析总结 (Generating analysis summary)...")
        
        # 收集所有分析结果
        structure = self.analyze_project_structure()
        slurm_scripts = self.analyze_slurm_scripts()
        python_files = self.analyze_python_code()
        config_files = self.analyze_configuration_files()
        
        # 生成总结
        summary = {
            'project_overview': {
                'name': self.analysis_result.project_name,
                'total_files': self.analysis_result.total_files,
                'python_files': self.analysis_result.python_files,
                'slurm_scripts': self.analysis_result.slurm_scripts,
                'config_files': self.analysis_result.config_files
            },
            'directory_structure': structure,
            'slurm_analysis': {
                'scripts': slurm_scripts,
                'patterns_found': self.analysis_result.slurm_patterns
            },
            'python_analysis': {
                'files': python_files,
                'common_dependencies': self._get_common_dependencies()
            },
            'configuration_analysis': {
                'files': config_files
            },
            'recommendations': self._generate_recommendations()
        }
        
        self.analysis_result.analysis_summary = summary
        return summary
    
    def _get_common_dependencies(self) -> List[str]:
        """获取常见依赖"""
        from collections import Counter
        dep_counter = Counter(self.analysis_result.dependencies)
        return [dep for dep, count in dep_counter.most_common(10)]
    
    def _generate_recommendations(self) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        if self.analysis_result.slurm_scripts == 0:
            recommendations.append("考虑添加Slurm作业脚本以支持集群执行")
        
        if self.analysis_result.config_files == 0:
            recommendations.append("建议添加配置文件来管理实验参数")
        
        if 'gpu_usage' not in self.analysis_result.slurm_patterns:
            recommendations.append("检查是否需要GPU资源配置")
        
        if 'job_dependencies' not in self.analysis_result.slurm_patterns:
            recommendations.append("考虑使用作业依赖来管理多阶段执行")
        
        return recommendations
    
    def save_analysis_report(self, output_path: Optional[str] = None) -> str:
        """保存分析报告"""
        if output_path is None:
            output_path = self.project_root / "analysis_report.json"
        
        summary = self.generate_analysis_summary()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 分析报告已保存到: {output_path}")
        return str(output_path)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='ConceptGCD代码分析工具')
    parser.add_argument('project_path', help='项目根目录路径')
    parser.add_argument('--output', '-o', help='输出报告路径')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.project_path):
        print(f"错误: 项目路径不存在: {args.project_path}")
        sys.exit(1)
    
    print(f"🚀 开始分析项目: {args.project_path}")
    print("=" * 50)
    
    analyzer = ConceptGCDAnalyzer(args.project_path)
    report_path = analyzer.save_analysis_report(args.output)
    
    print("=" * 50)
    print("🎉 分析完成!")
    print(f"📄 报告位置: {report_path}")
    
    # 显示基本统计信息
    result = analyzer.analysis_result
    print(f"\n📊 项目统计:")
    print(f"  - 总文件数: {result.total_files}")
    print(f"  - Python文件: {result.python_files}")
    print(f"  - Slurm脚本: {result.slurm_scripts}")
    print(f"  - 配置文件: {result.config_files}")
    print(f"  - 发现的Slurm模式: {', '.join(result.slurm_patterns) if result.slurm_patterns else '无'}")


if __name__ == "__main__":
    main()