import geopandas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import getData

boundaries = 'data/municipios.geojson'
boundaries_region = 'data/departamentos.geojson'
airports = 'data/aeropuertos.geojson'
boundaries = geopandas.read_file(boundaries)
boundaries_region = geopandas.read_file(boundaries_region)
airports = geopandas.read_file(airports)
data = getData.get_ins_data()

data = data.groupby('divipola', as_index=False)
data = data['id_case'].count()
data.columns = ['divipola', 'cases']

# Preparation for text comparison
boundaries['divipola'] = boundaries['COD_DANE'].astype(int)
geodata = boundaries.merge(data, how='left', left_on='divipola', right_on='divipola')
matched = len(geodata[geodata['divipola'].notna()])
unmatched = len(data) - matched
print('Matched boundaries: %i. Unmatched boundaries: %i' % (matched, unmatched))


# Plot Individual maps per region
title = 'COVID-19 cases near %s airport(s)'
airport_areas = [['Bogotá', (-76, 3.4, -73, 5.65)],
                 ['Antioquia - Chocó', (-76.5, 5.5, -75.5, 7.4)],
                 ['Cali', (-77, 3.3, -75, 4.8)],
                 ['North-East', (-74, 6.9, -72, 8.4)],
                 ['Caribbean Coast', (-76, 9.7, -72.5, 12.325)]]
geodata = geodata[geodata['cases'] > 0]
geodata['cases_log'] = np.log10(geodata['cases'])
# Single plot with region maps
title = 'COVID-19 confirmed cases & int. airports in Colombia (Bogotá)'
fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=(7, 9))
gs = ax1.get_gridspec()
ax1.remove()
ax2.remove()
ax1 = fig.add_subplot(gs[0, 0:])
airport_areas = [['  ', (-77, 3.3, -72, 5.4), ax1],
                 ['Antioquia - Chocó', (-77.8, 5, -74.5, 7.1), ax3],
                 ['Bucaramanga - Cúcuta', (-73.5, 6.9, -72, 8.4), ax4],
                 ['Caribbean Coast', (-76, 9.5, -72, 12.325), ax5],
                 ['Pacific Coast', (-77.8, 2.7, -74.8, 5), ax6]]
for region in airport_areas:
    limits = region[1]
    xlim = (limits[0], limits[2])
    ylim = (limits[1], limits[3])
    ax = region[2]
    base = boundaries.plot(ax=ax, color='black', edgecolor='gray', linewidth=0.2)
    boundaries_region.plot(ax=base, color='None', edgecolor='gray', linewidth=0.8)
    if ax == ax1:
        geodata.plot(ax=base, column='cases_log', cmap='OrRd', legend=True, legend_kwds={'label': "Log(x) Cases"})
    else:
        geodata.plot(ax=base, column='cases_log', cmap='OrRd', legend=False)
    airports[airports['internac'] == '1'].plot(ax=base, marker='o', color='cyan', legend=True, markersize=8, alpha=0.7)
    ax.tick_params(labelbottom=False, labelleft=False, left=False, bottom=False)
    ax.set_facecolor('black')
    ax.set_title(region[0])
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
fig.suptitle(title, fontsize=13)
fig.tight_layout()
plt.show()
plt.savefig('maps/map_contagion_airports.png')
plt.close()

print('Done')