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
data = getData.get_ins_data_file()

data = data.groupby('city', as_index=False)
data = data['id_case'].count()
data.columns = ['city', 'cases']

# Preparation for text comparison
data['city_key'] = data['city'].str.lower()
boundaries['boundary_key'] = boundaries['NOM_MUNICI'].str.lower()
data.loc[data['city_key'].str.startswith('bogo'), 'city_key'] = 'bogotá, d.c.'
geodata = boundaries.merge(data, how='left', left_on='boundary_key', right_on='city_key')
matched = len(geodata[geodata['city'].notna()])
unmatched = len(data) - matched
print('Matched boundaries: %i. Unmatched boundaries: %i' % (matched, unmatched))


# Plot Individual maps per region
title = 'COVID-19 cases near %s airport(s)'
airport_areas = [['Bogotá', (-76, 3.4, -73, 5.65)],
                 ['Medellín', (-77, 5.7, -75, 7.4)],
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
                 ['Medellín', (-76.8, 5.6, -74.8, 7.1), ax3],
                 ['Cali', (-77, 3.3, -75, 4.8), ax4],
                 ['Bucaramanga - Cúcuta', (-74, 6.9, -72, 8.4), ax5],
                 ['Caribbean Coast', (-76, 9.7, -72.5, 12.325), ax6]]
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