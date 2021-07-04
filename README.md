# Differential Privacy using K-Anonymity
## To-do list
- [x] Run 3 methods on 4 datasets 
- [x] Add L diversity, Classic Mondrian (no hierarchies)
- [ ] Implement classification models (basic classifier, clustering)
- [ ] Run experiment on 4 datasets x 5 methods x 2 ML models
- [ ] Finish report
- [ ] (Improvement) T-closeness method


## Reports:
Report edit link:
[![report](https://img.shields.io/badge/latex-%23008080.svg?style=for-the-badge&logo=latex&logoColor=white)](https://www.overleaf.com/4786864492ypscdyrmpwzd)


## Executing:
To anonymize dataset, run:
```
python anonymize.py --method=<[mondrian|topdown|cluster]> --k=<k-anonymity>
```

## References:
- https://github.com/Nuclearstar/K-Anonymity
- https://github.com/fhstp/k-AnonML
- [Privacy in a Mobile-Social World](https://courses.cs.duke.edu//fall12/compsci590.3/slides/lec3.pdf)
- [k-Anonymity in Practice: How Generalisation and Suppression Affect Machine Learning Classifiers](https://arxiv.org/abs/2102.04763)
