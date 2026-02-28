#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Git 提交前安全检查脚本

在提交代码前运行此脚本，检查是否包含敏感信息
"""
import re
import sys
from pathlib import Path

# 敏感信息模式
SENSITIVE_PATTERNS = [
    (r'password\s*=\s*["\'](?!your-|test-|\$\{)[^"\']+["\']', "明文密码"),
    (r'api[_-]?key\s*=\s*["\'](?!your-|test-|sk-your|\$\{)[^"\']+["\']', "API密钥"),
    (r'secret\s*=\s*["\'](?!your-|test-|\$\{)[^"\']+["\']', "密钥"),
]

# 需要检查的文件扩展名
CHECK_EXTENSIONS = {'.py', '.json', '.md', '.yaml', '.yml', '.env', '.sh', '.bat'}

# 排除的目录
EXCLUDE_DIRS = {'.git', '__pycache__', 'node_modules', 'venv', 'env', '.venv'}

def check_file(file_path: Path) -> list:
    """检查单个文件是否包含敏感信息"""
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        for pattern, description in SENSITIVE_PATTERNS:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                # 跳过注释行
                line_start = content.rfind('\n', 0, match.start()) + 1
                line = content[line_start:content.find('\n', match.start())]
                if line.strip().startswith('#'):
                    continue
                    
                line_num = content[:match.start()].count('\n') + 1
                issues.append({
                    'file': str(file_path),
                    'line': line_num,
                    'type': description,
                    'content': match.group()[:50]
                })
    except Exception as e:
        print(f"警告: 无法读取文件 {file_path}: {e}")
    
    return issues

def check_repository(repo_path: Path) -> list:
    """检查整个仓库"""
    all_issues = []
    
    for file_path in repo_path.rglob('*'):
        # 跳过目录
        if file_path.is_dir():
            continue
            
        # 跳过排除的目录
        if any(excluded in file_path.parts for excluded in EXCLUDE_DIRS):
            continue
            
        # 只检查指定扩展名的文件
        if file_path.suffix not in CHECK_EXTENSIONS:
            continue
            
        issues = check_file(file_path)
        all_issues.extend(issues)
    
    return all_issues

def main():
    """主函数"""
    print("=" * 80)
    print("Text2SQL 安全检查")
    print("=" * 80)
    
    repo_path = Path(__file__).parent.parent
    print(f"\n检查目录: {repo_path}")
    
    issues = check_repository(repo_path)
    
    if not issues:
        print("\n[OK] 未发现敏感信息，可以安全提交")
        return 0
    
    print(f"\n[WARN] 发现 {len(issues)} 个潜在的安全问题：\n")
    
    for i, issue in enumerate(issues, 1):
        print(f"{i}. {issue['file']}:{issue['line']}")
        print(f"   类型: {issue['type']}")
        print(f"   内容: {issue['content']}...")
        print()
    
    print("=" * 80)
    print("请修复以上问题后再提交代码")
    print("=" * 80)
    
    return 1

if __name__ == "__main__":
    sys.exit(main())
