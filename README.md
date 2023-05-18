## PARCEL UPDATER

the nationwide parcel service needs to be updated and the data needed for the update is provided via ftps from the provider. the bulk of the work is to get all the counties provided (over 3,000) compiled to the state level, and this script accomplishes that task. the below details provide information about each component of the script and also instructions for how to update this dataset.

__main.py__
    
the file where input paramaters are changed, name of the `output_workspace` and where the unzipped `data_dir` (path) exists. to run this programmatic upate process for the parcels, edit and run this main.py file using the esri provided [idle](https://docs.python.org/3/library/idle.html), or another method if you prefer, making sure you have access to the [arcpy](https://pro.arcgis.com/en/pro-app/latest/arcpy/get-started/what-is-arcpy-.htm) package.

__iterator.py__
    
the part of the script that iterates through each county folder and geodatabase provided in `data_dir`, makes a copy of the parcel polygon featureclass if it exists, runs repair geometry on the copied polygon, builds a pre-process count dictionary (`count_dict`), and builds the process dictionary (`process_dict`) used for processing in _compiler.build_. once `process_dict` is compiled, there are some print statements showing counts of gdbs and featureclasses, the dictionaries are written to file for reference, and the _compiler.build_ function is called using `process_dict` as instructions.

__compiler.py__

after much testing, this function is now a simple loop to iterate through the `process_dict` keys, which are state names. it runs _arcpy.management.Merge()_ on the values for each key which is a list of county parcel featureclasses with the full path (you can reference this input dictionary in the output text file from _iterator.py_). once a state has merged, the output polygon featureclass will be in the `output_workspace`.

__counter.py__

the _counter.py_ has two functions within the file. the `post_work` function runs a count for each state featureclass after they have been compiled in the `output_workspace` and appends that number to the `count_dict` for the appropriate state key in the 1 index position. the _counter.py_ file also contains the `write_dict` function which writes the dictionaries to file. when the the `post_work` function runs to get the post count for `count_dict`, it will add a second number to the list for each state key, the first ([0] index) will be the pre process count and the second ([1] index) will be the post process count.
    
    - the pre and post counts are meant to be a simple comparison of pre and post processing results to see if any records have been lost during processing.

__states.py__
    
used for reference in _iterator.py_. this is a python dictionary to retrieve state abbreviations or full state names, depending on which is needed.

__renamer.py__

simple function to batch rename featureclasses before and after importing the updated fcs into the enterprise geodatabase.


### FULL PARCEL UPDATE PROCESS INSTRUCTIONS

1. Run the _iterator.py_ script by opening _main.py_ and editing the required full path variables to point to the latest parcel update directory (`data_dir`) and your project working directory (`output_workspace`). These variables should be a path string with double backslashes (ie. 'G:\\Path\\TO\\YOUR\\DATA'). Running the _iterator.py_ will call all necessary functions for the script to complete so there is no further input required.

2. It will take some time, but when completed your `output_workspace` will have a featureclass for each state, plus the District of Columbia. Prepare the states in your working directory to be copied to the enterprise geodatabase by renaming each one to something different than the production state featureclasses (ie. just add an underscore 1 to the end - 'ALASKA_1'). A short script looping through `output_workspace` should make this easy, something like this:

```
import arcpy
    
arcpy.env.workspace = output_workspace
fc_list = arcpy.ListFeatureclasses()
    
for fc in fc_list:
    arcpy.management.Rename(fc, '{}_1'.format(fc))
```

3. Right-click _parcels.sde_ in the ArcGIS Pro catalog and choose __Import --> Featureclasses__ or you can run a script to copy each one from your local working directory to the production _parcels.sde_ geodatabase.    
    
    __NOTE:__ copying this data to the SDE might be best performed during off peak hours due to some strain it will have on the RDS.

4. Now, STOP the parcels service using ArcGIS Server Manager, then run the sql code below within [PGAdmin](https://www.pgadmin.org/) to remove schema lock connections on the _parcels.sde_ production database. 
    
    __NOTE:__ this should also be performed during offpeak hours in order to avoid user disruption.
    
```
DELETE FROM egdb.sde.SDE_process_information;
DELETE FROM egdb.sde.SDE_layer_locks;
DELETE FROM egdb.sde.SDE_state_locks;
DELETE FROM egdb.sde.SDE_table_locks;
DELETE FROM egdb.sde.SDE_object_locks;
```

5. Once the production parcel service has been stopped, RENAME all production state featureclasses to, for example, an underscore 2 ('ALASKA_2') and rename your imported new updated state featureclasses to what the production featureclasses were named (ie. without an underscore 1; see #2 above and you can use the provided code above or similar).

6. ~~Time to run the SQL to create the national parcel view, parcels.sde.lightbox_us_view. The SQL to do this is located [here](https://github.com/aypapower/GIS/blob/dev/sql/archive/lightbox_us_view_v4.sql). Open PGAdmin to run the SQL, or if you prefer using ArcGIS Pro to create the view, you should be able to do it there.~~

7. ~~Register the view with the geodatabase by finding it in the ArcGIS Pro catalog and right-clicking to select 'Register with Geodatabase'. The view_id should be used as the unique objectid.~~

    __NOTE:__ As of early 2023 (January parcel update), steps 6 & 7 above have been excluded from this workflow due to issues with the national parcel database view. Now, a __Merge__ geoprocess is run on all states to create one national parcel featureclass, `parcels.sde.lightbox_us_all`.

8. Restart the parcels service and check that it is working properly. If not, open up the parcels service map document, double-click the layer and make sure it is sourced to the view in the _parcels.sde_ database, then overwrite publish the parcel service.
