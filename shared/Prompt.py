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
    
    def from_dict(self, prompt):
        self.id = prompt["id"]
        self.name = prompt["username"]
        self.texts = prompt["texts"]
        
        return self
    
    def get_en(self):
        text = ""
        for i in self.texts:
            if i["language"] == "en":
                text = i["text"]
                break
            
        text = text.split(" ")
            
        return text