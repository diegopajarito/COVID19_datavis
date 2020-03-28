import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import getData

gdp = getData.get_gdp()
confirmed = getData.get_confirmed_aggregated()
data = confirmed.merge(gdp, how='left', left_on='Country/Region', right_on='country_name')

sns.lineplot()
