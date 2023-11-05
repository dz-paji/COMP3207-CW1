import json

class Prompt:
    def __init__(self, name, lang, text):
        self.id = 0
        self.name = name
        self.texts = []
        self.texts.append({"language": lang, "text": text})

    def from_json(self, result):
        for i in result:
            self.texts.append({"language": i["to"], "text": i["text"]})

        return self
    
    def to_dict(self):
        return {"id": self.id, "username": self.name, "texts": self.texts}