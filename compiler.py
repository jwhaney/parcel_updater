import arcpy
import os, sys


def build(workspace, process_dict):
    # compile state parcel featureclasses by merging list of values for
    # each state key in process_dict
    try:
        arcpy.env.workspace = workspace
        
        # run merge on each key in process_list dictionary
        for i in process_dict.keys():
            print('Merge process running for: {}'.format(i))
            arcpy.management.Merge(process_dict[i], os.path.join(workspace, i))

    except Exception as e:
        sys.exit('compiler.build function error:', e)

