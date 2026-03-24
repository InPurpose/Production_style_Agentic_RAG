# app.ingestion.document_loader.py

# from pathlib import Path
from langchain_community.document_loaders import (
        TextLoader, DirectoryLoader, PDFMinerLoader, PyPDFLoader # UnstructuredHTMLLoader , UnstructuredMarkdownLoader
)

# from langchain_community.document_loaders import pdf
from langchain_core.documents import Document
from langchain_community.document_loaders import UnstructuredPDFLoader

class BaseLoader:
    def load(self, path: str):
        raise NotImplementedError
    

class PDFLoader(BaseLoader):

    def __init__(self,path:str= "data/"):
        self.path = path
    
    def load(self, path= None):
        if not path:
            path = self.path

        pdf_loader = DirectoryLoader(
        path,
        glob="**/*.pdf",
        loader_cls=UnstructuredPDFLoader,
        loader_kwargs={},
        recursive=True,
        silent_errors=True,
        show_progress=True,
        use_multithreading=True,
        max_concurrency=4  # 降低避免资源争用
        )

        docs = pdf_loader.load()
        # print(f"Loaded {len(docs)} docs")
        # for doc in docs[:2]:
        #     print(doc.metadata)
        return docs
    
class TextFileLoader(BaseLoader):

    def __init__(self,path:str= "data/"):
        self.path = path
    
    def load(self, path= None):
        if not path:
            path = self.path

        loader = DirectoryLoader(
        path,
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding":"utf-8"},
        recursive=True,
        silent_errors=True,
        show_progress=True,
        use_multithreading=True,
        max_concurrency=4  # 降低避免资源争用
        )


        docs = loader.load()
        print(f"Loaded {len(docs)} docs")
        print()
        # print(type(docs[0]))
        # for doc in docs[:2]:
        #     print(doc.metadata)
        return docs
    
class MarkDownLoader(BaseLoader):

    def __init__(self,path:str= "data/"):
        self.path = path
    
    def load(self, path= None):
        if not path:
            path = self.path

        md_loader = DirectoryLoader(
        path,
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        recursive=True,
        silent_errors=True,
        show_progress=True,
        use_multithreading=True,
        max_concurrency=4  # 降低避免资源争用
        )

        docs = md_loader.load()
        print(f"Loaded {len(docs)} docs")
        for doc in docs[:2]:
            print(doc.metadata)
        return docs




class UnifiedLoader(BaseLoader):

    def __init__(self, path: str = 'data/'):
        self.path = path

    def load(self, path=None) -> list[Document]:
        if not path:
            path = self.path
            
        all_docs = []

        loaders = [
            ("**/*.txt", TextLoader),
            ("**/*.pdf", PyPDFLoader),
            ("**/*.md", TextLoader),
        ]

        clean_docs = []
        for glob, loader_cls in loaders:

            loader = DirectoryLoader(
                path,
                glob=glob,
                loader_cls=loader_cls,
                recursive=True,
                silent_errors=True,
                show_progress=True,
            )

            docs = loader.load()

            for doc in docs:

                if doc is None:
                    continue

                if not doc.page_content or not doc.page_content.strip():
                    continue

                clean_docs.append(doc)

            all_docs.extend(clean_docs)
            # all_docs.extend(docs)

        print(f"Loaded {len(all_docs)} docs")

        return all_docs
            
def main():
    d = UnifiedLoader()
    d.load()



if __name__ == '__main__':
    main()



