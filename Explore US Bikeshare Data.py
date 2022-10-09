from re import I
import time
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
    while True:
        city = str(input("Which city's data would you like to see? Please enter Chicago, New York City or Washington.").lower())
        if city in ['chicago', 'new york city', 'washington']:
            print('You have selected {}.'.format(city.title()))
            break
        else:
            print('Sorry, I did not understand that.')

    # get user input for month (all, january, february, ... , june)
    while True:
        month = str(input("Which month's data would you like to see? Enter 'all' if you do not wish to filter by month.").lower())
        if month in ['january', 'february', 'march', 'april', 'may', 'june']:
            print('You have selected {}.'.format(month.title()))
            break
        elif month.lower() == 'all':
            print('Okay, do not filter by month.')
            break
        else:
            print('Sorry, I did not understand that.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = str(input("Which weekday's data would you like to see? Please enter name of the day. Enter 'all' if you do not wish to filter by day.").lower())
        if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            print('You have selected {}.'.format(day.title()))
            break
        elif day.lower() == 'all':
            print('Okay, do not filter by day.')
            break
        else:
            print('Sorry, I did not understand that.')

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

    # load data file into a dataframe
    df = pd.read_csv('C:/Users/lucie/Downloads/all-project-files/' + CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_of_week

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        df = df[df['day_of_week'] == weekdays.index(day)]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    popular_month = months[df['month'].mode()[0] - 1].title()
    print('\nMost Popular Month:', popular_month)

    # display the most common day of week
    df['day'] = df['Start Time'].dt.day_of_week
    weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    popular_day = weekdays[df['day'].mode()[0]].title()
    print('\nMost Popular Day:', popular_day)

    # display the most common start hour

    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('\nMost Popular Start Hour:', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print('\nMost Popular Start Station:', popular_start)

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print('\nMost Popular End Station:', popular_end)

    # display most frequent combination of start station and end station trip
    df['Combo'] = 'Start Station: ' + df['Start Station'] + ', End Station: ' + df['End Station']
    popular_combo = df['Combo'].mode()[0]
    print('\nMost Popular Combination of Start Station and End Station:', popular_combo)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print('\nTotal travel time was:', time.strftime('%H:%M:%S', time.gmtime(total_time)))

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print('\nMean travel time was:', time.strftime('%H:%M:%S', time.gmtime(mean_time)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("\nUser type composition:", df['User Type'].value_counts())

    # Display counts of gender
    if city == 'washington':
        print('\nNo gender data available for Washington.')
    else:
        print("\nGender composition:", df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
    if city == 'washington':
        print('\nNo birth year data available for Washington.')
    else:
        print("\nEarliest year of birth:", int(df['Birth Year'].dropna().min()))
        print("\nMost recent year of birth:", int(df['Birth Year'].dropna().max()))
        print("\nMost common year of birth:", int(df['Birth Year'].dropna().mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        raw_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
        if raw_data == 'yes':
            counter = 1
            while True:
                print(df.iloc[counter * 5: (counter + 1) * 5])
                more_raw_data = input('\nWould you like to see 5 more lines of raw data? Enter yes or no.\n')
                counter += 1
                if more_raw_data == 'no':
                    break
                elif counter * 5 >= df.shape[0]:
                    print('No more raw data to display.')
                    break


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
