import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import squarify
import getData

data = getData.get_ins_data_file()

# Total cases per region
initial_day = data['date'].min()
data['day'] = (data['date'] - initial_day)
data['day'] = data['day']/np.timedelta64(1, 'D')
region_total = data.groupby(['region'], as_index=False)
region_total = region_total['id_case'].max()
region_total.columns = ['region', 'total_cases']
squarify.plot(sizes=region_total['total_cases'], label=region_total['region'], alpha=0.7)
plt.axis('off')
plt.show()
plt.close()

# cases per region animation
for day in data['day'].unique():
    region_day = data[data['day'] < day].groupby(['region'], as_index=False)
    region_day = region_day['id_case'].max()
    region_day.columns = ['region', 'total_cases']
    squarify.plot(sizes=region_day['total_cases'], label=region_day['region'], alpha=0.7)
    plt.axis('off')
    plt.title('Confirmed COVID-19 Cases in Colombia per region. Day %i' % day)
    plt.show()
    #plt.savefig('plots/total_cases_region.png')
    plt.close()

# cumulative curve per treatment
total_treatment = data.groupby(['day', 'treatment'], as_index=False)
total_treatment = total_treatment['id_case'].count()
total_treatment.columns = ['day', 'treatment', 'new_cases']
total_treatment['total_treatment'] = total_treatment.groupby('treatment')['new_cases'].transform(pd.Series.cumsum)
ax = ax = sns.lineplot('day', 'total_treatment', data=total_treatment, hue='treatment')
ax.set(xlabel='Days after first case detected', ylabel='Confirmed cases', title='COVID-19 Colombia')
plt.savefig('plots/total_cases_treatment.png')
plt.close()

# Cumulative curve per day
image_size = []
xlim = daily_total['day'].max() + 1
ylim = daily_total['total_cases'].max() + 10
images = []
for day in daily_total['day']:
    title = 'Confirmed cases COVID-19 in Colombia. Day %i' % day
    ax = sns.lineplot('day', 'total_cases', data=daily_total[daily_total['day'] <= day])
    ax.set(xlabel='Days after first case detected', ylabel='Confirmed cases',
           xlim=(0, xlim), ylim=(0, ylim), title=title)
    ax1 = sns.scatterplot('day', 'new_cases', data=daily_total[daily_total['day'] <= day], alpha=0.5)
    plt.savefig('plots/confirmed_cases_%i.png'% day)
    plt.close()
    #images.append(ax.get_figure())

# for animation visit this https://towardsdatascience.com/how-to-create-animated-graphs-in-python-bb619cc2dec1
# for filename in images:
#     images.append(imageio.imread(filename))
# imageio.mimsave('/plots/confirmed_cases.gif', images)
