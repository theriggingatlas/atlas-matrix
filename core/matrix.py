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
from core.utils import verification

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
        self.constraint_type = ""
        if not self.driven or not self.driver:
            raise ValueError("Provide driven and at least one driver (or select drivers then driven).")


    @property
    def constraining_name(self):
        """Return the constraining type in str

        Return:
            str: Constrain type
        """
        return {
            "parent": "pconstrainedby",
            "aim": "aconstrainedby"
        }.get(self.constraint_type, "")


    def mult_matrix(self):
        """Return driver multMatrix name for the driven object


        Example:
            self.driven = driven_obj
            self.driver = driver_obj
            constrain_type = "parent"

            return multmatrix_driven_obj_pconstrainedby_driver_obj

        Return:
            str: Name of the multMatrix
        """
        mult_matrix_name = f"multMatrix_{self.driven}_{self.constraining_name}_{self.driver}"
        cmds.createNode("multMatrix", name= mult_matrix_name)

        return mult_matrix_name


    def hold_matrix(self):
        """Return driver holdMatrix name for the driven object


        Example:
            self.driven = driven_obj
            self.driver = driver_obj
            constraint_type = "parent"

            return hold_driven_obj_pconstrainedby_driver_obj

        Return:
            str: Name of the holdMatrix
        """
        hold_matrix_name = f"holdMatrix_{self.driven}_{self.constraining_name}_{self.driver}"
        cmds.createNode("holdMatrix", name=hold_matrix_name)

        return hold_matrix_name


    def decompose_matrix(self):
        """Return driver decomposeMatrix name for the driven object


        Example:
            self.driven = driven_obj
            self.driver = driver_obj
            constraint_type = "parent"

            return decomposeMatrix_driven_obj_pconstrainedby_driver_obj

        Return:
            str: Name of the decomposeMatrix
        """
        decompose_matrix_name = f"decomposeMatrix_{self.driven}_{self.constraining_name}_{self.driver}"
        cmds.createNode("decomposeMatrix", name=decompose_matrix_name)

        return decompose_matrix_name


    def compose_matrix(self):
        """Return driver composeMatrix name for the driven object


        Example:
            self.driven = driven_obj
            self.driver = driver_obj
            constraint_type = "parent"

            return composeMatrix_driven_obj_pconstrainedby_driver_obj

        Return:
            str: Name of the composeMatrix
        """
        compose_matrix_name = f"composeMatrix_{self.driven}_{self.constraining_name}_{self.driver}"
        cmds.createNode("composeMatrix", name=compose_matrix_name)

        return compose_matrix_name


    def get_out_matrix(self, matrix_node):
        """Return the out attribute of the matrix


        Example:
            matrix_node = "multMatrix"

            return "multMatrix.matrixSum"

        Return:
            str: Complete name of the out matrix
        """
        if "matrix" in nodes.get_node_type(matrix_node.lower()):

            if verification.is_inversematrix(matrix_node):
                return f"{matrix_node}.outMatrix"

            elif verification.is_multmatrix(matrix_node) or verification.is_addmatrix(matrix_node) or verification.is_wtaddmatrix(matrix_node):
                return f"{matrix_node}.matrixSum"

            else:
                return f"{matrix_node}.outputMatrix"

        else:

            cmds.error("DETECTED ISSUE : Submitted node isn't a matrix node")


    def get_in_matrix(self, matrix_node:str, index:int=None)->str:
        """Return the in attribute of the matrix


        Example:
            matrix_node = "multMatrix"

            return "multMatrix.matrixSum"

        Return:
            str: Complete name of the in matrix
        """

        if "matrix" in nodes.get_node_type(matrix_node.lower()):

            if verification.is_holdmatrix(matrix_node):
                return f"{matrix_node}.inMatrix"

            elif verification.is_multmatrix(matrix_node) or verification.is_addmatrix(matrix_node):
                return f"{matrix_node}.matrixIn[{index}]"

            elif verification.is_blendmatrix(matrix_node) or verification.is_parentmatrix(matrix_node):
                return f"{matrix_node}.target[{index}].targetMatrix"

            else:
                return f"{matrix_node}.inputMatrix"

        else:

            cmds.error("DETECTED ISSUE : Submitted node isn't a matrix node")


    @staticmethod
    def attribute_validation(attribute_list: list):
        """Verify submitted attributes"""
        for attr in attribute_list:
             if verification.is_attribute_api(attr):
                 continue
             else:
                 cmds.error(f"DETECTED ISSUE : Submitted node {attr} aren't valid attributes to connect")
                 break


    def connect_matrix(self, in_matrix, out_matrix):
        """Connect two attributes together

        Example:
            in_matrix = "multMatrix.matrixSum"
            out_matrix = "object.offsetParentMatrix"
        """
        self.attribute_validation([in_matrix, out_matrix])

        cmds.connectAttr(in_matrix, out_matrix)


    def disconnect_matrix(self, in_matrix, out_matrix):
        """Disconnect two attributes

        Example:
            in_matrix = "multMatrix.matrixSum"
            out_matrix = "object.offsetParentMatrix"
        """
        self.attribute_validation([in_matrix, out_matrix])

        cmds.disconnectAttr(in_matrix, out_matrix)