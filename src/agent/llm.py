from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Callable, Mapping, Sequence


DEFAULT_VOLCENGINE_BASE_URL = "https://ark.cn-beijing.volces.com/api/coding/v3"
DEFAULT_VOLCENGINE_MODEL = "glm-5.2"
DEFAULT_DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEFAULT_DEEPSEEK_MODEL = "deepseek-v4-flash"


@dataclass(frozen=True)
class LLMSettings:
    provider: str
    base_url: str
    api_key: str
    model: str
    temperature: float = 0.1

    @classmethod
    def from_mapping(cls, source: Mapping[str, Any] | None = None) -> "LLMSettings":
        data = source or os.environ
        provider = str(data.get("LLM_PROVIDER") or "volcengine_ark")
        if provider not in {"volcengine_ark", "deepseek"}:
            raise ValueError(f"Unsupported LLM_PROVIDER: {provider}")

        if provider == "deepseek":
            return cls(
                provider=provider,
                base_url=str(data.get("DEEPSEEK_BASE_URL") or DEFAULT_DEEPSEEK_BASE_URL),
                api_key=str(data.get("DEEPSEEK_API_KEY") or ""),
                model=str(data.get("DEEPSEEK_MODEL") or DEFAULT_DEEPSEEK_MODEL),
                temperature=float(data.get("MODEL_TEMPERATURE") or 0.1),
            )

        return cls(
            provider=provider,
            base_url=str(data.get("VOLCENGINE_ARK_BASE_URL") or DEFAULT_VOLCENGINE_BASE_URL),
            api_key=str(data.get("VOLCENGINE_ARK_API_KEY") or ""),
            model=str(data.get("VOLCENGINE_ARK_MODEL") or DEFAULT_VOLCENGINE_MODEL),
            temperature=float(data.get("MODEL_TEMPERATURE") or 0.1),
        )


class OpenAICompatibleProvider:
    """Shared provider for OpenAI-compatible chat-completion APIs."""

    missing_key_name = "API key"

    def __init__(
        self,
        settings: LLMSettings | None = None,
        client_factory: Callable[..., Any] | None = None,
    ) -> None:
        self.settings = settings or LLMSettings.from_mapping()
        if not self.settings.api_key:
            raise ValueError(f"{self.missing_key_name} is required")

        if client_factory is None:
            from openai import OpenAI

            client_factory = OpenAI
        self.client = client_factory(
            base_url=self.settings.base_url,
            api_key=self.settings.api_key,
        )

    def complete(
        self,
        messages: Sequence[dict[str, str]],
        *,
        temperature: float | None = None,
        max_tokens: int = 1500,
    ) -> str:
        response = self.client.chat.completions.create(
            model=self.settings.model,
            messages=list(messages),
            temperature=self.settings.temperature if temperature is None else temperature,
            max_tokens=max_tokens,
        )
        return (response.choices[0].message.content or "").strip()


class VolcengineArkProvider(OpenAICompatibleProvider):
    """OpenAI-compatible provider for Volcengine Ark Coding Plan."""

    missing_key_name = "VOLCENGINE_ARK_API_KEY"


class DeepSeekProvider(OpenAICompatibleProvider):
    """OpenAI-compatible provider for DeepSeek fallback models."""

    missing_key_name = "DEEPSEEK_API_KEY"
