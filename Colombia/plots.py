import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import getData

data = getData.get_ins_data_file()

# cumulative curve
initial_day = data['date'].min()
data['day'] = (data['date'] - initial_day)
data['day'] = data['day']/np.timedelta64(1, 'D')
daily_total = data.groupby(['day'], as_index=False)
daily_total = daily_total['id_case'].count()
daily_total.columns = ['day', 'new_cases']
daily_total['total_cases'] = daily_total['new_cases'].cumsum()
ax = sns.lineplot('day', 'total_cases', data=daily_total)
ax.set(xlabel='Days after first case detected', ylabel='Confirmed cases', title='COVID-19 Colombia')
ax1 = sns.scatterplot('day', 'new_cases', data=daily_total, alpha=0.5)

plt.show()

