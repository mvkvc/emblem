# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: python3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # data
#
# > 

# %%
#| default_exp data

# %%
#| hide
from nbdev.showdoc import *

# %%
#| export
import re
from typing import Literal
import time
import json

import pandas as pd
import textract
from transformers import BertTokenizerFast
from transformers import PreTrainedTokenizerBase
import nltk
from nltk.tokenize import sent_tokenize


# %%
#| export
class InvalidFileError(Exception):
    def __init__(self, path, message):
        self.filename = filename
        super().__init__(f"INVALID FILE: {filename} - {message}")


# %%
#| export
def clean(text: bytes) -> str:
    try:
        text = text.decode("utf-8", "ignore")
    except AttributeError:
        return "Input is not bytes."

    text = re.sub(r"[^\x00-\x7F]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    text = text.strip()

    return text


# %%
#| export
def extract(path: str, type: Literal["pdf"] | None = None) -> str:
    if type is None:
        type = path.split(".")[-1]

    if type in ["pdf", "docx"]:
        text = textract.process(path)
    else:
        raise InvalidFileError(path=path, message="File type not supported.")

    return clean(text)


# %%
def test_extract(path: str, nwords: int = 100) -> str:
    words = extract(path).split(" ") #[0:nwords]
    return " ".join(words)


# %%
test_doc = "../data/case_brief.pdf"
text = test_extract(test_doc)
text[:1_000]


# %%
#| export
def _default_tokenizer() ->  PreTrainedTokenizerBase:
    return BertTokenizerFast.from_pretrained('bert-base-uncased')


# %%
#| export
def _count_chunk(text: str, tokenizer: PreTrainedTokenizerBase | None = None) -> int:
    # TODO: Get max sequence length from model and then loop over input if longer
    if tokenizer is None:
        tokenizer = _default_tokenizer()
        
    tokens = tokenizer.tokenize(text)
    
    return len(tokens)


# %%
#| export
def _count_chunk_timer(text: str, tokenizer: PreTrainedTokenizerBase | None = None) -> None:
    start_time = time.time()
    count = _count_chunk(text, tokenizer)
    elapsed_time = time.time() - start_time
    print(f"Total tokens: {count}")
    print(f"Time taken: {elapsed_time:.4f}")
    print(f"Tokens per second: {count / elapsed_time:.4f}")


# %%
_count_chunk_timer(text)

# %%
nltk.data.find("tokenizers/punkt")

# %%
# nltk.download('punkt')
sent_tokenize(text)[:5]


# %%
#| export
def _chunk_max_tokens(text: str, max_tokens: int, tokenizer: PreTrainedTokenizerBase) -> str:
    if _count_chunk(text) > max_tokens:
        tokens = tokenizer.tokenize(text)
        tokens_trim = tokens[:max_tokens]
        text = tokenizer.convert_tokens_to_string(text)

    return text


# %%
#| export
def _chunk(
        path: str,
        tokenizer: PreTrainedTokenizerBase | None = None,
        idx_start: int = 0,
        method: Literal["naive", "sentence"] = "naive", 
        max_tokens: int = 256,
        sent_context: int = 2
    ) -> pd.DataFrame:
    """
    Takes text and other inputs and returns tuples of {text_to_embed, text_to_retrieve}
    to be used for retrieval. The tokenizer is used to count tokens and should
    correspond to the model used if embedding locally.
    """
    text = extract(path)
    
    if tokenizer is None:
        tokenizer = _default_tokenizer()

    sent_tokenizer_name = "punkt"
    try:
        nltk.data.find(f"tokenizers/{sent_tokenizer_name}")
    except:
        nltk.download(sent_tokenizer_name)

    sentences = sent_tokenize(text)
    embeds = []
    chunks = []

    if method == "naive":
        temp_chunks = []
        tokens = 0
        for sentence in sentences:
            count = _count_chunk(text=sentence, tokenizer=tokenizer)
            if tokens + count >= max_tokens:
                tokens = 0
                embed = " ".join(temp_chunks)
                embeds.append(embed)
                temp_chunks = []
            sentence = _chunk_max_tokens(sentence, max_tokens, tokenizer)
            temp_chunks.append(sentence)
            tokens += count
        chunks = embeds.copy()  
    elif method == "sentence":
        n_sent = len(sentences)
        for i in range(n_sent):
            start = max(i-sent_context, 0)
            end = min(i+sent_context, n_sent-1)
            full_context_sent = sentences[start:end]
            full_context = " ".join(full_context_sent)
            sentence = _chunk_max_tokens(sentences[i], max_tokens, tokenizer)
            embeds.append(sentence)
            chunks.append(full_context)
    else:
        raise ValueError("Invalid method name.")

    ids = [i for i in range(0, len(embeds))]
    df = pd.DataFrame({
        'id': ids,
        'embeds': embeds,
        'chunks': chunks
    })

    return df


# %%
#| export
class Chunks:
    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data

    @classmethod
    def from_doc(
        cls,
        path: str,
        tokenizer: PreTrainedTokenizerBase | None = None,
        method: Literal["naive", "sentence"] = "naive", 
        max_tokens: int = 256,
        sent_context: int = 2,
        idx_start: int = 0
    ) -> 'Chunks':
        data = _chunk(
            path=path, 
            tokenizer=tokenizer, 
            idx_start=idx_start, 
            method=method, 
            max_tokens=max_tokens, 
            sent_context=sent_context
        )
        
        return cls(data)

    @classmethod
    def from_csv(cls, path: str) -> 'Chunks':
        data = pd.read_csv(path)

        return cls(data)

    def to_csv(self, path: str) -> None:
        self.data.to_csv(path)

    def to_beir(self, path: str) -> None:
        new_df = pd.DataFrame({
            '_id': self.data['id'].astype(str),
            'title': [''] * len(self.data),
            'text': self.data['embeds']
        })

        corpus = new_df.to_json(orient='records', lines=True)
        
        with open(path, 'w') as f:
            f.write(corpus)


# %%
chunks = Chunks.from_doc(path=test_doc)
chunks.data

# %%
path = "../data/corpus.jsonl"
chunks.to_beir(path)

with open(path, 'r') as f:
    for line in f:
        data = json.loads(line)
        print(data)

# %%
# | hide
import nbdev

nbdev.nbdev_export()

# %%
