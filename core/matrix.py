"""

Author: Clement Daures
Company: The Rigging Atlas
Website: theriggingatlas.com
Created: 2025
About: DEP function to use parent constraint matrix inside Maya

"""
import maya.cmds as cmds
from core.utils import nodes
from core.utils import attributes
from core.utils import transform

class Matrix:
    """Class to create a matrix-based parent constraint in Maya.

    This constraint system uses multMatrix, decomposeMatrix, and optionally
    pickMatrix, holdMatrix, and blendMatrix nodes for precise control over
    transformations.

    Attributes:

    """

    def __init__(self, driven:str=None, driver:list[str]=None):
        user_sel = cmds.ls(selection=True) or []
        self.driven = driven or (user_sel[-1] if user_sel else None)
        self.driver = driver or (user_sel[:-1] if user_sel else [])
        if not self.driven or not self.driver:
            raise ValueError("Provide driven and at least one driver (or select drivers then driven).")


    def constraining_string(self, constraint_type:str):
        """Return the constraining type in str

        Return:
            str: Constrain type
        """

        constraining_map = {
            "parent": "pconstrainedby",
            "aim": "aconstrainedby"
        }

        constraining_name = constraining_map.get(constraint_type)

        return constraining_name


    def mult_matrix(self, constraint_type:str):
        """Return driver multMatrix name for the driven object


        Example:
            self.driven = driven_obj
            self.driver = driver_obj
            constrain_type = "parent"

            return multmatrix_driven_obj_pconstrainedby_driver_obj

        Return:
            str: Name of the multMatrix
        """

        constraining_name = self.constraining_string(constraint_type)

        return f"multMatrix_{self.driven}_{constraining_name}_{self.driver}"


    def hold_matrix(self, constraint_type):
        """Return driver holdMatrix name for the driven object


        Example:
            self.driven = driven_obj
            self.driver = driver_obj
            constraint_type = "parent"

            return hold_driven_obj_pconstrainedby_driver_obj

        Return:
            str: Name of the holdMatrix
        """

        constraining_name = self.constraining_string(constraint_type)

        return f"holdMatrix_{self.driven}_{constraining_name}_{self.driver}"


    def decompose_matrix(self, constraint_type):
        """Return driver decomposeMatrix name for the driven object


        Example:
            self.driven = driven_obj
            self.driver = driver_obj
            constraint_type = "parent"

            return decomposeMatrix_driven_obj_pconstrainedby_driver_obj

        Return:
            str: Name of the decomposeMatrix
        """

        constraining_name = self.constraining_string(constraint_type)

        return f"decomposeMatrix_{self.driven}_{constraining_name}_{self.driver}"


    def compose_matrix(self, constraint_type):
        """Return driver composeMatrix name for the driven object


        Example:
            self.driven = driven_obj
            self.driver = driver_obj
            constraint_type = "parent"

            return composeMatrix_driven_obj_pconstrainedby_driver_obj

        Return:
            str: Name of the composeMatrix
        """

        constraining_name = self.constraining_string(constraint_type)

        return f"composeMatrix_{self.driven}_{constraining_name}_{self.driver}"