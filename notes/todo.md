# todo

- [X] Standardize chunk as class or something
- [X] Edit chunkers to be able to save and load from disk (easiest format)
- [X] Edit chunkers to be able to save to BIER jsonl corpus format
- [ ] Edit Chunks class to be able to recieve list of paths along with just one
- [ ] Write RAG evaluation task
    - [ ] Able to use saved chunks from disk
    - [ ] Generate questions from GPT-4 with selected N questions w/ randomly retrieved chunks (use embed, all should use embed retrieve only used in preference voting for generation)
        - [ ] GPT4 (seems better at first glance)
        - [ ] query-gen-msmarco-t5-large-v1
    - [ ] Persist RAG eval task (save both chunks and questions)
    - [ ] Connection should be chunks saved with id, embed, retrieve and questions saved as id, question and id matches question -> embed chunk
- [ ] Eval third party API embeddings
- [ ] Train TAS-G GPL model using gpl lib and jsonl corpus file
- [ ] Eval with generated queries from GPT4  (generate N)
<!-- SO DIFFICULT FOR NO REASON -->
- [ ] Setup Sagemaker for larger tests
    - [ ] New domain (collection of settings for Sagemaker)
    - [ ] Git repos
    - [ ] Shared data
    - [ ] Install packages on startup or customize image
