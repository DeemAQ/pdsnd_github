#  Copyright (c) 2021.
#  By Deem Alqud

import time

import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (int) month - number corresponding to the name of the month to filter by, or "all" to apply no month filter
        (int) day - number corresponding to the name of the day of week to filter by, or "all" to apply no day filter
    """
    cities = ['chicago', 'new york', 'washington']
    months = range(0, 7)
    dow = range(0, 8)
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Choose a city (Chicago, New York, Washington): ').lower()
    while city not in cities:
        city = input('Please choose again (Chicago, New York city, Washington): ').lower()

    # get user input for month (all, january, february, ... , june)
    month = int(input('Choose a month (0 = all, 1 = jan, 2 = feb, ..., 6 = jun): '))
    while month not in months:
        month = int(input('Please choose again (0 = all, 1 = jan, 2 = feb, ..., 6 = jun): '))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = int(input('Which day of the week? (all = 0, 1 = monday, 2 = tuesday, ... 7 = sunday): '))
    while day not in dow:
        day = int(input('Please choose again (all = 0, 1 = monday, 2 = tuesday, ... 7 = sunday): '))

    if city == 'new york':
        city += ' city'

    print('-' * 40)
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
    csv = CITY_DATA[city]

    df = pd.read_csv(csv)

    if month != 0:
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df = df[df['Start Time'].dt.month == month]
        if day != 0:
            df = df[df['Start Time'].dt.weekday == (day - 1)]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    most_common_month = df['Start Time'].dt.month.value_counts().keys()[0]
    month = months_in_string(most_common_month)
    print('Most common month is:', month)

    # display the most common day of week
    most_common_dow = df['Start Time'].dt.day_name().value_counts().keys()[0]
    print('Most common day of week is:', most_common_dow)

    # display the most common start hour
    most_common_hour = df['Start Time'].dt.hour.value_counts().keys()[0]
    from time import strptime
    from time import strftime
    t = strptime(str(most_common_hour), "%H")
    hour = strftime("%I %p", t)
    print('Most common hour is:', hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def months_in_string(month):
    switcher = {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June'
    }
    return switcher.get(month, "")


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].value_counts().keys()[0]
    print('Most commonly used start station is:', most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].value_counts().keys()[0]
    print('Most commonly used end station is:', most_common_end_station)

    # display most frequent combination of start station and end station trip
    freq_combination = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).keys()
    freq_combination = freq_combination[0]
    print(f'Most frequent start and end stations is:\nfrom {freq_combination[0]} to {freq_combination[1]}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print(f'Total time traveled: {total_travel} seconds')
    print(f'~{total_travel // 3600} hours')

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print(f'Mean of time traveled: %.3f seconds' % mean_travel)
    print('%.3f minutes' % (mean_travel / 60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print('Users type count:\n', user_type_count)

    if 'Gender' not in df.columns:
        print('No gender information')
    else:
        # Display counts of gender
        user_gender_count = df['Gender'].value_counts()
        print('Users gender counts:\n', user_gender_count)

    if 'Birth Year' not in df.columns:
        print('No birth year information')
    else:
        # Display earliest, most recent, and most common year of birth
        # earliest
        earliest_birth_year = df.sort_values(by=['Birth Year']).values[0]
        earliest_birth_year = int(earliest_birth_year[len(earliest_birth_year) - 1])
        print('Earliest birth year', earliest_birth_year)
        # most recent
        most_recent_birth_year = df.sort_values(by=['Birth Year'], ascending=False).values[0]
        most_recent_birth_year = int(most_recent_birth_year[len(most_recent_birth_year) - 1])
        print('Most recent birth year', most_recent_birth_year)
        # most common
        most_common_birth_year = int(df['Birth Year'].value_counts().keys()[0])
        print('Most common birth year is', most_common_birth_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display(df):
    view_data = input('\nWould you like to view 5 rows of trip data?\n(Y)es or (N)o: ').lower()
    view_data = check_answer(view_data)
    loc = 0
    while view_data[0] == 'y':
        print(df.iloc[loc: loc + 5])
        loc += 5
        view_data = input('Do you want to continue?\n(Y)es or (N)o: ').lower()
        view_data = check_answer(view_data)


def check_answer(ans):
    while ans != 'yes' or ans != 'y' and (ans != 'n' or ans != 'no'):
        ans = input('Please repeat your answer:\n(Y)es or (N)o: ')
        return ans


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display(df)

        restart = input('\nWould you like to restart? (Y)es or (N)o.\n').lower()
        restart = check_answer(restart)
        if restart[0] != 'y':
            break


if __name__ == "__main__":
    main()
