import arcpy
import sys, json


def post_work(workspace, count_dict):
    # get post count and create new count_dict instance with appended post count; write to file
    try:
        arcpy.env.workspace = workspace
        fc_list = arcpy.ListFeatureClasses()
        cname = 'count_dict_post'

        for fc in fc_list:
            # get post repair geom record count to append to count_dict
            desc = arcpy.Describe(fc)
            count_dict[desc.name].append(int(arcpy.management.GetCount(fc).getOutput(0)))

        # call counter.write_dict function to write count_dict to file
        write_dict(cname, count_dict)

    except Exception as e:
        sys.exit('counter.post_work function error:', e)


def write_dict(name, my_dict):
    # write the dictionary to text file with newline to seperate each key/value pair
    print('Writing {}.txt'.format(name))
    try:
        with open('{}.txt'.format(name), 'w') as data:
            data.write("{\n")
            for k in my_dict.keys():
                data.write("{}:{}\n".format(k, my_dict[k]))
            data.write("}")
            data.close()

    except Exception as e:
        sys.exit('counter.write_dict function error:', e)
