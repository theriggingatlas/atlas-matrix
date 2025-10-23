# -*- coding: utf-8 -*-
""" DEP class to use constraint parent matrix inside Maya

This module provides the `ParentCon` class, which allows precise matrix-based constraint
over objects using matrix nodes in Maya. It inherits from Matrix class.

Author: Clement Daures
Company: The Rigging Atlas
Website: theriggingatlas.com
Created: 2025
"""


# ---------- IMPORT ----------


from typing import Optional, List, Union, Tuple, Callable
from dataclasses import dataclass

from core.matrix import Matrix


# ---------- DATA CLASS ----------


@dataclass
class AxisFilter:
    x: bool = True
    y: bool = True
    z: bool = True


@dataclass
class AxisWeights:
    translate: float = 1.0
    rotate: float = 1.0
    scale: float = 1.0
    shear: float = 1.0


# ---------- MAIN CLASS ----------


class ParentCon(Matrix):
    """"
    Class to create a matrix-based parent constraint in Maya.

    This constraint system uses multMatrix, decomposeMatrix, and optionally
    pickMatrix, holdMatrix, and blendMatrix nodes for precise control over
    transformations.
    """
    def __init__(
            self,
            driven: Optional[str] = None,
            drivers: Optional[List[str]] = None,
            *,
            offset: bool = False,
            keep_hold: bool = False,
            envelope: bool = False,
            translate_filter: AxisFilter = AxisFilter(),
            rotate_filter: AxisFilter = AxisFilter(),
            scale_filter: AxisFilter = AxisFilter(),
            shear_filter: AxisFilter = AxisFilter(),
            weights: AxisWeights = AxisWeights()
    ):
        """
        Initialize the ParentCon constraint setup.

        Args:
            driven (Optional[str]): The name of the driven object.
            drivers (Optional[List[str]]): A list of driver object names.
        """
        super().__init__(driven, drivers)
        self.constraint_type="parent"
        self.offset = offset
        self.keep_hold = keep_hold
        self.envelope = envelope

        self.translate_filter = translate_filter
        self.rotate_filter = rotate_filter
        self.scale_filter = scale_filter
        self.shear_filter = shear_filter
        self.weights = weights


    def _mount_offset(self, driver: str):
        """
        Mount the necessary setup for the offset system

        Args:
            driver (str): The name of the driver object
        """
        # Create temporary mult to get the value of the offset
        mult_tmp_node, mult_tmp_in, mult_tmp_out = self.con_mult_matrix(f"tmp_{driver}")

        self.connect_attr(self.get_world_matrix(self.driven), mult_tmp_in(0))
        self.connect_attr(self.get_inverse_world_matrix(driver), mult_tmp_in(1))

        return mult_tmp_node, mult_tmp_in, mult_tmp_out


    def create_offset(self, driver: str, mult_in: Callable[[int], str]):
        """
        Create the wanted offset type

        Args:
            driver (str): The name of the driver object name
            mult_in(str): The in attribute of the multMatrix with great index.
        """
        if self.offset:
            mult_tmp_node, mult_tmp_in, mult_tmp_out = self._mount_offset(driver)
            if self.keep_hold:
                hold_node, hold_in, hold_out = self.hold_matrix(driver)
                self.get_set_attr(mult_tmp_out, hold_in)
                self.connect_attr(hold_out, mult_in(0))
            else:
                self.get_set_attr(mult_tmp_out, mult_in(0))
        else:
            pass


    def create_compose(self):
        """
        Create a composeMatrix if needed
        """
        pass


    def mount_system(self):
        """
        Internal setup to create the constraint chain and connect it.
        """
        parent_node = self.get_parent_driven()[0]
        parent_inverse = self.get_inverse_world_matrix(parent_node)

        mult_outs = []

        # Setup of the mult system
        for index, driver in enumerate(self.drivers):
            mult_node, mult_in, mult_out = self.con_mult_matrix(driver)
            self.connect_attr(self.get_world_matrix(driver), mult_in(1))
            self.connect_attr(parent_inverse, mult_in(2))

            # Generate offset
            self.create_offset(driver, mult_in)

            mult_outs.append(mult_out)

        # Setup of the blend system
        if len(self.drivers) > 1 or self.envelope:
            blend_node, blend_input, blend_in, blend_out = self.con_blend_matrix()
            for index, mult_out in enumerate(mult_outs):
                self.connect_attr(mult_outs[index], blend_in(index))
                self.connect_attr(blend_out, self.get_offset_parent_matrix(self.driven))
        # End connection if no blend created
        else:
            self.connect_attr(mult_outs[0], self.get_offset_parent_matrix(self.driven))