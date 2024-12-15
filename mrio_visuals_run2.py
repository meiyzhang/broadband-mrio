import pymrio  
import os
import matplotlib.pyplot as plt  
import numpy as np  
import seaborn as sns  
import plotly.graph_objects as go  
  
eora_path = 'C:/Users/megan/mz_codes/Eora26_2022_bp'  
eora26 = pymrio.parse_eora26(eora_path, year=2022)  
  
x_array = np.array(eora26.x)  
  
# Cleaning x array  
if np.any(x_array == 0):  
   mean_value = np.nanmean(x_array[x_array != 0])  
   x_array[x_array == 0] = mean_value  
   eora26.x = x_array  
  
eora26.calc_all()  
eora26.calc_extensions()  # for the environmental extensions  
  
if eora26.A is None:  
   print("The input-output table is not available.")  
else:  
   regions = eora26.A.index.get_level_values(0).unique()  
   sectors = eora26.A.index.get_level_values(1).unique()  
   io_table = eora26.A  
   fd_table = eora26.Y  
   leontief_inverse = eora26.L  
   print(io_table)  
   footprint = eora26.x  
   eora26 = pymrio.parse_eora26(eora_path, year=2022)  
   carbon_footprint = eora26.get_extensions()  
  
   carbon_footprint_df = np.array(carbon_footprint)  
   print("Done at this step.")  
  
downsampled_io_table = io_table.sample(frac=0.1, axis=0).sample(frac=0.1, axis=1)  
  
# Visualize the downsampled data using plotly  
fig = go.Figure(data=go.Heatmap(  
   z=downsampled_io_table.values,  
   x=downsampled_io_table.columns,  
   y=downsampled_io_table.index,  
   colorscale='Blues'  
))  
  
fig.update_layout(  
   title='Input-Output Table',  
   xaxis_title='Sectors',  
   yaxis_title='Regions'  
)  
  
fig.write_image('io_table_heatmap.png')  
print("IO table heatmap exported to io_table_heatmap.png")

plt.figure(figsize=(10, 8))  
sns.heatmap(fd_table, annot=True, cmap="Blues")  
plt.title("Final Demand Table")  
plt.xlabel("Sectors")  
plt.ylabel("Regions")  
plt.savefig("fd_table_heatmap.png", bbox_inches='tight')  
print("FD table heatmap exported to fd_table_heatmap.png")  
 
plt.figure(figsize=(10, 8))  
sns.heatmap(leontief_inverse, annot=True, cmap="Blues")  
plt.title("Leontief Inverse Table")  
plt.xlabel("Sectors")  
plt.ylabel("Regions")  
plt.savefig("leontief_inverse_heatmap.png", bbox_inches='tight')  
print("Leontief inverse heatmap exported to leontief_inverse_heatmap.png")  
 
plt.figure(figsize=(10, 8))  
sns.heatmap(footprint, annot=True, cmap="Blues")  
plt.title("Footprint Table")  
plt.xlabel("Sectors")  
plt.ylabel("Regions")  
plt.savefig("footprint_heatmap.png", bbox_inches='tight')  
print("Footprint heatmap exported to footprint_heatmap.png")  