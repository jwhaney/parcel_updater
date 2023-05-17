import arcpy
import os, sys
from states import state_ref
from compiler import build
from counter import *


def dict_creator(st, process_dict, c, count_dict, p):
    try:
        if st in process_dict:
            print('Appending {} to {} key in process_dict'.format(c, st))
            count_dict[st] = [int(count_dict[st][0]) + int(arcpy.management.GetCount(c).getOutput(0))]
            process_dict[st].append(p)

        elif st not in process_dict:
            print('Creating {} key with {} in process_dict'.format(st, c))
            count_dict[st] = [int(arcpy.management.GetCount(c).getOutput(0))]
            process_dict[st] = [p]

    except Exception as e:
        sys.exit('iterator.dict_creator function error:', e)


def floop(data_dir, workspace):
    try:
        gdb_count = 0
        fc_count = 0
        fc_pass_list = []
        other_list = []
        count_dict = {}
        process_dict = {}

        for folder in os.listdir(data_dir):
            d = os.path.join(data_dir, folder)

            for f in os.listdir(d):
                if f.endswith('.gdb') and state_ref[f.split('_')[0]]:
                    st = state_ref[f.split('_')[0]]
                    gdb_count+=1
                    gdb = os.path.join(d, f)

                    arcpy.env.workspace = gdb
                    fc_list = arcpy.ListFeatureClasses(feature_type='Polygon')
                    exists = [i for i in fc_list if '_copy' in i]

                    if len(exists) == 1:
                        fc_count += 1
                        c = exists[0]
                        print('{} already exists. Moving on...'.format(c))
                        p = os.path.join(gdb, c)
                        # call dict_creator function to write data to dictionaries
                        dict_creator(st, process_dict, c, count_dict, p)

                    elif len(fc_list) == 1:
                        fc_count += 1
                        c = '{}_copy'.format(fc_list[0])
                        # create copy before running repair geom
                        arcpy.management.Copy(fc_list[0], c)
                        print('Repairing geom for {}.'.format(c))
                        arcpy.management.RepairGeometry(c, 'DELETE_NULL', 'OGC')
                        p = os.path.join(gdb, c)
                        # call dict_creator function to write data to dictionaries
                        dict_creator(st, process_dict, c, count_dict, p)

                else:
                    other_list.append(f)


        print('gdb_count:', gdb_count)
        print('fc_count:', fc_count)
        print('other_list length:', len(other_list))

        # call counter.write function to write precount dictionary to file
        print('Calling write function to write precount dictionary to file.')
        cn = 'count_dict_pre'
        write_dict(cn, count_dict)

        # call counter.write function to write process_dict to file
        print('Calling write function to write process_dict to file for backup.')
        pn = 'process_dict'
        write_dict(pn, process_dict)
        
        # call compiler.build function to start merge process
        print('Process dictionary compiled, sending to build function.')
        build(workspace, process_dict)

        # call counter.post_work function
        print('Calling post_work function to create and write postcount dictionary to file.')
        post_work(workspace, count_dict)

    except Exception as e:
        sys.exit('iterator.floop function error:', e)