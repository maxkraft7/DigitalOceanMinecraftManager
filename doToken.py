from os import path

class token:
    @staticmethod
    def get(filename):
        if not path.exists(filename):
            raise ValueError("API_KEY nicht gefunden!") # throw an error if file is not found
		
        return open(filename).read()

