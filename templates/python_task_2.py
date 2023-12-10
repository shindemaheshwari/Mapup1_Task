import pandas as pd


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
    
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371  # Earth radius in kilometers

        dlat = pd.np.radians(lat2 - lat1)
        dlon = pd.np.radians(lon2 - lon1)

        a = pd.np.sin(dlat / 2) ** 2 + pd.np.cos(pd.np.radians(lat1)) * pd.np.cos(pd.np.radians(lat2)) * pd.np.sin(dlon / 2) ** 2
        c = 2 * pd.np.arctan2(pd.np.sqrt(a), pd.np.sqrt(1 - a))

        distance = R * c
        return distance
    
    
    if 'latitude' not in df.columns or 'longitude' not in df.columns:
        raise ValueError("DataFrame must contain 'latitude' and 'longitude' columns.")

    # Extract latitude and longitude columns
    coordinates = df[['latitude', 'longitude']].to_numpy()

    # Calculate pairwise distances using Haversine formula
    distances = pdist(coordinates, lambda u, v: haversine(u[0], u[1], v[0], v[1]))

    # Convert the distances to a square matrix
    distance_matrix = squareform(distances)

    # Create a DataFrame from the distance matrix
    distance_df = pd.DataFrame(distance_matrix, index=df.index, columns=df.index)

    return distance_df



def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
    if not pd.DataFrame(distance_matrix.index == distance_matrix.columns).all():
        raise ValueError("Input DataFrame must be a square matrix with valid index/column names.")

    # Melt the distance matrix to long format
    unrolled_df = pd.melt(distance_matrix.reset_index(), id_vars='id_start', var_name='id_end', value_name='distance')

    return unrolled_df



def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here
    # Filter rows corresponding to the reference_id
    reference_rows = df[(df['id_start'] == reference_id) | (df['id_end'] == reference_id)]

    # Calculate the average distance for the reference_id
    reference_avg_distance = reference_rows['distance'].mean()

    # Calculate the threshold for similarity (10% of the reference_avg_distance)
    threshold_distance = 0.1 * reference_avg_distance

    # Filter rows where the average distance is within the threshold
    similar_ids = df.groupby('id_start').agg({'distance': 'mean'}).reset_index()
    similar_ids = similar_ids[(similar_ids['distance'] >= reference_avg_distance - threshold_distance) &
                              (similar_ids['distance'] <= reference_avg_distance + threshold_distance)]

    return similar_ids



def calculate_toll_rate(df1, df2, df3) -> pd.DataFrame:
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df1 (pandas.DataFrame): DataFrame with columns 'id_1', 'id_2', 'route', 'moto', 'car', 'rv', 'bus', 'truck'.
        df2 (pandas.DataFrame): DataFrame with columns 'id', 'name', 'id_2', 'startDay', 'startTime', 'endDay', 'endTime', and various 'able' columns.
        df3 (pandas.DataFrame): DataFrame with columns 'id_start', 'id_end', 'distance'.

    Returns:
        pandas.DataFrame: DataFrame with toll rates calculated for each row.
    """
    # Write your logic here
    vehicle_types = ['moto', 'car', 'rv', 'bus', 'truck']

    # Merge the three datasets based on common columns
    merged_df = pd.merge(df1, df2, left_on=['id_2'], right_on=['id_2'], how='inner')
    merged_df = pd.merge(merged_df, df3, left_on=['id_1', 'id_2'], right_on=['id_start', 'id_end'], how='inner')

    # Example toll rate calculation logic (you can replace this with your own logic)
    for vehicle_type in vehicle_types:
        toll_column = f'{vehicle_type}_toll_rate'
        merged_df[toll_column] = 0.1 * merged_df[vehicle_type] * merged_df['distance']

    return merged_df


def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here

    # Convert 'startDay' and 'startTime' to datetime format
    df['startTime'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])

    # Define time intervals and corresponding toll rates
    time_intervals = [
        {'startTime': '00:00', 'end_time': '06:00', 'toll_rate': 0.05},
        {'startTime': '06:00', 'end_time': '12:00', 'toll_rate': 0.1},
        {'startTime': '12:00', 'end_time': '18:00', 'toll_rate': 0.15},
        {'startTime': '18:00', 'end_time': '24:00', 'toll_rate': 0.2},
    ]

    # Calculate toll rates based on time intervals
    df['time_based_toll_rate'] = 0.0  # Initialize the column
    for interval in time_intervals:
        mask = (df['startTime'].dt.time >= pd.to_datetime(interval['startTime']).time()) & \
               (df['startTime'].dt.time < pd.to_datetime(interval['endTime']).time())
        df.loc[mask, 'time_based_toll_rate'] = interval['toll_rate']

    return df

