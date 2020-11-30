from src import CommonMonths, SeparateMonths

if __name__ == '__main__':
    template_type = int(input("Step 1. Enter 1 for individual months and 2 for common months\n"))
    csv_path = input("Step 2. Enter the path along with file name ending with '.csv' for your csv file\n")
    shapefile_path = input("Step 3. Enter the path along with file name ending with for your shapefile\n")
    shapefile_name = input("Step 4. Enter the file name for your shapefile\n")

    if template_type == 1:
        separate_months = SeparateMonths(csv_path, shapefile_path, shapefile_name)
        separate_months.process_data()
    elif template_type == 2:
        common_months = CommonMonths(csv_path, shapefile_path, shapefile_name)
        common_months.process_data()
