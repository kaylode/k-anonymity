from algorithms.basic_mondrian.models.numrange import NumRange

class NCP:
    """
    Normalized Certainty Penalty implementation based on definition from
    http://www.tdp.cat/issues11/tdp.a169a14.pdf
    """
    def __init__(self, anon_data, qi_index, att_trees) -> None:
        self.anon_data = anon_data
        self.att_trees = att_trees
        self.qi_index = qi_index
        self.num_qi = len(qi_index)
        self.compute_each_dim_range()
        self.precompute_leaves()

    def get_normalized_width(self, partition, index):
        """
        return Normalized width of partition
        similar to NCP
        """
        if self.is_cat[index] is False:
            low = partition.width[index][0]
            high = partition.width[index][1]
            width = float(self.att_trees[index].sort_value[high]) - float(self.att_trees[index].sort_value[low])
        else:
            width = partition.width[index]
        return width * 1.0 / self.qi_range[index]

    def compute_each_dim_range(self):
        self.qi_range = []
        self.is_cat = []
        for t in self.att_trees:
            if isinstance(t, NumRange):
                self.is_cat.append(False)
            else:
                self.is_cat.append(True)

        for i in range(self.num_qi):
            if self.is_cat[i] is False:
                self.qi_range.append(self.att_trees[i].range)
            else:
                self.qi_range.append(len(self.att_trees[i]['*']))

    def precompute_leaves(self):
        self.qi_leaves = [{} for i in range(self.num_qi)]

        for i in range(self.num_qi):
            if self.is_cat[i]:
                for key in self.att_trees[i].keys():
                    self.qi_leaves[i][key] = len(self.att_trees[i][key])

    def compute_score(self):
        ncp = 0.0 
        for record in self.anon_data:
            rncp = 0.0
            for idx, qi_id in enumerate(self.qi_index):
                value = record[qi_id]
                if self.is_cat[idx]:
                    num_leaves = self.qi_leaves[idx][value]
                    rncp += (num_leaves*1.0/self.qi_range[idx])
                else:
                    low, high = value.split('~')
                    rncp += ((float(high) - float(low))/self.qi_range[idx])
            ncp += rncp
        ncp /= self.num_qi
        ncp /= len(self.anon_data)
        return ncp


        




            