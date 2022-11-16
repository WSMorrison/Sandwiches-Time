import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    Get sales figures input from the user.
    Run a while loop to collect a valid string from user,
    repeating as necessary until code is valid.
    """
    while True:
        print('---Please enter sales data from the last market.---')
        print('--Data should be six numbers, separated by commas--')
        print('------------Example: 10,20,30,40,50,60-------------\n')

        data_str = input('Enter your data here:\n')

        sales_data = data_str.split(',')

        if validate_data(sales_data):
            print('\n\nData accepted.\n')
            break

    return sales_data


def validate_data(values):
    """
    Inside the try, converst all string values into integers.
    Raises ValueError if strings cannot be converted,
    or if there are not exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f'Exactly 6 values are required, you provided {len(values)}'
            )
    except ValueError as e:
        print(f'Invalid data: {e}, please try again.\n')
        return False

    return True


def update_worksheet(data, worksheet):
    """
    Received a list of integers to be inserted into a worksheet,
    updates appropriate worksheet with new data.
    """
    print(f'Updating {worksheet} worksheet...\n')
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f'The {worksheet} worksheet has been updated successfully.\n')


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate surplus
    Surplus is defined as the sales subtracted from stock:
    -Positive indicates waste
    -Negative meant staff had to make up difference
    """
    print('Calculating surplus data...\n')
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data


def get_last_5_entries_sales():
    """
    Collects columns of data from sales worksheet,
    creates a list of lists of the last 5 entries of each.
    """
    sales = SHEET.worksheet('sales')
    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])

    return columns


def calculate_stock_data(data):
    """
    Calculate the stocking data using the last 5 sales entries.
    """
    print('Calculating stocking data...\n')
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_level = average * 1.1
        new_stock_data.append(round(stock_level))
        
    return new_stock_data


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, 'sales')
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, 'surplus')
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, 'stock')
    print('Thank you, see you tomorrow!\n')

print('\nWelcome to the Love Sandwiches Automated Analysis Progman\n')
main()
