class TextInput:
    def __init__(self, text: str) -> None:
        self.text: str = text

    def update(self, text: str) -> None:
        self.text += text

    def backspace(self) -> None:
        self.text = self.text[0:-1]

    def getText(self) -> str:
        return self.text