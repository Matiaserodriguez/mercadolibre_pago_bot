from mercadolibre_bot import get_place, get_receipt, get_day, get_payment,\
    get_product, get_user_payment, get_price, get_shipment_cost

import pytest


def test_get_place():

    assert get_place(
        'c.p.: thisisatest, CORRIENTESfacturanotascopyright') == 'CORRIENTES'
    assert get_place(
        'c.p.: 123testingifthisworks, bs asfacturanotascopyright') == 'bs as'
    assert get_place(
        'c.p.:calling to the test fuction 123, my result herenotascopyright') == 'my result here'
    assert get_place('I will just test the Not Found result') == 'Not found'


def test_get_receipt():

    assert get_receipt(
        'Factura6 de julio | 27222359142_006_00004_00002860.pdf') == 2860
    assert get_receipt(
        'Testing the get receipt function 27256243365_050_00009_00009210.pdf') == 9210
    assert get_receipt(
        'it doesn\'t matter what I put before this 27201299384_033_01900_00001827.pdf') == 1827
    assert get_receipt(
        'Let\'s test if it returns the Not Found') == 'Not Found'


def test_get_day():

    assert get_day('ventafactura29 de Febrero |') == '29 de Febrero'
    assert get_day(
        'ventafactura2 de abril | and it doesn\'t matter what do you have after') == '2 de abril'
    assert get_day(
        'ventafacturaJanuary 25th | and it doesn\'t matter what do you have after') == 'January 25th'
    assert get_day('Checking if the Not found will work') == 'Not Found'


def test_get_payment():

    assert get_payment(
        'askfbkjerb#2354326234236jdsfngjibr') == '#2354326234236'
    assert get_payment(
        'Testing with simbols # within the string / b#92138506, let\'s see') == '#92138506'
    assert get_payment(
        'Another test with 56% more (345) characters and #1984562 numbers 325324 ') == '#1984562'


def test_get_product():

    assert get_product(
        'testit#12354364253 productName$and also it doesnt matter here', '#12354364253') == 'productName'
    assert get_product(
        'lets test another#093496Bed SUPER TINY$ with more information', '#093496') == 'Bed SUPER TINY'
    assert get_product(
        '#235362and lets see if #9586Home Theater$also works on it', '#9586') == 'Home Theater'


def test_get_user_payment():
    
    assert get_user_payment(300, 500) == 800
    assert get_user_payment(30, 40) == 70
    assert get_user_payment(199, 293.54) == 492.54
    assert get_user_payment(213.43, 93.02) == 306.45


def test_get_price():

    assert get_price(
        'testtesttest$999,99testingtestingtesting-$9890moretests$3030') == 999.99
    assert get_price(
        'lets see the test here | $ # adding symbols$4392testingtestingtesting-$22moretests$3993') == 4392
    assert get_price(
        'the price is very important$739,21 because it\'ll give us the price\'s product') == 739.21


def test_get_shipment_cost():

    assert get_shipment_cost(
        'the string can make the things hard costo de envío$20234,99 but') == 20234.99
    assert get_shipment_cost(
        'It will give us the correct costo de envío$99 information') == 99
    assert get_shipment_cost(
        'and it doesnt matter what we take as costo de envío$21,39 \'cus') == 21.39
    assert get_shipment_cost(
        'we will be able to calculate the costo de envío$55483 anyways') == 55483


pytest.main(["-v", "--tb=line", "-rN", "mercadolibre_bot_test.py"])