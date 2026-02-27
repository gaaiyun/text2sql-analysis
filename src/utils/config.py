#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
配置管理模块

提供统一的配置加载功能，支持环境变量和配置文件两种方式。
确保敏感信息（如密码、API Key）不硬编码在代码中。

使用方法:
    from utils.config import Config

    # 加载配置
    config = Config.load()

    # 访问配置
    db_config = config.get_database_config()
    api_key = config.get_api_key()
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional


class Config:
    """配置管理类"""

    _instance: Optional['Config'] = None
    _config_data: Dict[str, Any] = {}
    _env_file: str = ".env"

    def __init__(self):
        """初始化配置"""
        self._load_env_file()
        self._load_config_file()

    @classmethod
    def load(cls) -> 'Config':
        """加载配置单例"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def reload(cls) -> 'Config':
        """重新加载配置"""
        cls._instance = cls()
        return cls._instance

    def _load_env_file(self) -> None:
        """加载 .env 文件"""
        env_path = Path(self._env_file)
        if not env_path.exists():
            # 尝试从父目录加载
            env_path = Path(__file__).parent.parent.parent / self._env_file

        if env_path.exists():
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # 跳过注释和空行
                    if not line or line.startswith('#'):
                        continue
                    # 解析 KEY=VALUE
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        # 移除引号
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        elif value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]
                        # 设置环境变量
                        os.environ[key] = value

    def _load_config_file(self) -> None:
        """加载 config.json 文件"""
        config_paths = [
            Path("config.json"),
            Path(__file__).parent.parent.parent / "config.json",
        ]

        for config_path in config_paths:
            if config_path.exists():
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        self._config_data = json.load(f)
                    break
                except (json.JSONDecodeError, IOError) as e:
                    print(f"[WARN] 加载配置文件失败：{e}")

    def _get_env_or_default(self, key: str, default: Any = None) -> Any:
        """获取环境变量或默认值"""
        value = os.environ.get(key)
        if value is None:
            if default is not None:
                return default
            raise ValueError(f"环境变量 {key} 未设置，请在 .env 文件中配置")
        return value

    def _get_nested(self, data: Dict, keys: list, default: Any = None) -> Any:
        """获取嵌套字典值"""
        for key in keys:
            if isinstance(data, dict) and key in data:
                data = data[key]
            else:
                return default
        return data

    def get_api_key(self, provider: str = "dashscope") -> str:
        """获取 API Key

        Args:
            provider: API 提供商，支持 'dashscope', 'kiro'

        Returns:
            API Key 字符串
        """
        # 优先从环境变量获取
        env_keys = {
            'dashscope': 'DASHSCOPE_API_KEY',
            'kiro': 'KIRO_API_KEY',
            'openai': 'OPENAI_API_KEY',
        }

        env_key = env_keys.get(provider, 'DASHSCOPE_API_KEY')
        if env_key in os.environ:
            return os.environ[env_key]

        # 从配置文件获取（支持 ${VAR} 格式）
        config_key = self._get_nested(self._config_data, [provider, 'api_key'], '')
        if config_key.startswith('${') and config_key.endswith('}'):
            var_name = config_key[2:-1]
            return os.environ.get(var_name, '')
        return config_key

    def get_kiro_config(self) -> Dict[str, str]:
        """获取 Kiro API 配置"""
        return {
            'base_url': os.environ.get('KIRO_BASE_URL', 'https://kiro.singforge.dpdns.org:11128/v1'),
            'api_key': self.get_api_key('kiro'),
            'model': os.environ.get('KIRO_MODEL', 'claude-opus-4.6')
        }

    def get_database_config(self, scenario: str = "scenario_1_3") -> Dict[str, Any]:
        """获取数据库配置

        Args:
            scenario: 场景名称
                - scenario_1_3: 场景 1-3 (Gaaiyun 数据库)
                - scenario_4_5: 场景 4-5 (gaaiyun_2 数据库)

        Returns:
            数据库配置字典
        """
        # 从环境变量获取
        db_configs = {
            'scenario_1_3': {
                'host': os.environ.get('DB_HOST_SCENARIO_1_3', os.environ.get('DB_HOST', 'localhost')),
                'port': int(os.environ.get('DB_PORT', '3306')),
                'user': os.environ.get('DB_USER_SCENARIO_1_3', os.environ.get('DB_USER', 'root')),
                'password': os.environ.get('DB_PASSWORD_SCENARIO_1_3', os.environ.get('DB_PASSWORD', '')),
                'database': os.environ.get('DB_NAME_SCENARIO_1_3', os.environ.get('DB_NAME', ''))
            },
            'scenario_4_5': {
                'host': os.environ.get('DB_HOST_SCENARIO_4_5', os.environ.get('DB_HOST', 'localhost')),
                'port': int(os.environ.get('DB_PORT', '3306')),
                'user': os.environ.get('DB_USER_SCENARIO_4_5', os.environ.get('DB_USER', 'root')),
                'password': os.environ.get('DB_PASSWORD_SCENARIO_4_5', os.environ.get('DB_PASSWORD', '')),
                'database': os.environ.get('DB_NAME_SCENARIO_4_5', os.environ.get('DB_NAME', ''))
            }
        }

        if scenario in db_configs:
            return db_configs[scenario]

        # 从配置文件获取
        db_config = self._get_nested(self._config_data, ['database'], {})
        if db_config:
            return {
                'host': db_config.get('host', 'localhost'),
                'port': int(db_config.get('port', 3306)),
                'user': db_config.get('user', 'root'),
                'password': db_config.get('password', ''),
                'database': db_config.get('database', '')
            }

        return db_configs.get(scenario, {})

    def get_model_config(self) -> Dict[str, Any]:
        """获取模型配置"""
        return {
            'name': os.environ.get('MODEL_NAME', self._get_nested(self._config_data, ['model', 'name'], 'qwen3.5-plus')),
            'temperature': float(os.environ.get('MODEL_TEMPERATURE', self._get_nested(self._config_data, ['model', 'temperature'], 0.1)))
        }

    def validate(self) -> tuple[bool, list]:
        """验证配置完整性

        Returns:
            (是否有效，错误信息列表)
        """
        errors = []

        # 检查必需的 API Key
        if not self.get_api_key('dashscope') and not self.get_api_key('kiro'):
            errors.append("缺少 API Key，请配置 DASHSCOPE_API_KEY 或 KIRO_API_KEY")

        # 检查数据库配置
        for scenario in ['scenario_1_3', 'scenario_4_5']:
            db_config = self.get_database_config(scenario)
            if not db_config.get('host'):
                errors.append(f"场景 {scenario} 缺少数据库 host 配置")
            if not db_config.get('database'):
                errors.append(f"场景 {scenario} 缺少数据库 database 配置")

        return len(errors) == 0, errors


# 便捷函数
def load_config() -> Config:
    """加载配置"""
    return Config.load()


def get_api_key(provider: str = "dashscope") -> str:
    """获取 API Key"""
    return Config.load().get_api_key(provider)


def get_database_config(scenario: str = "scenario_1_3") -> Dict[str, Any]:
    """获取数据库配置"""
    return Config.load().get_database_config(scenario)


def get_kiro_config() -> Dict[str, str]:
    """获取 Kiro 配置"""
    return Config.load().get_kiro_config()
