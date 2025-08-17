import maya.cmds as cmds
import maya.api.OpenMaya as om
from core.utils import verification

def get_node_type(name:str)-> str:
    selection_list = om.MSelectionList()
    selection_list.add(name)
    node_obj = selection_list.getDependNode(0)

    dependency_node = om.MFnDependencyNode(node_obj)

    node_type = dependency_node.typeName
    return node_type

class Matrix:
    def __init__(self):
        pass

    def decompose_matrix(self, input_node: str, name: str) -> str:
        """
        Create a decomposeMatrix node and connect an input matrix to it.

        Args:
            input_node (str): The input matrix attribute to connect (e.g., 'myNode.worldMatrix[0]').
            name (str): Suffix used to name the decomposeMatrix node.

        Returns:
            str: The name of the created decomposeMatrix node.
        """
        decompose_matrix_node = f"decomposematrix_{name}"

        cmds.createNode("decomposeMatrix", name = decompose_matrix_node)
        cmds.connectAttr(input_node, f"{decompose_matrix_node}.inputMatrix")

        return decompose_matrix_node

    def compose_matrix(self, input_node: str, name: str,
                       translate: list[str] = ["X", "Y", "Z"],
                       rotate: list[str] = ["X", "Y", "Z"],
                       scale: list[str] = ["X", "Y", "Z"]) -> str:
        """
        Create a composeMatrix node and connect selected transform components from an input_node node.

        Args:
            input_node (str): Name of the input node to read from.
            name (str): Name suffix for the new composeMatrix node.
            translate (list): Axes to connect for translation (e.g., ["X", "Y", "Z"]).
            rotate (list): Axes to connect for rotation.
            scale (list): Axes to connect for scale.

        Returns:
            str: The name of the created composeMatrix node.
        """
        compose_matrix_node = f"composeMatrix_{name}"
        if not cmds.objExists(compose_matrix_node):
            cmds.createNode("composeMatrix", name=compose_matrix_node)

        # Connect translate axes
        for axis in translate:
            if verification.is_decomposematrix(input_node):
                src_attr = f"{input_node}.outputTranslate{axis}"
            else:
                src_attr = f"{input_node}.translate{axis}"
            dst_attr = f"{compose_matrix_node}.inputTranslate{axis}"
            if cmds.objExists(src_attr):
                cmds.connectAttr(src_attr, dst_attr, force=True)

        # Connect rotate axes
        for axis in rotate:
            if verification.is_decomposematrix(input_node):
                src_attr = f"{input_node}.outputRotate{axis}"
            else:
                src_attr = f"{input_node}.rotate{axis}"
            dst_attr = f"{compose_matrix_node}.inputRotate{axis}"
            if cmds.objExists(src_attr):
                cmds.connectAttr(src_attr, dst_attr, force=True)

        # Connect scale axes
        for axis in scale:
            if verification.is_decomposematrix(input_node):
                src_attr = f"{input_node}.outputScale{axis}"
            else:
                src_attr = f"{input_node}.scale{axis}"
            dst_attr = f"{compose_matrix_node}.inputScale{axis}"
            if cmds.objExists(src_attr):
                cmds.connectAttr(src_attr, dst_attr, force=True)

        return compose_matrix_node

    def hold_matrix(self, input_node, name, matrix_input_suffix=None):
        hm_name = name
        cmds.createNode("holdMatrix", name=hm_name)
        if verification.is_multmatrix(input_node):
            cmds.connectAttr(f"{input_node}.matrixSum", f"{hm_name}.inMatrix")
        else:
            if matrix_input_suffix:
                cmds.connectAttr(f"{input_node}.{matrix_input_suffix}", f"{hm_name}.inMatrix")
            else:
                print("Please add a matrix_input_suffix")
        return f"{hm_name}.outMatrix"


    def mult_matrix(self, input_list, name):
        mm_name=name
        cmds.createNode("multMatrix", name=mm_name)
        for idx, input in enumerate(input_list):
            cmds.connectAttr(input, f"{mm_name}.matrixIn[{idx}]")

        return f"{mm_name}.matrixSum"

    def pick_matrix(self, input_node, name, translate_pick_matrix=True, rotate_pick_matrix=True, scale_pick_matrix=True):
        node_pick_matrix=name
        cmds.createNode("pickMatrix", name=node_pick_matrix)
        cmds.setAttr(f"{node_pick_matrix}.useTranslate", translate_pick_matrix)
        cmds.setAttr(f"{node_pick_matrix}.useRotate", rotate_pick_matrix)
        cmds.setAttr(f"{node_pick_matrix}.useScale", scale_pick_matrix)
        cmds.connectAttr(input_node, f"{node_pick_matrix}.inputMatrix")

        return f"{node_pick_matrix}.outputMatrix"