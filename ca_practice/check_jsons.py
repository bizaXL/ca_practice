import json
import os

files_to_check = [
    "./ca_practice/ca_practice/doctype/ca_client_director/ca_client_director.json",
    "./ca_practice/ca_practice/doctype/compliance_attachment/compliance_attachment.json", 
    "./ca_practice/ca_practice/doctype/ca_client/ca_client.json",
    "./ca_practice/ca_practice/doctype/compliance/compliance.json",
    "./ca_practice/ca_practice/doctype/ca_client_service/ca_client_service.json"
]

print("Checking JSON files for 'doctype' key...\n")

for file_path in files_to_check:
    print(f"Checking: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"  ❌ File not found!")
        continue
    
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Check for doctype key
        if 'doctype' not in data:
            print(f"  ❌ MISSING 'doctype' key!")
            print(f"     Current keys: {list(data.keys())}")
            
            # If it's a child table, it should have "istable": 1
            if 'istable' in data and data['istable'] == 1:
                print(f"  ⚠️  This is a child table (istable: 1)")
                print(f"  ⚠️  Child tables need 'doctype': 'DocField'")
                # Fix it
                data['doctype'] = 'DocField'
                with open(file_path, 'w') as f:
                    json.dump(data, f, indent=2)
                print(f"  ✅ Fixed: Added 'doctype': 'DocField'")
            else:
                # Regular doctype
                print(f"  ⚠️  This should be a regular doctype")
                print(f"  ⚠️  Adding 'doctype': 'DocType'")
                data['doctype'] = 'DocType'
                with open(file_path, 'w') as f:
                    json.dump(data, f, indent=2)
                print(f"  ✅ Fixed: Added 'doctype': 'DocType'")
        else:
            print(f"  ✅ Has 'doctype': {data['doctype']}")
            
            # Check if doctype value is correct
            if data['doctype'] not in ['DocType', 'DocField', 'DocPerm']:
                print(f"  ⚠️  Invalid doctype value: {data['doctype']}")
                print(f"  ⚠️  Changing to 'DocType'")
                data['doctype'] = 'DocType'
                with open(file_path, 'w') as f:
                    json.dump(data, f, indent=2)
                print(f"  ✅ Fixed doctype value")
        
        # Check other required fields
        required_fields = ['name', 'module']
        for field in required_fields:
            if field not in data:
                print(f"  ⚠️  Missing '{field}' key")
        
        print()
        
    except json.JSONDecodeError as e:
        print(f"  ❌ JSON Syntax Error: {str(e)}")
        print(f"  Line: {e.lineno}, Column: {e.colno}")
        print(f"  Check the JSON syntax!")
        print()
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        print()

print("\nDone checking files.")
