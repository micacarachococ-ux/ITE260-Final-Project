# MHAMA: LOCAL LAUNDRY SERVICE CASHIERING WITH RECEIPT SYSTEM
# BEGINNER VERSION - the whole program is organized into FUNCTIONS.
# No dictionaries are used. Only variables, lists, loops, if/elif/else and functions.
# (plus "import datetime" for the receipt date)
#
# VALIDATION RULE: every input() in this program is checked.
# If the answer is not valid, an error message is shown and the SAME question is asked again.

import datetime

# ---------------------------------------------------------------
# DATA (parallel lists: index 0 of every list belongs to service 0)
# ---------------------------------------------------------------
service_names = ["All in One Wash", "Thin Bedding", "Big Bedding", "Wash", "Dry"]
service_prices = [170, 195, 270, 65, 85]          # price for ONE load (up to the min. weight)
service_weights = [3.0, 4.0, 2.0, 8.0, 7.0]       # min. weight (kg) covered by that price
service_detergent = [True, True, True, False, False]
service_fabric_conditioner = [True, True, True, False, False]

staff_username = "staff"
staff_password = "wash123"

txn_dates = []
txn_customers = []
txn_services = []
txn_weights = []
txn_billed = []
txn_totals = []
txn_cash = []
txn_change = []
txn_detergent = []
txn_fabric_conditioner = []
txn_pickuptime = []


# ---------------------------------------------------------------
# VALIDATION HELPERS
# ---------------------------------------------------------------
def is_whole_number(text):
    """True if the text is only the digits 0-9 (example: 170)."""
    if text == "":
        return False
    for char in text:
        if char not in "0123456789":
            return False
    return True


def is_decimal_number(text):
    """True if the text is a decimal number (example: 170.50). Needs at least one digit."""
    if text == "":
        return False
    dot_count = 0
    digit_count = 0
    for char in text:
        if char not in "0123456789.":
            return False
        if char == ".":
            dot_count += 1
            if dot_count > 1:
                return False
        else:
            digit_count += 1
    return digit_count >= 1


def is_valid_person_name(text):
    """A person name: letters, spaces, . - ' only, at least one letter, up to 50 characters."""
    letters = 0
    for ch in text:
        if ch.isalpha():
            letters += 1
        elif ch not in " .-'":
            return False
    return letters >= 1 and len(text) <= 50


def is_valid_service_name(text):
    """A service name: letters, spaces, . - ' only, at least one letter, up to 50 characters."""
    return is_valid_person_name(text)


# ---------------------------------------------------------------
# TABLE / MENU DISPLAY
# ---------------------------------------------------------------
def table_lines(headers, rows):
    """Returns a list of strings; together they form a bordered table."""
    # width of each column = longest text in that column
    widths = []
    for header in headers:
        widths.append(len(str(header)))
    for row in rows:
        for i in range(len(row)):
            if len(str(row[i])) > widths[i]:
                widths[i] = len(str(row[i]))

    # border line like +------+-------+
    border = "+"
    for w in widths:
        border += "-" * (w + 2) + "+"

    # header line like | No. | Name |
    header_line = "|"
    for i in range(len(headers)):
        header_line += " " + str(headers[i]).center(widths[i]) + " |"

    lines = [border, header_line, border]
    for row in rows:
        line = "|"
        for i in range(len(row)):
            line += " " + str(row[i]).ljust(widths[i]) + " |"
        lines.append(line)
    lines.append(border)
    return lines


def print_table(headers, rows):
    """Prints a table with borders."""
    for line in table_lines(headers, rows):
        print(line)


def print_menu(title, options):
    """Prints a menu with a title and numbered options."""
    print(f"\n{title}")
    print("-" * len(title))
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")


def show_banner():
    """Prints the welcome banner."""
    print("=" * 50)
    print("             WELCOME TO MHAMA!")
    print("  LOCAL LAUNDRY SERVICE CASHIERING WITH RECEIPT")
    print("=" * 50)


def yes_no_text(value):
    """Returns 'Yes' if value is True, 'No' if value is False."""
    return "Yes" if value else "No"


SERVICE_HEADERS = ["No.", "Service Name", "Price per Load (PHP)", "Min Weight (kg)",
                   "Detergent", "Fabric Conditioner"]


def service_rows():
    """Builds the table rows for every service."""
    rows = []
    for i in range(len(service_names)):
        rows.append([i + 1, service_names[i], f"{service_prices[i]:.2f}", f"{service_weights[i]:.1f}",
                     yes_no_text(service_detergent[i]), yes_no_text(service_fabric_conditioner[i])])
    return rows


# ---------------------------------------------------------------
# INPUT HELPERS (each one repeats the question until the answer is valid)
# ---------------------------------------------------------------
def ask_menu_choice(prompt, valid_choices):
    """Keeps asking until the user types one of the valid choices."""
    choice = input(prompt).strip()
    while choice not in valid_choices:
        print("Invalid choice. Please type one of: " + ", ".join(valid_choices) + ".")
        choice = input(prompt).strip()
    return choice


def ask_positive(prompt, whole_number, allow_blank):
    """Keeps asking until the number is greater than zero.
    If whole_number is True, it must be a whole number.
    If allow_blank is True, typing nothing returns None."""
    while True:
        text = input(prompt).strip()
        if allow_blank and text == "":
            return None
        if whole_number:
            if is_whole_number(text):
                value = int(text)
                if value > 0:
                    return value
        else:
            if is_decimal_number(text):
                value = float(text)
                if value > 0:
                    return value
        print("Invalid input. Please enter a number greater than zero.")


def ask_yes_no(prompt, allow_blank):
    """Keeps asking until the user types y/yes or n/no.
    Returns "y" or "n" (or None if allow_blank is True and the user just pressed Enter)."""
    while True:
        text = input(prompt).strip().lower()
        if allow_blank and text == "":
            return None
        if text in ["y", "yes"]:
            return "y"
        if text in ["n", "no"]:
            return "n"
        print("Invalid input. Please type 'y' for yes or 'n' for no.")


def ask_text(prompt):
    """Keeps asking until the user types something that is not blank."""
    while True:
        text = input(prompt).strip()
        if text != "":
            return text
        print("This cannot be blank. Please try again.")


def ask_customer_name(prompt):
    """Returns a valid customer name, or "" if the user types 0 to go back."""
    while True:
        name = input(prompt).strip()
        if name == "0":
            return ""
        if is_valid_person_name(name):
            return name
        print("Invalid name. Use letters, spaces, . - ' only (at least one letter, up to 50 characters).")


def find_service(name):
    """Returns the index of the service with the given name, or -1 if not found."""
    for i in range(len(service_names)):
        if service_names[i].lower() == name.lower():
            return i
    return -1


def ask_new_service_name():
    """Asks for a NEW service name until it is valid and not a duplicate.
    Returns "" if the user types 0 to go back."""
    while True:
        name = input("Enter new service name (or 0 to go back): ").strip()
        if name == "0":
            return ""
        if not is_valid_service_name(name):
            print("Invalid service name. Use letters, spaces, . - ' only (at least one letter, up to 50 characters).")
            continue
        if find_service(name) != -1:
            print("This service already exists. Please enter a different service name.")
            continue
        return name


def ask_existing_service(prompt):
    """Asks for the name of a service that EXISTS.
    Returns the INDEX of that service, or -1 if the user types 0 to go back."""
    while True:
        name = input(prompt).strip()
        if name == "0":
            return -1
        index = find_service(name)
        if index != -1:
            return index
        print("Service not found. Please enter an existing service name or 0 to go back.")


# ---------------------------------------------------------------
# SERVICE FUNCTIONS (view / add / update / delete)
# ---------------------------------------------------------------
def show_services():
    """Prints every service with all of its details (used by staff and customers)."""
    print("\n~~~~~~ Service List ~~~~~~")
    if len(service_names) == 0:
        print("There are no services yet.")
        return
    print_table(SERVICE_HEADERS, service_rows())
    print("Note: the price covers one load up to the minimum weight.")
    print("      Heavier laundry is charged in proportion to the extra weight.")


def add_service():
    """Adds a new service to the lists."""
    print("\n~~~~~~ Add Service ~~~~~~")
    name = ask_new_service_name()
    if name == "":
        print("Add cancelled. Returning to the previous menu.")
        return

    price = ask_positive("Enter service price per load (whole number): ", True, False)
    weight = ask_positive("Enter minimum weight in kg: ", False, False)
    detergent = ask_yes_no("Does the service include detergent? (y/n): ", False) == "y"
    fabric_conditioner = ask_yes_no("Does the service include fabric conditioner? (y/n): ", False) == "y"

    service_names.append(name)
    service_prices.append(price)
    service_weights.append(weight)
    service_detergent.append(detergent)
    service_fabric_conditioner.append(fabric_conditioner)

    print("\n" + "*" * 50)
    print("'" + name + "' has been added to the service list.")
    print("*" * 50)


def update_service():
    """Updates a service. Leaving an answer blank keeps the current value."""
    print("\n~~~~~~ Update Service ~~~~~~")
    if len(service_names) == 0:
        print("There are no services to update.")
        return
    print_table(SERVICE_HEADERS, service_rows())
    i = ask_existing_service("Enter the name of the service to update (or 0 to go back): ")
    if i == -1:
        print("Update cancelled. Returning to the previous menu.")
        return

    print("Service found. Leave an answer blank to keep the current value.")
    new_price = ask_positive(f"Enter new price for '{service_names[i]}': ", True, True)
    new_weight = ask_positive(f"Enter new minimum weight for '{service_names[i]}': ", False, True)
    new_detergent = ask_yes_no(f"Does '{service_names[i]}' include detergent? (y/n): ", True)
    new_fabric = ask_yes_no(f"Does '{service_names[i]}' include fabric conditioner? (y/n): ", True)

    # Only overwrite a value if the user actually typed something
    if new_price is not None:
        service_prices[i] = new_price
    if new_weight is not None:
        service_weights[i] = new_weight
    if new_detergent is not None:
        service_detergent[i] = (new_detergent == "y")
    if new_fabric is not None:
        service_fabric_conditioner[i] = (new_fabric == "y")

    print("\n" + "*" * 50)
    print("'" + service_names[i] + "' has been updated in the service list.")
    print("*" * 50)


def delete_service():
    """Deletes a service from the lists."""
    print("\n~~~~~~ Delete Service ~~~~~~")
    if len(service_names) == 0:
        print("There are no services to delete.")
        return
    print_table(SERVICE_HEADERS, service_rows())
    i = ask_existing_service("Enter the name of the service to delete (or 0 to go back): ")
    if i == -1:
        print("Deletion cancelled. Returning to the previous menu.")
        return

    # Old transactions point to services by index, so deleting a service that
    # was already sold would break the receipts and the sales summary.
    for used in txn_services:
        if used >= i:
            print("This service cannot be deleted because transactions have already been recorded.")
            return

    confirm = ask_yes_no(f"Are you sure you want to delete '{service_names[i]}'? (y/n): ", False)
    if confirm == "y":
        deleted_service = service_names[i]
        del service_names[i]
        del service_prices[i]
        del service_weights[i]
        del service_detergent[i]
        del service_fabric_conditioner[i]
        print(f"Service '{deleted_service}' has been deleted successfully.")
    else:
        print("Deletion cancelled. Returning to the previous menu.")


# ---------------------------------------------------------------
# CASHIERING AND RECEIPT FUNCTIONS
# ---------------------------------------------------------------
def ask_number(prompt, minimum):
    """Keeps asking until the user types a number >= minimum.
    Returns the number as a float, or -1 if the user types 0 to go back."""
    while True:
        text = input(prompt).strip()
        if text == "0":
            return -1
        if is_decimal_number(text):
            value = float(text)
            if value >= minimum:
                return value
        print(f"Invalid input. Please enter a number greater than or equal to {minimum}.")


def ask_service():
    """Shows the service table and asks the user to choose one.
    Returns the index of the chosen service, or -1 if the user types 0 to go back."""
    print("\n~~~~~~ Choose a Service ~~~~~~")
    if len(service_names) == 0:
        print("There are no services available.")
        return -1
    print_table(SERVICE_HEADERS, service_rows())
    while True:
        choice = input("Enter the number of the service to choose (or 0 to go back): ").strip()
        if choice == "0":
            return -1
        if is_whole_number(choice):
            index = int(choice) - 1
            if 0 <= index < len(service_names):
                return index
        print("Invalid choice. Please enter a valid service number or 0 to go back.")


def compute_charge(price, minimum_weight, weight):
    """The price covers one load up to the minimum weight.
    Heavier laundry is charged in proportion to the weight."""
    if weight <= minimum_weight:
        return price
    return round(price * weight / minimum_weight, 2)


def generate_receipt(txn_index):
    """Returns the receipt as a simple list of text lines."""
    s = txn_services[txn_index]
    lines = []
    lines.append("MHAMA: LOCAL LAUNDRY SERVICE")
    lines.append("CASHIERING WITH RECEIPT SYSTEM")
    lines.append("=" * 50)
    lines.append(f"Date: {txn_dates[txn_index]}")
    lines.append(f"Customer: {txn_customers[txn_index]}")
    lines.append(f"Service: {service_names[s]}")
    lines.append(f"Weight: {txn_weights[txn_index]:.2f} kg")
    lines.append(f"Price per load: {service_prices[s]:.2f} PHP")
    lines.append(f"Minimum weight per load: {service_weights[s]:.2f} kg")
    lines.append(f"Detergent included: {yes_no_text(txn_detergent[txn_index])}")
    lines.append(f"Fabric conditioner included: {yes_no_text(txn_fabric_conditioner[txn_index])}")
    lines.append("-" * 50)
    lines.append(f"Total billed: {txn_billed[txn_index]:.2f} PHP")
    lines.append(f"Total paid: {txn_cash[txn_index]:.2f} PHP")
    lines.append(f"Change given: {txn_change[txn_index]:.2f} PHP")
    lines.append(f"Pickup time: {txn_pickuptime[txn_index]}")
    lines.append("=" * 50)
    lines.append("Tell us your name and we will call you when your laundry is ready for pickup.")
    lines.append("Thank you for choosing MHAMA! We appreciate your business.")
    return lines


def record_transaction(date_text, customer, s, weight, billed, total, cash, change,
                       detergent, fabric_conditioner, pickup_time):
    """Records a transaction in the transaction lists."""
    txn_dates.append(date_text)
    txn_customers.append(customer)
    txn_services.append(s)
    txn_weights.append(weight)
    txn_billed.append(billed)
    txn_totals.append(total)
    txn_cash.append(cash)
    txn_change.append(change)
    txn_detergent.append(detergent)
    txn_fabric_conditioner.append(fabric_conditioner)
    txn_pickuptime.append(pickup_time)


def new_transaction():
    """Whole cashiering process: name, service, weight, charge, cash, change, record, receipt."""
    print("\n~~~~~~ New Transaction ~~~~~~")
    customer = ask_customer_name("Enter customer name (or 0 to go back): ")
    if customer == "":
        print("Transaction cancelled. Returning to the previous menu.")
        return

    service_index = ask_service()
    if service_index == -1:
        print("Transaction cancelled. Returning to the previous menu.")
        return

    weight = ask_number("Enter weight of laundry in kg (or 0 to go back): ", 0.1)
    if weight == -1:
        print("Transaction cancelled. Returning to the previous menu.")
        return

    billed = compute_charge(service_prices[service_index], service_weights[service_index], weight)
    print(f"Total billed: {billed:.2f} PHP")

    cash = ask_number("Enter cash received (or 0 to go back): ", billed)
    if cash == -1:
        print("Transaction cancelled. Returning to the previous menu.")
        return

    change = round(cash - billed, 2)
    pickup_time = ask_text("Enter pickup time (e.g., Tomorrow at 3 PM): ")

    date_text = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    record_transaction(date_text, customer, service_index, weight, billed, billed, cash, change,
                       service_detergent[service_index], service_fabric_conditioner[service_index],
                       pickup_time)

    print()
    for line in generate_receipt(len(txn_dates) - 1):
        print(line)


def view_sales_summary():
    """Lists all transactions in a table, with a TOTAL row at the bottom."""
    print("\n~~~~~~ Sales Summary ~~~~~~")
    if len(txn_dates) == 0:
        print("There are no transactions yet.")
        return
    rows = []
    total_billed = 0
    total_cash = 0
    total_change = 0
    for i in range(len(txn_dates)):
        rows.append([i + 1, txn_dates[i], txn_customers[i], service_names[txn_services[i]],
                     f"{txn_weights[i]:.2f}", f"{txn_billed[i]:.2f}", f"{txn_cash[i]:.2f}",
                     f"{txn_change[i]:.2f}", txn_pickuptime[i]])
        total_billed += txn_billed[i]
        total_cash += txn_cash[i]
        total_change += txn_change[i]
    rows.append(["", "", "", "", "TOTAL", f"{total_billed:.2f}", f"{total_cash:.2f}",
                 f"{total_change:.2f}", ""])
    print_table(["No.", "Date", "Customer", "Service", "Weight (kg)", "Billed (PHP)",
                 "Cash (PHP)", "Change (PHP)", "Pickup Time"], rows)
    print("Note: records are not saved to a file. All data will be lost when the program ends.")


def check_order():
    """Customer types their name to see their order(s). Not case-sensitive.
    If the same name was used more than once, all of those orders are shown."""
    print("\n~~~~~~ Check Order ~~~~~~")
    if len(txn_dates) == 0:
        print("There are no transactions yet.")
        return
    name = ask_text("Enter your name to check your order (or 0 to go back): ")
    if name == "0":
        print("Returning to the previous menu.")
        return
    found = False
    for i in range(len(txn_dates)):
        if txn_customers[i].lower() == name.lower():
            print()
            for line in generate_receipt(i):
                print(line)
            found = True
    if not found:
        print(f"No orders found for '{name}'. Please check the spelling or try again later.")


# ---------------------------------------------------------------
# LOGIN AND MENUS
# ---------------------------------------------------------------
def staff_login():
    """Gives the user 3 wrong attempts. Returns True if the login worked, otherwise False.
    A blank username or password shows an error and asks again (it does not use an attempt).
    Typing 0 as the username goes back to the main menu."""
    print("\nStaff Login")
    attempts = 0
    while attempts < 3:
        username = input("Enter username (or 0 to go back): ").strip()
        if username == "0":
            print("Returning to the main menu.")
            return False
        if username == "":
            print("Username cannot be blank. Please try again.")
            continue
        password = input("Enter password: ").strip()
        if password == "":
            print("Password cannot be blank. Please try again.")
            continue
        if username == staff_username and password == staff_password:
            print("Login successful!")
            return True
        attempts += 1
        print(f"Incorrect username or password. You have {3 - attempts} attempts left.")
    print("Too many failed attempts. Returning to the main menu.")
    return False


def staff_menu():
    """Staff session loop. Stays in the staff menu until the user chooses to log out."""
    while True:
        print_menu("Staff Menu", ["View Services", "New Transaction", "Add Service", "Update Service",
                                  "Delete Service", "View Sales Summary", "Log Out"])
        choice = ask_menu_choice("Choose an option (1-7): ", ["1", "2", "3", "4", "5", "6", "7"])
        if choice == "1":
            show_services()
        elif choice == "2":
            new_transaction()
        elif choice == "3":
            add_service()
        elif choice == "4":
            update_service()
        elif choice == "5":
            delete_service()
        elif choice == "6":
            view_sales_summary()
        elif choice == "7":
            print("Logging out. Returning to the main menu.")
            break


def customer_menu():
    """Customer session loop. Stays here until the customer chooses to go back."""
    while True:
        print_menu("Customer Menu", ["View Services", "Check Order", "Exit"])
        choice = ask_menu_choice("Choose an option (1-3): ", ["1", "2", "3"])
        if choice == "1":
            show_services()
        elif choice == "2":
            check_order()
        elif choice == "3":
            print("Exiting the customer menu. Returning to the main menu.")
            break


def main():
    """Main program loop: keeps returning to the main menu until the user chooses to exit."""
    show_banner()
    while True:
        print_menu("Main Menu", ["Staff Login", "Customer Menu", "Exit"])
        choice = ask_menu_choice("Choose an option (1-3): ", ["1", "2", "3"])
        if choice == "1":
            if staff_login():
                staff_menu()
        elif choice == "2":
            customer_menu()
        elif choice == "3":
            print("Exiting the program. Goodbye!")
            break


main()