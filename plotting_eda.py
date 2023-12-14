import matplotlib.pyplot as plt
import seaborn as sns
import os
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import pandas as pd

file_to_read='Date_for_plot.csv'

if not os.path.exists("%s" % ('plotting_Eda')):
    os.makedirs("%s" % ('plotting_Eda'))

# Load data from a CSV file
data = pd.read_csv(file_to_read)

data.head()
sns.set(rc={"figure.figsize":(15,8)})

flierprops = dict(marker='o', markersize=5, markeredgecolor='black', markerfacecolor='green', alpha=0.5)


#temperature
p = sns.boxplot(x='occ', y='temp', data=data, flierprops=flierprops)
p.set_xlabel('Occupancy', fontsize= 14, fontweight='bold')
p.set_ylabel('Temperature', fontsize= 14, fontweight='bold')

plt.savefig('plotting_Eda/box_plot_temp.pdf', format="pdf", bbox_inches="tight")
plt.savefig('plotting_Eda/box_plot_temp.eps', format='eps')
plt.savefig('plotting_Eda/box_plot_temp.svg', format='svg', dpi=1200)

#humidity
p = sns.boxplot(x='occ', y='humidity', data=data, flierprops=flierprops)
p.set_xlabel('Occupancy', fontsize= 14, fontweight='bold')
p.set_ylabel('Humidity', fontsize= 14, fontweight='bold')
plt.ylim(0, 40)
plt.savefig('plotting_Eda/box_plot_humidity.pdf', format="pdf", bbox_inches="tight")
plt.savefig('plotting_Eda/box_plot_humidity.eps', format='eps')
plt.savefig('plotting_Eda/box_plot_humidity.svg', format='svg', dpi=1200)

#light
p = sns.boxplot(x='occ', y='light', data=data, flierprops=flierprops)
p.set_xlabel('Occupancy', fontsize= 14, fontweight='bold')
p.set_ylabel('Light', fontsize= 14, fontweight='bold')
plt.ylim(0, 1500)
plt.savefig('plotting_Eda/box_plot_light.pdf', format="pdf", bbox_inches="tight")
plt.savefig('plotting_Eda/box_plot_light.eps', format='eps')
plt.savefig('plotting_Eda/box_plot_light.svg', format='svg', dpi=1200)

#CO2
p = sns.boxplot(x='occ', y='co2', data=data, flierprops=flierprops)
p.set_xlabel('Occupancy', fontsize= 14, fontweight='bold')
p.set_ylabel('CO2', fontsize= 14, fontweight='bold')
plt.ylim(0, 5000)
plt.savefig('plotting_Eda/box_plot_co2.pdf', format="pdf", bbox_inches="tight")
plt.savefig('plotting_Eda/box_plot_co2.eps', format='eps')
plt.savefig('plotting_Eda/box_plot_co2.svg', format='svg', dpi=1200)

#############scatter######################
sns.set(rc={"figure.figsize":(15,8)})

fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(10, 4))
ax1.scatter(data['temp'], data['occ'])
ax1.set_xlabel('Temperature (C)')
ax1.set_ylabel('Occupancy')
ax2.scatter(data['humidity'], data['occ'])
ax2.set_xlabel('Humidity (%)')
ax2.set_ylabel('Occupancy')
ax2.set(xlim=(0, 40))
ax3.scatter(data['co2'], data['occ'])
ax3.set_xlabel('CO2 (ppm)')
ax3.set_ylabel('Occupancy')
ax4.scatter(data['light'], data['occ'])
ax4.set_xlabel('Light')
ax4.set_ylabel('Occupancy')

plt.savefig('plotting_Eda/scatter_plot.pdf', format="pdf", bbox_inches="tight")
plt.savefig('plotting_Eda/scatter_plot.eps', format='eps')
plt.savefig('plotting_Eda/scatter_plot.svg', format='svg', dpi=1200)
plt.show()

