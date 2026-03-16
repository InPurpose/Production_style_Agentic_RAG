# app.ingestion.document_loader.py


from pathlib import Path
from langchain_community.document_loaders import (
        TextLoader, DirectoryLoader, UnstructuredHTMLLoader,PDFMinerLoader
)
from langchain_core.documents import Document

class BaseLoader:
    def load(self, path: str):
        raise NotImplementedError
    

class PDFLoader(BaseLoader):
    
    def load(self, path= "docs-corpus/aws/"):
        pdf_loader = DirectoryLoader(
        path,
        glob="**/*.pdf",
        loader_cls=PDFMinerLoader,
        loader_kwargs={},
        recursive=True,
        silent_errors=True,
        show_progress=True,
        use_multithreading=True,
        max_concurrency=4  # 降低避免资源争用
        )

        docs = pdf_loader.load()
        print(f"Loaded {len(docs)} docs")
        for doc in docs[:2]:
            print(doc.metadata)
        return docs
    
class TextLoader(BaseLoader):

    def __init__(self,path:str= "docs-corpus/books/"):
        self.document_loader = DirectoryLoader(
        path,
        glob="**/*.txt",
        loader_kwargs={"encoding":"utf-8"},
        recursive=True,
        silent_errors=True,
        show_progress=True,
        use_multithreading=True,
        max_concurrency=4  # 降低避免资源争用
        )
    
    def load(self, path= "docs-corpus/books/"):
        pdf_loader = self.document_loader
        docs = pdf_loader.load()
        print(f"Loaded {len(docs)} docs")
        print()
        # print(type(docs[0]))
        # for doc in docs[:2]:
        #     print(doc.metadata)
        return docs
    
class MarkDownLoader(BaseLoader):
    
    def load(self, path= "docs-corpus/rust_md/"):
        pdf_loader = DirectoryLoader(
        path,
        glob="**/*.md",
        loader_kwargs={},
        recursive=True,
        silent_errors=True,
        show_progress=True,
        use_multithreading=True,
        max_concurrency=4  # 降低避免资源争用
        )

        docs = pdf_loader.load()
        print(f"Loaded {len(docs)} docs")
        for doc in docs[:2]:
            print(doc.metadata)
        return docs
    

            
def main():
    d = PDFLoader()
    d.load()

    a = TextLoader()
    a.load()

    b = MarkDownLoader()
    b.load()


if __name__ == '__main__':
    main()



