import hashlib
import datetime

# Password hashing function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Initialize appliances list
appliances = [
    {"name": "Electric Fan", "power_watts": 75, "hours_per_day": 9, "days": 30,"warranty":"1 year"},
    {"name": "Refrigerator", "power_watts": 175, "hours_per_day": 24, "days": 30,"warranty":"6 months"},
    {"name": "Television", "power_watts": 120, "hours_per_day": 7, "days": 30,"warranty":"4 months"},
]

# In-memory user database
users_db = {
    
}

# User registration
def register():
    global users_db
    print("\n----- Registration ----- ")
    user_name = input("Enter User Name: ")
    user_email = input("Enter Your Email: ")

    # Check if the username or email already exists
    for user in users_db.values():
        if user["email"] == user_email:
            print("User with this email already exists.")
            return

    if user_name in users_db:
        print("Username already exists.")
        return

    password = input("Enter Password: ")
    hashed_pwd = hash_password(password)

    # Add user to the database
    users_db[user_name] = {
        "name": user_name,
        "email": user_email,
        "password": hashed_pwd,
        "appliances": []
    }

    print("Congratulations, Registration Successful!\n")
    login()

# User login
def login():
    print("\n--- Login ---")
    user_email = input("Enter your email: ")
    password = input("Enter your password: ")
    hashed_pwd = hash_password(password)

    # Search for user by email
    for user in users_db.values():
        if user["email"] == user_email and user["password"] == hashed_pwd:
            print(f"Welcome back, {user['name']}!\n")
            power_calculator()
        else:
            print("Incorrect password or email.\n")
             

    

def calculate_energy_consumption(watts, hours_per_day, days):
    kilowatts = watts / 1000  # convert watts to kilowatts
    return kilowatts * hours_per_day * days

def display_appliances(appliances):
    if not appliances:
        print("\nNo appliances added yet.")
        return
    print("\n--- Current Appliances ---")
    for idx, app in enumerate(appliances, start=1):
        print(f"{idx}. {app['name']} - {app['power_watts']}W, {app['hours_per_day']} hrs/day, {app['days']} days, {app['warranty']}")

def view_report(appliances, cost_per_kwh,alert=2000):
    total_energy = 0
    total_cost = 0
    if not appliances:
        print("\nNo appliances to display.")
        return
    print("\n--- Consumption Report ---")
    for app in appliances:
        energy = calculate_energy_consumption(app['power_watts'], app['hours_per_day'], app['days'])
        cost = energy * cost_per_kwh
        print(f"{app['name']}: {energy:.2f} kWh, Cost: {cost:.2f}")
        total_energy += energy
        total_cost += cost
    print("\n--- Summary ---")
    print(f"Total Energy Consumed: {total_energy:.2f} kWh")
    print(f"Total Estimated Cost: {total_cost:.2f}")
    
    # ⚠️ Alert if cost is too high
    if total_cost > alert:
        print("\n⚠️ ALERT: Your total estimated cost exceeds ₱{:.2f}!".format(alert))
        print("   Consider reducing appliance usage or checking for high-consuming devices.")
        
    # Warranty alert for items with less than 6 months warranty
    for appliance in appliances:
    # Extract number of months from warranty string
      warranty_str = str(appliance["warranty"]).lower()
      if "month" in warranty_str:
        months = int(warranty_str.split()[0])
        if months < 6:
            print(f"🔧 WARRANTY ALERT: '{appliance['name']}' has only {appliance['warranty']} warranty left!")
              
# Power Consumption Calculator
def power_calculator():
    global appliances
    print("⚡ Welcome to the Electricity Consumption Calculator ⚡")
    print(f"📊 Initial appliances: {len(appliances)} found.")

    try:
        cost_per_kwh = float(input("💰 Enter cost per kWh (default is 10): ") or 10)

        while True:
            print("\n📌 ━━━ MENU ━━━")
            print("1️⃣  Add Appliance")
            print("2️⃣  Edit Appliance")
            print("3️⃣  Delete Appliance")
            print("4️⃣  View Appliances and Report")
            print("5️⃣  View Summary Only")
            print("6️⃣  Monthly Report")
            print("7️⃣  Sort Appliances by Cost or Energy")
            print("8️⃣  Save and Exit")
            
            choice = input("➡️  Choose an option (1-7): ")

            if choice == "1":
                # Add appliance
                name = input("📦 Appliance name: ")
                power_watts = float(input(f"🔌 Power rating of {name} (in watts): "))
                hours_per_day = float(input(f"⏰ Hours used per day for {name}: "))
                days = int(input(f"📅 Number of days used: "))
                warranty = int(input(f"📅 Warranty in years or months: "))
                appliances.append({
                    "name": name,
                    "power_watts": power_watts,
                    "hours_per_day": hours_per_day,
                    "days": days,
                    "warranty": warranty
                    
                })
                print(f"✅ {name} added successfully.")

            elif choice == "2":
                # Edit appliance
                display_appliances(appliances)
                if appliances:
                    idx = int(input("✏️ Enter appliance number to edit: ")) - 1
                    if 0 <= idx < len(appliances):
                        app = appliances[idx]
                        print(f"🔧 Editing {app['name']}...")
                        app['name'] = input(f"New name (Enter to keep '{app['name']}'): ") or app['name']
                        power_input = input(f"New power (Enter to keep {app['power_watts']}W): ")
                        hours_input = input(f"New hours/day (Enter to keep {app['hours_per_day']}): ")
                        days_input = input(f"New days (Enter to keep {app['days']}): ")

                        if power_input: app['power_watts'] = float(power_input)
                        if hours_input: app['hours_per_day'] = float(hours_input)
                        if days_input: app['days'] = int(days_input)

                        print("✅ Appliance updated.")
                    else:
                        print("❌ Invalid appliance number.")

            elif choice == "3":
                # Delete appliance
                display_appliances(appliances)
                if appliances:
                    idx = int(input("🗑️ Enter appliance number to delete: ")) - 1
                    if 0 <= idx < len(appliances):
                        deleted = appliances.pop(idx)
                        print(f"🗑️ {deleted['name']} deleted.")
                    else:
                        print("❌ Invalid appliance number.")

            elif choice == "4":
                # View full report
                display_appliances(appliances)
                view_report(appliances, cost_per_kwh,alert=2000)

            elif choice == "5":
                # View summary only
                total_energy = sum(
                    calculate_energy_consumption(a['power_watts'], a['hours_per_day'], a['days'])
                    for a in appliances
                )
                total_cost = total_energy * cost_per_kwh
                print("\n📈 ━━━ SUMMARY ━━━")
                print(f"Total Energy: {total_energy:.2f} kWh")
                print(f"Total Cost:   {total_cost:.2f} currency units")
                
            elif choice == '6':
                cost_per_kwh = float(input("Enter cost per kWh: "))
                display_monthly_report(appliances, cost_per_kwh) 
                
            elif choice == "7":
                # Sort appliances
                print("\n🔽 Sort by:")
                print("1. Cost (Highest First)")
                print("2. Energy Usage (Highest First)")
                sort_choice = input("Choose (1-2): ")

                if sort_choice == "1":
                    sorted_apps = sorted(appliances, key=lambda a: calculate_energy_consumption(
                        a['power_watts'], a['hours_per_day'], a['days']) * cost_per_kwh, reverse=True)
                elif sort_choice == "2":
                    sorted_apps = sorted(appliances, key=lambda a: calculate_energy_consumption(
                        a['power_watts'], a['hours_per_day'], a['days']), reverse=True)
                else:
                    print("❌ Invalid sort option.")
                    continue

                print("\n📊 Sorted Appliances:")
                for app in sorted_apps:
                    energy = calculate_energy_consumption(app['power_watts'], app['hours_per_day'], app['days'])
                    cost = energy * cost_per_kwh
                    print(f"- {app['name']}: {energy:.2f} kWh, Cost: {cost:.2f}")

            elif choice == "8":
                if appliances:
                    filename = f"electricity_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                    with open(filename, "w") as f:
                        f.write("--- Consumption Report ---\n")
                        total_energy = 0
                        total_cost = 0
                        for app in appliances:
                            energy = calculate_energy_consumption(app['power_watts'], app['hours_per_day'], app['days'])
                            cost = energy * cost_per_kwh
                            f.write(f"{app['name']}: {energy:.2f} kWh, Cost: {cost:.2f}\n")
                            total_energy += energy
                            total_cost += cost
                        f.write("\n--- Summary ---\n")
                        f.write(f"Total Energy Consumed: {total_energy:.2f} kWh\n")
                        f.write(f"Total Estimated Cost: {total_cost:.2f}\n")
                    print(f"\nReport saved as {filename}")
                
                print("👋 Goodbye! Your session is complete.")
                break

            else:
                print("❌ Invalid choice. Please choose from 1 to 7.")

    except ValueError:
        print("\n❗ Invalid input! Use numbers where required.")
    except Exception as e:
        print(f"\n❗ Unexpected error: {e}")

# Monthly Report
def display_monthly_report(appliances, cost_per_kwh):
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║          📊 Monthly Energy Consumption Report         ║")
    print("╠════════════════════════╦══════════════╦═══════════════╣")
    print("║ Appliance              ║ Energy (kWh) ║     Cost ($)  ║")
    print("╠════════════════════════╬══════════════╬═══════════════╣")

    total_energy = 0
    total_cost = 0
    cost_summary = []

    for app in appliances:
        energy = calculate_energy_consumption(app['power_watts'], app['hours_per_day'], app['days'])
        cost = energy * cost_per_kwh
        print("║ {:<22} ║ {:>12.2f} ║ {:>13.2f} ║".format(app['name'], energy, cost))
        total_energy += energy
        total_cost += cost
        cost_summary.append({'name': app['name'], 'cost': cost})

    print("╠════════════════════════╬══════════════╬═══════════════╣")
    print("║ TOTAL                  ║ {:>12.2f} ║ {:>13.2f} ║".format(total_energy, total_cost))
    print("╚════════════════════════╩══════════════╩═══════════════╝")

    # 🔍 Cost comparison summary
    highest = max(cost_summary, key=lambda x: x['cost'])
    lowest = min(cost_summary, key=lambda x: x['cost'])

    print("\n📌 Cost Comparison:")
    print(f"🔺 Most Expensive Appliance: {highest['name']} (${highest['cost']:.2f})")
    print(f"🔻 Least Expensive Appliance: {lowest['name']} (${lowest['cost']:.2f})\n")


# Contact Us
def contact_us():
    print("\n📞━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("              CONTACT US              ")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━📧")
    print("📍 For any inquiries, feel free to reach out to us:")
    print("   ✉️  Email: group6@Cpe-1203.com")
    print("   🌐  Website: www.group6.com")
    print("   🕑  Support Hours: Mon–Fri, 9 AM – 5 PM")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")


# Main Menu
def main():
    while True:
            print("\n--- Main Menu ---")
            print("1. Registration")
            print("2. Login")
            print("3. Contact Us")
            print("4. Exit")
            choice = input("Choose an option (1-4): ")

            if choice == '1':
                register()
            elif choice == '2':
                logged_in = login()  # This will set logged_in = True if login is successful
            elif choice == '3':
                contact_us()
            elif choice == '4':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please choose a valid option.")


# Run the program
main()
