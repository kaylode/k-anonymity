# Top_Down_Greedy_Anonymization

Top_Down_Greedy_Anonymization is a Top-down greedy data anonymization algorithm for relational dataset, proposed by Jian Xu in his papers[1]. The author showed that Top_Down_Greedy_Anonymization can preserve more data utility than Mondrian[2]. The key idea of Top_Down_Greedy_Anonymization is binary split and balance (merge sub-groups or move some records from larger group to smaller group). So it need more running time than Mondrian.

This repository is an **open source python implementation for Top_Down_Greedy_Anonymization**. I release this algorithm in python for further study.

### Motivation

Researches on data privacy have lasted for more than ten years, lots of great papers have been published. However, only a few open source projects are available on Internet [3-4], most open source projects are using algorithms proposed before 2004! Fewer projects have been used in real life. Worse more, most people even don't hear about it. Such a tragedy! 

I decided to make some effort. Hoping these open source repositories can help researchers and developers on data privacy (privacy preserving data publishing).

### Attention
I used **both adult and INFORMS** dataset in this implementation. For clarification, **we transform NCP to percentage**, making the NCP (information loss) more meaningful (NCP=2000 v.s. NCP=20%, the former one is sensitive to size of dataset, the latter one is suit for any dataset). This NCP percentage (also called GCP[5]) is computed by dividing NCP value with the number of values in dataset (the number of values can be treated as losing all information).

### Usage:

My Implementation is based on Python 2.7 (not Python 3.0). Please make sure your Python environment is correctly installed. You can run Mondrian in following steps: 

1) Download (or clone) the whole project. 

2) Run "anonymized.py" in root dir with CLI.



	# run Top_Down_Greedy_Anonymization with default K(K=10)

	python anonymizer.py 

	

	# run Top_Down_Greedy_Anonymization with K=20

	python anonymized.py 20



### For more information:

[1] J. Xu, W. Wang, J. Pei, X. Wang, B. Shi, A. W.-C. Fu. Utility-based anonymization using local recoding. Proceedings of the 12th ACM SIGKDD international conference on Knowledge discovery and data mining, ACM, 2006, 785-790



[2] LeFevre, Kristen, David J. DeWitt, and Raghu Ramakrishnan. Mondrian multidimensional k-anonymity. Data Engineering, 2006. ICDE'06. Proceedings of the 22nd International Conference on. IEEE, 2006.



[3] [UTD Anonymization Toolbox](http://cs.utdallas.edu/dspl/toolbox/)

[4] [ARX- Powerful Data Anonymization](https://github.com/arx-deidentifier/arx)

[5] G. Ghinita, P. Karras, P. Kalnis, N. Mamoulis. Fast data anonymization with low information loss. Proceedings of the 33rd international conference on Very large data bases, VLDB Endowment, 2007, 758-769