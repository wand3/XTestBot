import pandas as pd

filename = 'data.csv'

data = [
    {'email': 'alice@example.com', 'password': 'nhnjkjmo', 'username': 'fireboy', 'cookies_file': 'cookies_file'},
    {'email': 'bob@example.com', 'password': 'nhnjkjmo', 'username': 'fjjkireboy', 'cookies_file': 'cookies_file'},
    {'email': 'charlie@example.com', 'password': 'nhnjkjmo', 'username': 'firjky', 'cookies_file': 'cookies_file'}
]


def create_csv(filename, data):
    # Create a pandas DataFrame from the data
    df = pd.DataFrame(data)

    # Write the DataFrame to a CSV file
    df.to_csv(filename, index=True)  # `index=False` to avoid writing the DataFrame index to the CSV


def create_record(filename, new_data):
    # Create a DataFrame for the new data
    df = pd.DataFrame(new_data)
    # Append the DataFrame to the existing CSV file
    df.to_csv(filename, mode='a', header=False, index=True)

# create_record(filename, {'email': 'zod@gmail.com', 'password': 'Bofggb', 'cookies_file': 'nofile yet'})


def read_records(filename):
    """
        read
    """
    df = pd.read_csv(filename)
    print(df)
# read_records('data.csv')


def update_record_by_email(filename, email, updated_data):
    df = pd.read_csv(filename)

    # Strip any leading/trailing spaces in column names to avoid mismatches
    df.columns = df.columns.str.strip()

    # Print the column names to check if 'email' exists
    print("Columns in CSV:", df.columns)
    df.loc[df['email'] == email, list(updated_data.keys())] = list(updated_data.values())
    df.to_csv(filename, index=False)

# update_record_by_email('data.csv', 'zoddd@gmail.com', {'password': 'Alice'})


def delete_record(filename, email):
    # Load the CSV file
    df = pd.read_csv(filename)

    # Strip any leading/trailing spaces in column names to avoid mismatches
    df.columns = df.columns.str.strip()

    # Print current records before deletion
    print("Before deletion:")
    print(df)

    # Delete the row where the 'email' matches
    df = df[df['email'] != email]  # Keep rows where email is not equal to the provided email

    # Print the DataFrame after deletion
    print("\nAfter deletion:")
    print(df)

    # Save the updated DataFrame back to the CSV
    df.to_csv(filename, index=False)

# delete_record('data.csv', 3)


def query_record_by_email(filename, email):
    # Load the CSV file
    df = pd.read_csv(filename)

    # Strip any leading/trailing spaces in column names to avoid mismatches
    df.columns = df.columns.str.strip()

    # Query the row where the 'email' matches
    record = df[df['email'] == email]

    # Check if any records were found
    if record.empty:
        print(f"No record found for email: {email}")
    else:
        # Display the full record
        return record
