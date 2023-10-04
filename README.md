## Building monthly RSV vaccination aggregate report using Python and SQL

### To run code
	python rsv_report_generator.py
	
    Enter number of rows to output(1-11): 3
	
### Output
1. A CSV file with each row containing vaccination and Date Of Birth(DOB) date ranges along with vaccination and population counts for various age groups.
2. The vaccination and population counts are only computed for the rows entered as input. This allows us to generate cumulative counts upto the month of interest.
3. The 11 rows pertain to the 11 months in the reporting period.

### Algorithm
1. Build individual columns that contain static content.
1. Write the header of the CSV file.
2. Repeat the following until 11 rows are built
	- Assemble the columns containing static content.
	- For columns that need vaccination and population counts, call the appropriate SQL functions but only for the rows requested.
	- Combine the data as a comma separated string and write to CSV file.