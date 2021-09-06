import PyPDF2 as pdf
from argparse import ArgumentParser
from typing import AnyStr
import sys
import os
import time

"""
:return: Returns an argument parser for command line usage
"""
def get_parser() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(description='Unfuck a PDF slideshow')
    parser.add_argument('input', type=str, help='The name of the PDF to unfuck')
    parser.add_argument('--output', help='The name to save the unfucked PDF under')

    return parser

"""
Takes a PdfFileReader representing a PDF to unfuck and an output name as the filename to save the unfucked PDF as.
"""
def unfuck_and_save(pdf_reader: pdf.PdfFileReader, output_name: AnyStr) -> int:
    pdf_writer: pdf.PdfFileWriter = pdf.PdfFileWriter()
    
    included_pages = 0
    initial_pages = pdf_reader.getNumPages()
    last_page_index = pdf_reader.getNumPages() - 1
    for i in range(last_page_index):
        current_page = pdf_reader.getPage(i)
        next_page = pdf_reader.getPage(i + 1)

        current_text = current_page.extractText()
        next_text = next_page.extractText()

        # Check to see if the next slide contains this slide's text.  Good indicator that this slide is a duplicate.
        if not current_text in next_text:
            pdf_writer.addPage(current_page)
            included_pages += 1

        # Check to see if the next slide is the last slide.  Add it if it is.
        if i == last_page_index - 1:
            pdf_writer.addPage(next_page)
            included_pages += 1
        
    with open(output_name, 'wb') as output_file:
        pdf_writer.write(output_file)

    return initial_pages - included_pages

def main():
    parser: ArgumentParser = get_parser()
    args = parser.parse_args()
    input_file = args.input

    if not os.path.isfile(input_file):
        print(f'File \'{input_file}\' does not exist.')
        sys.exit(1)

    start_time = time.time()
    number_of_removed_pages = 0
    with open(input_file, 'rb') as file:
        pdf_reader: pdf.PdfFileReader = pdf.PdfFileReader(file)
        output_name = f'{input_file}.o'
        if args.output:
            output_name = args.output
        number_of_removed_pages = unfuck_and_save(pdf_reader, output_name)
    end_time = time.time()
    print(f'Unfucked {number_of_removed_pages} page{"s" if number_of_removed_pages > 1 else ""} in {(end_time - start_time):.3f} seconds')



if __name__ == '__main__':
    main()
    
