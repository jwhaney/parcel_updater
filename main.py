from iterator import floop
import count_analysis1
import count_analysis2
from renamer import rename

# setup variables
data_dir = 'DRIVE:\\PARCEL\\DATA\\LIVES\\HERE\\'
out_workspace = 'parcel_update.gdb'
parcels_sde = 'parcel_enterprise_gdb.sde'

# run the repair function first which then calls the state_compiler
run = floop(data_dir, out_workspace)

# run rename function
# r = rename(parcels_sde)
