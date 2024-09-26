import pandas as pd

df = pd.read_csv('fcc-forum-pageviews.csv')
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

df

print(df.dtypes)

lower_bound = df['value'].quantile(0.025)
upper_bound = df['value'].quantile(0.975)

df_cleaned = df[(df['value'] >= lower_bound) & (df['value'] <= upper_bound)]

df_cleaned

import matplotlib.pyplot as plt

def draw_line_plot():
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df_cleaned.index, df_cleaned['value'], color='red')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    plt.show()

draw_line_plot()

def draw_bar_plot():
    df_cleaned['year'] = df_cleaned.index.year
    df_cleaned['month'] = df_cleaned.index.month_name()
    df_grouped = df_cleaned.groupby(['year', 'month'])['value'].mean().unstack()
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']
    df_grouped = df_grouped[month_order]
    fig, ax = plt.subplots(figsize=(10, 7))
    df_grouped.plot(kind='bar', ax=ax)
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.set_title('Average Daily Page Views per Month')
    ax.legend(title='Months')
    plt.tight_layout()
    plt.show()

draw_bar_plot()

import seaborn as sns

def draw_box_plot():
    df_box = df_cleaned.copy()
    df_box.reset_index(inplace=True)  
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')  
    df_box['month_num'] = df_box['date'].dt.month  
    df_box = df_box.sort_values('month_num')
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 5))
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1], order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                                                                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')
    plt.tight_layout()
    plt.show()
    
draw_box_plot()







