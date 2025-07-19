# wfst_nlp_tutorials
This repository contains materials from a 5-hour WFST tutorial I delivered to LU Lab interns on 13 July 2025. The focus is on leveraging the power of Weighted Finite State Transducers (WFSTs) for core NLP tasks including word segmentation, POS tagging, and machine translation. Whether you’re new to WFSTs or looking for practical implementations, these tutorials provide a solid foundation for understanding their applications in NLP.

## Lecture Slide  

- Finite State Machines for NLP, UTYCC NLP Class, 2019, Ye Kyaw Thu, [https://github.com/ye-kyaw-thu/wfst_nlp_tutorials/blob/main/slide/11-fsm4nlp.pdf](https://github.com/ye-kyaw-thu/wfst_nlp_tutorials/blob/main/slide/11-fsm4nlp.pdf)  

## Notebooks

1.[WFST_Word_Segmentation_Small_Corpus.ipynb](https://github.com/ye-kyaw-thu/wfst_nlp_tutorials/blob/main/visualization/tiny_ws/WFST_Word_Segmentation_Small_Corpus.ipynb)  
2.[WFST_POS_Tagging_Small_Corpus.ipynb](https://github.com/ye-kyaw-thu/wfst_nlp_tutorials/blob/main/visualization/tiny_pos/WFST_POS_Tagging_Small_Corpus.ipynb)  
3.[WFST_MT_Small_Corpus.ipynb](https://github.com/ye-kyaw-thu/wfst_nlp_tutorials/blob/main/visualization/tiny_mt/WFST_MT_Small_Corpus.ipynb)  
4.[WFST_Word_Segmentation.ipynb](https://github.com/ye-kyaw-thu/wfst_nlp_tutorials/blob/main/fst_decoder/WFST_Word_Segmentation.ipynb)  
5.[WFST_POS_Tagging.ipynb](https://github.com/ye-kyaw-thu/wfst_nlp_tutorials/blob/main/wfst_pos/WFST_POS_Tagging.ipynb)   
6.[WFST_MT.ipynb](https://github.com/ye-kyaw-thu/wfst_nlp_tutorials/blob/main/wfst_mt/WFST_MT.ipynb)  

## License  

The Bash shell scripts, Python code, and Jupyter notebooks in this WFST-NLP tutorial repository are licensed under the **MIT License**.  

However, the datasets used in these tutorials follow their original licenses:  

- **Word Segmentation & POS Tagging Tutorial**: Uses [myPOS (Version 3.0)](https://github.com/ye-kyaw-thu/myPOS), licensed as per its original source.  
- **Machine Translation Tutorial**: Uses the **Myanmar-Rakhine Parallel Corpus** (full version not yet publicly released).  
  - For research purposes, I’ve included **aligned phrase pairs** (Myanmar-Rakhine) generated using the `anymalign` alignment toolkit.  
