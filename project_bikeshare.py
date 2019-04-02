import time
import pandas as pd
import numpy as np
from datetime import timedelta

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    """

    print('\nHello! Let\'s explore some US bikeshare data.\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while(1):
        print('Please type a city to explore :\'Chicago\' or \'New York City \' or \'Washington \'.')
        fir_string=input('Type a city..\n')
        string=fir_string.lower()
        if (string == 'chicago' or string =='new york city' or string=='washington'):
            print('Thank you.')
            break
        else:
            print('Please type more carefully!')
            continue
    city=string


    # get user input for month (all, january, february, ... , june)
    months = ['all','january', 'february', 'march', 'april', 'may', 'june']
    while (1):
        print('\nPlease type the month to filter by from January to June  \nor type \"all\" to apply no month filter.')
        fir_string = input('Type a month..\n')
        string = fir_string.lower()
        if (string not in months):
            print('Please type more carefully!')
            continue
        else:
            print('Thank you.')
            break

    month = string



    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday','wednesday','thursday', 'friday', 'saturday', 'sunday']
    while (1):
        print('\nPlease type the name of the day of week to filter by for example \'Monday\' \nor type \"all\" to apply no day filter.')
        fir_string = input('Type a day..\n')
        string=fir_string.lower()
        if (string not in days):
            print('Please type more carefully!')
            continue
        else:
            print('Thank you.')
            break
    day=string


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    """
    df=pd.read_csv(CITY_DATA[city])
    print('Loading...\n')
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if(month=='all' and day=='all'):
        return df
    elif(month != 'all' and day!='all'):
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df.loc[(df['month'] == month) & (df['day_of_week'] == day.title())]
        df=df.dropna()
        df = df.reset_index(drop=True)
        return df
    elif(day != 'all' and month=='all'):
        df = df.loc[df['day_of_week'] == day.title()]
        return df
    elif(day == 'all' and month !='all'):
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df.loc[df['month'] == month]
        return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('-' * 40)
    print('\nCalculating statistics on the most frequent times of travel.\n')
    start_time = time.time()

    # display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    temp=df['hour'].value_counts().reset_index(drop=True)
    print('The most common hour to start cycling is ' +str(popular_hour) +':00.\tObservations:' +str(temp[0])  + '\n')


    # display the most common day of week
    popular_day=df['day_of_week'].mode()[0]
    temp = df['day_of_week'].value_counts().reset_index(drop=True)
    print('The most common day of the week is ' + str(popular_day)  +'.\tObservations:' +str(temp[0])  + '\n')


    # display the most common month
    popular_month = df['month'].mode()[0]
    temp = df['month'].value_counts().reset_index(drop=True)
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    final_month = months[popular_month-1]

    print('and the most common month is ' + (str(final_month).title()) +'.\tObservations:' +str(temp[0])  + '\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating statistics on the most popular stations ..\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    #variable=df['Start Station'].describe()
    variable2=df['Start Station'].value_counts().reset_index(drop=True)
    print('The most common Start Station for cycling is ' + str(popular_start_station) + '.\tObservations:' +str(variable2[0])  + '\n')



    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    #variable = df['End Station'].describe()
    variable2 = df['End Station'].value_counts().reset_index(drop=True)
    print('The most common End Station for cycling is ' + str(popular_end_station) + '.\tObservations:' + str(variable2[0]) + '\n')


    # display most frequent combination of start station and end station trip
    temp='From '+ df['Start Station']+ '  to   '+df['End Station']
    popular_start_end_station = temp.mode()[0]
    #variable = temp.describe()
    variable2 = temp.value_counts().reset_index(drop=True)
    print('The most common combination of Start & End Station is :' + str(popular_start_end_station) + '.\tObservations:' + str(variable2[0]) + '\n')




    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating statistics on the total and average trip duration..\n')
    start_time = time.time()

    # display total travel time
    t1 = pd.to_datetime(df['Start Time'])
    t2= pd.to_datetime(df['End Time'])

    sum=0
    for i in range(len(t1)):
        h1 = t1.iloc[i]
        h2 = t2.iloc[i]
        sum+=pd.Timedelta(h2 - h1).seconds / 3600.0


    print('The Total Trip Duration is {} hour(s). \n'.format(sum))
    print('The Average Trip Duration is {} hour(s). \n'.format(sum/(t1.count())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating statistics on Bikeshare users..\n')
    start_time = time.time()

    # Display counts of user types
    print('Display the counts of Bikeshare Users.\n')
    vlist=df['User Type'].value_counts().index
    temp=df['User Type'].value_counts()
    for i in vlist:
        print(i+": "+ str(temp[i]))


    # Display counts of gender & earliest, most recent, and most common year of birth (ONLY FOR NYC AND CHICAGO)
    if(city=='new york city' or city=='chicago'):
        print('\nDisplay the counts of Gender of  Bikeshare Users.\n')
        vlist = df['Gender'].value_counts().index
        temp = df['Gender'].value_counts()
        for i in vlist:
            print(i + ": " + str(temp[i]))

        print('\n')
        print('The earliest year of Birth is {}.'.format(int(df['Birth Year'].min())))
        print('The most recent year of Birth is {}.'.format(int(df['Birth Year'].max())))
        print('The most common year of Birth is {}.'.format(int(df['Birth Year'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():

    while(1):
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print(df.head())
        print(df.shape)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break



if __name__ == "__main__":
     main()