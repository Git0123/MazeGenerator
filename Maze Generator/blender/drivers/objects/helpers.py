"""
Stores all the drivers used in the helpers objects
"""


from ..methods import (
    setup_driver,
    DriverProperties,
    DriverVariable,
)
from ....maze_logic.cells import SQUARE, TRIANGLE, HEXAGON, OCTOGON


def setup_drivers(scene, props):
    names = props.mod_names
    obj_cylinder = props.objects.cylinder
    obj_torus = props.objects.torus
    obj_thickness_shrinkwrap = props.objects.thickness_shrinkwrap
    obj_cells = props.objects.cells
    setup_driver(obj_thickness_shrinkwrap, DriverProperties(
        "location",
        [
            DriverVariable("stairs", 'OBJECT', obj_cells,
                           f'modifiers["{names.stairs}"].strength'),
            DriverVariable("thickness", 'OBJECT', obj_cells,
                           f'modifiers["{names.thickness_disp}"].strength'),
        ],
        expression="thickness if stairs > 0 else stairs + thickness",
        prop_to_dim=2))

    # Scale the cylinder and torus objects when scaling the size of the maze
    for i, obj in enumerate((obj_cylinder, obj_torus)):
        exp = 'var * 0.314'
        if props.cell_type == SQUARE or props.cell_type == OCTOGON:
            exp = 'var * 0.15915'
        elif props.cell_type == TRIANGLE:
            if i == 0:
                exp = 'var * 0.07963'
            else:
                exp = 'var * 0.13791'
        elif props.cell_type == HEXAGON:
            if i == 0:
                exp = 'var * 0.2388'
            else:
                exp = 'var * 0.2758'
        setup_driver(
            obj,
            DriverProperties(
                "scale",
                DriverVariable("var", 'SCENE', scene, "mg_props.maze_columns" if i ==
                               0 else "mg_props.maze_rows_or_radius"),
                expression=exp
            ))
