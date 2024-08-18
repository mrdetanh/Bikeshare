import time
import pandas as pd

CITY_DATA = { 
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv' 
}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Welcome to the Bikeshare Data Explorer! Let\'s dive into the data and uncover some interesting insights!')
    
    # get user input for city (chicago, new york city, washington)
    while True:
        city = input('Which city would you like to explore: Chicago, New York City, or Washington?\n').lower()
        if city in CITY_DATA:
            break
        else:
            print('Invalid input. Please enter a valid city name.')

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Which month would you like to filter by: January, February, March, April, May, June, or "all" to apply no month filter?\n').lower()
        if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            break
        else:
            print('Invalid input. Please enter a valid month or "all".')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Which day would you like to filter by: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or "all" to apply no day filter?\n').lower()
        if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            break
        else:
            print('Invalid input. Please enter a valid day or "all".')

    print('-'*40)
    return city, month, day

#Check and notify if DataFrame is empty
def check_empty(df):
    """Checks if the DataFrame is empty and prints a message if it is."""
    if df.empty:
        print("No data available for the selected filters.")
        return True
    return False

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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name().str.lower()
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    df['start_hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    if check_empty(df):
        return
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print(f'Most Common Month: {most_common_month}')

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print(f'Most Common Day of Week: {most_common_day}')

    # display the most common start hour
    most_common_start_hour = df['start_hour'].mode()[0]
    print(f'Most Common Start Hour: {most_common_start_hour}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    if check_empty(df):
        return
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print(f'Most Commonly Used Start Station: {most_common_start_station}')

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print(f'Most Commonly Used End Station: {most_common_end_station}')

    # display most frequent combination of start station and end station trip
    most_common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f'Most Frequent Combination of Start and End Station: {most_common_trip}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    if check_empty(df):
        return
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f'Total Travel Time: {total_travel_time} seconds')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f'Mean Travel Time: {mean_travel_time} seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    if check_empty(df):
        return
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(f'User Types:\n{user_types}')

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print(f'Gender Counts:\n{gender_counts}')
    else:
        print('Gender data not available for this city.')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])
        print(f'Earliest Year of Birth: {earliest_year}')
        print(f'Most Recent Year of Birth: {most_recent_year}')
        print(f'Most Common Year of Birth: {most_common_year}')
    else:
        print('Birth Year data not available for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
         
# Display_data1
def display_data1(df):
    most_common_months = df['month'].mode()
    most_common_day = df['day_of_week'].mode()
    most_common_start_hour = df['start_hour'].mode()

    filtered_df = df[
        df['month'].isin(most_common_months) &
        df['day_of_week'].isin(most_common_day) &
        df['start_hour'].isin(most_common_start_hour)
    ]

    start_loc = 0
    keep_asking = True
    user_input = input("Do you want to see the data for the most frequent times of travel? (yes/no): ").strip().lower()
    if user_input != 'yes':
        keep_asking = False

    while keep_asking and start_loc < len(filtered_df):
        end_loc = start_loc + 5
        print(filtered_df.iloc[start_loc:end_loc])
        start_loc += 5

        if start_loc < len(filtered_df):
            user_input = input("Do you want to see the next 5 rows of data for the most frequent times of travel? (yes/no): ").strip().lower()
            if user_input != 'yes':
                keep_asking = False
        else:
            print("You have reached the end of the available data for this section.")
            keep_asking = False

# Display_data2
def display_data2(df):
    most_common_start_station = df['Start Station'].mode()
    most_common_end_station = df['End Station'].mode()
    
    filtered_df = df[
        df['Start Station'].isin(most_common_start_station) &
        df['End Station'].isin(most_common_end_station)
    ]

    start_loc = 0
    keep_asking = True
    user_input = input("Do you want to see the data for the most popular stations and trip? (yes/no): ").strip().lower()
    if user_input != 'yes':
        keep_asking = False

    while keep_asking and start_loc < len(filtered_df):
        end_loc = start_loc + 5
        print(filtered_df.iloc[start_loc:end_loc])
        start_loc += 5

        if start_loc < len(filtered_df):
            user_input = input("Do you want to see the next 5 rows of data for the most popular stations and trip? (yes/no): ").strip().lower()
            if user_input != 'yes':
                keep_asking = False
        else:
            print("You have reached the end of the available data for this section.")
            keep_asking = False

# Display_data3
def display_data3(df):
    if 'Birth Year' in df.columns:
        # Find the earliest, most recent, and most common years of birth
        earliest_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()
        most_common_years = df['Birth Year'].mode()
        
        # Filter rows with the earliest year of birth
        earliest_years_df = df[df['Birth Year'] == earliest_year]

        # Filter rows with the most recent year of birth
        most_recent_years_df = df[df['Birth Year'] == most_recent_year]

        # Filter rows with the most common year(s) of birth
        common_years_df = df[df['Birth Year'].isin(most_common_years)]

        start_loc = 0
        keep_asking = True

        # Ask the user if they want to see the data for earliest_year
        user_input = input("Do you want to see the data for the earliest year(s) of birth? (yes/no): ").strip().lower()
        if user_input == 'yes':
            while keep_asking and start_loc < len(earliest_years_df):
                end_loc = start_loc + 5
                print("\nEarliest Year(s) of Birth Data:")
                print(earliest_years_df.iloc[start_loc:end_loc])
                start_loc += 5

                if start_loc < len(earliest_years_df):
                    user_input = input("Do you want to see the next 5 rows of data for the earliest year(s)? (yes/no): ").strip().lower()
                    if user_input != 'yes':
                        keep_asking = False
                else:
                    print("You have reached the end of the available data for this section.")
                    keep_asking = False

        start_loc = 0
        keep_asking = True

        # Ask the user if they want to see the data for most_recent_year
        user_input = input("Do you want to see the data for the most recent year(s) of birth? (yes/no): ").strip().lower()
        if user_input == 'yes':
            while keep_asking and start_loc < len(most_recent_years_df):
                end_loc = start_loc + 5
                print("\nMost Recent Year(s) of Birth Data:")
                print(most_recent_years_df.iloc[start_loc:end_loc])
                start_loc += 5

                if start_loc < len(most_recent_years_df):
                    user_input = input("Do you want to see the next 5 rows of data for the most recent year(s)? (yes/no): ").strip().lower()
                    if user_input != 'yes':
                        keep_asking = False
                else:
                    print("You have reached the end of the available data for this section.")
                    keep_asking = False

        start_loc = 0
        keep_asking = True

        # Ask the user if they want to see the data for most_common_years
        user_input = input("Do you want to see the data for the most common year(s) of birth? (yes/no): ").strip().lower()
        if user_input == 'yes':
            while keep_asking and start_loc < len(common_years_df):
                end_loc = start_loc + 5
                print("\nMost Common Year(s) of Birth Data:")
                print(common_years_df.iloc[start_loc:end_loc])
                start_loc += 5

                if start_loc < len(common_years_df):
                    user_input = input("Do you want to see the next 5 rows of data for the most common year(s)? (yes/no): ").strip().lower()
                    if user_input != 'yes':
                        keep_asking = False
                else:
                    print("You have reached the end of the available data for this section.")
                    keep_asking = False
    else:
        print('Birth Year data is not available for this city.')


# Display_data all
def display_data(df):

    display_data1(df)
    display_data2(df)
    display_data3(df)
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
