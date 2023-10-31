from coffee_data import MENU, resources
import prettytable

print('Hello')
curr_resources = resources
total_profit = 0
MENU = MENU


def check_availability(drink):
    ingredients = MENU[drink]['ingredients']
    for k in ingredients:
        if ingredients[k] > resources[k]:
            print(f'Sorry. We do not have enough {k} for the drink')
            return False
    return True


def collect_cash(drink):
    denominations = {'quarters': 0.25, 'dimes': 0.1, 'nickel': 0.05, 'pennies': 0.01}
    bill = MENU[drink]['cost']
    print(f'The cost for the {drink} is {bill}')
    for coin in denominations:
        cash = int(input(f'How many {coin} will you pay with?'))
        bill -= denominations[coin] * cash
        if bill < 0:
            print(f'Thanks. Refunding you {-bill}')
            return True
        if bill == 0:
            print('Thanks for the payment')
            return True
    if bill > 0:
        print('Sorry that\'s not enough money. Money refunded')
        return False


def update_report(drink):
    global total_profit
    ingredients = MENU[drink]['ingredients']
    for i in ingredients:
        curr_resources[i] -= ingredients[i]
    total_profit += MENU[drink]['cost']


def get_drink(drink):
    drink_available = check_availability(drink)
    if drink_available:
        cash = collect_cash(drink)
        if cash:
            update_report(drink)
            print(f'Here is your {drink}. Enjoy')


def print_report(report):
    units = {'water': 'ml', 'milk': 'ml', 'coffee': 'gm'}
    for detail in report:
        print(f'{detail}: {str(report[detail]) + units[detail]}')


def check_resources():
    drink_list = []
    avail = True
    global curr_resources
    global MENU
    for drink_name in MENU:  # for each drink
        drink = MENU[drink_name]
        ingred = drink['ingredients']
        for i1 in ingred:  # for each ingredient
            if ingred[i1] > curr_resources[i1]:
                avail = False
                break
        if avail:
            drink_list.append(drink_name.capitalize())
    return drink_list


off = False
while not off:
    drink_list = check_resources()
    print('\n')
    if not drink_list:
        print('Sorry. Shop closed. None of the drinks can be provided now!')
        break
    choices = ' , '.join(drink_list)
    prompt = input("What would you like?: " + choices)
    if prompt.lower() not in drink_list + ['off', 'report'] and prompt.capitalize() not in drink_list + ['off', 'report']:
        print(drink_list + ['off', 'report'])
        print('Drink not recognized. Choose another drink ! ')
        continue
    if prompt == 'off':
        off = True
        print('Switching machine off....')
        continue
    if prompt == 'report':
        print_report(curr_resources)
        print('Profit: $', total_profit)
        continue
    get_drink(prompt)
