import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sickle_project.settings")
django.setup()

from marketplace.models import Category, HSNCode

categories = [
    {"name": "Cereals & Grains", "description": "Wheat, rice, oats, barley, etc."},
    {"name": "Vegetables & Fruits", "description": "Fresh and organic produce."},
    {"name": "Pulses & Legumes", "description": "Lentils, peas, beans, dal."},
    {"name": "Spices & Herbs", "description": "Raw and ground spices."},
    {"name": "Dairy Products", "description": "Milk, butter, ghee."},
    {"name": "Fertilizers & Manure", "description": "Organic and chemical fertilizers."},
    {"name": "Seeds", "description": "High yield seeds for sowing."},
    {"name": "Farming Equipment", "description": "Tools and machinery."},
]

hsn_codes = [
    {"code": "1001", "cat": "Cereals & Grains", "description": "Wheat (Packaged)", "igst": 5.0, "cgst": 2.5, "sgst": 2.5},
    {"code": "1006", "cat": "Cereals & Grains", "description": "Rice (Packaged)", "igst": 5.0, "cgst": 2.5, "sgst": 2.5},
    {"code": "0709", "cat": "Vegetables & Fruits", "description": "Fresh Vegetables", "igst": 0.0, "cgst": 0.0, "sgst": 0.0},
    {"code": "0804", "cat": "Vegetables & Fruits", "description": "Fresh Fruits", "igst": 0.0, "cgst": 0.0, "sgst": 0.0},
    {"code": "0713", "cat": "Pulses & Legumes", "description": "Pulses (Packaged)", "igst": 5.0, "cgst": 2.5, "sgst": 2.5},
    {"code": "0910", "cat": "Spices & Herbs", "description": "Spices (Turmeric, Ginger)", "igst": 5.0, "cgst": 2.5, "sgst": 2.5},
    {"code": "0401", "cat": "Dairy Products", "description": "Fresh Milk", "igst": 0.0, "cgst": 0.0, "sgst": 0.0},
    {"code": "0405", "cat": "Dairy Products", "description": "Ghee and Butter", "igst": 12.0, "cgst": 6.0, "sgst": 6.0},
    {"code": "3101", "cat": "Fertilizers & Manure", "description": "Organic Fertilizers", "igst": 5.0, "cgst": 2.5, "sgst": 2.5},
    {"code": "1209", "cat": "Seeds", "description": "Seeds for sowing", "igst": 0.0, "cgst": 0.0, "sgst": 0.0},
    {"code": "8432", "cat": "Farming Equipment", "description": "Agricultural Machinery", "igst": 12.0, "cgst": 6.0, "sgst": 6.0},
]

for cat_data in categories:
    cat, created = Category.objects.get_or_create(name=cat_data["name"], defaults={"description": cat_data["description"]})
    if created:
        print(f"Created category: {cat.name}")

for hsn_data in hsn_codes:
    cat = Category.objects.filter(name=hsn_data["cat"]).first()
    hsn, created = HSNCode.objects.get_or_create(
        code=hsn_data["code"], 
        defaults={
            "description": hsn_data["description"],
            "category": cat,
            "igst_rate": hsn_data["igst"],
            "cgst_rate": hsn_data["cgst"],
            "sgst_rate": hsn_data["sgst"]
        }
    )
    if not created:
        hsn.category = cat
        hsn.save()
        print(f"Updated HSN code: {hsn.code}")
    else:
        print(f"Created HSN code: {hsn.code} ({hsn.igst_rate}% GST)")

print("Categories and HSN codes seeded successfully.")
