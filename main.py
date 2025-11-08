import csv
import json
import os
from datetime import datetime
from tabulate import tabulate
import matplotlib.pyplot as plt

data_files = {"climate_data": "climate_data.csv", "researchers": "researchers.csv", "reports": "reports.csv", "categories": "categories.csv", "access": "access.csv"}

admins = [{"username": "admin1", "password": "pass1"}, {"username": "admin2", "password": "pass2"}, {"username": "admin3", "password": "pass3"}]

climate_fields = ["record_id", "region", "date", "temperature", "rainfall", "air_quality", "co2_level", "humidity"]
researcher_fields = ["researcher_id", "name", "org", "field", "contact", "pwd"]
report_fields = ["report_id", "researcher_id", "type", "parameters", "generated_on"]
categories_fields = ["cat_id", "name", "description"]
access_fields = ["req_id", "researcher_id", "status", "approved_by"]


def ensure_files_exist():
    for key, file in data_files.items():
        if not os.path.exists(file):
            with open(file, "w", newline='') as f:
                writer = csv.writer(f)
                if key == "climate_data":
                    writer.writerow(climate_fields)
                elif key == "researchers":
                    writer.writerow(researcher_fields)
                elif key == "reports":
                    writer.writerow(report_fields)
                elif key == "categories":
                    writer.writerow(categories_fields)
                elif key == "access":
                    writer.writerow(access_fields)

def load_csv(file_path, expected_fields=None):
    if not os.path.exists(file_path):
        return []
    with open(file_path, newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        if expected_fields:
            for r in rows:
                for ef in expected_fields:
                    if ef not in r:
                        r[ef] = ""
            file_fields = reader.fieldnames or []
            missing = [ef for ef in expected_fields if ef not in file_fields]
            if missing:
                write_csv(file_path, rows, expected_fields)
        return rows

def write_csv(file_path, rows, fieldnames):
    with open(file_path, "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            row = {k: ("" if r.get(k) is None else r.get(k)) for k in fieldnames}
            writer.writerow(row)

def append_row(file_path, row, fieldnames):
    file_exists = os.path.exists(file_path) and os.path.getsize(file_path) > 0
    with open(file_path, "a", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        out = {k: (row.get(k, "")) for k in fieldnames}
        writer.writerow(out)

def display_table(list_of_dicts):
    if not list_of_dicts:
        print("\nNo records found.\n")
        return
    print(tabulate(list_of_dicts, headers="keys", tablefmt="grid"))

def safe_input(prompt):
    try:
        return input(prompt)
    except EOFError:
        return ""

def admin_login():
    print("\n--- Admin Login ---")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    for adm in admins:
        if adm["username"] == username and adm["password"] == password:
            print(f"\nWelcome, {username}!\n")
            return username
    print("Invalid admin credentials.\n")
    return None

def add_climate_record():
    data = load_csv(data_files["climate_data"], climate_fields)
    max_id = 0
    for r in data:
        val = int(r.get("record_id", "0"))
        if val > max_id: max_id = val
    record_id = str(max_id + 1)
    print("\nEnter new climate record details:")
    region = safe_input("Region: ").strip()
    date = safe_input("Date (YYYY-MM-DD): ").strip()
    temperature = safe_input("Temperature: ").strip()
    rainfall = safe_input("Rainfall: ").strip()
    air_quality = safe_input("Air Quality: ").strip()
    co2_level = safe_input("CO2 Level: ").strip()
    humidity = safe_input("Humidity: ").strip()
    row = {"record_id": record_id,
        "region": region,
        "date": date,
        "temperature": temperature,
        "rainfall": rainfall,
        "air_quality": air_quality,
        "co2_level": co2_level,
        "humidity": humidity}
    append_row(data_files["climate_data"], row, climate_fields)
    print("Record added successfully.\n")


def update_delete_climate_data():
    data = load_csv(data_files["climate_data"], climate_fields)
    if not data:
        print("No climate data available to modify.")
        return
    display_table(data)
    rid = safe_input("Enter record_id to Update/Delete: ").strip()
    for i, r in enumerate(data):
        if r.get("record_id") == rid:
            action = safe_input("Type U to update or D to delete: ").strip().lower()
            if action == 'd':
                data.pop(i)
                write_csv(data_files["climate_data"], data, climate_fields)
                print("Record deleted.")
                return
            elif action == 'u':
                print("Press Enter to keep current value.")
                for field in climate_fields:
                    if field == 'record_id':
                        continue
                    cur = r.get(field, "")
                    new = safe_input(f"{field} ({cur}): ").strip()
                    if new != "":
                        r[field] = new
                data[i] = r
                write_csv(data_files["climate_data"], data, climate_fields)
                print("Record updated.")
                return
            else:
                print("Unknown action.")
                return
    if 'action' not in locals():
        print("record_id not found.")


def manage_categories():
    data = load_csv(data_files["categories"], categories_fields)
    while True:
        print("\n--- Manage Categories ---")
        print("1. Add Category\n2. View Categories\n3. Update Category\n4. Delete Category\n5. Back")
        choice = safe_input("Choice: ").strip()
        if choice == '1':
            max_id = 0
            for c in data:
                v = int(c.get('cat_id','0'))
                if v>max_id: max_id=v
            cid = str(max_id+1)
            name = safe_input("Category name: ").strip()
            desc = safe_input("Description: ").strip()
            append_row(data_files["categories"], {"cat_id":cid, "name":name, "description":desc}, categories_fields)
            data = load_csv(data_files["categories"], categories_fields)
            print("Category added.")
        elif choice == '2':
            display_table(load_csv(data_files["categories"], categories_fields))
        elif choice == '3':
            display_table(data)
            cid = safe_input("Enter cat_id to update: ").strip()
            for i,c in enumerate(data):
                if c.get('cat_id')==cid:
                    print("Press Enter to keep current value.")
                    for f in categories_fields:
                        if f=='cat_id': continue
                        new = safe_input(f"{f} ({c.get(f,'')}): ").strip()
                        if new!='': c[f]=new
                    data[i]=c
                    write_csv(data_files["categories"], data, categories_fields)
                    print("Category updated.")
                    break
            else:
                print("cat_id not found.")
        elif choice == '4':
            display_table(data)
            cid = safe_input("Enter cat_id to delete: ").strip()
            data = [c for c in data if c.get('cat_id')!=cid]
            write_csv(data_files["categories"], data, categories_fields)
            print("Category deleted if it existed.")
        elif choice == '5':
            break
        else:
            print("Invalid choice.")


def upload_bulk_data():
    path = safe_input("Enter path to CSV or JSON file for bulk climate data import: ").strip()
    if not os.path.exists(path):
        print("File does not exist.")
        return
    new_records = []
    try:
        if path.lower().endswith('.csv'):
            with open(path, newline='') as f:
                reader = csv.DictReader(f)
                for r in reader:
                    new_records.append(r)
        elif path.lower().endswith('.json'):
            with open(path, 'r') as f:
                loaded = json.load(f)
                if isinstance(loaded, list):
                    new_records = loaded
                elif isinstance(loaded, dict):
                    if all(isinstance(v, dict) for v in loaded.values()):
                        new_records = list(loaded.values())
                    else:
                        new_records = [loaded]
                else:
                    print("JSON format not recognized. Expecting list or dict.")
                    return
        else:
            print("Unsupported file type. Use .csv or .json")
            return
    except Exception as e:
        print("Failed to load file:", e)
        return
    climate = load_csv(data_files["climate_data"], climate_fields)
    max_id = 0
    for r in climate:
        v = int(r.get('record_id','0'))
        if v>max_id: max_id=v
    next_id = max_id + 1
    prepared = []
    for rec in new_records:
        row = {}
        for f in climate_fields:
            if f == 'record_id':
                row['record_id'] = str(next_id)
            else:
                val = rec.get(f, None)
                if val is None:
                    alt = f.replace('_',' ')
                    val = rec.get(alt, rec.get(alt.lower(), rec.get(alt.upper(), '')))
                row[f] = str(val) if val is not None else ''
        prepared.append(row)
        next_id += 1
    for r in prepared:
        append_row(data_files["climate_data"], r, climate_fields)
    print(f"Imported {len(prepared)} records into {data_files['climate_data']}.")


def generate_reports_admin():
    data = load_csv(data_files["climate_data"], climate_fields)
    if not data:
        print("No climate data available.")
        return
    print("\n--- Admin Analytics ---\n1. Monthly Trend\n2. Annual Trend\n3. Anomaly Detection (Z-score)\n4. Extreme Events (top 5)")
    choice = safe_input("Select option: ").strip()
    region = safe_input("Region (leave blank for ALL): ").strip()
    param = safe_input("Parameter (temperature / air_quality / co2_level / rainfall / humidity): ").strip()
    if param not in ["temperature","air_quality","co2_level","rainfall","humidity"]:
        print("Invalid parameter.")
        return
    filtered = data
    if region:
        filtered = [r for r in data if r.get('region','').lower()==region.lower()]
    if not filtered:
        print("No matching records.")
        return
    for r in filtered:
        r[param] = float(r.get(param,'0'))

    if choice == '1':
        buckets = {}
        for r in filtered:
            y,m,_ = r['date'].split('-')
            key = f"{y}-{m}"
            buckets.setdefault(key, []).append(r[param])
        print(f"\nMONTHLY AVG for {param}:")
        for k,v in sorted(buckets.items()):
            vv = [x for x in v if x is not None]
            if vv: print(k, "->", round(sum(vv)/len(vv),2))

    elif choice == '2':
        buckets = {}
        for r in filtered:
            y = r['date'][:4]
            buckets.setdefault(y, []).append(r[param])
        print(f"\nANNUAL AVG for {param}:")
        for k,v in sorted(buckets.items()):
            vv=[x for x in v if x is not None]
            if vv: print(k, "->", round(sum(vv)/len(vv),2))

    elif choice == '3':
        vals = [r[param] for r in filtered if r[param] is not None]
        avg = sum(vals)/len(vals)
        import math
        sd = math.sqrt(sum((x-avg)**2 for x in vals)/len(vals))
        print(f"\nANOMALIES in {param} (|Z| > 2):")
        for r in filtered:
            v = r[param]
            if v is None: continue
            z=(v-avg)/sd
            if abs(z)>2:
                print(r['date'], r['region'], v, f"Z={round(z,2)}")

    elif choice == '4':
        top = sorted(filtered, key=lambda x:x[param], reverse=True)[:5]
        print(f"\nTOP 5 EXTREME {param.upper()} EVENTS:")
        display_table(top)

    else:
        print("Invalid option.")
        return


def manage_researcher_access(admin_username):
    access = load_csv(data_files["access"], access_fields)
    if not access:
        print("No access requests present.")
    display_table(access)
    req = safe_input("Enter req_id to update (or press Enter to go back): ").strip()
    if not req:
        return
    for i,a in enumerate(access):
        if a.get('req_id')==req:
            new = safe_input("Enter status (approved/rejected/pending): ").strip()
            a['status']=new
            a['approved_by']=admin_username
            access[i]=a
            write_csv(data_files['access'], access, access_fields)
            print("Access request updated.")
            return
    print("req_id not found.")


def admin_menu(admin_username):
    while True:
        print("\n--- Admin Menu ---")
        print("1. Add Climate Record\n2. Update/Delete Climate Data\n3. Manage Categories\n4. Upload Bulk Data\n5. Generate Reports\n6. Manage Researcher Access\n7. Logout")
        choice = safe_input("Choice: ").strip()
        if choice == '1':
            add_climate_record()
        elif choice == '2':
            update_delete_climate_data()
        elif choice == '3':
            manage_categories()
        elif choice == '4':
            upload_bulk_data()
        elif choice == '5':
            generate_reports_admin()
        elif choice == '6':
            manage_researcher_access(admin_username)
        elif choice == '7':
            print("Logging out...")
            break
        else:
            print("Invalid choice.")


def register_researcher():
    data = load_csv(data_files['researchers'], researcher_fields)
    max_id = 0
    for r in data:
        v = int(r.get('researcher_id', '0'))
        if v > max_id: max_id = v
    rid = str(max_id+1)
    print("\n--- Researcher Registration ---")
    name = safe_input("Name: ").strip()
    org = safe_input("Organization: ").strip()
    field = safe_input("Field of Study: ").strip()
    contact = safe_input("Contact: ").strip()
    while True:
        pwd = safe_input("Create a password: ")
        if pwd == safe_input("Retype password: "): break
        else: print("Passwords don't match.")
    append_row(data_files['researchers'], {
        'researcher_id': rid,
        'name': name,
        'org': org,
        'field': field,
        'contact': contact,
        'pwd': pwd
    }, researcher_fields)
    append_row(data_files['access'], {
        'req_id': rid,
        'researcher_id': rid,
        'status': 'pending',
        'approved_by': ''
    }, access_fields)
    print(f"Registration complete. Your Researcher ID is {rid}. Access pending approval.\n")


def researcher_login():
    print("\n--- Researcher Login ---")
    rid = safe_input("Researcher ID: ").strip()
    pwd = safe_input("Password: ").strip()
    researchers = load_csv(data_files['researchers'], researcher_fields)
    for r in researchers:
        if r.get('researcher_id')==rid and r.get('pwd')==pwd:
            access = load_csv(data_files['access'], access_fields)
            status = False
            for a in access:
                if a.get('researcher_id') == rid and a.get('status','').lower() in ('approved','approve'):
                    status = "approved"
                    break
                elif a.get('researcher_id') == rid and a.get('status', '').lower() in ('rejected', 'reject'):
                    status =  "rejected"
                    break
            if status != 'approved':
                if status == 'rejected':
                    print("Access request has been rejected by admin.")
                else:
                    print("Access not approved yet. Contact an admin.")
                return None
            print(f"\nWelcome, {r.get('name')}!\n")
            researcher_menu(rid)
            return rid
    print("Invalid ID or password.")
    return None

def search_climate_data():
    data = load_csv(data_files['climate_data'], climate_fields)
    if not data:
        print("No climate data present.")
        return
    print("\n--- Search Climate Data ---")
    region = safe_input("Region (leave blank to skip): ").strip()
    start_date = safe_input("Start date (YYYY-MM-DD or blank): ").strip()
    end_date = safe_input("End date (YYYY-MM-DD or blank): ").strip()
    param = safe_input("Filter parameter (e.g., air_quality) or blank: ").strip()
    low = safe_input("Parameter min value (blank to skip): ").strip()
    high = safe_input("Parameter max value (blank to skip): ").strip()

    results = []
    for r in data:
        if region and r.get('region','').lower() != region.lower():
            continue
        if start_date and r.get('date','') < start_date:
            continue
        if end_date and r.get('date','') > end_date:
            continue
        if param:
            val = r.get(param,'')
            f_val = float(val)
            if low:
                if f_val < float(low): continue
            if high:
                if f_val > float(high): continue
        results.append(r)
    display_table(results)


def perform_analysis():
    data = load_csv(data_files["climate_data"], climate_fields)
    if not data:
        print("\nNo climate data present.\n")
        return

    menu = "\n--- Perform Analysis ---\n" \
           "1. Monthly Trend\n" \
           "2. Annual Trend\n" \
           "3. Anomaly Detection (Z-score)\n" \
           "4. Extreme Events (top 5)\n" \
           "5. Visualize Trends\n" \
           "6. Back\n"
    print(menu)

    choice = safe_input("Select option: ").strip()
    if choice == '6':
        return

    if choice == '5':
        visualize_params(data)
        return

    region = safe_input("Region (leave blank for ALL): ").strip()
    param = safe_input("Parameter (temperature / air_quality / co2_level / rainfall / humidity): ").strip()
    if param not in climate_fields:
        print("\nInvalid parameter.\n")
        return

    filtered = data if not region else [r for r in data if r.get('region','').lower()==region.lower()]
    if not filtered:
        print("\nNo matching records.\n")
        return

    for r in filtered:
        r[param] = float(r.get(param,'0'))

    if choice == '1':
        buckets = {}
        for r in filtered:
            y, m, _ = r['date'].split('-')
            key = f"{y}-{m}"
            buckets.setdefault(key, []).append(r[param])

        start_p = safe_input("Start month (YYYY-MM or blank): ").strip()
        end_p = safe_input("End   month (YYYY-MM or blank): ").strip()

        out = "\nMONTHLY AVG (" + param + "):\n"
        for k in sorted(buckets.keys()):
            if start_p and k < start_p: continue
            if end_p and k > end_p: continue
            vv = [x for x in buckets[k] if x is not None]
            if vv: out += f"{k} -> {round(sum(vv) / len(vv), 2)}\n"


    elif choice == '2':
        buckets = {}
        for r in filtered:
            y = r['date'][:4]
            buckets.setdefault(y, []).append(r[param])
        start_p = safe_input("Start year (YYYY or blank): ").strip()
        end_p = safe_input("End   year (YYYY or blank): ").strip()
        out = "\nANNUAL AVG (" + param + "):\n"
        for k in sorted(buckets.keys()):
            if start_p and k < start_p: continue
            if end_p and k > end_p: continue
            vv = [x for x in buckets[k] if x is not None]
            if vv: out += f"{k} -> {round(sum(vv) / len(vv), 2)}\n"


    elif choice == '3':
        vals=[r[param] for r in filtered if r[param] is not None]
        avg=sum(vals)/len(vals)
        import math
        sd=math.sqrt(sum((x-avg)**2 for x in vals)/len(vals))
        out=f"\nANOMALIES in {param} (|Z|>2):\n"
        for r in filtered:
            v=r[param]
            if v is None: continue
            z=(v-avg)/sd
            if abs(z)>2:
                out+=f"{r['date']} {r['region']} {v} Z={round(z,2)}\n"

    elif choice == '4':
        top=sorted(filtered,key=lambda x:x[param],reverse=True)[:5]
        out=f"\nTOP 5 {param.upper()}:\n\n"
        from tabulate import tabulate
        out+=tabulate(top,headers="keys",tablefmt="grid")+"\n"
    else:
        print("\nInvalid option.\n")
        return

    print(out)


def visualize_params(data):
    region = safe_input("Region (blank for all): ").strip()

    p_input = safe_input("Parameters space separated (temperature air_quality co2_level rainfall humidity): ").strip()
    params = p_input.split()
    valid = ["temperature","air_quality","co2_level","rainfall","humidity"]
    params = [p for p in params if p in valid]
    if not params:
        print("\nNo valid parameters selected.\n")
        return

    mode = safe_input("Type 'month' or 'year': ").strip().lower()
    if mode not in ("month","year"):
        print("\nInvalid mode.\n")
        return

    filtered = data if not region else [r for r in data if r.get('region','').lower() == region.lower()]
    if not filtered:
        print("\nNo matching data.\n")
        return

    for r in filtered:
        for p in params:
            r[p] = float(r.get(p,"0"))

    bucket = {}

    for r in filtered:
        d = r.get('date','')
        key = d[:7] if mode=="month" else d[:4]
        bucket.setdefault(key, {p:[] for p in params})
        for p in params:
            if r[p] is not None:
                bucket[key][p].append(r[p])

    start_p = safe_input(f"Start {mode} (YYYY-MM if month / YYYY if year): ").strip()
    end_p = safe_input(f"End   {mode} (YYYY-MM if month / YYYY if year): ").strip()
    period_keys = [k for k in sorted(bucket.keys()) if (not start_p or k >= start_p) and (not end_p or k <= end_p)]

    if not period_keys:
        print("\nNo data in selected period range.\n")
        return

    x = []
    y = {p: [] for p in params}
    for period in period_keys:
        x.append(period)
        for p in params:
            vals = bucket[period][p]
            y[p].append(sum(vals) / len(vals) if vals else None)

    plt.figure()
    for p in params:
        plt.plot(x, y[p], label=p)

    plt.xlabel("Period ("+mode+")")
    plt.ylabel("Value")
    plt.title("Climate Trend ("+", ".join(params)+")")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    save = safe_input("Save PNG image? (Y/N): ").strip().lower()
    if save == "y":
        f_name = "vis_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
        plt.savefig(f_name)
        print(f"\nSaved as {f_name}\n")
    plt.close()


def generate_report(researcher_id):
    print("\n--- Generate Report ---")
    region = safe_input("Region (leave blank for all): ").strip()
    date1 = safe_input("Start date (YYYY-MM-DD or blank): ").strip()
    date2 = safe_input("End date (YYYY-MM-DD or blank): ").strip()

    data = load_csv(data_files["climate_data"], climate_fields)

    results = []
    for r in data:
        if region and r.get('region','').lower() != region.lower():
            continue
        d = r.get('date','')
        if date1 and d < date1: continue
        if date2 and d > date2: continue
        results.append(r)

    print("\nCLIMATE DATA (FILTERED):")
    display_table(results)
    report_id = str(int(datetime.now().timestamp()))
    params = json.dumps({"region": region, "date1": date1, "date2": date2})

    append_row(data_files['reports'], {
        'report_id': report_id,
        'researcher_id': researcher_id,
        'type': 'region_date_range',
        'parameters': params,
        'generated_on': str(datetime.now())
    }, report_fields)

    print(f"\nReport generated and saved with id {report_id}.\n")


def export_report():
    reports = load_csv(data_files['reports'], report_fields)
    data = load_csv(data_files['climate_data'], climate_fields)
    if not reports:
        print("No reports to export.")
        return

    display_table(reports)
    rid = safe_input("Enter report_id to export: ").strip()

    for rep in reports:
        if rep.get('report_id') == rid:
            p = json.loads(rep.get("parameters","{}"))
            region = p.get("region","")
            date1 = p.get("date1","")
            date2 = p.get("date2","")
            results = []
            for r in data:
                if region and r.get('region','').lower() != region.lower(): continue
                d = r.get('date','')
                if date1 and d < date1: continue
                if date2 and d > date2: continue
                results.append(r)

            csv_name = f"export_report_{rid}.csv"
            json_name = f"export_report_{rid}.json"
            write_csv(csv_name, results, climate_fields)
            with open(json_name,'w') as f:
                json.dump(results, f, indent=4)
            print(f"Exported {len(results)} records to {csv_name} and {json_name}.")
            return

    print("report_id not found.")


def view_profile(researcher_id):
    researchers = load_csv(data_files['researchers'], researcher_fields)
    for r in researchers:
        if r.get('researcher_id') == researcher_id:
            r.pop('pwd')
            display_table([r])
            return

def change_pwd(researcher_id):
    data = load_csv(data_files['researchers'], researcher_fields)
    for i, r in enumerate(data):
        if r.get("researcher_id") == researcher_id:
            while True:
                if r.get("pwd", "") == safe_input("Enter the current password: "):
                    new_pwd = input("Enter new password: ")
                    if new_pwd == input("Retype password: "):
                        r['pwd'] = new_pwd
                        data[i] = r
                        write_csv(data_files["researchers"], data, researcher_fields)
                        print("Password changed.")
                        break
                    else: print("New Passwords don't match.")
                else:
                    print("Current Password doesn't match.")

def researcher_menu(researcher_id):
    while True:
        print("\n--- Researcher Menu ---")
        print("1. Search Climate Data\n2. Perform Analysis / Visualizations\n3. Generate Report\n4. Export Report\n5. View Profile\n6. Change Password\n7. Logout")
        choice = safe_input("Choice: ").strip()
        if choice == '1':
            search_climate_data()
        elif choice == '2':
            perform_analysis()
        elif choice == '3':
            generate_report(researcher_id)
        elif choice == '4':
            export_report()
        elif choice == '5':
            view_profile(researcher_id)
        elif choice == '6':
            change_pwd(researcher_id)
        elif choice == '7':
            print("Logging out...")
            break
        else:
            print("Invalid choice.")

def main():
    ensure_files_exist()
    _ = load_csv(data_files['climate_data'], climate_fields)
    _ = load_csv(data_files['researchers'], researcher_fields)
    _ = load_csv(data_files['reports'], report_fields)
    _ = load_csv(data_files['access'], access_fields)
    if not os.path.exists(data_files['categories']):
        write_csv(data_files['categories'], [], categories_fields)

    while True:
        print("\n=== Climate Data Analysis System ===\n1. Admin Login\n2. Researcher Login\n3. Register as New Researcher\n4. Exit\n")
        choice = safe_input("Choice: ").strip()
        if choice == '1':
            admin_user = admin_login()
            if admin_user:
                admin_menu(admin_user)
        elif choice == '2':
            researcher_login()
        elif choice == '3':
            register_researcher()
        elif choice == '4':
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")


if __name__ == '__main__':
    main()
