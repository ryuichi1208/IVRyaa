"""セッション管理モジュール"""

from rich.console import Console

from ivryaa.dialog.intent import IntentParser, IntentType
from ivryaa.dialog.response import ResponseGenerator
from ivryaa.utils.logger import logger
from ivryaa.voice import AudioRecorder, SpeechRecognizer, SpeechSynthesizer


class DialogSession:
    """音声対話セッションを管理するクラス"""

    def __init__(self) -> None:
        self.recorder = AudioRecorder()
        self.recognizer = SpeechRecognizer()
        self.synthesizer = SpeechSynthesizer()
        self.intent_parser = IntentParser()
        self.response_generator = ResponseGenerator()
        self.console = Console()
        self._running = False

    def run(self) -> None:
        """対話セッションを実行する"""
        self._running = True
        self._greet()

        while self._running:
            try:
                self._process_turn()
            except Exception as e:
                logger.error(f"エラーが発生しました: {e}")
                self.synthesizer.speak("エラーが発生しました。もう一度お試しください。")

        self._cleanup()

    def _greet(self) -> None:
        """挨拶メッセージを再生"""
        greeting = "IVRyaaへようこそ。サーバーの状態について音声でお答えします。"
        self.console.print(f"[green]{greeting}[/green]")
        self.synthesizer.speak(greeting)

    def _process_turn(self) -> None:
        """1ターンの対話を処理"""
        self.console.print("\n[cyan]話しかけてください...[/cyan]")

        audio_data = self.recorder.record(duration=5.0)
        text = self.recognizer.transcribe(audio_data)

        self.console.print(f"[blue]認識結果:[/blue] {text}")

        intent = self.intent_parser.parse(text)
        response = self.response_generator.generate(intent)

        self.console.print(f"[green]応答:[/green] {response}")
        self.synthesizer.speak(response)

        if intent.type == IntentType.EXIT:
            self._running = False

    def _cleanup(self) -> None:
        """リソースを解放"""
        self.recorder.close()
        logger.info("セッションを終了しました")
