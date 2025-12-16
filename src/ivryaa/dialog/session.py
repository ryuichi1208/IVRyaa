"""Session management module"""

from rich.console import Console

from ivryaa.dialog.intent import IntentParser, IntentType
from ivryaa.dialog.response import ResponseGenerator
from ivryaa.utils.logger import logger
from ivryaa.voice import AudioRecorder, SpeechRecognizer, SpeechSynthesizer


class DialogSession:
    """Class for managing voice dialog sessions"""

    def __init__(self) -> None:
        self.recorder = AudioRecorder()
        self.recognizer = SpeechRecognizer()
        self.synthesizer = SpeechSynthesizer()
        self.intent_parser = IntentParser()
        self.response_generator = ResponseGenerator()
        self.console = Console()
        self._running = False

    def run(self) -> None:
        """Run the dialog session"""
        self._running = True
        self._greet()

        while self._running:
            try:
                self._process_turn()
            except Exception as e:
                logger.error(f"Error occurred: {e}")
                self.synthesizer.speak("エラーが発生しました。もう一度お試しください。")

        self._cleanup()

    def _greet(self) -> None:
        """Play greeting message"""
        greeting = "IVRyaaへようこそ。サーバーの状態について音声でお答えします。"
        self.console.print(f"[green]{greeting}[/green]")
        self.synthesizer.speak(greeting)

    def _process_turn(self) -> None:
        """Process one turn of dialog"""
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
        """Release resources"""
        self.recorder.close()
        logger.info("Session ended")
