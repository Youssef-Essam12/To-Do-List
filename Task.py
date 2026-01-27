from pydantic import BaseModel

class TaskModel(BaseModel):
    title: str
    state: str = "Not Started"

class Task():
    def __init__(self, title="NULL TASK", id=0, state="Not Started", done=False):
        self.title = title
        self.state = state
        self.done = done
        self.id = id

    def to_json(self):
        return {
            "Title": self.title,
            "ID": self.id,
            "State": self.state,
            "Done": self.done
        }