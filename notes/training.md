# training

- 3 stages
    - Unsupervised pre-train
    - Supervised fine-tune
    - Domain adaptation
- Best from ST researchers states
    - Pretrain on target domain with TSDAE
    - Fine-tune on labelled dataset
        - Existing MSMarco or whatever
        - Opportunity for users to have qualified people label their data
    - Adaptation by query generation
- Looks like best result is from TAS-B model using GPL with base model as embedding model used
    - Know as TAS-B-GPL
    - What this library will offer
        - Evaluation for RAG (to start) on custom datasets
        - Use of pretrained models
        - Fine tune on both supervised/unsupervised data
        - Adapters for any black box embedding model
- Goal is to find some combination of techniques that provide X lift over OpenAI embeddings for domain specific corpuses
