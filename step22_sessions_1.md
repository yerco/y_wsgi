# Sessions

## Typical of a Memento implementation
```python
# Originator
class TextEditor:
    def __init__(self, content=""):
        self._content = content
        self._caretaker = Caretaker()
        # Save the initial state
        self._caretaker.keep(self.create_memento())

    def get_content(self):
        return self._content

    def write(self, text):
        self._content += text
        self._caretaker.keep(self.create_memento())

    def create_memento(self):
        return Memento(self._content)

    def get_from_memento(self, memento):
        if memento:
            return memento.get()
        return self._content

    def undo(self):
        self._content = self.get_from_memento(self._caretaker.retrieve())

    def redo(self):
        self._content = self.get_from_memento(self._caretaker.redo())
    


class Memento:
    def __init__(self, content):
        self._content = content

    def get(self):
        return self._content


# Caretaker
class Caretaker:
    def __init__(self):
        self._mementos = []
        self._redo_mementos = []

    def keep(self, content):
        self._mementos.append(content)
        self._redo_mementos.clear()  # Clear redo stack on new action

    def retrieve(self):
        if len(self._mementos) > 1:
            self._redo_mementos.append(self._mementos.pop())
            return self._mementos[-1]
        elif self._mementos:
            return self._mementos[0]
        return None

    def redo(self):
        if self._redo_mementos:
            memento = self._redo_mementos.pop()
            self._mementos.append(memento)
            return memento
        return None


editor = TextEditor()

editor.write("uno")
print(editor.get_content())

editor.write(" dos")
print(editor.get_content())

editor.write(" tres")
print(editor.get_content())

editor.undo()
print(editor.get_content())

editor.undo()
print(editor.get_content())

editor.redo()
print(editor.get_content())

editor.redo()
print(editor.get_content())
```
Output
```bash
uno
uno dos
uno dos tres
uno dos
uno
uno dos
uno dos tres
```

We will make this resemble this structure to implement sessions.

## Example of a typical session data structure
```json
{
  "id": "abc123",
  "user_id": "user456",
  "created_at": "2023-07-14T12:34:56Z",
  "last_accessed": "2023-07-14T13:34:56Z",
  "expiry": "2023-07-14T14:34:56Z",
  "ip_address": "192.168.1.1",
  "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
  "data": {
    "cart": {
      "items": [
        {"product_id": "prod123", "quantity": 2},
        {"product_id": "prod456", "quantity": 1}
      ]
    },
    "csrf_token": "def789"
  }
}
```


