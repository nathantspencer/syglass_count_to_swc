# syglass_count_to_swc
Converts syGlass project counting points to SWC nodes and imports them into the project. Preserves the counting points in the process.

## Usage
Modify the `TYPE_MAPPING` and `RADIUS_MAPPING` in the script to indicate what SWC node type and radius should be associated with a given counting point color.

Then run the script as shown below:

```
python count_to_swc.py [path/to/syglass_project.syg]
```

Please ensure that the project is not already open in syGlass when the script is run. Only one process can effectively open a syGlass project at one time.
