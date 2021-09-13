import time
import pandas as pd
import numpy as np
from tabulate import tabulate


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


pd.set_option('display.max_columns', 200)

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    city = ''
    while city not in CITY_DATA.keys():
        
        city = input('What is your city ?\t').lower()
        
        """
        Asks user if he/she wants to display some data to have an idea of how the data is structured in the files based on a specific city.

        Returns:
         (DataFrame) view data - data table containing information based on what the user wants to view according to a specific city
        """
        i = 0
        while True:
            view_data = input("Would you like to view 5 rows of raw data? Enter a 'yes' or 'no'\t").lower()
            if view_data != 'yes':
                break
            df = pd.read_csv(CITY_DATA[city])
            print(tabulate(df.iloc[np.arange(0+i, 5+i)], headers = 'keys'))
            i += 5
        
        if city not in CITY_DATA.keys():
            print('This city does not exist among required cities')
            #break
        else:
            print('Your city is {}'.format(city))
            #continue
            
    # TO DO: get user input for month (all, january, february, ... , june)
    month = ''
    MONTH_LIST = ['all', 'january', 'february', 'march' , 'april', 'may', 'june']
    while month not in MONTH_LIST:
        month = input('What is your month ?\t').lower()
        if month not in MONTH_LIST:
            print('This month does not exist among required months')
            #break
        else:
            print('Your month is {}'.format(month))
            #continue

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    DAY_LIST = ['all', 'monday', 'tuesday', 'wednesday' , 'thursday', 'friday', 'saturday', 'sunday']
    while day not in DAY_LIST:
        day = input('What is your day of the week ?\t').lower()
        if day not in DAY_LIST:
            print('This day does not exist among required days')
            #break
        else:
            print('Your day is {}'.format(day))
            #continue

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    df['month'] = df['Start Time'].dt.month
    
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        
        df = df[df['month'] == month]
        
    if day != 'all':
        
        df = df[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].mode()[0]
    print('The most common month is {}'.format(common_month))

    # TO DO: display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('The most common day is {}'.format(common_day))

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    
    print('The most common start hour is {}\n'.format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_stat = df['Start Station'].mode()[0]
    print('The most commonly used start station is {}\n'.format(common_start_stat))
    # TO DO: display most commonly used end station
    common_end_stat = df['End Station'].mode()[0]
    print('The most commonly used end station is {}\n'.format(common_end_stat))
    
    # TO DO: display most frequent combination of start station and end station trip
    group_stations = df[['Start Station', 'End Station']].groupby(['Start Station', 'End Station'])
    combination = group_stations.size().sort_values().nlargest(1)
    
    print('The most frequent combination of start station and end station is {}'.format(combination))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time = df['Trip Duration'].sum()
    print('The total travel time is {}\n'.format(total_time))
    
    # TO DO: display mean travel time
    mean_time = df['Trip Duration'].mean()
    print('The mean travel time is {}\n'.format(mean_time))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    count_user = df['User Type'].value_counts()
    print('The number of user types is: {}'.format(count_user))


    if city != 'washington':
        # TO DO: Display counts of gender
        count_gender = df['Gender'].value_counts()
        print('The number of gender is: {}'.format(count_gender))
        
        # TO DO: Display earliest, most recent, and most common year of birth
        df_birth = df['Birth Year']
        earliest_year = int(df_birth.min())
        recent_year = int(df_birth.max())
        common_year = int(df_birth.mode()[0])
        print('The earliest year is ({}), the most recent year is ({}) and the most common year is ({})\n'.format(earliest_year, recent_year, common_year))
    else:
        print('There is no gender type and birth year in washington city')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
