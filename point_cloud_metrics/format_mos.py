import pandas as pd

# Read the CSV into a DataFrame, ignoring the first row
df = pd.read_csv('predicted_mos.csv', header=None, skiprows=1, names=['name', 'value'])

# Define the datasets, name filters, and dataset types
datasets = ['drjohnson', 'playroom', 'train', 'images_dark', 'truck', 'bin_new_medium', 'pingpong', 'bin_new_dark']
dataset_types = ['exposure', 'edge', 'both', '']
name_filters = {
    'old': '_old_input',
    'default': '_input',
    'old_post': '_old_input_post',
    'default_post': '_input_post'
}

# Create a dictionary to hold the grouped data
grouped_data = {(dataset, dtype): {version: None for version in name_filters} for dataset in datasets for dtype in dataset_types}

# Iterate over the rows and populate the grouped_data dictionary
for _, row in df.iterrows():
    name = row['name']
    value = row['value']
    matched = False
    for dataset in datasets:
        if dataset in name:
            for dtype in dataset_types:
                if dtype in name:
                    for version, filter_suffix in name_filters.items():
                        if name.endswith(filter_suffix):
                            grouped_data[(dataset, dtype)][version] = value
                            matched = True
                            break
                if matched:
                    break
        if matched:
            break

new_data = {
    'dataset': [],
    'dataset_type': [],
    'default': [],
    'old': [],
    'default_post': [],
    'old_post': []
}

for (dataset, dtype), versions in grouped_data.items():
    new_data['dataset'].append(dataset)
    new_data['dataset_type'].append(dtype)
    for version in name_filters:
        new_data[version].append(versions[version])

new_df = pd.DataFrame(new_data)

# Write the new DataFrame to a CSV file
new_df.to_csv('grouped_data.csv', index=False)
