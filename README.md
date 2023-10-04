# RSV vaccine monthly aggregate report using Python and SQL

### To run code
	python rsv_report_generator.py
	
    Enter number of rows to output(1-11): 3
	
### Output
1. A CSV file with each row containing vaccination and DOB date ranges, vaccine counts and population counts for various age groups.
2. The vaccine and population counts are only computed for the rows entered as input. This allows us to generate cumulative counts only upto the month of interest.

### Algorithm
1. Write the header of the CSV file.
2. Repeat the following until 11 rows are built
	- Build each row of the output by assembling the columns and calling the appropriate SQL functions to get vaccine and population counts but only for the rows requested.