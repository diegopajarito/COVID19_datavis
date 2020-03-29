import geopandas
import pandas as pd
import matplotlib.pyplot as plt
import getData

boundaries = 'data/municipios.geojson'
airports = 'data/aeropuertos.geojson'
boundaries = geopandas.read_file(boundaries)
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

fig, ax = plt.subplots(1, 1)
base = boundaries[boundaries['NOM_DEPART'] == 'CUNDINAMARCA'].plot(ax=ax, color='black', edgecolor='white')
geodata = geodata[(geodata['NOM_DEPART'] == 'CUNDINAMARCA') & (geodata['cases'] > 0)]
geodata.plot(ax=base, column='cases', legend=True,
             legend_kwds={'label': "Confirmed cases per municipality", 'orientation': "horizontal"})
airports[airports['lugar'] == 'Bogotá'].plot(ax=base, marker='x', color='red', markersize=3)
plt.show()
plt.savefig('maps/map_cases.png')

print('Done')