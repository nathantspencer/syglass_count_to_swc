import csv
import sys
import os
import syglass as sy
from syglass import pyglass as py


# Modify TYPE_MAPPING to set the type of SWC node to be created
# for a given counting point color.

TYPE_MAPPING = {
    "Red"    : 0,
    "Orange" : 0,
    "Yellow" : 0,
    "Green"  : 0,
    "Cyan"   : 0,
    "Blue"   : 0,
    "Violet" : 0
}

# Modify RADIUS_MAPPING to set the radius of the SWC node to be
# created for a given counting point color.

RADIUS_MAPPING = {
    "Red"    : 1.0,
    "Orange" : 1.0,
    "Yellow" : 1.0,
    "Green"  : 1.0,
    "Cyan"   : 1.0,
    "Blue"   : 1.0,
    "Violet" : 1.0
}

TEMP_FILE_NAME = "temp.swc"


def get_project(project_path: str) -> sy.Project:
    if not sy.is_project(project_path):
        raise ValueError("Project path is invalid")
    return sy.get_project(project_path)


def main(project_path: str):
    project = get_project(project_path)
    counts = project.get_counting_points()
    print("Successfully opened project.")

    # write temp SWC file containing remapped points
    with open(TEMP_FILE_NAME, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=' ')
        node_id = 1
        for color in TYPE_MAPPING:
            for point in counts[color]:
                csv_writer.writerow([str(node_id), str(TYPE_MAPPING[color]), point[2], point[1],
                    point[0], str(RADIUS_MAPPING[color]), "-1"])
                node_id = node_id + 1
        if node_id == 1:
            print("No counting points found.")
        else:
            print(f"Converted {node_id - 1} counting points to SWC nodes.")

    # adjust project coordinate frame and import temp SWC
    voxel_size = project.impl.GetVoxelSize()
    ivec3_dimensions = project.impl.GetProjectDimensionsInUnitVoxels()
    vec3_dimensions = py.vec3(ivec3_dimensions.x, ivec3_dimensions.y, ivec3_dimensions.z)
    frame = py.CoordinateFrame(voxel_size, vec3_dimensions)
    frame.SetOrigin(py.CoordinateFrame.BottomLeft)
    frame.SetUnits(py.CoordinateFrame.Voxels)
    project.impl.SetCoordinateFrame(frame)
    project.import_swcs([TEMP_FILE_NAME], "default")

    # clean up temporary files
    os.remove(TEMP_FILE_NAME)
    print("Finished!")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python count_to_swc.py [path/to/project.syg]")
    else:
        main(sys.argv[1])
