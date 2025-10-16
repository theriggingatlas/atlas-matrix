# -*- coding: utf-8 -*-
""" DEP class to use matrix inside Maya

This module provides the `Matrix` class, which allows precise control
over object transformations using matrix nodes in Maya. It can create
and manage nodes such as multMatrix, decomposeMatrix, composeMatrix,
holdMatrix, and blendMatrix, enabling matrix-based parent and aim
constraints without relying on standard Maya constraint nodes.

Author: Clement Daures
Company: The Rigging Atlas
Website: theriggingatlas.com
Created: 2025

To do : adding get_world_matrix, get_inverse_world_matrix, get_offset_parent_matrix
"""

# ---------- IMPORT ----------

from typing import Optional, List, Union

import maya.cmds as cmds
from core.utils import nodes
from core.utils import transform
from core.utils import verification


# ---------- MAIN CLASS ----------


class Matrix:
    """Class to create a matrix-based parent constraint in Maya.

    This constraint system uses multMatrix, decomposeMatrix, and optionally
    pickMatrix, holdMatrix, and blendMatrix nodes for precise control over
    transformations.
    """

    def __init__(self, driven: Optional[str] = None, drivers: Optional[List[str]] = None) -> None:
        """Initialize the Matrix constraint builder.

        Args:
            driven (Optional[str]): The name of the driven object.
            drivers (Optional[List[str]]): A list of driver object names.

        Raises:
            ValueError: If neither `driven` nor `drivers` are provided.
        """
        user_sel = cmds.ls(selection=True) or []
        self.driven = driven or (user_sel[-1] if user_sel else None)
        self.drivers = drivers or (user_sel[:-1] if user_sel else [])
        self.constraint_type = ""
        if not self.driven or not self.drivers:
            raise ValueError("Provide driven and at least one driver.")


    @property
    def constraining_name(self) -> str:
        """Get the type name used for constraint node naming.

        Returns:
            str: The constraint type identifier (e.g., "pconstrainedby" or "aconstrainedby").
        """
        return {
            "parent": "pconstrainedby",
            "aim": "aconstrainedby"
        }.get(self.constraint_type, "")


    @staticmethod
    def _attribute_validation(attribute_list: List[str]) -> None:
        """Validate that all submitted strings are valid Maya attributes.

        Args:
            attribute_list (List[str]): A list of attribute strings to validate.

        Raises:
            ValueError: If one or more attributes are invalid.
        """
        invalid = [attr for attr in attribute_list if not verification.is_attribute_api(attr)]
        if invalid:
            raise ValueError(f"Invalid attributes detected: {invalid}")


    @staticmethod
    def _index_validation(matrix_node: str, index: Optional[int] = None) -> None:
        """Validate that an index is provided for a matrix node connection.

        Args:
            matrix_node (str): The name of the matrix node.
            index (Optional[int]): The index value to validate.

        Raises:
            ValueError: If `index` is None.
        """
        if index is None:
            raise ValueError(f"Index required for node {matrix_node}")


    @staticmethod
    def _driver_name(driver: Union[str, List[str]]) -> str:
        """Get a formatted driver name for node naming.

        Args:
            driver (str | list[str]): The driver name or list of name parts.

        Returns:
            str: A single driver name string.
        """
        return driver if isinstance(driver, str) else "_".join(driver)


    def _create_matrix_node(self, node_type: str, driver: str) -> str:
        """Create a Maya matrix-related node for the given driver.

        Args:
            node_type (str): The Maya node type to create (e.g., "multMatrix").
            driver (str): The name of the driver node.

        Returns:
            str: The name of the created matrix node.
        """
        node_name = f"{node_type.lower()}_{self.driven}_{self.constraining_name}_{self._driver_name(driver)}"
        node = cmds.createNode(node_type, name=node_name)
        return node


    def mult_matrix(self, driver: str) -> str:
        """Create a multMatrix node for the given driver.

        Args:
            driver (str): The name of the driver node.

        Returns:
            str: The name of the created multMatrix node.
        """
        return self._create_matrix_node("multMatrix", driver)


    def hold_matrix(self, driver: str) -> str:
        """Create a holdMatrix node for the given driver.

        Args:
            driver (str): The name of the driver node.

        Returns:
            str: The name of the created holdMatrix node.
        """
        return self._create_matrix_node("holdMatrix", driver)


    def decompose_matrix(self, driver: str) -> str:
        """Create a decomposeMatrix node for the given driver.

        Args:
            driver (str): The name of the driver node.

        Returns:
            str: The name of the created decomposeMatrix node.
        """
        return self._create_matrix_node("decomposeMatrix", driver)


    def compose_matrix(self, driver: str) -> str:
        """Create a composeMatrix node for the given driver.

        Args:
            driver (str): The name of the driver node.

        Returns:
            str: The name of the created composeMatrix node.
        """
        return self._create_matrix_node("composeMatrix", driver)


    def get_out_matrix(self, matrix_node: str) -> str:
        """Get the output matrix attribute name for a given matrix node.

        Args:
            matrix_node (str): The name of the matrix node.

        Returns:
            str: The full output attribute path (e.g., "multMatrix.matrixSum").

        Raises:
            ValueError: If the provided node is not a valid matrix node.
        """
        if "matrix" in nodes.get_node_type(matrix_node.lower()):

            if verification.is_inversematrix(matrix_node):
                return f"{matrix_node}.outMatrix"

            elif verification.is_multmatrix(matrix_node) or verification.is_addmatrix(matrix_node) or verification.is_wtaddmatrix(matrix_node):
                return f"{matrix_node}.matrixSum"

            else:
                return f"{matrix_node}.outputMatrix"

        else:

            raise ValueError(f"Invalid matrix node : {matrix_node}")


    def get_in_matrix(self, matrix_node: str, index: Optional[int] = None) -> str:
        """
        Get the input matrix attribute name for a given matrix node.

        Args:
            matrix_node (str): The name of the matrix node.
            index (int | None): The index for the input if applicable.

        Returns:
            str: The full input attribute path (e.g., "multMatrix.matrixIn[0]").

        Raises:
            ValueError: If the node is invalid or index is missing where required.
        """

        if "matrix" in nodes.get_node_type(matrix_node.lower()):

            if verification.is_holdmatrix(matrix_node):
                return f"{matrix_node}.inMatrix"

            elif verification.is_multmatrix(matrix_node) or verification.is_addmatrix(matrix_node):
                self._index_validation(matrix_node, index)
                return f"{matrix_node}.matrixIn[{index}]"

            elif verification.is_blendmatrix(matrix_node) or verification.is_parentmatrix(matrix_node):
                self._index_validation(matrix_node, index)
                return f"{matrix_node}.target[{index}].targetMatrix"

            else:
                return f"{matrix_node}.inputMatrix"

        else:

            raise ValueError(f"Invalid matrix node : {matrix_node}")


    @staticmethod
    def get_world_matrix(matrix_node: str) -> str:
        """
        Get the worldMatrix attribute name for a given matrix node.

        Args:
            matrix_node (str): The name of the matrix node.

        Returns:
            str: The full worldMatrix attribute path (e.g., "cube1.worldMatrix[0]").

        Raises:
            ValueError: If the worldMatrix attribute is missing.
        """
        if not cmds.attributeQuery('worldMatrix', node=matrix_node, exists=True):
            raise ValueError(f"Submitted node {matrix_node} does not contain a worldMatrix attribute")

        return f"{matrix_node}.worldMatrix[0]"


    @staticmethod
    def get_inverse_world_matrix(matrix_node: str) -> str:
        """
        Get the worldInverseMatrix attribute name for a given matrix node.

        Args:
            matrix_node (str): The name of the matrix node.

        Returns:
            str: The full worldInverseMatrix attribute path (e.g., "cube1.worldMatrix[0]").

        Raises:
            ValueError: If the worldInverseMatrix attribute is missing.
        """
        if not cmds.attributeQuery('worldInverseMatrix', node=matrix_node, exists=True):
            raise ValueError(f"Submitted node {matrix_node} does not contain a worldInverseMatrix attribute")

        return f"{matrix_node}.worldInverseMatrix[0]"


    @staticmethod
    def get_offset_parent_matrix(matrix_node: str) -> str:
        """
        Get the offsetParentMatrix attribute name for a given matrix node.

        Args:
            matrix_node (str): The name of the matrix node.

        Returns:
            str: The full offsetParentMatrix attribute path (e.g., "cube1.offsetParentMatrix").

        Raises:
            ValueError: If the offsetParentMatrix attribute is missing.
        """
        if not cmds.attributeQuery('offsetParentMatrix', node=matrix_node, exists=True):
            raise ValueError(f"Submitted node {matrix_node} does not contain a offsetParentMatrix attribute")

        return f"{matrix_node}.offsetParentMatrix"


    def connect_matrix(self, source: str, target: str) -> None:
        """Connect one matrix attribute to another.

        Args:
            source (str): The source attribute (e.g., "multMatrix.matrixSum").
            target (str): The target attribute (e.g., "object.offsetParentMatrix").

        Raises:
            ValueError: If either attribute is invalid.
        """
        self._attribute_validation([source, target])

        cmds.connectAttr(source, target)


    def disconnect_matrix(self, source: str, target: str) -> None:
        """Disconnect one matrix attribute from another.

        Args:
            source (str): The source attribute (e.g., "multMatrix.matrixSum").
            target (str): The target attribute (e.g., "object.offsetParentMatrix").

        Raises:
            ValueError: If either attribute is invalid.
        """
        self._attribute_validation([source, target])

        cmds.disconnectAttr(source, target)