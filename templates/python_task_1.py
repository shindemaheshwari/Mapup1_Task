import pandas as pd


def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here
    df = df.pivot(index='id_1', columns='id_2', values='car')

    return df


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    if 'car' in df.columns:
        car_counts = df['car'].value_counts().to_dict()
        
    else:
        
        return {}

    return car_counts


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
    if 'bus' in df.columns:
        bus_mean = df['bus'].mean()
        bus_indexes = df[df['bus'] > 2 * bus_mean].index.tolist()
        return bus_indexes
    
    else:
        return {}

  

def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    if 'truck' in df.columns:
        route_avg_truck = df.groupby('route')['truck'].mean()
        filtered_routes = route_avg_truck[route_avg_truck > 7].index.tolist()
        return filtered_routes
        
    else:
        return {}




def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    def custom_multiply(value):
        if value > 5:
            return value * 2
        else:
            return value

    modified_matrix = matrix.applymap(custom_multiply)

    return modified_matrix

  

def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
    df["start_timestamp"] = pd.to_datetime(df["startDay"] + " " + df["startTime"], errors='coerce')
    df["end_timestamp"] = pd.to_datetime(df["endDay"] + " " + df["endTime"], errors='coerce')

    # Drop rows with NaT values (invalid timestamps)
    df = df.dropna(subset=['start_timestamp', 'end_timestamp'])

    # Ensure the 'start_timestamp' and 'end_timestamp' columns are of datetime type
    df['start_timestamp'] = pd.to_datetime(df['start_timestamp'])
    df['end_timestamp'] = pd.to_datetime(df['end_timestamp'])

    # Calculate the duration for each row in hours and days
    df['duration_hours'] = (df["end_timestamp"] - df["start_timestamp"]).dt.total_seconds() / 3600
    df['duration_days'] = (df["end_timestamp"] - df["start_timestamp"]).dt.days + 1

    # Group data by unique (`id`, `id_2`) pairs
    grouped_df = df.groupby(["id", "id_2"])

    # Check if each entry covers at least 24 hours and 7 days
    is_complete = grouped_df.all()[['duration_hours', 'duration_days']] >= [24, 7]

    return is_complete
