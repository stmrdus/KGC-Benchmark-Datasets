# Knowledge Graph Completion Benchmark Datasets

<img alt="GitHub top language" src="https://img.shields.io/github/languages/top/nhutnamhcmus/KGC-Benchmark-Datasets"><a href="https://github.com/nhutnamhcmus/KGC-Benchmark-Datasets/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/nhutnamhcmus/KGC-Benchmark-Datasets"></a>
<img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/nhutnamhcmus/KGC-Benchmark-Datasets">
<img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/nhutnamhcmus/KGC-Benchmark-Datasets">
<a href="https://github.com/nhutnamhcmus/KGC-Benchmark-Datasets/network"><img alt="GitHub forks" src="https://img.shields.io/github/forks/nhutnamhcmus/KGC-Benchmark-Datasets"></a>
<a href="https://github.com/nhutnamhcmus/KGC-Benchmark-Datasets/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/nhutnamhcmus/KGC-Benchmark-Datasets"></a>
<img alt="GitHub" src="https://img.shields.io/github/license/nhutnamhcmus/KGC-Benchmark-Datasets">

Standard Staticcal Benchmark Datasets for Knowledge Graph Completion Github repository.

This repository contains dataset for Knowledge Graph Completion task include: link prediction (enity prediction, relation prediction). We upload common datasets like FB15K, FB15K-237, WN18, WN18RR, YAGO3-10. For each dataset, we extract 1-1, 1-N, N-1, N-N relation to text files, relation properties in dataset include symmetric, antisymmetric, reflexive, irreflexive, transitive, partial equivalence, equivalence, order and preorder type.

## Dataset statistical information

FB15k-237 is upgraded version of FB15k. Inverse relations are deleted in order to prevent direct inference of test triples, model can't predict easily. In FB15K-237, we have some relation types like symmetric, antisymmetric and composite

WN18RR is a subset of WN18. Seven inverse relations are deleted similar to FB15k-237. It describe lexical and semantic hierarchies between concepts, which is mainly concerned with symmetry, anti-symmetry.

YAGO3-10 is a subset of YAGO3, mainly concerned with symmetry, anti-symmetry. It has 123,182 entities and 37 relations, and most of the triples describe attributes of persons such as citizenship, gender, and profession.

|   | Entities  | Relations  | Train  | Valid  | Test  |
|---|---|---|---|---|---|
| FB15K [1] | 14951  | 1345  |  483142 | 50000  | 50971  |
| WN18 [1] | 40943  | 18  | 141442  | 5000  | 5000  |
| FB15K-237 [2] | 14541  | 237  | 272115  | 17535  | 20466  |
| WN18RR [3] |  40943 | 11  | 86835  | 3034  |  3134 |
| YAGO3-10 [4] | 123182  |  37 | 1079040  | 5000  | 5000  |
| Kinship [5] | 104  | 25  |  8544 | 1068  | 1074  |
| UMLS  | 135  | 46  |  5216 |  652 | 661  |

## References

[1] Bordes, Antoine, Nicolas Usunier, Alberto García-Durán, Jason Weston and Oksana Yakhnenko. “Translating Embeddings for Modeling Multi-relational Data.” NIPS (2013).

[2] Toutanova, Kristina and Danqi Chen. “Observed versus latent features for knowledge base and text inference.” (2015).

[3] Dettmers, Tim, Pasquale Minervini, Pontus Stenetorp and Sebastian Riedel. “Convolutional 2D Knowledge Graph Embeddings.” AAAI (2018).

[4] Suchanek, Fabian M., Gjergji Kasneci and Gerhard Weikum. “Yago: a core of semantic knowledge.” WWW '07 (2007).

[5] Lin, Xi Victoria, Richard Socher and Caiming Xiong. “Multi-Hop Knowledge Graph Reasoning with Reward Shaping.” EMNLP (2018).

[6] Kok, Stanley and Pedro M. Domingos. “Statistical predicate invention.” ICML '07 (2007).

[7] [research.lpca](https://github.com/merialdo/research.lpca): project analyzes the results of various models for Link Prediction on Knowledge Graphs using Knowledge Graph Embeddings

