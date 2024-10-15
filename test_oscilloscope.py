import pymeasure
from src.agilent54624A import Agilent54624A
print(pymeasure.__version__)

instrument = Agilent54624A(port='COM1')
instrument.connect()
instrument.checkOperational()
# instrument.select_channel(1)
# instrument.set_waveform_type("WORD")
# instrument.retrieve_data("WORD")
# instrument.select_channel(2)
# instrument.set_waveform_type("WORD")
# instrument.retrieve_data("WORD")
# instrument.disconnect()

def get_menu_response(items):
    response = ''
    while response == '':
        for i, item in enumerate(items):
            print(f'{i + 1}. {item}')

        print('q. Quit')
        print()

        response = input('> ')
        print()

        try:
            response = int(response)
        except:
            if response.lower() == 'q':
                return None
            print('ERROR: Non-integer input!')
            print()
            response = ''
            continue
        
        if response < 1 or response > len(items):
            print('ERROR: Input out of range!')
            print()
            response = ''

    return response

print()
print('Hello!')
print()

while True:
    print('---------')
    print('Main Menu')
    print('---------')
    print()
    response = get_menu_response(['Select Channel', 'Set Mode', 'Get Data'])

    if response == None:
        break

    elif response == 1:
        channel = get_menu_response(['Channel 1', 'Channel 2', 'Channel 3', 'Channel 4'])

        if channel != None:
            instrument.select_channel(channel)
    elif response == 2:
        items = ['WORD', 'BYTE', 'ASCII']
        selection = get_menu_response(items)

        if selection != None:
            instrument.set_waveform_type(items[selection - 1])

    elif response == 3:
        instrument.retrieve_data()

print('Goodbye :)')
print()