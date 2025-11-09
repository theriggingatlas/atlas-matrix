# -*- coding: utf-8 -*-
""" DEP class to remove matrix constraints inside Maya

This module provides the `RemoveCon` class, which removes matrix-based constraints
and restores original transformations. It inherits from the Matrix class.

Author: Clement Daures
Company: The Rigging Atlas
Website: theriggingatlas.com
Created: 2025

# ---------- LICENSE ----------

Copyright 2025 Clement Daures - The Rigging Atlas

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

# ---------- IMPORT ----------

from typing import Optional, List
import maya.cmds as cmds
from atlas_matrix.core.matrix import Matrix

# ---------- MAIN CLASS ----------


class RemoveCon(Matrix):
    """
    Class to remove matrix-based constraints in Maya.

    This class handles the deletion of constraint nodes, custom attributes,
    and restoration of original transformation values.
    """

    def __init__(
            self,
            driven: Optional[str] = None,
            constraint_type: Optional[str] = None
    ):
        """
        Initialize the RemoveCon constraint removal.

        Args:
            driven (Optional[str]): The name of the driven object.
            constraint_type (Optional[str]): Type of constraint ("parent" or "aim").
                If None, will attempt to detect automatically.
        """
        # Get selection if no driven provided
        user_sel = cmds.ls(selection=True) or []
        self.driven = driven or (user_sel[0] if user_sel else None)

        if not self.driven:
            raise ValueError("Provide driven object or select one.")

        # Don't call super().__init__ to avoid driver requirement
        self.drivers = []
        self.constraint_type = constraint_type or self._detect_constraint_type()

        if not self.constraint_type:
            raise ValueError(
                f"Could not detect constraint type on {self.driven}. "
                "Please specify 'parent' or 'aim'."
            )


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


    def _detect_constraint_type(self) -> Optional[str]:
        """
        Detect the type of constraint applied to the driven object.

        Returns:
            Optional[str]: "parent" or "aim" if detected, None otherwise.
        """
        # Check offsetParentMatrix connections first (most reliable)
        opm_attr = f"{self.driven}.offsetParentMatrix"
        if cmds.attributeQuery('offsetParentMatrix', node=self.driven, exists=True):
            connections = cmds.listConnections(
                opm_attr,
                source=True,
                destination=False,
                plugs=False
            ) or []

            for node in connections:
                # Check for explicit constraint naming
                if 'pconstrainedby' in node:
                    return "parent"
                elif 'aconstrainedby' in node:
                    return "aim"
                # Check for space_shifter (blendMatrix) or other constraint patterns
                elif 'space_shifter' in node and self.driven in node:
                    # Assume parent constraint for space shifter
                    return "parent"
                # Check node types that indicate constraints
                node_type = cmds.nodeType(node)
                if node_type in ['blendMatrix', 'multMatrix', 'decomposeMatrix']:
                    if self.driven in node:
                        return "parent"  # Default to parent if driven name is in node

        # Check all connections to the driven object
        all_connections = cmds.listConnections(
            self.driven,
            source=True,
            destination=False
        ) or []

        for node in all_connections:
            if 'pconstrainedby' in node and self.driven in node:
                return "parent"
            elif 'aconstrainedby' in node and self.driven in node:
                return "aim"
            elif 'space_shifter' in node and self.driven in node:
                return "parent"

        # Check for weight attributes that indicate constraint type
        user_attrs = cmds.listAttr(self.driven, userDefined=True) or []

        # Look for W0, W1, etc. attributes (common in constraints)
        has_weights = any(attr.startswith('W') and attr[1:].isdigit()
                          for attr in user_attrs)

        # If we have weight attributes and initialTransform or initialMatrix,
        # assume parent constraint
        if has_weights:
            if ('initialTransform' in user_attrs or
                    'initialMatrix' in user_attrs):
                return "parent"
            # Even without initial attributes, W attributes strongly suggest parent constraint
            return "parent"

        return None

    def _get_constraint_nodes(self) -> List[str]:
        """
        Get all nodes related to the constraint.

        Returns:
            List[str]: List of constraint-related node names.
        """
        constraint_nodes = []
        search_pattern = self.constraining_name

        # Start from offsetParentMatrix connection
        opm_attr = f"{self.driven}.offsetParentMatrix"
        if cmds.attributeQuery('offsetParentMatrix', node=self.driven, exists=True):
            opm_connections = cmds.listConnections(
                opm_attr,
                source=True,
                destination=False
            ) or []

            for node in opm_connections:
                # Add nodes that match pattern OR contain driven name and are matrix-related
                if search_pattern and search_pattern in node:
                    constraint_nodes.append(node)
                elif self.driven in node:
                    node_type = cmds.nodeType(node)
                    if 'matrix' in node_type.lower():
                        constraint_nodes.append(node)

        # Get all history connections (includes upstream nodes)
        all_history = cmds.listHistory(self.driven, pruneDagObjects=True) or []

        # Filter nodes that match the constraint naming pattern or contain driven name
        for node in all_history:
            if search_pattern and search_pattern in node and self.driven in node:
                constraint_nodes.append(node)
            elif self.driven in node:
                node_type = cmds.nodeType(node)
                # Include matrix nodes and other constraint-related nodes
                if 'matrix' in node_type.lower() or node_type in ['holdMatrix']:
                    constraint_nodes.append(node)

        # Also check direct connections
        all_connections = cmds.listConnections(
            self.driven,
            source=True,
            destination=False
        ) or []

        for node in all_connections:
            if search_pattern and search_pattern in node and self.driven in node:
                constraint_nodes.append(node)
            elif self.driven in node:
                node_type = cmds.nodeType(node)
                if 'matrix' in node_type.lower():
                    constraint_nodes.append(node)

                    # Get upstream nodes connected to this constraint node
                    upstream = cmds.listHistory(node, pruneDagObjects=True) or []

                    for upstream_node in upstream:
                        if self.driven in upstream_node:
                            upstream_type = cmds.nodeType(upstream_node)
                            if 'matrix' in upstream_type.lower():
                                constraint_nodes.append(upstream_node)

        return list(set(constraint_nodes))  # Remove duplicates

    def _restore_transform_values(self) -> None:
        """
        Restore original transformation values from preserved attributes.
        """
        # Restore from initialTransform if it exists
        if cmds.attributeQuery('initialTransform', node=self.driven, exists=True):
            transform_types = [
                ('translate', ['X', 'Y', 'Z']),
                ('rotate', ['X', 'Y', 'Z']),
                ('scale', ['X', 'Y', 'Z']),
                ('shear', ['X', 'Y', 'Z'])
            ]

            for attr_type, axes in transform_types:
                for axis in axes:
                    initial_attr = f"{self.driven}.initial{attr_type.capitalize()}{axis}"
                    transform_attr = f"{self.driven}.{attr_type}{axis}"

                    if cmds.objExists(initial_attr):
                        try:
                            # Check if there's a connection to initial attribute
                            connections = cmds.listConnections(
                                initial_attr,
                                source=True,
                                destination=False,
                                plugs=True
                            )

                            if connections:
                                # Reconnect to original transform attribute
                                source_attr = connections[0]
                                cmds.connectAttr(source_attr, transform_attr, force=True)
                            else:
                                # Set the value from initial attribute
                                value = cmds.getAttr(initial_attr)
                                cmds.setAttr(transform_attr, value)
                        except Exception as e:
                            cmds.warning(
                                f"Could not restore {transform_attr} from {initial_attr}: {e}"
                            )

    def _restore_matrix_value(self) -> None:
        """
        Restore original offsetParentMatrix value from preserved attribute.
        """
        initial_matrix_attr = f"{self.driven}.initialMatrix"
        opm_attr = f"{self.driven}.offsetParentMatrix"

        if cmds.attributeQuery('initialMatrix', node=self.driven, exists=True):
            try:
                # Check if there's a connection to initial matrix
                connections = cmds.listConnections(
                    initial_matrix_attr,
                    source=True,
                    destination=False,
                    plugs=True
                )

                if connections:
                    # Reconnect to offsetParentMatrix
                    source_attr = connections[0]
                    cmds.connectAttr(source_attr, opm_attr, force=True)
                else:
                    # Set the value from initial matrix
                    matrix_value = cmds.getAttr(initial_matrix_attr)
                    cmds.setAttr(opm_attr, matrix_value, type='matrix')
            except Exception as e:
                cmds.warning(
                    f"Could not restore {opm_attr} from {initial_matrix_attr}: {e}"
                )

    def _remove_constraint_attributes(self) -> None:
        """
        Remove all constraint-related custom attributes from the driven object.
        """
        user_attrs = cmds.listAttr(self.driven, userDefined=True) or []

        attrs_to_remove = []

        # Remove weight attributes (W0, W1, etc.)
        for attr in user_attrs:
            if attr.startswith('W') and len(attr) > 1 and attr[1:].isdigit():
                attrs_to_remove.append(attr)

        # Remove initialTransform compound attribute
        if 'initialTransform' in user_attrs:
            attrs_to_remove.append('initialTransform')

        # Remove initialMatrix attribute
        if 'initialMatrix' in user_attrs:
            attrs_to_remove.append('initialMatrix')

        # Delete attributes
        for attr in attrs_to_remove:
            full_attr = f"{self.driven}.{attr}"
            try:
                if cmds.objExists(full_attr):
                    cmds.deleteAttr(full_attr)
            except Exception as e:
                cmds.warning(f"Could not delete attribute {full_attr}: {e}")

    def _disconnect_offset_parent_matrix(self) -> None:
        """
        Disconnect any remaining connections to offsetParentMatrix.
        """
        opm_attr = f"{self.driven}.offsetParentMatrix"

        if cmds.attributeQuery('offsetParentMatrix', node=self.driven, exists=True):
            connections = cmds.listConnections(
                opm_attr,
                source=True,
                destination=False,
                plugs=True
            )

            if connections:
                for source_attr in connections:
                    try:
                        cmds.disconnectAttr(source_attr, opm_attr)
                    except Exception as e:
                        cmds.warning(
                            f"Could not disconnect {source_attr} from {opm_attr}: {e}"
                        )

    def remove(self) -> None:
        """
        Remove the matrix constraint and restore original transformations.

        This method:
        1. Identifies all constraint-related nodes
        2. Restores original transformation values
        3. Disconnects constraint connections
        4. Deletes constraint nodes
        5. Removes custom constraint attributes
        """
        with self.undo_chunk(name="remove"):
            # Get all constraint nodes before restoration
            constraint_nodes = self._get_constraint_nodes()

            if not constraint_nodes:
                cmds.warning(
                    f"No constraint nodes found for {self.driven} "
                    f"with type '{self.constraint_type}'"
                )
                return

            # Disconnect offsetParentMatrix
            self._disconnect_offset_parent_matrix()

            # Restore original values
            self._restore_transform_values()
            self._restore_matrix_value()

            # Delete constraint nodes
            for node in constraint_nodes:
                try:
                    if cmds.objExists(node):
                        cmds.delete(node)
                except Exception as e:
                    cmds.warning(f"Could not delete node {node}: {e}")

            # Remove custom attributes
            self._remove_constraint_attributes()

            print(f"Successfully removed {self.constraint_type} constraint from {self.driven}")


# ---------- CONVENIENCE FUNCTIONS ----------


def remove_constraint(driven: Optional[str] = None, constraint_type: Optional[str] = None):
    """
    Convenience function to remove a matrix constraint.

    Args:
        driven (Optional[str]): The name of the driven object. If None, uses selection.
        constraint_type (Optional[str]): Type of constraint ("parent" or "aim").
            If None, will attempt to detect automatically.

    Example:
        remove_constraint("pCube1", "parent")
        remove_constraint()  # Uses selected object
    """
    remover = RemoveCon(driven=driven, constraint_type=constraint_type)
    remover.remove()