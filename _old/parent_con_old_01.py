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
    def __init__(self, object_list=None, translate_bm=1, rotate_bm=1, scale_bm=1, offset=False, hold=False, pick_mat=False, translate_pm=False, rotate_pm=False, scale_pm=False):
        self.blend_matrix_node = None
        self.translate_bm = translate_bm
        self.rotate_bm = rotate_bm
        self.scale_bm = scale_bm

        self.pick_mat = pick_mat
        self.translate_pm = translate_pm
        self.rotate_pm = rotate_pm
        self.scale_pm = scale_pm

        self.node = nodes.Matrix()

        self.offset = offset
        self.object_list = object_list or cmds.ls(selection=True)
        self.constrained_obj = self.object_list[-1]

        self.hold = hold


    def hold_matrix(self, constrainer, constrained, name_hm):
        name_mm = "tmp_multmatrix"

        out_mm = self.node.mult_matrix([attributes.get_world_matrix(constrained), attributes.get_world_inverse_matrix(constrainer)], name=name_mm)
        self.node.hold_matrix(input=name_mm, name=name_hm)

        existing_connections = cmds.listConnections(attributes.get_in_matrix(name_hm), s=True, d=False, p=True)
        if existing_connections:
            cmds.disconnectAttr(out_mm, attributes.get_in_matrix(name_hm))
        cmds.delete(name_mm)
        return f"{name_hm}.outMatrix"


    def _mount_system(self, constraining_obj, parent):
        existing_connections = cmds.listConnections(attributes.get_offset_parent_matrix(self.constrained_obj), s=True, d=False, p=True)
        if existing_connections:
            for connection in existing_connections:
                print(f"Disconnecting {connection} from {self.constrained_obj}.offsetParentMatrix")
                cmds.disconnectAttr(connection, attributes.get_offset_parent_matrix(self.constrained_obj))

        if self.pick_mat:
            name_pm = f"pickmatrix_{self.constrained_obj}_constrainedby_{constraining_obj}"
            out_pm = self.node.pick_matrix(input=attributes.get_world_matrix(constraining_obj), name=name_pm, translate_pm=self.translate_pm, rotate_pm=self.rotate_pm, scale_pm=self.scale_pm)
            primary_world = out_pm
        else:
            primary_world = attributes.get_world_matrix(constraining_obj)

        if self.offset:
            name_hm = f"holdmatrix_{self.constrained_obj}_constrainedby_{constraining_obj}"
            out_hm = self.hold_matrix(constrainer=constraining_obj,constrained=self.constrained_obj, name_hm=name_hm)
            multmatrix_list = [out_hm, primary_world, attributes.get_world_inverse_matrix(parent)]
        else:
            multmatrix_list = [primary_world, attributes.get_world_inverse_matrix(parent)]

        name_mm = f"multmatrix_{self.constrained_obj}_constrainedby_{constraining_obj}"
        out_mm = self.node.mult_matrix(multmatrix_list, name=name_mm)

        if self.offset and not self.hold:
            hm_out_attr = attributes.get_out_matrix(name_hm)
            matrix_value = cmds.getAttr(hm_out_attr)
            cmds.disconnectAttr(f"{name_mm}.matrixIn[0]", hm_out_attr)

            # Set the matrixIn[0] input of multMatrix with the retrieved matrix
            cmds.setAttr(f'{name_mm}.matrixIn[0]', matrix_value, type='matrix')

        cmds.connectAttr(out_mm, attributes.get_offset_parent_matrix(self.constrained_obj))
        transform.idtransform(self.constrained_obj)

        return  name_mm


    def _bm_weights(self):

        if not self.blend_matrix_node or not cmds.objExists(self.blend_matrix_node):
            print(" Error: Blend Matrix node does not exist. Skipping weight update.")
            return

        target_count = cmds.getAttr(f"{self.blend_matrix_node}.target", size=True)

        if target_count == 0:
            print(f" Warning: Blend Matrix '{self.blend_matrix_node}' has no targets. Skipping weight updates.")
            return

        for i in range(target_count):
            cmds.setAttr(f"{self.blend_matrix_node}.target[{i}].translateWeight", self.translate_bm)
            cmds.setAttr(f"{self.blend_matrix_node}.target[{i}].rotateWeight", self.rotate_bm)
            cmds.setAttr(f"{self.blend_matrix_node}.target[{i}].scaleWeight", self.scale_bm)
        print(
            f"Set target[{i}] weights -> Translate: {self.translate_bm}, Rotate: {self.rotate_bm}, Scale: {self.scale_bm}")


    def _create_blend_matrix(self, multmatrix_list):

        name_bm = f"blendmat_{self.constrained_obj}"
        self.blend_matrix_node = cmds.createNode("blendMatrix", name=name_bm)

        cmds.connectAttr(f"{multmatrix_list[0]}.matrixSum", f"{self.blend_matrix_node}.inputMatrix")

        for idx, multmatrix in enumerate(multmatrix_list[1:], start=1):
            cmds.connectAttr(f"{multmatrix}.matrixSum", f"{self.blend_matrix_node}.target[{idx - 1}].targetMatrix")

        existing_connections = cmds.listConnections(attributes.get_offset_parent_matrix(self.constrained_obj), s=True, d=False, p=True)
        if existing_connections:
            for connection in existing_connections:
                print(f"Disconnecting {connection} from {self.constrained_obj}.offsetParentMatrix")
                cmds.disconnectAttr(connection, attributes.get_offset_parent_matrix(self.constrained_obj))

        cmds.connectAttr(f"{self.blend_matrix_node}.outputMatrix", attributes.get_offset_parent_matrix(self.constrained_obj))

        self._bm_weights()
        return name_bm

    def create_constraint(self):
        if len(self.object_list) < 2:
            raise ValueError("Please select at least two objects.")

        constraining_objs = self.object_list[:-1]

        parent = cmds.listRelatives(self.constrained_obj, parent=True)

        if not parent:
            # Create a group offset
            offset_constrained_obj = cmds.createNode('transform', name=self.constrained_obj + '_off')
            cmds.matchTransform(offset_constrained_obj, self.constrained_obj)
            cmds.parent(self.constrained_obj, offset_constrained_obj)
            cmds.select(clear=True)
            print("Offset parent for constrained object has been created")
            parent = offset_constrained_obj  # Corrected: Set parent to the new offset object

        else:
            parent = parent[0]

        multmatrix_list = []

        for constraining_obj in constraining_objs:
            print(constraining_objs)
            print(attributes.get_world_matrix(constraining_obj))
            multmatrix = self._mount_system(constraining_obj, parent)
            multmatrix_list.append(multmatrix)

        if len(constraining_objs) > 1:
            name_bm = self._create_blend_matrix(multmatrix_list)
            return name_bm

