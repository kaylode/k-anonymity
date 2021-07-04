# Differential Privacy using K-Anonymity
## To-do list
- [x] Run 3 methods on 4 datasets 
- [x] Add L diversity, Classic Mondrian (no hierarchies), Datafly algorithm
- [ ] Make NCP loss a separated module
- [ ] Implement classification models (basic classifier, clustering)
- [ ] Run experiment on 4 datasets x 5 methods x 2 ML models
- [ ] Finish report
- [ ] (Improvement) T-closeness method, Igconito Algorithm
- [ ] (Optional) Simple Deanonymize Attack


## Reports:
Report edit link:
[![report](https://img.shields.io/badge/latex-%23008080.svg?style=for-the-badge&logo=latex&logoColor=white)](https://www.overleaf.com/4786864492ypscdyrmpwzd)


## Executing:
To anonymize dataset, run:
```
python anonymize.py --method=<[mondrian|topdown|cluster]> --k=<k-anonymity>
```

## References:
- Basic Mondrian, Top-Down Greedy, Cluster-based (https://github.com/fhstp/k-AnonML)
- L-Diversity (https://github.com/Nuclearstar/K-Anonymity, https://github.com/qiyuangong/Mondrian_L_Diversity)
- Classic Mondrian (https://github.com/qiyuangong/Mondrian)
- Datafly Algorithm (https://github.com/nazilkbahar/python-datafly)
- [Privacy in a Mobile-Social World](https://courses.cs.duke.edu//fall12/compsci590.3/slides/lec3.pdf)
- Code and idea based on [k-Anonymity in Practice: How Generalisation and Suppression Affect Machine Learning Classifiers](https://arxiv.org/abs/2102.04763)
