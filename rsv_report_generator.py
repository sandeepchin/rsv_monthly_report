
# Author: Sandeep Chintabathina
# Python program to generate monthly RSV vaccine dose report

import connect
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta

#Globals
conn= None
conn = connect.get_connection()
cursor = conn.cursor()

# Function to get number of rsv vaccine doses given dob range and vax date range
# Uses YYYY-MM-DD format for dates
def get_rsv_dose_count(dob_start: str,dob_end: str,vax_date_start: str,vax_date_end: str):
    try:
        cursor.execute('select prd_dmowner.get_rsv_count(%s,%s,%s,%s)',(dob_start,dob_end,vax_date_start,vax_date_end))
        rows=cursor.fetchall() # returns list of tuples(rows)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return rows[0]

# Function to get the population count given dob range
# Uses YYYY-MM-DD format for dates
def get_pop_count(dob_start: str,dob_end: str):
    try:
        cursor.execute('select prd_dmowner.get_pop_count(%s,%s)',(dob_start,dob_end))
        rows=cursor.fetchall() # returns list of tuples(rows)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return rows[0]

# Given a date the function will return the last date of that month
def get_last_day_date(somedate):
    if somedate.month==12:
        next_month_first_date = datetime(year=somedate.year+1,month=1,day=1)
    else:
        next_month_first_date = datetime(year=somedate.year,month=somedate.month+1,day=1)
    # Next month's first day - 1 day gives the month's last date
    last_day_date = next_month_first_date - timedelta(days=1)
    return last_day_date

# Changes date in mm/dd/yyyy to yyyy-mm-dd
def format_change(somedate):
    tokens = somedate.split('/')
    if len(tokens)<3:
        return ''
    year = tokens[2].strip()
    month = tokens[0].strip().zfill(2)
    date = tokens[1].strip().zfill(2)
    return year+'-'+month+'-'+date
    
    
if __name__=='__main__':
    
    # Output file
    outfile = open('rsv_monthly_report.csv','w')
    # Creating long string with parenthesis which does not add spaces, newlines etc. Using \ or triple quotes adds spaces
    header= ('RSV Season,Month,Vax date,0 months-7 months DOB range,0 months-7 months numerator,0 months-7 months population,'
    '8 months-19 months DOB range,8 months-19 months numerator,8 months-19 months population,60+ years DOB range,60+ years numerator,60+ years population,'
    '0 months-19 months DOB range,0 months-19 months numerator,0 months-19 months population,Report Due Date')
    # Create a dictionary of columns
    column={}
    column['a']='2023-24'
    column['b']=['Aug','Sept','Oct','Nov','Dec','Jan','Feb','Mar','Apr','May','Jun']
    # Building column c
    start_date = '7/1/2023'
    next_date = datetime.strptime('8/1/2023','%m/%d/%Y') 
    column['c']=[]
    for i in range(11):
        end_date = get_last_day_date(next_date)
        # Get the first of month for next iteration
        next_date = end_date +timedelta(days=1)
        # Build the string - # symbol allows no zero padding
        date_range = start_date+'-'+datetime.strftime(end_date,'%#m/%d/%Y')
        column['c'].append(date_range)
       
        '''
        Relativedelta is giving 30 days from current day and not last date, plus does not work with leap year
        # Convert str to datetime object
        end_date = datetime.strptime(end_date,'%m/%d/%Y')
        # Add a month
        end_date = end_date + relativedelta(months=)
        # Convert back to str
        end_date = datetime.strftime(end_date,'%#m/%d/%Y')
        '''
    #print(column['c'])
    column['d']='1/31/2023-9/30/2023'
    column['g']='1/31/2022-1/30/2023'
    column['j'] = '9/30/1963'
    column['m'] = '1/31/2022-9/30/2023'
    column['p'] = ['10/9/2023','10/9/2023']
    next_date = datetime.strptime('10/9/2023','%m/%d/%Y') 
    for i in range(9):
        end_date = get_last_day_date(next_date)
        # Add 9 days to end_date to get to 9th of every month
        next_date = end_date+timedelta(days=9)
        column['p'].append(datetime.strftime(next_date,'%#m/%d/%Y'))
   
    #print(column['p'])
    
    num_of_rows = int(input('Enter number of rows to output(1-11):'))
    
    outfile.write(header+'\n')
    # Building the report with 11 rows
    for i in range(11):
        # Get the vax end date which changes for each row
        # get it from column c constructed earlier
        vax_end_date = format_change(column['c'][i].split('-')[1])
        print(vax_end_date)
        if i< num_of_rows:
            # Get rsv dose count from db
            # returns a tuple of tuples, so must use index 0 after func call to get the return value
            column['e']=str(get_rsv_dose_count('2023-01-31','2023-09-30','2023-07-01',vax_end_date)[0])
            # Get pop count
            column['f']=str(get_pop_count('2023-01-31','2023-09-30')[0])
            column['h']=str(get_rsv_dose_count('2022-01-31','2023-01-30','2023-07-01',vax_end_date)[0])
            column['i']=str(get_pop_count('2022-01-31','2023-01-30')[0])
            column['k']=str(get_rsv_dose_count('1900-01-01','1963-09-30','2023-07-01',vax_end_date)[0])
            column['l']=str(get_pop_count('1900-01-01','1963-09-30')[0])
            column['n']=str(get_rsv_dose_count('2022-01-31','2023-09-30','2023-07-01',vax_end_date)[0])
            column['o']=str(get_pop_count('2022-01-31','2023-09-30')[0])
        else:
            column['e']=column['f']=''
            column['h']=column['i']=''
            column['k']=column['l']=''
            column['n']=column['o']=''
        row=''
        for key in sorted(column.keys()):
            # Could also use type() to check 
            if isinstance(column[key],str):
                row+=column[key]+','
            else:
                row+=column[key][i]+','
        #data=[column_a,column_b[i],column_c[i],column_d,column_e,column_f,column_g,column_h,column_i,column_j,column_k,column_l,column_m,column_n,column_o,column_p[i]]
        #print(data)
        #row = ','.join(data)
        row=row.strip(',')
        print(row)
        outfile.write(row+'\n')
    
   
    outfile.close()
    
#End of program