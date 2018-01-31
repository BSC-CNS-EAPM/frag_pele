import sys
import re
import os
import string
from shutil import copyfile
import logging


# Getting the name of the module for the log system
logger = logging.getLogger(__name__)


def template_reader(template_name, path_to_template="DataLocal/Templates/OPLS2005/HeteroAtoms/"):
    """
    This function reads the content of a PELE's template and return it
    """

    with open(os.path.join(path_to_template, template_name), "r") as template_file:
        template_content = template_file.read()
        if not template_content:
            logger.critical("Template file {} is empty!".format(template_name))

    return template_content


def section_selector(template, pattern_1, pattern_2):
    """
    From a template string, this function return a section between two patterns.
    :param template: input template (string).
    :param pattern_1: pattern which sets the begining of the section.
    :param pattern_2: pattern which sets the end of the section.
    :return: string with the content of the section.
    """

    section_selected = re.search("{}\n(.*?){}".format(pattern_1, pattern_2), template, re.DOTALL)

    return section_selected.group(1)


def atoms_selector(template):
    """
    Given a template, it returns a dictionary with the atoms found.
    :param template: input template (string)
    :return: dictionary {"PDB atom name":"index"}
    """
    ROW_PATTERN = "\s+(\d+)\s+(\d+)\s+(\w)\s+(\w*)\s+(\w{4,})\s+(\d*)\s+(-?[0-9]*\.[-]?[0-9]*)\s+(-?[0-9]*\.[0-9]*)\s+(-?[0-9]*\.[0-9]*)"

    # Select the section of the templates where we have the atoms defined
    atoms_section = section_selector(template, "\*", "NBON")
    # Obtain all rows (list of lists)
    rows = re.findall(ROW_PATTERN, atoms_section)
    # Get the atom name from all rows and insert it in a dictionary
    atoms = {}
    for row in rows:
        atoms[row[4]] = row[0]
    return atoms


# Temporary function
def new_atoms_detector(initial_atoms, final_atoms):
    """
    :param initial_atoms: initial dictionary with {"PDB atom names" : "index"}
    :param final_atoms: final dictionary with {"PDB atom names" : "index"}
    :return: dictionary with {"PDB atom names" : "index"} of the new atoms found.
    """
    # Find the differences between keys in both dictionaries
    differences = final_atoms.keys()-initial_atoms.keys()

    # Now, transform the object to dictionary in order to find the keys
    diff_dictionary = {}
    for atom_name in differences:
        diff_dictionary[atom_name] = final_atoms[atom_name]
    return diff_dictionary


def get_atom_properties(atoms_dictionary, template):
    """
    :param atoms_dictionary: dictionary with {"PDB atom names" : "index"}
    :param template: input template (string)
    :return: dictionary {"index" : ("vdw", "charge")}
    """
    # Definition of the pattern correspondent to NBON section
    NBON_PATTERN = "\s+(\d+)\s+(\d+\.\d{4})\s+(\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)"
    # Selection of NBON section of the template
    nbon_section = section_selector(template, "NBON", "BOND")
    # Obtain all rows (list of lists)
    rows = re.findall(NBON_PATTERN, nbon_section)
    # Obtain a list with the indexes of atoms
    atom_indexes = []
    for atom_name, index in atoms_dictionary.items():
        atom_indexes.append(index)
    # Get the properties for each index
    properties = {}
    for row in rows:
        index = row[0]
        if index in atom_indexes:
            properties[index] = (row[1], row[3])
        else:
            pass

    return properties


def transform_properties(original_atom, final_atom, initial_atm_dictionary, final_atm_dictionary,
                         initial_prp_dictionary, final_prp_dictionary):
    """
    :param original_atom: atom that we want to transform into another.
    :param final_atom: atom that we want to finally get.
    :param initial_atm_dictionary: initial dictionary {"PDB atom name" : "index"} which contain the atom.
    :param final_atm_dictionary: final dictionary {"PDB atom name" : "index"} which contain the atom.
    :param initial_prp_dictionary: initial dictionary {"index" : ("vdw", "charge")} which contain the properties
    of the template.
    :param final_prp_dictionary: final dictionary {"index" : ("vdw", "charge")} which contain the properties of
    the template.
    :return: dictionary with the properties modified.
    """
    # Collect indexes from original and final dictionaries
    index_original = initial_atm_dictionary[original_atom]
    index_final = final_atm_dictionary[final_atom]
    # Use this indexes to transform the properties of the final dictionary to the original ones
    initial_properties = initial_prp_dictionary[index_original]
    final_prp_dictionary[index_final] = initial_properties

    return final_prp_dictionary


def get_bonds(template):
    """
    :param template: template (string) that we want to extract bonding information
    :return: dictionary {("index_1", "index_2"): "bond length" }
    """
    # Definition of the reggex pattern needed in this section
    BOND_PATTERN = "\s+(\d+)\s+(\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)"
    # Selecting BOND information
    bonds_section = section_selector(template, "BOND", "THET")
    # Find data (list of lists)
    rows = re.findall(BOND_PATTERN, bonds_section)
    # Creating a dictionary having as key a tuple of indexes (atoms in bond) and the bond length
    bonds = {}
    for row in rows:
        bonds[(row[0], row[1])] = row[3]

    return bonds


def get_specific_bonds(atoms_dictionary, bonds_dictionary):
    """
    :param atoms_dictionary: dictionary with {"PDB atom names" : "index"} of the atoms that we want to get
    their bond length.
    :param bonds_dictionary: dictionary {("index_1", "index_2"): "bond length" } to obtain the information.
    :return: dictionary {("index_1", "index_2"): "bond length" }
    """
    # Get indexes of the dictionary with all the atoms
    atom_indexes = []
    for atom_name, index in atoms_dictionary.items():
        atom_indexes.append(index)
    # Get indexes of the dictionary with bonding data
    bonded_indexes = []
    for bond_indexes, length in bonds_dictionary.items():
        bonded_indexes.append(bond_indexes)
    # Create a dictionary where we are going to select the bonds for the atoms of the atom_dictionary
    selected_bonds_dictionary = {}
    for index in atom_indexes:
        for bond in bonded_indexes:
            # If we want to obtain only bonds that correspond to our atoms dictionary indexes
            # we have to apply this criteria (bond[1] is the atom that "recives" the bond)
            if bond[1] == index:
                selected_bonds_dictionary[bond] = bonds_dictionary[bond]
            else:
                pass
    return selected_bonds_dictionary


# TESTING PART, PLEASE IGNORE IT
initial_template = template_reader("mbez")
final_template = template_reader("pyjz")

atoms_selected_1 = atoms_selector(initial_template)
atoms_selected_2 = atoms_selector(final_template)

new_atoms = new_atoms_detector(atoms_selected_1, atoms_selected_2)
properties = get_atom_properties(new_atoms, final_template)

prp1 = get_atom_properties(atoms_selected_1, initial_template)
prp2 = get_atom_properties(atoms_selected_2, final_template)

transformed_properties = transform_properties("_H8_", "_C8_", atoms_selected_1, atoms_selected_2, prp1, prp2)
bonds = get_bonds(initial_template)
bonds_2 = get_bonds(final_template)

print(new_atoms)
bonding = get_specific_bonds(new_atoms, bonds_2)
print(bonding)
