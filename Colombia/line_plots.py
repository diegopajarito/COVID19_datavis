import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import getData

data = getData.get_ins_data()

# cumulative curve
initial_day = data['fis'].min()
data['day'] = (data['fis'] - initial_day)
data['day'] = data['day']/np.timedelta64(1, 'D')
daily_total = data.groupby(['day'], as_index=False)
daily_total = daily_total['id_case'].count()
daily_total.columns = ['day', 'new_cases']
daily_total['total_cases'] = daily_total['new_cases'].cumsum()
ax = sns.lineplot('day', 'total_cases', data=daily_total)
ax1 = sns.scatterplot('day', 'new_cases', data=daily_total, alpha=0.5, label='New Cases')
ax.set(xlabel='Days after symptoms reported (FIS)', ylabel='Confirmed cases', title='COVID-19 Colombia')
plt.savefig('plots/total_cases.png')
plt.show()
plt.close()

# cumulative curve per origin
total_origin = data.groupby(['day', 'origin'], as_index=False)
total_origin = total_origin['id_case'].count()
total_origin.columns = ['day', 'origin', 'new_cases']
total_origin['total_origin'] = total_origin.groupby('origin')['new_cases'].transform(pd.Series.cumsum)
ax = ax = sns.lineplot('day', 'total_origin', data=total_origin, hue='origin')
ax.set(xlabel='Days after symptoms reported (FIS)', ylabel='Confirmed cases', title='COVID-19 Colombia')
plt.savefig('plots/total_cases_origin.png')
plt.close()

# cumulative curve per treatment
total_treatment = data.groupby(['day', 'treatment'], as_index=False)
total_treatment = total_treatment['id_case'].count()
total_treatment.columns = ['day', 'treatment', 'new_cases']
total_treatment['total_treatment'] = total_treatment.groupby('treatment')['new_cases'].transform(pd.Series.cumsum)
ax = ax = sns.lineplot('day', 'total_treatment', data=total_treatment, hue='treatment')
ax.set(xlabel='Days after symptoms reported (FIS)', ylabel='Confirmed cases', title='COVID-19 Colombia')
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
    ax.set(xlabel='Days after symptoms reported (FIS)', ylabel='Confirmed cases',
           xlim=(0, xlim), ylim=(0, ylim), title=title)
    ax1 = sns.scatterplot('day', 'new_cases', data=daily_total[daily_total['day'] <= day], alpha=0.5)
    plt.savefig('plots/confirmed_cases_%i.png'% day)
    plt.close()
    #images.append(ax.get_figure())

# for animation visit this https://towardsdatascience.com/how-to-create-animated-graphs-in-python-bb619cc2dec1
# for filename in images:
#     images.append(imageio.imread(filename))
# imageio.mimsave('/plots/confirmed_cases.gif', images)
