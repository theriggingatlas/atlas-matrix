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

    def decompose_matrix(self, node_decomposed:str, suffix:str=None) -> str:
        if suffix:
            node_name = f"decomposematrix_{node_decomposed}_{suffix}"
        else:
            node_name = f"decomposematrix_{node_decomposed}"

        cmds.createNode("decomposeMatrix", name = node_name)
        cmds.connectAttr(f"{node_decomposed}.worldMatrix[0]", f"{node_name}.inputMatrix")

        return node_name


    def hold_matrix(self, input, name, matrix_input_suffix=None):
        hm_name = name
        cmds.createNode("holdMatrix", name=hm_name)
        if verification.is_multmatrix(input):
            cmds.connectAttr(f"{input}.matrixSum", f"{hm_name}.inMatrix")
        else:
            if matrix_input_suffix:
                cmds.connectAttr(f"{input}.{matrix_input_suffix}", f"{hm_name}.inMatrix")
            else:
                print("Please add a matrix_input_suffix")
        return f"{hm_name}.outMatrix"


    def mult_matrix(self, input_list, name):
        mm_name=name
        cmds.createNode("multMatrix", name=mm_name)
        for idx, input in enumerate(input_list):
            cmds.connectAttr(input, f"{mm_name}.matrixIn[{idx}]")

        return f"{mm_name}.matrixSum"

    def pick_matrix(self, input, name, translate_pick_matrix=True, rotate_pick_matrix=True, scale_pick_matrix=True):
        node_pick_matrix=name
        cmds.createNode("pickMatrix", name=node_pick_matrix)
        cmds.setAttr(f"{node_pick_matrix}.useTranslate", translate_pick_matrix)
        cmds.setAttr(f"{node_pick_matrix}.useRotate", rotate_pick_matrix)
        cmds.setAttr(f"{node_pick_matrix}.useScale", scale_pick_matrix)
        cmds.connectAttr(input, f"{node_pick_matrix}.inputMatrix")

        return f"{node_pick_matrix}.outputMatrix"