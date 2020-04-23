def add_column_in_csv(input_file, output_file, transform_row, col_name=None):
    from csv import writer
    from csv import reader
    """ Append a column in existing csv using csv.reader / csv.writer classes"""
    # Open the input_file in read mode and output_file in write mode
    with open(input_file, 'r') as read_obj, \
    open(output_file, 'w', newline='') as write_obj:
        # Create a csv.reader object from the input file object
        csv_reader = reader(read_obj)
        # Create a csv.writer object from the output file object
        csv_writer = writer(write_obj)
        # Read each row of the input csv file as list
        for row in csv_reader:
            # Insert column name here.
            if col_name != None and csv_reader.line_num == 1:
                row.append(col_name)
            else:
                # Pass the list / row in the transform function to add column text for this row
                transform_row(row, csv_reader.line_num)
                # Write the updated row / list to the output file
            csv_writer.writerow(row)

def insert_to_the_top(bottom, top):
    import pandas as pd
    

