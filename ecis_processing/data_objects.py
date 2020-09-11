class Note:
    def __init__(self, note_type, date, note_text):
        self.note_type: str = note_type
        self.date = date
        self.note_text: str = note_text

    def __str__(self):
        wordcount = len(self.note_text.split())
        return f"{self.date:%Y-%m-%d}: {self.note_type} Note ({wordcount} words)"

    def __repr__(self):
        return str(self)


if __name__ == "__main__":
    note = Note("radiology", "2020-09-07", "M")
    print(note)