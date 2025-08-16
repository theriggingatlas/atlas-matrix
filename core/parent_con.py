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
    def __init__(self, object_list=None, bm_translate=1, bm_rotate=1, bm_scale=1, offset=False, pick_mat=False, pm_translate=False, pm_rotate=False, pm_scale=False):
        self.blend_matrix_node = None
        self.bm_translate = bm_translate
        self.bm_rotate = bm_rotate
        self.bm_scale = bm_scale

        self.pick_mat = pick_mat
        self.pm_translate = pm_translate
        self.pm_rotate = pm_rotate
        self.pm_scale = pm_scale

        self.node = nodes.Matrix()

        self.offset = offset
        self.object_list = object_list or cmds.ls(selection=True)
        self.constrained_obj = self.object_list[-1]



    def hold_matrix(self, constrainer, constrained, hm_name):
        mm_name = "tmp_multmatrix"

        out_mm = self.node.mult_matrix([attributes.get_world_matrix(constrained), attributes.get_world_inverse_matrix(constrainer)], name=mm_name)
        self.node.hold_matrix(input=mm_name, name=hm_name)

        existing_connections = cmds.listConnections(attributes.get_in_matrix(hm_name), s=True, d=False, p=True)
        if existing_connections:
            cmds.disconnectAttr(out_mm, attributes.get_in_matrix(hm_name))
        cmds.delete(mm_name)
        return f"{hm_name}.outMatrix"


    def _mount_system(self, constraining_obj, parent):
        existing_connections = cmds.listConnections(attributes.get_offset_parent_matrix(self.constrained_obj), s=True, d=False, p=True)
        if existing_connections:
            for connection in existing_connections:
                print(f"Disconnecting {connection} from {self.constrained_obj}.offsetParentMatrix")
                cmds.disconnectAttr(connection, attributes.get_offset_parent_matrix(self.constrained_obj))

        if self.pick_mat:
            pm_name = f"pickmatrix_{self.constrained_obj}_constrainedby_{constraining_obj}"
            out_pm = self.node.pick_matrix(input=attributes.get_world_matrix(constraining_obj), name=pm_name, pm_translate=self.pm_translate, pm_rotate=self.pm_rotate, pm_scale=self.pm_scale)
            primary_world = out_pm
        else:
            primary_world = attributes.get_world_matrix(constraining_obj)

        if self.offset:
            hm_name = f"holdmatrix_{self.constrained_obj}_constrainedby_{constraining_obj}"
            out_hm = self.hold_matrix(constrainer=constraining_obj,constrained=self.constrained_obj, hm_name=hm_name)
            multmatrix_list = [out_hm, primary_world, attributes.get_world_inverse_matrix(parent)]
        else:
            multmatrix_list = [primary_world, attributes.get_world_inverse_matrix(parent)]

        mm_name = f"multmatrix_{self.constrained_obj}_constrainedby_{constraining_obj}"
        out_mm = self.node.mult_matrix(multmatrix_list, name=mm_name)

        cmds.connectAttr(out_mm, attributes.get_offset_parent_matrix(self.constrained_obj))
        transform.idtransform(self.constrained_obj)

        return  mm_name


    def _bm_weights(self):

        if not self.blend_matrix_node or not cmds.objExists(self.blend_matrix_node):
            print(" Error: Blend Matrix node does not exist. Skipping weight update.")
            return

        target_count = cmds.getAttr(f"{self.blend_matrix_node}.target", size=True)

        if target_count == 0:
            print(f" Warning: Blend Matrix '{self.blend_matrix_node}' has no targets. Skipping weight updates.")
            return

        for i in range(target_count):
            cmds.setAttr(f"{self.blend_matrix_node}.target[{i}].translateWeight", self.bm_translate)
            cmds.setAttr(f"{self.blend_matrix_node}.target[{i}].rotateWeight", self.bm_rotate)
            cmds.setAttr(f"{self.blend_matrix_node}.target[{i}].scaleWeight", self.bm_scale)
        print(
            f"Set target[{i}] weights -> Translate: {self.bm_translate}, Rotate: {self.bm_rotate}, Scale: {self.bm_scale}")


    def _create_blend_matrix(self, multmatrix_list):

        bm_name = f"blendmat_{self.constrained_obj}"
        self.blend_matrix_node = cmds.createNode("blendMatrix", name=bm_name)

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
        return bm_name

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
            bm_name = self._create_blend_matrix(multmatrix_list)
            return bm_name

