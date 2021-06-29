Basic Mondrian [![Build Status](https://travis-ci.org/qiyuangong/Basic_Mondrian.svg?branch=master)](https://travis-ci.org/qiyuangong/Basic_Mondrian)
===========================
Mondrian is a Top-down greedy data anonymization algorithm for relational dataset, proposed by Kristen LeFevre in his papers[1]. The original Mondrian is designed for numerical attributes. When comes to categorical attributes, Mondrian needs to transform categorical attributes to numerical ones. This transformation is not good for some applications. In 2006[2], LeFevre proposed basic Mondrian, which supports both categorical and numerical attributes, named `Basic_Mondrian`. The `Basic_Mondrian` can efficiently split categorical attributes with the help of **generalization hierarchies**.

**Note that in most papers people claim that they are using Mondrian with generalization hierarchies. In that case, it must be `Basic_Mondrian`. Because original Mondrian doesn't need generalization hierarchies.**

This repository is an **open source python implementation for basic Mondrian**. I implement this algorithm in python for further study.

### Motivation 
Researches on data privacy have lasted for more than ten years, lots of great papers have been published. However, only a few open source projects are available on Internet [3-4], most open source projects are using algorithms proposed before 2004! Fewer projects have been used in real life. Worse more, most people even don't hear about it. Such a tragedy!

I decided to make some effort. Hoping these open source repositories can help researchers and developers on data privacy (privacy preserving data publishing, data anonymization).

### Attention
I used **both adult and INFORMS** dataset in this implementation. For clarification, **we transform NCP (Normalized Certainty Penalty) to percentage**. This NCP percentage is computed by dividing NCP value with the number of values in dataset (also called GCP (Global Certainty Penalty) [5]). The range of NCP percentage is from 0 to 1, where 0 means no information loss, 1 means loses all information (more meaningful than original NCP, which is sensitive to size of dataset).

The Final NCP of basic Mondrian on [adult dataset](https://archive.ics.uci.edu/ml/datasets/adult) is about 28.52% and 18.52% on [INFORMS data](https://sites.google.com/site/informsdataminingcontest/) (with K=10). Although the NCP of basic Mondrian is higher than original Mondrian, the results on categorical attributes are more meaningful (with the help of well-defined generalization hierarchies).

### Basic Idea

Hope you have read the basic idea of [Mondrian](https://github.com/qiyuangong/Mondrian). `Basic_Mondrian` is an extended version of Mondrian. Then, you can read below.

#### First, what are Generalization Hierarchies?

For some numerical or categorical values, range values are meaningless, for example [Male-Female], ICD09 [200-210]. In this case, these presentations will break the semantic information in these values. To avoid this issue, pre-defined generalization hierarchies are introduced. Note that all nodes in hierarchies should have their natural meaning. Imaging you have a large set of numerical disease values, e.g., ICD09. A pre-defined hierarchy is [always there](http://icd9.chrisendres.com/index.php?action=contents). Then, you can use generalize values according to this hierarchy. During generalization, all values involved can be transform to a more general value in their common ancestors. For example, 291, 295 etc. can be transformed to 290-319 (MENTAL DISORDERS).

<p align="center">
<img src=https://cloud.githubusercontent.com/assets/3848789/26336347/807be240-3fa4-11e7-87a7-d28a05d914a2.png width=750>
</p>
<p align="center">
Figure 1. Generalization Based on Generalization Hierarchies.
</p>

As shown in Fig. 1(a), numerical Age value can be evenly split into balanced a generalization hierarchy. This presentation is more uniform for analyzer. This is another benefit of generalization hierarchies.

### Usage and Parameters:
My Implementation is based on Python 2.7 (not Python 3.0). Please make sure your Python environment is correctly installed. You can run Mondrian in following steps:

1) Download (or clone) the whole project.

2) Run `anonymized.py` in root dir with CLI.

3) **Get the anonymized dataset** from `data/anonymized.data`, if you didn't add `[k | qi | data]`.

Parameters:

	# run Mondrian with adult data and default K (K=10)
	python anonymizer.py 
	
	# run Mondrian with adult data K=20
	python anonymized.py a 20

	a: adult dataset, 'i': INFORMS ataset
	k: varying k, qi: varying qi numbers, data: varying size of dataset, one: run only once


### For more information:
[1] K. LeFevre, D. J. DeWitt, R. Ramakrishnan. Mondrian Multidimensional K-Anonymity ICDE '06: Proceedings of the 22nd International Conference on Data Engineering, IEEE Computer Society, 2006, 25

[2] K. LeFevre, D. J. DeWitt, R. Ramakrishnan. Workload-aware Anonymization. Proceedings of the 12th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, ACM, 2006, 277-286

[3] [UTD Anonymization Toolbox](http://cs.utdallas.edu/dspl/cgi-bin/toolbox/index.php?go=home)

[4] [ARX- Powerful Data Anonymization](https://github.com/arx-deidentifier/arx)

[5] G. Ghinita, P. Karras, P. Kalnis, N. Mamoulis. Fast data anonymization with low information loss. Proceedings of the 33rd international conference on Very large data bases, VLDB Endowment, 2007, 758-769

### Support

- You can post bug reports and feature requests at the [Issue Page](https://github.com/qiyuangong/Basic_Mondrian/issues).
- Contributions via [Pull request](https://github.com/qiyuangong/Basic_Mondrian/pulls) is welcome.
- Also, you can contact me via [email](mailto:qiyuangong@gmail.com).

==========================

by [Qiyuan Gong](mailto:qiyuangong@gmail.com)

2015-1-21
