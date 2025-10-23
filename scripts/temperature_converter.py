def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5/9

# Input and Output
choice = input("Convert from (C)elsius to Fahrenheit or (F)ahrenheit to Celsius? ").lower()

if choice == 'c':
    celsius = float(input("Enter temperature in Celsius: "))
    print(f"{celsius}°C is {celsius_to_fahrenheit(celsius)}°F")
elif choice == 'f':
    fahrenheit = float(input("Enter temperature in Fahrenheit: "))
    print(f"{fahrenheit}°F is {fahrenheit_to_celsius(fahrenheit)}°C")
else:
    print("Invalid choice!")
