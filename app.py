import os
import json

# Configuration constants
DATA_FOLDER = "data"
DATABASE_FILE = os.path.join(DATA_FOLDER, "karvands.json")
REPORT_FILE = os.path.join(DATA_FOLDER, "report.json")

# Main execution loop of the program
def main():
    database = load_data()  # Load JSON file into memory safely
    karvands = database['karvands']  # Extract the list of karvands

    print("Welcome to karvand management.")

    # Menu loop
    while True:
        choice = get_choice(
            "\n1-Add karvand\n2-Show karvands\n3-Search by ID\n4-Search by skills\n"
            "5-Edit karvand\n6-Delete karvand\n7-General Report\n8-Exit\nYour choice: "
        )
        match choice:
            case "1":
                add(karvands, database)
            case "2":
                show(karvands)
            case "3":
                search_by_id(karvands)
            case "4":
                search_by_skill(karvands)
            case "5":
                edit(karvands, database) 
            case "6":
                delete(karvands, database) 
            case "7":
                report(karvands) 
            case "8":
                print("Goodbye!")
                break

# Handles menu input validation
def get_choice(prompt):
    while True:
        try:
            choice = input(prompt).strip()
            # Allowed range updated to 8 to accommodate Report and Exit options
            if 1 <= int(choice) <= 8:
                return choice
            else:
                print("\tEnter a number from 1 to 8.")
        except ValueError:
            print("\tEnter a number.")

# Add a new karvand to the system
def add(karvands, database):
    print("\nEnter information of karvand")

    karvand = {}
    education = {}
    skills = []

    # Basic info
    karvand["id"] = assign_ID(karvands)
    karvand["full_name"] = input("Full name: ")
    karvand["email"] = input("Email: ")
    karvand["city"] = input("City: ")

    # Education
    education["degree"] = input("Degree: ")
    education["field"] = input("Field: ")

    # Collect skills
    while True:
        name = input("Skill (or press enter to finish): ").strip()
        if name == "":
            break
        skills.append(get_skill(name))

    karvand["education"] = education
    karvand["skills"] = skills

    karvands.append(karvand)
    save_data(database)
    print("\tAdding karvand was successful.")

# Display all registered karvands
def show(karvands):
    if not karvands:
        print("\nNo karvands found in the list.")
        return
    
    print("\n=========Registered Karvands==========")
    for index, karvand in enumerate(karvands, start=1):
        print(f"\t[{index}] ID: {karvand.get('id')} | {karvand.get('full_name','No Name')}")
        print(f"\tEmail: {karvand.get('email','N/A')}")
        print(f"\tCity: {karvand.get('city','N/A')}")

        edu = karvand.get("education", {})
        print(f"\tEducation: {edu.get('degree', 'N/A')} in {edu.get('field', 'N/A')}")

        skills = karvand.get("skills", [])
        if skills:
            print("\tSkills:")
            for skill in skills:
                name = skill.get("name", "N/A")
                level = skill.get("level", "N/A")
                score = skill.get("score", "N/A")
                print(f"\t  - {name} ({level}) | Score: {score}")
        else:
            print("\tSkills: None listed")
        print("\t" + "-" * 30)
    print("=======================================")

# Search for a specific karvand using their ID
def search_by_id(karvands):
    try:
        search_id = int(input("Enter the ID of the karvand to search for: "))
    except ValueError:
        print("\tPlease enter a valid numeric ID.")
        return

    target_karvand = None
    for karvand in karvands:
        if karvand.get("id") == search_id:
            target_karvand = karvand
            break

    if target_karvand:
        print(f"\n========== Karvand Details (ID: {search_id}) ==========")
        print(f"Name: {target_karvand.get('full_name', 'No Name')}")
        print(f"Email: {target_karvand.get('email', 'N/A')}")
        print(f"City: {target_karvand.get('city', 'N/A')}")

        edu = target_karvand.get("education", {})
        print(f"Education: {edu.get('degree', 'N/A')} in {edu.get('field', 'N/A')}")

        skills = target_karvand.get("skills", [])
        if skills:
            print("Skills:")
            for skill in skills:
                print(f"  - {skill.get('name', 'N/A')} ({skill.get('level', 'N/A')}) | Score: {skill.get('score', 'N/A')}")
        else:
            print("Skills: None listed")
        print("=" * 50)
    else:
        print(f"\nNo karvand found with ID {search_id}")


# Search for karvands who have a specific skill
def search_by_skill(karvands):
    search_query = input("Enter the skill name to search for: ").strip().lower()
    if not search_query:
        print("Invalid search input.")
        return

    found_any = False
    print(f"\n--- Search results for skill: '{search_query}' ---")
    for karvand in karvands:
        skills = karvand.get("skills", [])
        for skill in skills:
            if skill.get("name", "").strip().lower() == search_query:
                found_any = True
                print(f"ID: {karvand.get('id', 'N/A')} | Name: {karvand.get('full_name', 'No Name')} | City: {karvand.get('city', 'N/A')}")
                print(f"  - Skill: {skill.get('name')} | Level: {skill.get('level', 'N/A')} | Score: {skill.get('score', 'N/A')}")
                print("-" * 40)
                break 
                
    if not found_any:
        print("No participants found with that skill.")
    print("-------------------------------------------\n")

# Edit an existing karvand record
def edit(karvands, database):
    while True:
        try:
            search_id = int(input("Enter the ID of the karvand you want to edit: "))
            target_karvand = None

            for karvand in karvands:
                if karvand["id"] == search_id:
                    target_karvand = karvand
                    break

            if target_karvand is None:
                choice = input("Karvand not found, do you want to continue? (y/n): ")
                if choice.lower() != "y":
                    return
            else:
                break
        except ValueError:
            print("Enter karvand ID as a number.")

    print(f"\n--- Editing {target_karvand['full_name']} (ID: {search_id}) ---")

    # 1. Basic Info
    print("\nDo you want to edit basic information (Name, Email, City)? (y/n)")
    if input().lower() == "y":
        print("Leave blank and press Enter to keep current value.")
        name = input(f"Full Name [{target_karvand.get('full_name', '')}]: ")
        if name: target_karvand["full_name"] = name

        email = input(f"Email [{target_karvand.get('email', '')}]: ")
        if email: target_karvand["email"] = email

        city = input(f"City [{target_karvand.get('city', '')}]: ")
        if city: target_karvand["city"] = city

    # 2. Education
    print("\nDo you want to edit education details? (y/n)")
    if input().lower() == "y":
        print("Leave blank and press Enter to keep current value.")
        if "education" not in target_karvand:
            target_karvand["education"] = {"degree": "", "field": ""}
        edu = target_karvand["education"]

        degree = input(f"Degree [{edu.get('degree', '')}]: ")
        if degree: edu["degree"] = degree

        field = input(f"Field [{edu.get('field', '')}]: ")
        if field: edu["field"] = field

    # 3. Skills
    print("\nDo you want to edit skills? (y/n)")
    if input().lower() == "y":
        new_skills = []
        while True:
            s_name = input("Skill Name (leave blank to finish): ").strip()
            if not s_name:
                break
            new_skills.append(get_skill(s_name))
        if new_skills:
            target_karvand["skills"] = new_skills

    save_data(database)
    print("\n\tUpdate successful!")

# Delete a participant
def delete(karvands, database):
    while True:
        try:
            search_id = int(input("Enter the ID of the karvand you want to delete: "))
            target_karvand = None

            for karvand in karvands:
                if karvand["id"] == search_id:
                    target_karvand = karvand
                    break

            if target_karvand is None:
                choice = input("Karvand not found. Do you want to try another ID? (y/n): ")
                if choice.lower() != "y":
                    return 
            else:
                break
        except ValueError:
            print("Enter karvand ID as a number.")

    confirm = input(f"Are you sure you want to delete {target_karvand['full_name']} (ID: {search_id})? (y/n): ")
    if confirm.lower() == "y":
        karvands.remove(target_karvand)
        save_data(database)
        print(f"\n\tID {search_id} has been successfully deleted!")
    else:
        print("\n\tDeletion cancelled.")

# Generate statistics and save report as JSON
def report(karvands):
    if not karvands:
        print("\n\tNo data available to generate a report.")
        return

    total_students = len(karvands)
    total_skills_count = 0
    unique_skills = set()
    unique_cities = set()
    total_score = 0
    score_count = 0

    for k in karvands:

        city = k.get("city", "").strip().title()
        if city:
            unique_cities.add(city)

        skills = k.get("skills", [])
        for skill in skills:
            total_skills_count += 1
            skill_name = skill.get("name", "").strip().title()
            if skill_name:
                unique_skills.add(skill_name)
            
            try:
                score = float(skill.get("score", 0))
                total_score += score
                score_count += 1
            except (ValueError, TypeError):
                continue

    avg_score = (total_score / score_count) if score_count > 0 else 0.0
    unique_skills_list = sorted(list(unique_skills))
    unique_cities_list = sorted(list(unique_cities))

    # Format the report dictionary for JSON output
    report_data = {
        "total_karvands": total_students,
        "total_registered_skills": total_skills_count,
        "average_skill_score": round(avg_score, 2),
        "unique_skills": unique_skills_list,
        "unique_cities": unique_cities_list
    }

    # Print the report to the console
    print("\n================ GENERAL REPORT ================")
    print(f"Total Registered Karvands: {report_data['total_karvands']}")
    print(f"Total Registered Skills: {report_data['total_registered_skills']}")
    print(f"Average Skill Score: {report_data['average_skill_score']}")
    print(f"Unique Skills Count: {len(report_data['unique_skills'])}")
    print(f"Skills List: {', '.join(report_data['unique_skills']) if report_data['unique_skills'] else 'None'}")
    print(f"Cities List: {', '.join(report_data['unique_cities']) if report_data['unique_cities'] else 'None'}")
    print("================================================\n")

    # Save to report.json
    try:
        os.makedirs(DATA_FOLDER, exist_ok=True)
        with open(REPORT_FILE, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=4, ensure_ascii=False)
        print(f"\tReport successfully saved to {REPORT_FILE}")
    except Exception as e:
        print(f"Error saving report file: {e}")

# Validate and capture skill values
def get_skill(name):
    level = input(f"Level for {name}: ")
    while True:
        try:
            score = int(input(f"Score for {name} (0-100): "))
            if 0 <= score <= 100:
                return {"name": name, "level": level, "score": score}
            print("\tScore must be between 0 and 100.")
        except ValueError:
            print("\tPlease enter a valid integer.")

# Write the database to disk
def save_data(data):
    try:
        os.makedirs(DATA_FOLDER, exist_ok=True)
        with open(DATABASE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"\n\tData saved successfully to {DATABASE_FILE}!")
    except Exception as e:
        print(f"Error saving data: {e}")

# Load database and handle corruption automatically
def load_data():
    default_data = {
        "bootcamp": {
            "title": "Karvand Python",
            "year": 2026
        },
        "karvands": []
    }
    
    os.makedirs(DATA_FOLDER, exist_ok=True)

    if not os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "w", encoding="utf-8") as f:
            json.dump(default_data, f, indent=4, ensure_ascii=False)
        return default_data

    try:
        with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, TypeError) as e:
        print(f"\n[Warning] Database file is empty or corrupted: {e}")
        print("Recreating database file with default values...")
        with open(DATABASE_FILE, "w", encoding="utf-8") as f:
            json.dump(default_data, f, indent=4, ensure_ascii=False)
        return default_data

# Generate unique ID
def assign_ID(karvands):
    if not karvands:
        return 1
    return max(k.get("id", 0) for k in karvands) + 1


if __name__ == "__main__":
    main()
