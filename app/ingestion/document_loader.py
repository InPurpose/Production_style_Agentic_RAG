from pathlib import Path


class DocumentLoader:

    def load_txt(self, path: str):
        with open(path, "r") as f:
            return f.read()


    def load_directory(self, dir_path: str):
        texts = []

        for file in Path(dir_path).glob("*.txt"):
            text = self.load_txt(file)
            texts.append({
                "text": text,
                "source": file.name
            })

        return texts