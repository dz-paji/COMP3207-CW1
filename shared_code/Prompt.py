import json

class Prompt:
    def __init__(self, name, lang, text):
        self.id = 0
        self.name = name
        self.texts = []
        self.texts.append({"language": lang, "text": text})

    def from_json(self, result):
        ''' import json formatted prompt texts
        '''
        for i in result:
            self.texts.append({"language": i["to"], "text": i["text"]})

        return self
    
    def to_dict(self):
        ''' export as dict
        '''
        return {"id": self.id, "username": self.name, "texts": self.texts}
    
    def from_dict(self, prompt):
        ''' import from dict
        '''
        self.id = prompt["id"]
        self.name = prompt["username"]
        self.texts = prompt["texts"]
        
        return self
    
    def get_en(self):
        ''' return a list fo english prompt text separated by space
        '''
        text = ""
        for i in self.texts:
            if i["language"] == "en":
                text = i["text"]
                break
            
        text = text.split(" ")
            
        return text
    
    def get_text_by_lang(self, lang):
        ''' return prompt text by lang code
        '''
        text = ""
        for i in self.texts:
            if i["language"] == lang:
                text = i["text"]
                break
            
        return text