"""
MIT License

Copyright (c) 2020 Karan Matalia

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""
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
