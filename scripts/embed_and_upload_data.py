import os
import re
from pathlib import Path

import weaviate
import weaviate.classes.config as wvcc
from weaviate.classes.config import Configure


def chunk_list(lst, chunk_size):
    """Break a list into chunks of the specified size."""
    return [lst[i : i + chunk_size] for i in range(0, len(lst), chunk_size)]


def split_into_sentences(text):
    """Split text into sentences using regular expressions."""
    sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", text)
    return [sentence.strip() for sentence in sentences if sentence.strip()]


def read_and_chunk_files(main_folder_path):
    """
    Read .md files from the folder path, split into sentences,
    and chunk every 5 sentences.
    """
    journal_chunks = []
    data_folder_path = Path(main_folder_path).resolve()

    print("Reading .md files in data folder:")
    for filename in data_folder_path.iterdir():
        print(filename.name)
        if ".md" in filename.name:
            print(f"Reading {filename.name}...")
            with open(filename, "r", encoding="utf-8") as file:
                content = file.read()
                sentences = split_into_sentences(content)
                sentence_chunks = chunk_list(sentences, 5)
                sentence_chunks = [
                    " ".join(chunk) for chunk in sentence_chunks
                ]
                journal_chunks.extend(sentence_chunks)
    return journal_chunks


if __name__ == "__main__":

    data_location = (
        "demo_data/"
        if os.getenv("IS_DEMO") in ["1", "true", "True"]
        else "data/"
    )
    data_folder = Path(data_location).resolve()

    WEAVIATE_COLLECTION_NAME = (
        os.getenv("WEAVIATE_COLLECTION_NAME") or "WeaviateTextChunks"
    )

    client = weaviate.connect_to_local(host="localhost")

    collection = client.collections.create(
        name=WEAVIATE_COLLECTION_NAME,
        vectorizer_config=[
            Configure.NamedVectors.text2vec_ollama(
                name="title_vector",
                source_properties=["title"],
                api_endpoint="http://host.docker.internal:11434",
                model="llama3:8b",
            )
        ],
        generative_config=Configure.Generative.ollama(
            api_endpoint="http://host.docker.internal:11434"
        ),
        properties=[
            wvcc.Property(name="content", data_type=wvcc.DataType.TEXT),
            wvcc.Property(name="author", data_type=wvcc.DataType.TEXT),
        ],
    )

    text_chunks = read_and_chunk_files(data_folder)

    print(f"Created {len(text_chunks)} text chunks.")

    collection = client.collections.get(WEAVIATE_COLLECTION_NAME)

    idx = -1
    for idx, text_chunk in enumerate(text_chunks):
        upload = collection.data.insert(properties={"content": text_chunk})

    print(f"Uploaded {idx + 1} text chunks.")

    client.close()
