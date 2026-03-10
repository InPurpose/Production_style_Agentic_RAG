from dataclasses import dataclass

from app.schemas import DocumentChunk


class BaseChunker:

    def chunk(self, text: str, source: str) -> list:
        raise NotImplementedError
    

class FixedSizeChunker(BaseChunker):

    def __init__(self, chunk_size: int = 500, overlap: int = 100):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str, source: str = 'data/') -> list[DocumentChunk]:
        ...



def main():
    ...

if __name__ == '__main__':
    main()