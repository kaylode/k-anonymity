class DM:
    """
    Discernibility Metric implementation based on definition from
    http://www.tdp.cat/issues11/tdp.a169a14.pdf    
    """
    def __init__(self, anon_data, qi_index) -> None:
        self.anon_data = anon_data
        self.qi_index = qi_index
        self.num_qi = len(qi_index)

    def compute_eq(self):
        self.eq_count = {}
        for record in self.anon_data:
            qi_values = []
            for idx, qi_id in enumerate(self.qi_index):
                value = record[qi_id]
                qi_values.append(value)
            
            # Make set, because set is hashable
            eq = tuple(qi_values)

            # Count set of qi values
            if eq not in self.eq_count.keys():
                self.eq_count[eq] = 0
            self.eq_count[eq] += 1

    def compute_score(self):
        self.compute_eq()
        dm = 0
        for eq in self.eq_count.keys():
            dm += (self.eq_count[eq]**2)

        return dm
            
                