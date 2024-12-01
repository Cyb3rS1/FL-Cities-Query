# Florida Cities Population Query
# This program simulates a Florida city populations database that has options for viewing the population growth
# of 10 hand-picked cities. After querying the database for a city, all of its population data is gathered
# and illustrated on a graph for the user to see. The user can view all the cities as many times as they want until
# they are finished.

import sqlite3 as sq
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import rc

global choice

# divider used for neater code
DIV = "===" * 20 + "\n"

# function that creates a table named "population" inside a database(population_SS.db)
def create_table():

    # connect to the database
    conn = sq.connect('population_SS.db')

    # create a cursor to interact with the database
    cursor = conn.cursor()

    # drop any table named 'population' that already exists
    cursor.execute('DROP TABLE IF EXISTS population')

    # define a new table named 'population' and its columns
    table = '''CREATE TABLE population (
        city TEXT,
        year INTEGER,
        population INTEGER)'''

    # execute the table's creation to the database
    cursor.execute(table)

    # call next function, passing 'conn' and 'cursor' in as parameters
    collect_data(conn, cursor)
    

# function collecting population growth data for 10 Florida cities, simulates 2% population
# growth every year for 20 years and stores the results into the 'population' table
def collect_data(conn, cursor):

    # start with populations of 10 Florida cities recorded in 2023

    # list where all current and future data about each city, year, and population is stored
    population_data = [
        ('Bradenton', 2023, 57076),
        ('Sarasota', 2023, 57602),
        ('Cape Coral', 2023, 224455),
        ('Palmetto', 2023, 13577),
        ('Fort Lauderdale', 2023, 184255),
        ('Venice', 2023, 28150),
        ('St. Petersburg', 2023, 263553),
        ('Tampa', 2023, 403364),
        ('Naples', 2023, 1970),
        ('Pensacola', 2023, 53724)
    ]

    # convert the list of tuples that contains each city, year, and population into a flat list
    flat_population_data = [item for c in population_data for item in c]

    # take every 3 items from flat_population_data and append them to a new 'cities' list
    cities = [flat_population_data[i:i + 3] for i in range(0, len(flat_population_data), 3)]

    # 'for' loop that iterates 20 times, simulating the passing of 20 years
    for count in range(20):

        # 'for' loop for recording growth of one city "per year"
        for city in cities:

            # no need to change the city's name, so assign it to one_city
            one_city = city[0]

            # assign one_year to the city's current year, add one and the value of count to it
            one_year = city[1] + 1 + count

            # calculate the 2% growth and add it to the current number
            city[2] += city[2] * 0.02

            # assign the result from directly above to 'one_population'
            one_population = int(city[2])

            # append a new list to population_growth
            population_data.append((one_city, one_year, one_population))


    # insert each tuple from 'population_data' into the 'population' table
    cursor.executemany('INSERT INTO population (city, year, population) '
                       'VALUES (?,?,?)', population_data)

    # commit the changes and close the connection to the database
    conn.commit()
    conn.close()

    # call next function
    cities_inquiry()


# user-choice function that gives options for displaying city population growth
def cities_inquiry():

    # start-up message
    print("Welcome to the Florida Population Query")
    print(DIV)

    # a list of options (cities) for the user to choose from
    options_list = ["Bradenton", "Sarasota", "Cape Coral", "Palmetto", "Fort Lauderdale",
                    "Venice", "St. Petersburg", "Tampa", "Naples", "Pensacola", "=> Exit"]

    display_options(options_list)

    print("\nView the population growth for any of these cities!")

    print(DIV)

    choose_option(options_list)

    # 'while' loop that iterates until the user chooses to exit
    while choice != "=> Exit":

        display_city_growth()

        choose_option(options_list)

    else:

        exit()


# helper function that iterates through and displays the options_list (one-time use)
def display_options(options_list):

    count = 0

    for city in options_list:

        # use 'count' to number and index each option from 'options_list'
        print(f"{count + 1}. {options_list[count]}")

        count += 1


# helper function that takes input from the user
def choose_option(options_list):

    global choice

    # take user input
    choice = int(input("Please enter the number of your choice: "))

    # minus one from the input to use it as an index for the options_list
    choice -= 1

    # reassign 'choice' to the indexed value in options_list
    choice = options_list[choice]


# function that takes a query and makes a graph from the data stored in the population table
def display_city_growth():

    # establish a connection with 'population_SS.db'
    conn = sq.connect('population_SS.db')

    # create a cursor to interact with the .db file
    cursor = conn.cursor()

    # select all data in the table according to which city the user chose to view
    cursor.execute("SELECT * FROM population WHERE city = ?", (choice,))

    # save the results of all fetched data to 'results'
    results = cursor.fetchall()

    # a list where all populations for the specific city will be stored
    a = []

    # 'for' loop that appends all population numbers from 'results' to 'a'
    for row in results:

        # take the index 2 of each 'row' in 'results' and assign it to 'population'
        population = row[2]

        # the empty list gets filled with populations for the specific city
        a.append(population)

    # array used for x-axis of population growth, indicates the starting and ending years (2023-2043) of documentation
    years = np.linspace(2023, 2043, num=21)

    # converting the minimum and maximum populations into strings and formatting them
    min_pop = '{:,}'.format(min(a))
    max_pop = '{:,}'.format(max(a))

    # using numpy.arange to define specific ticks for the x-axis
    x_ticks = np.arange(2023, 2044, 5)

    # using matplotlib.rc to format the graph's font family
    rc('mathtext', default='regular')
    matplotlib.rcParams.update({'font.family': 'Monospace'})

    # define figure and axis to use plt.subplots()
    fig, ax = plt.subplots()

    # use 'ax' methods to add visual details such as a grid and x and y labels
    ax.grid()
    ax.set_xlabel('Years')
    ax.set_ylabel('Population')

    # use 'plt' methods to add visual details such as x-axis ticks, a line, specific coordinates, and the title
    plt.xticks(x_ticks)
    plt.plot(years, a)
    plt.scatter([years[0], years[-1]], [a[0], a[-1]])
    plt.title(f"{choice} Population Growth from 2023-2043")

    # add text near the first and last coordinates to emphasize the beginning and final populations
    plt.text(years[1], a[0], min_pop, ha='left', va='bottom')
    plt.text(years[-2], a[-1], max_pop, ha='right', va='top')

    # display the graph
    plt.show()

    # commit any changes to the database and close its connection
    conn.commit()
    conn.close()


# main function that initiates all other included functions
def main():

    create_table()

# call the first function
main()


