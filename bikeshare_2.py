import time
import calendar
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    city_list = (('chicago', 'new york city', 'washington'))
    while city not in city_list:
        city = input('Please choose a city to analyze. Type Chicago, New York City or Washington to start.').lower()
        if city not in  city_list:
            print('Sorry, I don\'t understand your answer.')

    print('OK, we will look at {}.'.format(city.title()))


    # get user input for month (all, january, february, ... , june)
    month = ''
    months_list = ('january', 'february', 'march', 'april', 'may', 'june', 'all')
    while month not in months_list:
        month = input('Please choose a month to look at. Type January, February, March, April, May, June or all, if you want to look at all data.').lower()
        if month not in months_list:
            print('Sorry, I don\'t understand your answer.')

    print('OK, we will look at {}.'.format(month.title()))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    day_list = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all')
    while day not in day_list:
        day = input('Please choose a day to look at. Type Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all, if you want to look at all data.').lower()
        if day not in day_list:
            print('Sorry, I don\'t understand your answer.')

    print('OK, we will look at {}.'.format(day.title()))

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
    df = df.reindex(columns=['Start Time', 'End Time', 'Trip Duration', 'Start Station', 'End Station', 'User Type', 'Gender', 'Birth Year'], fill_value=0)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day)
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]


    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    common_month_name = calendar.month_name[common_month]
    print('The most common month is {}.'.format(common_month_name))

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    common_day_name = calendar.day_name[common_day]
    print('The most common day is {}.'.format(common_day_name))


    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('The most common hour is {}.'.format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('The most common start station is {}.'.format(common_start_station))

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('The most common end station is {}.'.format(common_end_station))

    # display most frequent combination of start station and end station trip
    common_start_end_station = (df['Start Station'] + ' and ' + df['End Station']).mode()[0]
    print('The most common combination is {}.'.format(common_start_end_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total = np.sum(df['Trip Duration'])
    print('The total travel time has been {} seconds.'.format(total))

    # display mean travel time
    mean = np.mean(df['Trip Duration'])
    print('The mean travel time has been {} seconds.'.format(mean))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()

    print('{} subscribers and {} customers used the service.'.format(df['User Type'].value_counts()[0],df['User Type'].value_counts()[1]))

    # Display counts of gender
    gender = df['Gender'].value_counts()

    try:
        print('{} men and {} women used the service.'.format(df['Gender'].value_counts()[0],df['Gender'].value_counts()[1]))
    except KeyError:
        print('Sorry, no data about gender available.')
    # Display earliest, most recent, and most common year of birth
    most_common_year = int(df['Birth Year'].mode()[0])
    earliest = int(df['Birth Year'].min())
    most_recent = int(df['Birth Year'].max())

    if most_common_year == 0 and earliest == 0 and most_recent == 0:
        print('')

    else:
        print('The most common year of bith is {}.'.format(most_common_year))
        print('The most earliest year of bith is {}.'.format(earliest))
        print('The most recent year of bith is {}.'.format(most_recent))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):

    view_data = input('Would you like to view 5 rows of individual trip data? Enter yes or no.').lower()
    start_loc = 0

    while view_data == 'yes' and start_loc <= len(df.index):
        print(df.iloc[start_loc:(start_loc+5)])
        start_loc += 5
        view_data = input("Do you wish to continue?: ").lower()



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
