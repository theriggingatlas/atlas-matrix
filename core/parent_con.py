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

class ParentCon:
    """
    Class to create a matrix-based parent constraint in Maya.

    This constraint system uses multMatrix, decomposeMatrix, and optionally
    pickMatrix, holdMatrix, and blendMatrix nodes for precise control over
    transformations.

    Attributes:
        object_list (list): List of selected objects. Last is the constrained.
        translate_blend_matrix (float): Blend weight for translation.
        rotate_blend_matrix (float): Blend weight for rotation.
        scale_blend_matrix (float): Blend weight for scale.
        offset (bool): Whether to maintain offset between objects.
        hold (bool): Whether to keep initial offset in place using holdMatrix.
        pick_matrix (bool): Whether to use pickMatrix for filtering transformations.
        translate_all (bool): Enable translation filter on constraint.
        rotate_all (bool): Enable rotation filter on constraint.
        scale_all (bool): Enable scale filter on constraint.
        shear_all (bool): Enable shear filter on constraint.
    """
    def __init__(self, object_list=None, translate_blend_matrix=1, rotate_blend_matrix=1, scale_blend_matrix=1,
                 offset=False, hold=False, pick_matrix=False,
                 translate_all=False, rotate_all=False, scale_all=False, shear_all=False,
                 translate=None, rotate=None, scale=None, shear=None
                 ):
        """Initialize the ParentCon constraint setup."""
        self.blend_matrix_node = None
        self.translate_blend_matrix = translate_blend_matrix
        self.rotate_blend_matrix = rotate_blend_matrix
        self.scale_blend_matrix = scale_blend_matrix

        self.pick_matrix = pick_matrix
        self.translate_all = translate_all
        self.rotate_all = rotate_all
        self.scale_all = scale_all
        self.shear_all = shear_all

        translate = translate if translate is not None else [True, True, True]
        rotate = rotate if rotate is not None else [True, True, True]
        scale = scale if scale is not None else [True, True, True]
        shear = shear if shear is not None else [True, True, True]

        self.translate = [axis for axis, flag in zip("XYZ", translate) if flag]
        self.rotate = [axis for axis, flag in zip("XYZ", rotate) if flag]
        self.scale = [axis for axis, flag in zip("XYZ", scale) if flag]
        self.shear = [axis for axis, flag in zip("XYZ", shear) if flag]

        self.matrix_node = nodes.Matrix()

        self.offset = offset
        self.object_list = object_list or cmds.ls(selection=True)
        self.constrained_obj = self.object_list[-1]

        self.hold = hold


    @staticmethod
    def disconnect_input(attr):
        """Disconnect any input connections from the given attribute."""
        connections = cmds.listConnections(attr, s=True, d=False, p=True) or []
        for src in connections:
            cmds.disconnectAttr(src, attr)


    def hold_matrix(self, constrainer, constrained, name_hold_matrix):
        """
        Create a hold matrix node to maintain offset between objects.

        Args:
            constrainer (str): Object acting as the source.
            constrained (str): Object being constrained.
            name_hold_matrix (str): Desired name for the holdMatrix node.

        Returns:
            str: Output matrix attribute.
        """
        node_multmatrix = "tmp_multmatrix"

        out_multmatrix = self.matrix_node.mult_matrix([attributes.get_world_matrix(constrained), attributes.get_world_inverse_matrix(constrainer)], name=node_multmatrix)
        self.matrix_node.hold_matrix(input=node_multmatrix, name=name_hold_matrix)

        self.disconnect_input(attributes.get_in_matrix(name_hold_matrix))
        cmds.delete(node_multmatrix)
        return f"{name_hold_matrix}.outMatrix"

    def _driver_node(self, driver_object: str) -> str:
        """
        Determines and returns the appropriate matrix output node for a driver object,
        based on the current pick/compose options and selected axes.

        Args:
            driver_object (str): The object that drives the constraint.

        Returns:
            str: Output attribute of a matrix node (e.g., worldMatrix, pickMatrix, or composeMatrix).
        """
        name_pick_matrix = f"pickmatrix_{self.constrained_obj}_constrainedby_{driver_object}"

        # Group data for generic iteration
        channels = {
            "translate": {"all": self.translate_all, "axes": self.translate},
            "rotate": {"all": self.rotate_all, "axes": self.rotate},
            "scale": {"all": self.scale_all, "axes": self.scale},
            "shear": {"all": self.shear_all, "axes": self.shear}
        }

        # Case 1: All *_all are True → use full world matrix directly
        if all(data["all"] for data in channels.values()):
            return attributes.get_world_matrix(driver_object)

        # Case 2: Only one *_all is True, others are False and have empty axes → use pickMatrix
        active_all_keys = [key for key, data in channels.items() if data["all"]]
        inactive_empty_keys = [key for key, data in channels.items() if not data["all"] and not data["axes"]]

        if (
                len(active_all_keys) == 1 and
                len(inactive_empty_keys) == 3  # only one active, rest disabled and empty
        ):
            return self.matrix_node.pick_matrix(
                input=attributes.get_world_matrix(driver_object),
                name=name_pick_matrix,
                translate_pick_matrix=self.translate_all,
                rotate_pick_matrix=self.rotate_all,
                scale_pick_matrix=self.scale_all,
                shear_pick_matrix=self.shear_all
            )

        # Case 3: Custom axis selections → decompose + compose
        any_custom_axes = any(data["axes"] for data in channels.values())

        if any_custom_axes:
            decompose = self.matrix_node.decompose_matrix(
                input=attributes.get_world_matrix(driver_object),
                name=f"decompose_{driver_object}"
            )
            return self.matrix_node.compose_matrix(
                input=decompose,
                name=driver_object,
                translate=self.translate,
                rotate=self.rotate,
                scale=self.scale,
                shear=self.shear
            )

        # Fallback: default to worldMatrix
        return attributes.get_world_matrix(driver_object)

    def _mount_system(self, driver_object, parent):
        """
        Internal setup to create the multMatrix chain and connect it.

        Args:
            driver_object (str): The driver object.
            parent (str): Parent of the constrained object.

        Returns:
            str: The multMatrix node name.
        """
        self.disconnect_input(attributes.get_offset_parent_matrix(self.constrained_obj))

        if self.pick_matrix:
            name_pick_matrix = f"pickmatrix_{self.constrained_obj}_constrainedby_{driver_object}"
            driver_world_matrix = self.matrix_node.pick_matrix(input=attributes.get_world_matrix(driver_object), name=name_pick_matrix, translate_pick_matrix=self.translate_all, rotate_pick_matrix=self.rotate_all, scale_pick_matrix=self.scale_all)
        else:
            driver_world_matrix = attributes.get_world_matrix(driver_object)

        if self.offset:
            name_hold_matrix = f"holdmatrix_{self.constrained_obj}_constrainedby_{driver_object}"
            out_hold_matrix = self.hold_matrix(constrainer=driver_object,constrained=self.constrained_obj, name_hold_matrix=name_hold_matrix)
            multmatrix_nodes = [out_hold_matrix, driver_world_matrix, attributes.get_world_inverse_matrix(parent)]
        else:
            multmatrix_nodes = [driver_world_matrix, attributes.get_world_inverse_matrix(parent)]

        node_multmatrix = f"multmatrix_{self.constrained_obj}_constrainedby_{driver_object}"
        out_multmatrix = self.matrix_node.mult_matrix(multmatrix_nodes, name=node_multmatrix)

        if self.offset and not self.hold:
            hold_matrix_out_attr = attributes.get_out_matrix(name_hold_matrix)
            matrix_value = cmds.getAttr(hold_matrix_out_attr)
            cmds.disconnectAttr(f"{node_multmatrix}.matrixIn[0]", hold_matrix_out_attr)

            # Set the matrixIn[0] input of multMatrix with the retrieved matrix
            cmds.setAttr(f'{node_multmatrix}.matrixIn[0]', matrix_value, type='matrix')

        cmds.connectAttr(out_multmatrix, attributes.get_offset_parent_matrix(self.constrained_obj))
        transform.idtransform(self.constrained_obj)

        return  node_multmatrix


    def _blend_matrix_weights(self):
        """Set blend weights on the blendMatrix node."""
        if not self.blend_matrix_node or not cmds.objExists(self.blend_matrix_node):
            print(" Error: Blend Matrix node does not exist. Skipping weight update.")
            return

        target_count = cmds.getAttr(f"{self.blend_matrix_node}.target", size=True)

        if target_count == 0:
            print(f" Warning: Blend Matrix '{self.blend_matrix_node}' has no targets. Skipping weight updates.")
            return

        for i in range(target_count):
            cmds.setAttr(f"{self.blend_matrix_node}.target[{i}].translateWeight", self.translate_blend_matrix)
            cmds.setAttr(f"{self.blend_matrix_node}.target[{i}].rotateWeight", self.rotate_blend_matrix)
            cmds.setAttr(f"{self.blend_matrix_node}.target[{i}].scaleWeight", self.scale_blend_matrix)
        print(
            f"Set target[{i}] weights -> Translate: {self.translate_blend_matrix}, Rotate: {self.rotate_blend_matrix}, Scale: {self.scale_blend_matrix}")


    def _create_blend_matrix(self, multmatrix_nodes):
        """
        Create a blendMatrix node and connect multMatrix outputs.

        Args:
            multmatrix_nodes (list): List of multMatrix node names.

        Returns:
            str: Name of the blendMatrix node.
        """
        name_blend_matrix = f"blendmat_{self.constrained_obj}"
        self.blend_matrix_node = cmds.createNode("blendMatrix", name=name_blend_matrix)

        cmds.connectAttr(f"{multmatrix_nodes[0]}.matrixSum", f"{self.blend_matrix_node}.inputMatrix")

        for idx, multmatrix in enumerate(multmatrix_nodes[1:], start=1):
            cmds.connectAttr(f"{multmatrix}.matrixSum", f"{self.blend_matrix_node}.target[{idx - 1}].targetMatrix")

        self.disconnect_input(attributes.get_offset_parent_matrix(self.constrained_obj))

        cmds.connectAttr(f"{self.blend_matrix_node}.outputMatrix", attributes.get_offset_parent_matrix(self.constrained_obj))

        self._blend_matrix_weights()
        return name_blend_matrix

    def create_constraint(self):
        """
        Entry method to create the full constraint system.

        Returns:
            str: Blend matrix name if used, otherwise None.
        """
        if len(self.object_list) < 2:
            raise ValueError("Please select at least two objects.")

        driver_objects = self.object_list[:-1]

        parent = cmds.listRelatives(self.constrained_obj, parent=True)

        if not parent:
            # Create a group offset
            offset_constrained_obj = cmds.createNode('transform', name=self.constrained_obj + '_off')
            cmds.matchTransform(offset_constrained_obj, self.constrained_obj)
            cmds.parent(self.constrained_obj, offset_constrained_obj)
            cmds.select(clear=True)
            print("Offset parent for constrained object has been created")
            parent = offset_constrained_obj

        else:
            parent = parent[0]

        multmatrix_nodes = []

        for driver_object in driver_objects:
            print(driver_objects)
            print(attributes.get_world_matrix(driver_object))
            multmatrix = self._mount_system(driver_object, parent)
            multmatrix_nodes.append(multmatrix)

        if len(driver_objects) > 1:
            name_blend_matrix = self._create_blend_matrix(multmatrix_nodes)
            return name_blend_matrix

