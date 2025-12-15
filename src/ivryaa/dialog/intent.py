"""意図解析モジュール"""

from dataclasses import dataclass
from enum import Enum


class IntentType(Enum):
    """意図の種類"""

    GET_CPU = "get_cpu"
    GET_MEMORY = "get_memory"
    GET_DISK = "get_disk"
    GET_NETWORK = "get_network"
    GET_ALL = "get_all"
    HELP = "help"
    EXIT = "exit"
    UNKNOWN = "unknown"


@dataclass
class Intent:
    """解析された意図"""

    type: IntentType
    confidence: float
    raw_text: str


class IntentParser:
    """ユーザーの発話から意図を解析するクラス"""

    KEYWORDS: dict[IntentType, list[str]] = {
        IntentType.GET_CPU: ["cpu", "シーピーユー", "プロセッサ", "処理"],
        IntentType.GET_MEMORY: ["メモリ", "memory", "ram", "ラム"],
        IntentType.GET_DISK: ["ディスク", "disk", "ストレージ", "容量"],
        IntentType.GET_NETWORK: ["ネットワーク", "network", "通信", "ネット"],
        IntentType.GET_ALL: ["全部", "すべて", "all", "全体", "まとめて"],
        IntentType.HELP: ["ヘルプ", "help", "使い方", "何ができる"],
        IntentType.EXIT: ["終了", "exit", "quit", "終わり", "さようなら", "バイバイ"],
    }

    def parse(self, text: str) -> Intent:
        """テキストから意図を解析する"""
        text_lower = text.lower()

        for intent_type, keywords in self.KEYWORDS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return Intent(
                        type=intent_type,
                        confidence=0.8,
                        raw_text=text,
                    )

        return Intent(
            type=IntentType.UNKNOWN,
            confidence=0.0,
            raw_text=text,
        )
