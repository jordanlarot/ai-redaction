import pandas as pd
import ast

FORGIVEN_LIST = [
'$', '$U', 'Accountability', 'Accounts', 'Administrator', 'Analyst', 'Applications',
'Assistant', 'Associate', 'Auto Loan Account', 'Branding', 'Checking Account',
'Chief Accounts Associate', 'Communications', 'Creative', 'Credit Card Account',
'Developer', 'Direct Accountability Architect', 'Director',
'District Accountability Coordinator', 'District Accountability Technician',
'Engineer', 'Facilitator', 'Female', 'Forward Accounts Developer', 'Functionality',
'Global Accountability Executive', 'Global Accounts Analyst', 'Home Loan Account',
'Identity', 'Infrastructure', 'Integration', 'Intranet', 'Investment Account',
'Investor Accountability Manager', 'Lead Accounts Supervisor',
'Legacy Accountability Administrator', 'Legacy Accounts Producer', 'Liaison',
'Male', 'Manager', 'Metrics', 'Miss', 'Money Market Account', 'Mr.', 'Mrs.', 'Ms.',
'Operations', 'Optimization', 'Personal Loan Account'
]



def redaction_accuracy(file_path):
    """
    Calculate the redaction accuracy of a model.
    """

    # Load data
    model_results = pd.read_csv(file_path)
    actual_results = pd.read_csv("./experiments/data/benchmark_data.csv")

    # Merge the two dataframes on the id column
    merged_results = pd.merge(actual_results, model_results, on="id")

    # Filter the merged results to only include the columns we want
    merged_results = merged_results[["id", "target_text", "privacy_mask", "redacted_text", "total_duration_seconds", "created_at", "model", "redacted_cases", "source_text"]]

    # Create a new column to list the redaction instance counts
    merged_results['n_redaction_instances'] = 0
    merged_results['redacted_count'] = 0

    # Loop through each row in the dataframe
    for index, row in merged_results.iterrows():
        # Fix the string by adding a comma between the dictionaries
        fixed_string_data = str(row["privacy_mask"]).replace("\n", "").replace("} {'", "}, {'")
        list_of_dicts = ast.literal_eval(fixed_string_data)  # Convert to list of dictionaries

        # Update total count
        merged_results.at[index, 'n_redaction_instances'] = len(list_of_dicts)

        # Check to see if the value is present in the redacted_text
        redacted_count = 0  # Reset redacted_count for each row
        unredacted_values = []  # List to store unredacted values
        for item in list_of_dicts:
            if item["value"] not in row["redacted_text"]:
                redacted_count += 1
            else:
                unredacted_values.append(item["value"])  # Add value that wasn't properly redacted
        merged_results.at[index, 'unredacted_values'] = unredacted_values  # Store the unredacted values
        
        merged_results.at[index, 'redacted_count'] = redacted_count  # Set the redacted_count for the current row

    # Reorder the columns
    merged_results = merged_results[[
        "id", 
        "created_at", 
        "model",
        "total_duration_seconds", 
        "source_text",
        "target_text", 
        "privacy_mask",
        "redacted_text",
        "redacted_cases",
        "n_redaction_instances",
        "redacted_count",
        "unredacted_values"
        ]]
    
    # Adjust the redaction instances and count
    merged_results['n_redaction_instances_adjusted'] = merged_results['n_redaction_instances'].copy()
    merged_results['redacted_count_adjusted'] = merged_results['redacted_count'].copy()
    merged_results['unredacted_values_adjusted'] = merged_results['unredacted_values'].copy()

    # Filter out any values that are in FORGIVEN_LIST from unredacted_values and update redacted_count
    for idx, row in merged_results.iterrows():
        removed = sum(1 for val in row['unredacted_values'] if val in FORGIVEN_LIST)
        merged_results.at[idx, 'n_redaction_instances_adjusted'] -= removed
        merged_results.at[idx, 'unredacted_values_adjusted'] = [val for val in row['unredacted_values'] if val not in FORGIVEN_LIST]

    # Create format accuracy column 
    merged_results['format_accuracy'] = 0

    # Check if all placeholder tags from redacted_cases are present in redacted_text
    for idx, row in merged_results.iterrows():
        # Convert string representation of list to actual list of dictionaries
        redacted_cases = ast.literal_eval(row['redacted_cases'])
        
        # Get all placeholder tags that should be in redacted_text
        placeholder_tags = [case['placeholder'] for case in redacted_cases]
        
        # Check if all placeholder tags are in redacted_text
        all_tags_present = all(tag in row['redacted_text'] for tag in placeholder_tags)
        
        merged_results.at[idx, 'format_accuracy'] = 1 if all_tags_present else 0

    return merged_results
    


if __name__ == "__main__":
    
    print("Calculating metrics for gemma3-4b...")

    # Get the results for the gemma-4b model
    results_4b = redaction_accuracy("./experiments/gemma3-4b/redacted_outputs.csv")

    print("Calculating metrics for gemma3-12b...")

    # Get the results for the gemma-4b model
    results_12b = redaction_accuracy("./experiments/gemma3-12b/redacted_outputs.csv")

    # Export the results for the gemma-4b model
    results_4b.to_csv("./experiments/gemma3-4b/evaluation_results.csv", index=False)

    # Export the results for the gemma-12b model
    results_12b.to_csv("./experiments/gemma3-12b/evaluation_results.csv", index=False)

    print("Exporting results to csv...")
