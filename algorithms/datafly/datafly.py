import argparse
import csv
import sys
from datetime import datetime
from io import StringIO
import os
from .dgh import CsvDGH


_DEBUG = False


class _Table:

    def __init__(self, pt_path: str, dgh_paths: dict):

        """
        Instantiates a table and the specified Domain Generalization Hierarchies from the
        corresponding files.

        :param pt_path:             Path to the table to anonymize.
        :param dgh_paths:           Dictionary whose values are paths to DGH files and whose keys
                                    are the corresponding attribute names.
        :raises IOError:            If a file cannot be read.
        :raises FileNotFoundError:  If a file cannot be found.
        """

        self.table = None
        """
        Reference to the table file.
        """
        self.attributes = dict()
        """
        Dictionary whose keys are the table attributes names and whose values are the corresponding
        column indices.
        """
        self._init_table(pt_path)
        """
        Reference to the table file.
        """
        self.dghs = dict()
        """
        Dictionary whose values are DGH instances and whose keys are the corresponding attribute 
        names.
        """
        for attribute in dgh_paths:
            self._add_dgh(dgh_paths[attribute], attribute)

    def __del__(self):

        """
        Closes the table file.
        """

        self.table.close()

    def anonymize(self, qi_names: list, k: int, output_path: str, v=True):

        """
        Writes a k-anonymous representation of this table on a new file. The maximum number of
        suppressed rows is k.

        :param qi_names:    List of names of the Quasi Identifiers attributes to consider during
                            k-anonymization.
        :param k:           Level of anonymity.
        :param output_path: Path to the output file.
        :param v:           If True prints some logging.
        :raises KeyError:   If a QI attribute name is not valid.
        :raises IOError:    If the output file cannot be written.
        """

        global _DEBUG

        if v:
            _DEBUG = False

        self._debug("[DEBUG] Creating the output file...", _DEBUG)
        # try:
        #     output = open(output_path, 'w+')
        # except IOError:
        #     raise
        # self._log("[LOG] Created output file.", endl=True, enabled=v)

        # Start reading the table file from the top:
        self.table.seek(0)

        self._debug("[DEBUG] Instantiating the QI frequency dictionary...", _DEBUG)
        # Dictionary whose keys are sequences of values for the Quasi Identifiers and whose values
        # are couples (n, s) where n is the number of occurrences of a sequence and s is a set
        # containing the indices of the rows in the original table file with those QI values:
        qi_frequency = dict()

        self._debug("[DEBUG] Instantiating the attributes domains dictionary...", _DEBUG)
        # Dictionary whose keys are the indices in the QI attribute names list, and whose values are
        # sets containing the corresponding domain elements:
        domains = dict()
        for i, attribute in enumerate(qi_names):
            domains[i] = set()

        # Dictionary whose keys are the indices in the QI attribute names list, and whose values are
        # the current levels of generalization, from 0 (not generalized):
        gen_levels = dict()
        for i, attribute in enumerate(qi_names):
            gen_levels[i] = 0

        for i, row in enumerate(self.table):

            qi_sequence = self._get_values(row, qi_names, i)

            # Skip if this row must be ignored:
            if qi_sequence is None:
                self._debug("[DEBUG] Ignoring row %d with values '%s'..." % (i, row.strip()),
                            _DEBUG)
                continue
            else:
                qi_sequence = tuple(qi_sequence)

            if qi_sequence in qi_frequency:
                occurrences = qi_frequency[qi_sequence][0] + 1
                rows_set = qi_frequency[qi_sequence][1].union([i])
                qi_frequency[qi_sequence] = (occurrences, rows_set)
            else:
                # Initialize number of occurrences and set of row indices:
                qi_frequency[qi_sequence] = (1, set())
                qi_frequency[qi_sequence][1].add(i)

                # Update domain set for each attribute in this sequence:
                for j, value in enumerate(qi_sequence):
                    domains[j].add(value)

            self._log("[LOG] Read line %d from the input file." % i, endl=False, enabled=v)

        self._log('', endl=True, enabled=v)

        lines = []
        while True:

            # Number of tuples which are not k-anonymous.
            count = 0

            for qi_sequence in qi_frequency:

                # Check number of occurrences of this sequence:
                if qi_frequency[qi_sequence][0] < k:
                    # Update the number of tuples which are not k-anonymous:
                    count += qi_frequency[qi_sequence][0]
            self._debug("[DEBUG] %d tuples are not yet k-anonymous..." % count, _DEBUG)
            self._log("[LOG] %d tuples are not yet k-anonymous..." % count, endl=True, enabled=v)

            # Limit the number of tuples to suppress to k:
            if count > k:

                # Get the attribute whose domain has the max cardinality:
                max_cardinality, max_attribute_idx = 0, None
                for attribute_idx in domains:
                    if len(domains[attribute_idx]) > max_cardinality:
                        max_cardinality = len(domains[attribute_idx])
                        max_attribute_idx = attribute_idx

                # Index of the attribute to generalize:
                attribute_idx = max_attribute_idx
                self._debug("[DEBUG] Attribute with most distinct values is '%s'..." %
                            qi_names[attribute_idx], _DEBUG)
                self._log("[LOG] Current attribute with most distinct values is '%s'." %
                          qi_names[attribute_idx], endl=True, enabled=v)

                # Generalize each value for that attribute and update the attribute set in the
                # domains dictionary:
                domains[attribute_idx] = set()
                # Look up table for the generalized values, to avoid searching in hierarchies:
                generalizations = dict()

                # Note: using the list of keys since the dictionary is changed in size at runtime
                # and it can't be used an iterator:
                for j, qi_sequence in enumerate(list(qi_frequency)):

                    self._log("[LOG] Generalizing attribute '%s' for sequence %d..." %
                              (qi_names[attribute_idx], j), endl=False, enabled=v)

                    # Get the generalized value:
                    if qi_sequence[attribute_idx] in generalizations:
                        # Find directly the generalized value in the look up table:
                        generalized_value = generalizations[attribute_idx]
                    else:
                        self._debug(
                            "[DEBUG] Generalizing value '%s'..." % qi_sequence[attribute_idx],
                            _DEBUG)
                        # Get the corresponding generalized value from the attribute DGH:
                       
                        # print(self.dghs[qi_names[attribute_idx]])
                        try:
                            generalized_value = self.dghs[qi_names[attribute_idx]].generalize(
                                qi_sequence[attribute_idx],
                                gen_levels[attribute_idx])
                        except KeyError as error:
                            self._log('', endl=True, enabled=True)
                            self._log("[ERROR] Value '%s' is not in hierarchy for attribute '%s'."
                                      % (error.args[0], qi_names[attribute_idx]),
                                      endl=True, enabled=True)
                            # output.close()
                            return

                        if generalized_value is None:
                            # Skip if it's a hierarchy root:
                            continue

                        # Add to the look up table:
                        generalizations[attribute_idx] = generalized_value

                    # Tuple with generalized value:
                    new_qi_sequence = list(qi_sequence)
                    new_qi_sequence[attribute_idx] = generalized_value
                    new_qi_sequence = tuple(new_qi_sequence)

                    # Check if there is already a tuple like this one:
                    if new_qi_sequence in qi_frequency:
                        # Update the already existing one:
                        # Update the number of occurrences:
                        occurrences = qi_frequency[new_qi_sequence][0] \
                                      + qi_frequency[qi_sequence][0]
                        # Unite the row indices sets:
                        rows_set = qi_frequency[new_qi_sequence][1]\
                            .union(qi_frequency[qi_sequence][1])
                        qi_frequency[new_qi_sequence] = (occurrences, rows_set)
                        # Remove the old sequence:
                        qi_frequency.pop(qi_sequence)
                    else:
                        # Add new tuple and remove the old one:
                        qi_frequency[new_qi_sequence] = qi_frequency.pop(qi_sequence)

                    # Update domain set with this attribute value:
                    domains[attribute_idx].add(qi_sequence[attribute_idx])

                self._log('', endl=True, enabled=v)

                # Update current level of generalization:
                gen_levels[attribute_idx] += 1

                self._log("[LOG] Generalized attribute '%s'. Current generalization level is %d." %
                          (qi_names[attribute_idx], gen_levels[attribute_idx]), endl=True,
                          enabled=v)

            else:

                self._debug("[DEBUG] Suppressing max k non k-anonymous tuples...")
                # Drop tuples which occur less than k times:
                qi_sequences = []
                for qi_sequence, data in qi_frequency.items():
                    if data[0] < k:
                        qi_sequences.append(qi_sequence)
                for qi_sequence in qi_sequences:
                    qi_frequency.pop(qi_sequence)

                self._log("[LOG] Suppressed %d tuples." % count, endl=True, enabled=v)

                # Start to read the table file from the start:
                self.table.seek(0)

                self._debug("[DEBUG] Writing the anonymized table...", _DEBUG)
                self._log("[LOG] Writing anonymized table...", endl=True, enabled=v)
                for i, row in enumerate(self.table):

                    self._debug("[DEBUG] Reading row %d from original table..." % i, _DEBUG)
                    table_row = self._get_values(row, list(self.attributes), i)

                    # Skip this row if it must be ignored:
                    if table_row is None:
                        self._debug("[DEBUG] Skipped reading row %d from original table..." % i,
                                    _DEBUG)
                        continue

                    # Find sequence corresponding to this row index:
                    for qi_sequence in qi_frequency:
                        if i in qi_frequency[qi_sequence][1]:
                            line = self._set_values(table_row, qi_sequence, qi_names)
                            lines.append(line.strip().split(','))
                            self._debug("[DEBUG] Writing line %d from original table to anonymized "
                                        "table..." % i, _DEBUG)
                            # print(line, file=output, end="")
                            break

                break

        # output.close()

        self._log("[LOG] All done.", endl=True, enabled=v)
        return lines

    @staticmethod
    def _log(content, enabled=True, endl=True):

        """
        Prints a log message.

        :param content: Content of the message.
        :param enabled: If False the message is not printed.
        """

        if enabled:
            if endl:
                print(content)
            else:
                sys.stdout.write('\r' + content)

    @staticmethod
    def _debug(content, enabled=False):

        """
        Prints a debug message.

        :param content: Content of the message.
        :param enabled: If False the message is not printed.
        """

        if enabled:
            print(content)

    def _init_table(self, pt_path: str):

        """
        Gets a reference to the table file and instantiates the attribute dictionary.

        :param pt_path:             Path to the table file.
        :raises IOError:            If the file cannot be read.
        :raises FileNotFoundError:  If the file cannot be found.
        """

        try:
            self.table = open(pt_path, 'r')
        except FileNotFoundError:
            raise

    def _get_values(self, row: str, attributes: list, row_index=None):

        """
        Gets the values corresponding to the given attributes from a row.

        :param row:         Line of the table file.
        :param attributes:  Names of the attributes to get the data of.
        :param row_index:   Index of the row in the table file.
        :return:            List of corresponding values if valid, None if this row must be ignored.
        :raises KeyError:   If an attribute name is not valid.
        :raises IOError:    If the row cannot be read.
        """

        # Ignore empty lines:
        if row.strip() == '':
            return None

    def _set_values(self, row, values, attributes: list) -> str:

        """
        Sets the values of a row for the given attributes and returns the row as a formatted string.

        :param row:         List of values of the row.
        :param values:      Values to set.
        :param attributes:  Names of the attributes to set.
        :return:            The new row as a formatted string.
        """

        pass

    def _add_dgh(self, dgh_path: str, attribute: str):

        """
        Adds a Domain Generalization Hierarchy to this table DGH collection, from its file.

        :param dgh_path:            Path to the DGH file.
        :param attribute:           Name of the attribute with this DGH.
        :raises IOError:            If the file cannot be read.
        :raises FileNotFoundError:  If the file cannot be found.
        """

        pass


class CsvTable(_Table):

    def __init__(self, pt_path: str, dgh_paths: dict):

        super().__init__(pt_path, dgh_paths)

    def __del__(self):

        super().__del__()

    def anonymize(self, qi_names, k, output_path, v=False):

        return super().anonymize(qi_names, k, output_path, v)

    def _init_table(self, pt_path):

        super()._init_table(pt_path)

        try:
            # Try to read the first line (which contains the attribute names):
            csv_reader = csv.reader(StringIO(next(self.table)), delimiter=';')
        except IOError:
            raise

        # Initialize the dictionary of table attributes:
        for i, attribute in enumerate(next(csv_reader)):
            self.attributes[attribute] = i

    def _get_values(self, row: str, attributes: list, row_index=None):

        super()._get_values(row, attributes, row_index)

        # Ignore the first line (which contains the attribute names):
        if row_index is not None and row_index == 0:
            return None

        # Try to parse the row:
        try:
            csv_reader = csv.reader(StringIO(row), delimiter=';')
        except IOError:
            raise
        parsed_row = next(csv_reader)
      
        values = list()
        for attribute in attributes:
            if attribute in self.attributes:
                values.append(parsed_row[self.attributes[attribute]])
            else:
                raise KeyError(attribute)

        return values

    def _set_values(self, row: list, values, attributes: list):

        for i, attribute in enumerate(attributes):
            row[self.attributes[attribute]] = values[i]

        values = StringIO()
        csv_writer = csv.writer(values)
        csv_writer.writerow(row)

        return values.getvalue()

    def _add_dgh(self, dgh_path, attribute):

        try:
            self.dghs[attribute] = CsvDGH(dgh_path)
        except FileNotFoundError:
            raise
        except IOError:
            raise


def datafly(k, qi_names, csv_path, data_name, dgh_folder, res_folder):
 
    start = datetime.now()

    dgh_paths = dict()
    for i, qi_name in enumerate(qi_names):
        dgh_paths[qi_name] = os.path.join(dgh_folder, f'{data_name}_hierarchy_{qi_name}.csv')
    
    output = f"{res_folder}/{data_name}_anonymized_{k}.csv"
    table = CsvTable(csv_path, dgh_paths)
    data = table.anonymize(qi_names, k, output, v=False)

    end = (datetime.now() - start).total_seconds()

    return data, end