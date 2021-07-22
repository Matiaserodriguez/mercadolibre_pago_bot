import io
import re
import csv


from csv import writer
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage


def main():

    fieldnames = ['Date', 'Receipt_N°', 'Payment',
                  'Location', 'Payment_N°', 'Product_Name']

    all_data = []

    opened_program = True

    while opened_program:

        file_on_folder = False
        while file_on_folder == False:
            try:
                ml_file_input = input('Which is the MercadoLibre file? ')
                print()
                ml_file = ml_file_input + '.pdf'
                text_ml = extract_text_from_pdf(ml_file).lower()
                file_on_folder = True
            except FileNotFoundError:
                print('We were not able to find the file, please try again.')
                continue

        file_on_folder = False
        while file_on_folder == False:
            try:
                mp_file_input = input('Which is the MercadoPago file? ')
                print()
                mp_file = mp_file_input + '.pdf'
                text_mp = extract_text_from_pdf(mp_file).lower()
                file_on_folder = True
            except FileNotFoundError:
                print('We were not able to find the file, please try again.')
                continue

        try:

            day = get_day(text_ml)
            receipt = get_receipt(text_ml)
            user_payment = get_user_payment(
                get_price(text_mp), get_shipment_cost(text_mp))
            place = get_place(text_ml)
            payment_num = get_payment(text_mp)
            product_name = get_product(text_mp, payment_num)

            data = []

            append_list(data, day)
            append_list(data, str(receipt))
            append_list(data, str(user_payment))
            append_list(data, place)
            append_list(data, payment_num)
            append_list(data, product_name)

            # data.append(day)
            # data.append(str(receipt))
            # data.append(str(user_payment))
            # data.append(place)
            # data.append(payment_num)
            # data.append(product_name)

            append_list(all_data, data)

        except IndexError as index_error:
            print()
            print('There was an error on the program.')
            print(f'{index_error}. Please contact your administrator.')

        except ValueError as value_error:
            print()
            print('There was an error on the program.')
            print(f'{value_error}. Please contact your administrator.')

        except SyntaxError as syntax_error:
            print()
            print('There was an error on the program.')
            print(f'{syntax_error}. Please contact your administrator.')

        asking = True

        while asking:

            print()
            wants_continue = input(
                'Would you like to continue working? (y/n) ')

            if wants_continue.lower() == 'y':
                asking = False

            elif wants_continue.lower() == 'n':

                error_message = True

                while error_message:
                    print(
                        'Did your program work before, or it gave you an error message?')
                    new_answer = input(
                        'Please type "y" if it worked or "n" if it didn\'t: ')

                    if new_answer == 'y':

                        existing_file = True
                        while existing_file:
                            print()
                            save_work = input(
                                'Do you wanna save your file on an EXISTING file? y/n: ')

                            if save_work == 'y':
                                print()
                                file_name_input = input(
                                    'What is the name of the EXISTING csv file name? ')

                                try:
                                    file_name = file_name_input + '.csv'
                                    append_list_as_row(file_name, all_data)
                                except PermissionError:
                                    print()
                                    print(
                                        'There was a permission error. Your program must be opened, please, close it and try again.')
                                    continue

                                existing_file = False
                                error_message = False
                                asking = False
                                opened_program = False

                            elif save_work == 'n':
                                print()
                                file_name_input = input(
                                    'What name would you prefer for the NEW csv file name? ')
                                file_name = file_name_input + '.csv'
                                creates_csv(
                                    file_name, fieldnames, all_data)

                                existing_file = False
                                error_message = False
                                asking = False
                                opened_program = False

                            else:
                                print()
                                print(
                                    'Couldn\'t process your answer. Make sure to typed y or n, please')
                                continue

                    elif new_answer == 'n':

                        continue_working = True
                        while continue_working:
                            print()
                            print(
                                'Would you like to close the program or continue working?')
                            user_input = input(
                                'Type "quit" to close it or "continue" to keep working: ')
                            print()

                            if user_input == 'quit':
                                continue_working = False
                                error_message = False
                                asking = False
                                opened_program = False

                            elif user_input == 'continue':
                                print()
                                continue_working = False
                                error_message = False
                                asking = False
                                continue

                            else:
                                print()
                                print(
                                    'Couldn\'t process your answer. Make sure to type quit or continue, please')
                                continue

                    else:
                        print()
                        print(
                            'Couldn\'t process your answer. Make sure to type y or n, please')
                        continue

            else:
                print()
                print(
                    'Couldn\'t process your answer. Make sure to type y or n, please')
                continue


def creates_csv(file_name, fieldnames, list):
    '''@file_name: The name of the file the user wants to create
    @fieldnames: the fields of the columns
    @list: the list of the first row after the columns one.'''

    with open(file_name, 'w', newline='') as f:

        writer = csv.writer(f)
        writer.writerow(fieldnames)
        writer.writerows(list)


def append_list_as_row(file_name, list_of_lists):
    '''@file_name: the name of the existing csv file.
    @list_of_lists: the list within a list to loop and extract the data.
    f: the assigned name of the program on the function.
    csv_writer: it allows the program to be written.
    the "a+" is for append a new line at the end of the file.'''

    with open(file_name, 'a+', newline='') as f:

        csv_writer = writer(f)

        for i in list_of_lists:
            csv_writer.writerow(i)


def extract_text_from_pdf(pdf_path):
    '''Resource extracted from: https://dzone.com/articles/exporting-data-from-pdfs-with-python
    @pdf_path: takes the name of the pdf or the specific path.'''
    resource_manager = PDFResourceManager()
    file_handle = io.StringIO()
    converter = TextConverter(resource_manager, file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)

        text = file_handle.getvalue()

    # close open handles
    converter.close()
    file_handle.close()

    if text:
        return text


def append_list(list, str_num):
    '''@list: takes a list and appends the str_num to it.
    @str_num: a string or number to be appended to the list.
    new_list: the new list appended.'''

    list.append(str_num)


def get_place(string_ml):
    '''@string_ml: given string extracted from MercadoLibre PDF.
    place_search: matches the most closer approximation of the place.
    place: splits a couple specific times over specific objets.
    If the pattern doesn't work on the first try it will try another type of receipt
    and if that one doesn't work it will just return Not Found.'''

    try:
        place_search = re.findall(
            pattern='c\.p\.:.*facturanotascopyright', string=string_ml)

        place = place_search[0].split('c.p.:')[1:][0].split(
            ',')[1:][0].split('facturanotascopyright')[0].strip()

        return place

    except IndexError:
        try:
            place_search = re.findall(
                pattern='c\.p\.:.*notascopyright', string=string_ml)

            place = place_search[0].split('c.p.:')[1:][0].split(
                ',')[1:][0].split('notascopyright')[0].strip()

            return place

        except IndexError:
            return 'Not found'


def get_receipt(string_ml):
    '''@string_ml: given string extracted from MercadoLibre PDF.
    receipt_search: finds an approximate value of the receipt attached.
    receipt: splits over the string with '_' then takes the last element
    on the list, splits it again with '.pdf' and takes the rest. Then
    converts the value on int.
    If the attachment isn't on the PDF it will return Not Found'''

    try:
        receipt_search = re.findall(
            pattern='[0-9]+_[0-9]+.*.pdf', string=string_ml)

        receipt = int(receipt_search[0].split(
            '_')[-1].split('.pdf')[0])

        return receipt

    except IndexError:
        return 'Not Found'


def get_day(string_ml):
    '''@string_ml: given string extracted from MercadoLibre PDF.
    day_search: searches the most closer information about.
    If the receipt's day is not uploaded it will return Not Found'''

    try:
        day_search = re.findall(pattern='ventafactura.*\|', string=string_ml)

        day = day_search[0].split('ventafactura')[1:][0].split(' |')[:1]

        return day[0]

    except IndexError:
        return 'Not Found'


def get_payment(string_mp):
    '''@string_mp: given string extracted from MercadoPago PDF.
    -payment: matches the #followedByNumbers.
    if there are more than 1 n° of pyments (due to different cards)
    it will return the last match because that's the one we need.'''

    payment = re.findall(pattern='#[0-9]+', string=string_mp)

    if len(payment) == 3:
        return payment[2]
    elif len(payment) == 2:
        return payment[1]
    elif len(payment) == 1:
        return payment[0]
    else:
        return '+3 payments, contact your admin please.'


def get_product(string_mp, payment):
    '''@string_mp: given string extracted from MercadoPago PDF.
    @payment: the number of the payment.
    -product_search: looks over the closer approximation using regular expressions.
    product_name: acess the only element of the list and plits it over payment, 
    then takes the second argument and splits it again over '$' taking then the
    first parameter.
    If for some reason it cannot find the product, will return Not Found.'''

    try:
        product_search = re.findall(pattern=f'{payment}.*\$', string=string_mp)

        product_name = product_search[0].split(
            payment)[1:][0].split('$')[:1][0].strip()

        return product_name

    except IndexError:
        return 'Not found'


def get_user_payment(total_product, total_shipment):
    '''@total_product: takes the price of the product.
    @total_shipment: takes the price of the shipment
    -total: sum between parameters.'''

    total = total_product + total_shipment

    return total


def get_price(string_mp):
    '''@string_mp: given string extracted from MercadoPago PDF
    -price: searches for all the prices and all the alternatives using 
    regular expressions with the operaton '|'. 
    -product_price: the first item on the list will ALWAYS be the
    product price(what we want). Then splits over the $, takes the
    second string and then replaces the , for . if needed.'''

    price = re.findall(
        pattern='-\$[0-9]+.[0-9]+,[0-9]+|-\$[0-9]+.[0-9]+|-\$[0-9]+,[0-9]+|-\$[0-9]+|\$[0-9]+.[0-9]+,[0-9]+|\$[0-9]+.[0-9]+|\$[0-9]+,[0-9]+|\$[0-9]+', string=string_mp)

    product_price = float(price[0].split('$')[1:][0].replace(',', '.'))

    return product_price


def get_shipment_cost(string_mp):
    '''@string_mp: given string extracted from MercadoPago PDF
    -shipment_search: will match the search closer than possible
    -shipment: splits over the unservible text, takes the second string on the list
    and replace the ',' for '.' to be able to convert it to float.
    Sometimes there is no shipment cost, so it will return 0'''

    try:
        shipment_search = re.findall(
            pattern='costo de envío\$[0-9]+,[0-9]+|costo de envío\$[0-9]+|costo de envío\$[0-9]+.[0-9]+|costo de envío\$[0-9]+.[0-9]+,[0-9]+', string=string_mp)

        shipment = float(shipment_search[0].split(
            'costo de envío$')[1:][0].replace(',', '.'))

        return shipment

    except IndexError:
        return 0


if __name__ == '__main__':
    main()
