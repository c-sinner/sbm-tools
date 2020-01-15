class PDB:
    class Atom:
        def __init__(self, serial_number: int, name: str, alt_loc_ind: str, residue_name: str, chain_id: str,
                     residue_seq_number: str, code_ins_residue: str, x_coord: float, y_coord: float, z_coord: float,
                     occupancy: float,
                     temp_factor: float, seg_id: str, element_symbol: str):
            self.serial_number = serial_number
            self.name = name
            self.alt_loc_ind = alt_loc_ind
            self.residue_name = residue_name
            self.chain_id = chain_id
            self.residue_seq_number = residue_seq_number
            self.code_ins_residue = code_ins_residue
            self.x_coord = x_coord
            self.y_coord = y_coord
            self.z_coord = z_coord
            self.occupancy = occupancy
            self.temp_factor = temp_factor
            self.seg_id = seg_id
            self.element_symbol = element_symbol

        def __str__(self):
            return "Name : {0} X : {1}, Y : {2}, Z : {3}".format(self.name, self.x_coord, self.y_coord, self.z_coord)

    def __init__(self, path_to__pdb: str):
        self.path = path_to__pdb

    def find_and_trim(self, target: str, start_idx: int, end_idx: int, return_type='str', offset=0):
        trimmed = target[start_idx - offset: end_idx - offset + 1].strip()
        if return_type == 'str':
            return trimmed
        elif return_type == 'int':
            try:
                converted = int(trimmed)
                return converted
            except ValueError:
                raise ValueError(
                    'ValueError : the section cannot be converted into int. Offending string : {0} '
                    'Offending indices : {1} and {2}'.format(
                        target, start_idx - offset, end_idx - offset))
        elif return_type == 'float':
            try:
                converted = float(trimmed)
                return converted
            except ValueError:
                raise ValueError(
                    'ValueError : the section cannot be converted into float. Offending string : {0} '
                    'Offending indices : {1} and {2}'.format(
                        target, start_idx - offset, end_idx - offset))

    # Open a pdb file in the path and get all the atoms in an array
    def PDB_to_Atoms(self):
        list_of_atoms = []
        with open(self.path, 'r') as file:
            target = file.read().split('\n')
            for l in target:
                if len(l) > 3 and l[0:4] == 'ATOM':
                    atom = self.Atom(self.find_and_trim(l, 7, 11, 'int', 1),
                                     self.find_and_trim(l, 13, 16, 'str', 1),
                                     self.find_and_trim(l, 17, 17, 'str', 1),
                                     self.find_and_trim(l, 18, 20, 'str', 1),
                                     self.find_and_trim(l, 22, 22, 'str', 1),
                                     self.find_and_trim(l, 23, 26, 'str', 1),
                                     self.find_and_trim(l, 27, 27, 'str', 1),
                                     self.find_and_trim(l, 31, 38, 'float', 1),
                                     self.find_and_trim(l, 39, 46, 'float', 1),
                                     self.find_and_trim(l, 47, 54, 'float', 1),
                                     self.find_and_trim(l, 55, 60, 'float', 1),
                                     self.find_and_trim(l, 61, 66, 'float', 1),
                                     self.find_and_trim(l, 73, 76, 'str', 1),
                                     self.find_and_trim(l, 77, 78, 'str', 1), )
                    list_of_atoms.append(atom)
        return list_of_atoms


# Driver
def main():
    pdb = PDB('sample.pdb')
    target, success, failure = pdb.PDB_to_Atoms()
    print('successes : ' + str(success))
    print('failures : ' + str(failure))
    for atom in target:
        print(atom)


if __name__ == '__main__':
    main()
