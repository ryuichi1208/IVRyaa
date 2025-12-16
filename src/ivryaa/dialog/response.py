"""Response generation module"""

from ivryaa.dialog.intent import Intent, IntentType
from ivryaa.metrics import get_all_metrics
from ivryaa.metrics.cpu import CPUCollector
from ivryaa.metrics.disk import DiskCollector
from ivryaa.metrics.memory import MemoryCollector
from ivryaa.metrics.network import NetworkCollector


class ResponseGenerator:
    """Class for generating responses based on intent"""

    def generate(self, intent: Intent) -> str:
        """Generate response for the given intent"""
        handlers = {
            IntentType.GET_CPU: self._handle_cpu,
            IntentType.GET_MEMORY: self._handle_memory,
            IntentType.GET_DISK: self._handle_disk,
            IntentType.GET_NETWORK: self._handle_network,
            IntentType.GET_ALL: self._handle_all,
            IntentType.HELP: self._handle_help,
            IntentType.EXIT: self._handle_exit,
            IntentType.UNKNOWN: self._handle_unknown,
        }

        handler = handlers.get(intent.type, self._handle_unknown)
        return handler()

    def _handle_cpu(self) -> str:
        cpu = CPUCollector().collect()
        return f"現在のCPU使用率は{cpu:.1f}パーセントです。"

    def _handle_memory(self) -> str:
        memory = MemoryCollector().collect()
        return f"現在のメモリ使用率は{memory:.1f}パーセントです。"

    def _handle_disk(self) -> str:
        disk = DiskCollector().collect()
        return f"現在のディスク使用率は{disk:.1f}パーセントです。"

    def _handle_network(self) -> str:
        net = NetworkCollector().collect()
        return (
            f"ネットワーク統計です。"
            f"送信量は{net['bytes_sent_mb']:.1f}メガバイト、"
            f"受信量は{net['bytes_recv_mb']:.1f}メガバイトです。"
        )

    def _handle_all(self) -> str:
        metrics = get_all_metrics()
        return (
            f"システム全体の状況をお伝えします。"
            f"CPU使用率は{metrics['cpu']:.1f}パーセント、"
            f"メモリ使用率は{metrics['memory']:.1f}パーセント、"
            f"ディスク使用率は{metrics['disk']:.1f}パーセントです。"
        )

    def _handle_help(self) -> str:
        return (
            "次のことができます。"
            "CPUの状態、メモリの状態、ディスクの状態、ネットワークの状態を確認できます。"
            "また、全部と言えばすべてのメトリクスをお伝えします。"
            "終了と言えばセッションを終了します。"
        )

    def _handle_exit(self) -> str:
        return "セッションを終了します。ご利用ありがとうございました。"

    def _handle_unknown(self) -> str:
        return "すみません、よく聞き取れませんでした。もう一度お願いします。"
