import os
import uuid
import numpy as np
import gdown
import random
import string
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from django.conf import settings
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input
from keras.models import load_model
from django.contrib.auth.decorators import login_required
from .models import Doctor,Appointment
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import logout
from django.shortcuts import redirect
# Model Path
MODEL_PATH = os.path.join(settings.BASE_DIR, "model.h5")
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomSignupForm

def signup(request):
    if request.method == "POST":
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data["email"]
            user.save()
            return redirect("login")
    else:
        form = CustomSignupForm()

    return render(request, "signup.html", {"form": form})
# Google Drive Model Download
# def download_model():
#     if not os.path.exists(MODEL_PATH):
#         print("Downloading model...")
#         file_id = "1i-uE2sN-Lh96WVe1AkegbyE8QQ0eoNLq"
#         url = f"https://drive.google.com/uc?id={file_id}"
#         gdown.download(url, MODEL_PATH, quiet=False)
#         print("Model downloaded.")

# # Download before load
# download_model()

# Load Model
model = load_model(MODEL_PATH)

# Class labels
class_names = {0: "Acne", 1: "Actinic_Keratosis", 2: "Benign_tumors", 3: "Bullous", 4: "Candidiasis", 5: "DrugEruption", 6: "Eczema", 7: "Infestations_Bites", 8: "Lichen", 9: "Lupus", 10: "Moles", 11: "Psoriasis", 12: "Rosacea", 13: "Seborrh_Keratoses", 14: "SkinCancer", 15: "Sun_Sunlight_Damage", 16: "Tinea", 17: "Unknown_Normal", 18: "Vascular_Tumors", 19: "Vasculitis", 20: "Vitiligo", 21: "Warts"}
# DISEASE_DATA = {

#     "Acne": {
#         "causes": (
#             "Excess sebum (oil) production leading to clogged pores.\n"
#             "Bacterial growth (Cutibacterium acnes) within hair follicles.\n"
#             "Hormonal changes, stress, and certain medications."
#         ),
#         "symptoms": (
#             "Blackheads, whiteheads, and inflamed pimples.\n"
#             "Red, tender bumps sometimes filled with pus.\n"
#             "Oily skin, primarily affecting face, chest, and back."
#         ),
#         "precautions": (
#             "Cleanse skin gently twice daily.\n"
#             "Avoid harsh scrubbing and squeezing pimples.\n"
#             "Use non-comedogenic skincare products."
#         ),
#         "treatment": (
#             "Topical retinoids and benzoyl peroxide.\n"
#             "Antibiotics or hormonal therapy when required.\n"
#             "Dermatologist-guided medical treatment for severe cases."
#         ),
#         "exercises": (
#             "Regular physical activity to reduce stress.\n"
#             "Proper post-workout hygiene to prevent pore blockage."
#         )
#     },

#     "Actinic_Keratosis": {
#         "causes": (
#             "Chronic exposure to ultraviolet (UV) radiation.\n"
#             "Cumulative sun damage over several years.\n"
#             "Weakened immune system increasing skin sensitivity."
#         ),
#         "symptoms": (
#             "Rough, scaly, or crusty patches on sun-exposed areas.\n"
#             "Lesions that may be pink, red, or skin-colored.\n"
#             "Occasional itching or tenderness."
#         ),
#         "precautions": (
#             "Apply broad-spectrum sunscreen daily.\n"
#             "Avoid prolonged sun exposure.\n"
#             "Regular dermatological skin checks."
#         ),
#         "treatment": (
#             "Cryotherapy (freezing lesions).\n"
#             "Topical medicated creams.\n"
#             "Laser or photodynamic therapy."
#         ),
#         "exercises": (
#             "No specific exercises required.\n"
#             "Focus on overall healthy lifestyle."
#         )
#     },

#     "Benign_tumors": {
#         "causes": (
#             "Non-cancerous abnormal skin cell growth.\n"
#             "Genetic predisposition.\n"
#             "Age-related skin changes."
#         ),
#         "symptoms": (
#             "Painless, slow-growing skin lumps.\n"
#             "Well-defined borders.\n"
#             "Stable size over time."
#         ),
#         "precautions": (
#             "Monitor growth for sudden changes.\n"
#             "Avoid unnecessary trauma to the area.\n"
#             "Regular skin examinations."
#         ),
#         "treatment": (
#             "Observation if asymptomatic.\n"
#             "Surgical removal for cosmetic or functional reasons.\n"
#             "Medical consultation if changes occur."
#         ),
#         "exercises": (
#             "No specific exercises required.\n"
#             "Maintain general skin health."
#         )
#     },

#     "Bullous": {
#         "causes": (
#             "Autoimmune reaction against skin layers.\n"
#             "Certain medications triggering immune response.\n"
#             "Age-related immune dysfunction."
#         ),
#         "symptoms": (
#             "Large fluid-filled blisters.\n"
#             "Fragile skin with easy tearing.\n"
#             "Itching and discomfort."
#         ),
#         "precautions": (
#             "Avoid skin trauma.\n"
#             "Maintain clean and dry skin.\n"
#             "Follow dermatologist instructions strictly."
#         ),
#         "treatment": (
#             "Corticosteroids to control inflammation.\n"
#             "Immunosuppressive therapy.\n"
#             "Wound care to prevent infection."
#         ),
#         "exercises": (
#             "Gentle movements only.\n"
#             "Avoid friction-causing activities."
#         )
#     },

#     "Candidiasis": {
#         "causes": (
#             "Overgrowth of Candida yeast.\n"
#             "Moist environments and excessive sweating.\n"
#             "Weakened immune system or diabetes."
#         ),
#         "symptoms": (
#             "Red, itchy rashes.\n"
#             "White discharge or scaling.\n"
#             "Burning sensation."
#         ),
#         "precautions": (
#             "Keep affected areas dry.\n"
#             "Avoid tight clothing.\n"
#             "Maintain proper hygiene."
#         ),
#         "treatment": (
#             "Topical antifungal creams.\n"
#             "Oral antifungal medication in severe cases.\n"
#             "Address underlying health conditions."
#         ),
#         "exercises": (
#             "General fitness exercises.\n"
#             "Ensure post-exercise hygiene."
#         )
#     },

#     "DrugEruption": {
#         "causes": (
#             "Allergic reaction to medications.\n"
#             "Immune hypersensitivity responses.\n"
#             "Drug accumulation in sensitive individuals."
#         ),
#         "symptoms": (
#             "Widespread red rashes.\n"
#             "Itching and skin peeling.\n"
#             "Sometimes fever or swelling."
#         ),
#         "precautions": (
#             "Avoid known triggering drugs.\n"
#             "Inform doctors about drug allergies.\n"
#             "Seek immediate care if severe."
#         ),
#         "treatment": (
#             "Discontinuation of offending drug.\n"
#             "Antihistamines or corticosteroids.\n"
#             "Supportive skin care."
#         ),
#         "exercises": (
#             "No exercises required.\n"
#             "Rest until recovery."
#         )
#     },

#     "Eczema": {
#         "causes": (
#             "Genetic predisposition.\n"
#             "Immune system overactivity.\n"
#             "Environmental triggers like soaps or allergens."
#         ),
#         "symptoms": (
#             "Dry, itchy, inflamed skin patches.\n"
#             "Cracked or oozing skin.\n"
#             "Chronic flare-ups."
#         ),
#         "precautions": (
#             "Regular moisturization.\n"
#             "Avoid irritants and allergens.\n"
#             "Use gentle skin care products."
#         ),
#         "treatment": (
#             "Topical corticosteroids.\n"
#             "Moisturizers and barrier creams.\n"
#             "Advanced therapies for severe cases."
#         ),
#         "exercises": (
#             "Stress-relieving exercises like yoga.\n"
#             "Avoid excessive sweating."
#         )
#     },

#     "Psoriasis": {
#         "causes": (
#             "Autoimmune skin cell overproduction.\n"
#             "Genetic factors.\n"
#             "Triggers such as stress or infections."
#         ),
#         "symptoms": (
#             "Red patches with silvery scales.\n"
#             "Dry, cracked skin.\n"
#             "Itching or burning sensation."
#         ),
#         "precautions": (
#             "Avoid known triggers.\n"
#             "Keep skin well moisturized.\n"
#             "Avoid harsh skin products."
#         ),
#         "treatment": (
#             "Topical treatments.\n"
#             "Phototherapy.\n"
#             "Systemic medications for severe disease."
#         ),
#         "exercises": (
#             "Low-impact exercises.\n"
#             "Stress management techniques."
#         )
#     },

#     "SkinCancer": {
#         "causes": (
#             "DNA damage from excessive UV exposure.\n"
#             "History of sunburns.\n"
#             "Genetic susceptibility."
#         ),
#         "symptoms": (
#             "Non-healing sores.\n"
#             "Irregular or changing moles.\n"
#             "Bleeding or ulcerated lesions."
#         ),
#         "precautions": (
#             "Routine skin self-examination.\n"
#             "Consistent sun protection.\n"
#             "Early dermatological evaluation."
#         ),
#         "treatment": (
#             "Surgical removal.\n"
#             "Radiation or immunotherapy.\n"
#             "Targeted therapy depending on cancer type."
#         ),
#         "exercises": (
#             "Light physical activity.\n"
#             "Physician-approved exercises."
#         )
#     },

#     "Vitiligo": {
#         "causes": (
#             "Autoimmune destruction of pigment cells.\n"
#             "Genetic predisposition.\n"
#             "Oxidative stress."
#         ),
#         "symptoms": (
#             "White patches on skin.\n"
#             "Loss of pigmentation.\n"
#             "Symmetrical distribution."
#         ),
#         "precautions": (
#             "Sun protection to prevent burns.\n"
#             "Psychological support if needed.\n"
#             "Avoid skin trauma."
#         ),
#         "treatment": (
#             "Topical steroids.\n"
#             "Phototherapy.\n"
#             "Advanced medical treatments under supervision."
#         ),
#         "exercises": (
#             "Stress reduction exercises.\n"
#             "General fitness activities."
#         )
#     }

# }

DISEASE_DATA = {

    "Acne": {
        "causes": (
            "Excess sebum (oil) production leading to clogged pores.\n"
            "Bacterial growth (Cutibacterium acnes) within hair follicles.\n"
            "Hormonal changes, stress, and certain medications."
        ),
        "symptoms": (
            "Blackheads, whiteheads, and inflamed pimples.\n"
            "Red, tender bumps sometimes filled with pus.\n"
            "Oily skin, primarily affecting face, chest, and back."
        ),
        "precautions": (
            "Cleanse skin gently twice daily.\n"
            "Avoid harsh scrubbing and squeezing pimples.\n"
            "Use non-comedogenic skincare products."
        ),
        "treatment": (
            "Topical retinoids and benzoyl peroxide.\n"
            "Antibiotics or hormonal therapy when required.\n"
            "Dermatologist-guided medical treatment for severe cases."
        ),
        "exercises": (
            "Regular physical activity to reduce stress.\n"
            "Proper post-workout hygiene to prevent pore blockage."
        )
    },

    "Actinic_Keratosis": {
        "causes": (
            "Chronic exposure to ultraviolet (UV) radiation.\n"
            "Cumulative sun damage over several years.\n"
            "Weakened immune system increasing skin sensitivity."
        ),
        "symptoms": (
            "Rough, scaly, or crusty patches on sun-exposed areas.\n"
            "Lesions that may be pink, red, or skin-colored.\n"
            "Occasional itching or tenderness."
        ),
        "precautions": (
            "Apply broad-spectrum sunscreen daily.\n"
            "Avoid prolonged sun exposure.\n"
            "Regular dermatological skin checks."
        ),
        "treatment": (
            "Cryotherapy (freezing lesions).\n"
            "Topical medicated creams.\n"
            "Laser or photodynamic therapy."
        ),
        "exercises": (
            "No specific exercises required.\n"
            "Focus on overall healthy lifestyle."
        )
    },

    "Benign_tumors": {
        "causes": (
            "Non-cancerous abnormal skin cell growth.\n"
            "Genetic predisposition.\n"
            "Age-related skin changes."
        ),
        "symptoms": (
            "Painless, slow-growing skin lumps.\n"
            "Well-defined borders.\n"
            "Stable size over time."
        ),
        "precautions": (
            "Monitor growth for sudden changes.\n"
            "Avoid unnecessary trauma to the area.\n"
            "Regular skin examinations."
        ),
        "treatment": (
            "Observation if asymptomatic.\n"
            "Surgical removal for cosmetic or functional reasons.\n"
            "Medical consultation if changes occur."
        ),
        "exercises": (
            "No specific exercises required.\n"
            "Maintain general skin health."
        )
    },

    "Bullous": {
        "causes": (
            "Autoimmune reaction against skin layers.\n"
            "Certain medications triggering immune response.\n"
            "Age-related immune dysfunction."
        ),
        "symptoms": (
            "Large fluid-filled blisters.\n"
            "Fragile skin with easy tearing.\n"
            "Itching and discomfort."
        ),
        "precautions": (
            "Avoid skin trauma.\n"
            "Maintain clean and dry skin.\n"
            "Follow dermatologist instructions strictly."
        ),
        "treatment": (
            "Corticosteroids to control inflammation.\n"
            "Immunosuppressive therapy.\n"
            "Wound care to prevent infection."
        ),
        "exercises": (
            "Gentle movements only.\n"
            "Avoid friction-causing activities."
        )
    },

    "Candidiasis": {
        "causes": (
            "Overgrowth of Candida yeast.\n"
            "Moist environments and excessive sweating.\n"
            "Weakened immune system or diabetes."
        ),
        "symptoms": (
            "Red, itchy rashes.\n"
            "White discharge or scaling.\n"
            "Burning sensation."
        ),
        "precautions": (
            "Keep affected areas dry.\n"
            "Avoid tight clothing.\n"
            "Maintain proper hygiene."
        ),
        "treatment": (
            "Topical antifungal creams.\n"
            "Oral antifungal medication in severe cases.\n"
            "Address underlying health conditions."
        ),
        "exercises": (
            "General fitness exercises.\n"
            "Ensure post-exercise hygiene."
        )
    },

    "DrugEruption": {
        "causes": (
            "Allergic reaction to medications.\n"
            "Immune hypersensitivity responses.\n"
            "Drug accumulation in sensitive individuals."
        ),
        "symptoms": (
            "Widespread red rashes.\n"
            "Itching and skin peeling.\n"
            "Sometimes fever or swelling."
        ),
        "precautions": (
            "Avoid known triggering drugs.\n"
            "Inform doctors about drug allergies.\n"
            "Seek immediate care if severe."
        ),
        "treatment": (
            "Discontinuation of offending drug.\n"
            "Antihistamines or corticosteroids.\n"
            "Supportive skin care."
        ),
        "exercises": (
            "No exercises required.\n"
            "Rest until recovery."
        )
    },

    "Eczema": {
        "causes": (
            "Genetic predisposition.\n"
            "Immune system overactivity.\n"
            "Environmental triggers like soaps or allergens."
        ),
        "symptoms": (
            "Dry, itchy, inflamed skin patches.\n"
            "Cracked or oozing skin.\n"
            "Chronic flare-ups."
        ),
        "precautions": (
            "Regular moisturization.\n"
            "Avoid irritants and allergens.\n"
            "Use gentle skin care products."
        ),
        "treatment": (
            "Topical corticosteroids.\n"
            "Moisturizers and barrier creams.\n"
            "Advanced therapies for severe cases."
        ),
        "exercises": (
            "Stress-relieving exercises like yoga.\n"
            "Avoid excessive sweating."
        )
    },

    "Infestations_Bites": {
        "causes": (
            "Insect bites or parasitic infestations.\n"
            "Exposure to unhygienic environments.\n"
            "Close contact with infected individuals or animals."
        ),
        "symptoms": (
            "Itchy red bumps or rashes.\n"
            "Swelling or bite marks.\n"
            "Possible secondary infections from scratching."
        ),
        "precautions": (
            "Maintain personal hygiene.\n"
            "Use insect repellents.\n"
            "Wash bedding and clothing regularly."
        ),
        "treatment": (
            "Topical antiparasitic or anti-itch creams.\n"
            "Oral medications if severe.\n"
            "Treat close contacts if required."
        ),
        "exercises": (
            "No specific exercises required.\n"
            "Avoid activities causing sweating on affected areas."
        )
    },

    "Lichen": {
        "causes": (
            "Autoimmune skin reaction.\n"
            "Stress or genetic predisposition.\n"
            "Possible drug-related triggers."
        ),
        "symptoms": (
            "Flat, purplish itchy bumps.\n"
            "Skin thickening over time.\n"
            "Oral or nail involvement in some cases."
        ),
        "precautions": (
            "Avoid scratching.\n"
            "Reduce stress levels.\n"
            "Follow dermatologist guidance."
        ),
        "treatment": (
            "Topical corticosteroids.\n"
            "Immunomodulatory medications.\n"
            "Phototherapy in chronic cases."
        ),
        "exercises": (
            "Stress reduction exercises.\n"
            "Light physical activity."
        )
    },

    "Lupus": {
        "causes": (
            "Autoimmune disorder affecting skin and organs.\n"
            "Genetic and hormonal factors.\n"
            "Triggered by sunlight or infections."
        ),
        "symptoms": (
            "Butterfly-shaped facial rash.\n"
            "Photosensitivity.\n"
            "Joint pain and fatigue."
        ),
        "precautions": (
            "Strict sun protection.\n"
            "Regular medical follow-ups.\n"
            "Avoid known triggers."
        ),
        "treatment": (
            "Immunosuppressive medications.\n"
            "Topical steroids for skin lesions.\n"
            "Systemic therapy when required."
        ),
        "exercises": (
            "Low-impact exercises.\n"
            "Adequate rest and stress management."
        )
    },

    "Moles": {
        "causes": (
            "Clusters of pigment-producing cells.\n"
            "Genetic predisposition.\n"
            "Sun exposure."
        ),
        "symptoms": (
            "Small dark or skin-colored spots.\n"
            "Usually painless.\n"
            "May change in size or color."
        ),
        "precautions": (
            "Monitor for changes.\n"
            "Avoid excessive sun exposure.\n"
            "Regular skin checks."
        ),
        "treatment": (
            "No treatment if benign.\n"
            "Surgical removal if suspicious.\n"
            "Dermatological evaluation."
        ),
        "exercises": (
            "No specific exercises required.\n"
            "General fitness encouraged."
        )
    },

    "Psoriasis": {
        "causes": (
            "Autoimmune skin cell overproduction.\n"
            "Genetic factors.\n"
            "Triggers such as stress or infections."
        ),
        "symptoms": (
            "Red patches with silvery scales.\n"
            "Dry, cracked skin.\n"
            "Itching or burning sensation."
        ),
        "precautions": (
            "Avoid known triggers.\n"
            "Keep skin well moisturized.\n"
            "Avoid harsh skin products."
        ),
        "treatment": (
            "Topical treatments.\n"
            "Phototherapy.\n"
            "Systemic medications for severe disease."
        ),
        "exercises": (
            "Low-impact exercises.\n"
            "Stress management techniques."
        )
    },

    "Rosacea": {
        "causes": (
            "Blood vessel abnormalities.\n"
            "Genetic predisposition.\n"
            "Triggers like heat, alcohol, or spicy food."
        ),
        "symptoms": (
            "Facial redness.\n"
            "Visible blood vessels.\n"
            "Burning or stinging sensation."
        ),
        "precautions": (
            "Avoid trigger foods.\n"
            "Use gentle skincare products.\n"
            "Sun protection."
        ),
        "treatment": (
            "Topical antibiotics.\n"
            "Laser therapy.\n"
            "Oral medications if severe."
        ),
        "exercises": (
            "Moderate exercises.\n"
            "Avoid overheating."
        )
    },

    "Seborrh_Keratoses": {
        "causes": (
            "Age-related skin growths.\n"
            "Genetic factors.\n"
            "Non-cancerous cell proliferation."
        ),
        "symptoms": (
            "Waxy or scaly raised lesions.\n"
            "Brown, black, or tan growths.\n"
            "Usually painless."
        ),
        "precautions": (
            "Monitor for sudden changes.\n"
            "Avoid picking lesions.\n"
            "Regular skin evaluation."
        ),
        "treatment": (
            "No treatment required.\n"
            "Cryotherapy or removal if needed.\n"
            "Medical consultation."
        ),
        "exercises": (
            "No specific exercises required.\n"
            "Maintain healthy lifestyle."
        )
    },

    "SkinCancer": {
        "causes": (
            "DNA damage from excessive UV exposure.\n"
            "History of sunburns.\n"
            "Genetic susceptibility."
        ),
        "symptoms": (
            "Non-healing sores.\n"
            "Irregular or changing moles.\n"
            "Bleeding or ulcerated lesions."
        ),
        "precautions": (
            "Routine skin self-examination.\n"
            "Consistent sun protection.\n"
            "Early dermatological evaluation."
        ),
        "treatment": (
            "Surgical removal.\n"
            "Radiation or immunotherapy.\n"
            "Targeted therapy depending on cancer type."
        ),
        "exercises": (
            "Light physical activity.\n"
            "Physician-approved exercises."
        )
    },

    "Sun_Sunlight_Damage": {
        "causes": (
            "Prolonged sun exposure.\n"
            "Lack of sun protection.\n"
            "Cumulative UV radiation damage."
        ),
        "symptoms": (
            "Wrinkles and pigmentation.\n"
            "Rough skin texture.\n"
            "Premature aging signs."
        ),
        "precautions": (
            "Daily sunscreen use.\n"
            "Protective clothing.\n"
            "Avoid peak sun hours."
        ),
        "treatment": (
            "Topical retinoids.\n"
            "Laser or cosmetic treatments.\n"
            "Skin repair therapies."
        ),
        "exercises": (
            "No specific exercises required.\n"
            "Healthy lifestyle habits."
        )
    },

    "Tinea": {
        "causes": (
            "Fungal infection of the skin.\n"
            "Warm and moist environments.\n"
            "Poor hygiene."
        ),
        "symptoms": (
            "Ring-shaped rashes.\n"
            "Itching and redness.\n"
            "Scaling skin."
        ),
        "precautions": (
            "Keep skin dry.\n"
            "Avoid sharing personal items.\n"
            "Maintain hygiene."
        ),
        "treatment": (
            "Topical antifungal creams.\n"
            "Oral antifungals if severe.\n"
            "Complete treatment course."
        ),
        "exercises": (
            "General fitness exercises.\n"
            "Shower after workouts."
        )
    },

    "Normal": {
        "causes": (
            "Normal skin condition.\n"
            "No identifiable disease.\n"
            "Natural skin variations."
        ),
        "symptoms": (
            "Healthy skin appearance.\n"
            "No discomfort or lesions.\n"
            "Normal texture and color."
        ),
        "precautions": (
            "Maintain regular skincare routine.\n"
            "Protect skin from sun.\n"
            "Healthy lifestyle."
        ),
        "treatment": (
            "No treatment required.\n"
            "Routine skincare maintenance.\n"
            "Regular check-ups."
        ),
        "exercises": (
            "All regular exercises allowed.\n"
            "Promotes overall skin health."
        )
    },

    "Vascular_Tumors": {
        "causes": (
            "Abnormal blood vessel growth.\n"
            "Congenital conditions.\n"
            "Hormonal influences."
        ),
        "symptoms": (
            "Red or purple skin lesions.\n"
            "Raised or flat growths.\n"
            "May bleed if injured."
        ),
        "precautions": (
            "Avoid trauma to lesions.\n"
            "Monitor size changes.\n"
            "Medical evaluation."
        ),
        "treatment": (
            "Laser therapy.\n"
            "Surgical removal if needed.\n"
            "Medical supervision."
        ),
        "exercises": (
            "Gentle exercises.\n"
            "Avoid pressure on affected areas."
        )
    },

    "Vasculitis": {
        "causes": (
            "Inflammation of blood vessels.\n"
            "Autoimmune disorders.\n"
            "Infections or medications."
        ),
        "symptoms": (
            "Red or purple spots.\n"
            "Skin ulcers.\n"
            "Pain or burning sensation."
        ),
        "precautions": (
            "Follow medical advice.\n"
            "Avoid known triggers.\n"
            "Regular monitoring."
        ),
        "treatment": (
            "Corticosteroids.\n"
            "Immunosuppressive drugs.\n"
            "Treat underlying cause."
        ),
        "exercises": (
            "Light physical activity.\n"
            "Avoid strenuous exercise."
        )
    },

    "Vitiligo": {
        "causes": (
            "Autoimmune destruction of pigment cells.\n"
            "Genetic predisposition.\n"
            "Oxidative stress."
        ),
        "symptoms": (
            "White patches on skin.\n"
            "Loss of pigmentation.\n"
            "Symmetrical distribution."
        ),
        "precautions": (
            "Sun protection to prevent burns.\n"
            "Psychological support if needed.\n"
            "Avoid skin trauma."
        ),
        "treatment": (
            "Topical steroids.\n"
            "Phototherapy.\n"
            "Advanced medical treatments under supervision."
        ),
        "exercises": (
            "Stress reduction exercises.\n"
            "General fitness activities."
        )
    },

    "Warts": {
        "causes": (
            "Human papillomavirus (HPV) infection.\n"
            "Direct skin contact.\n"
            "Weakened immune system."
        ),
        "symptoms": (
            "Small rough growths.\n"
            "Skin-colored or dark lesions.\n"
            "May appear on hands or feet."
        ),
        "precautions": (
            "Avoid touching warts.\n"
            "Do not share personal items.\n"
            "Maintain hygiene."
        ),
        "treatment": (
            "Topical salicylic acid.\n"
            "Cryotherapy.\n"
            "Medical removal if persistent."
        ),
        "exercises": (
            "No specific exercises required.\n"
            "Avoid friction on affected areas."
        )
    }

}
DISPLAY_NAME_MAP = {
    "Acne": "Acne",
    "Actinic_Keratosis": "Actinic Keratosis",
    "Benign_tumors": "Benign Tumors",
    "Bullous": "Bullous Disorders",
    "Candidiasis": "Candidiasis",
    "DrugEruption": "Drug Eruption",
    "Eczema": "Eczema",
    "Infestations_Bites": "Infestations & Bites",
    "Lichen": "Lichen Planus",
    "Lupus": "Lupus",
    "Moles": "Moles",
    "Psoriasis": "Psoriasis",
    "Rosacea": "Rosacea",
    "Seborrh_Keratoses": "Seborrheic Keratoses",
    "SkinCancer": "Skin Cancer",
    "Sun_Sunlight_Damage": "Sun / Sunlight Damage",
    "Tinea": "Tinea (Fungal Infection)",
    "Unknown_Normal": "Normal",
    "Vascular_Tumors": "Vascular Tumors",
    "Vasculitis": "Vasculitis",
    "Vitiligo": "Vitiligo",
    "Warts": "Warts"
}

@login_required
def home(request):
    return render(request, "index.html")
def custom_logout_view(request):
    logout(request)
    return redirect('logout_success')
@login_required
def about(request):
    return render(request, "about.html")

@login_required
def disease(request):
    return render(request, "diseases.html")

@login_required
def prediction_page(request):
    return render(request, "prediction.html")

@login_required
def contact(request):
    return render(request, "contact.html")

def format_as_bullets(text):
    if not text:
        return "Information not available."

    lines = text.split("\n")
    return "\n".join(f"• {line.strip()}" for line in lines if line.strip())


@login_required
def predict(request):
    if request.method == "POST" and request.FILES.get("image"):

        image_file = request.FILES["image"]
        filename = image_file.name

        upload_path = os.path.join(settings.BASE_DIR, "static/uploads")
        os.makedirs(upload_path, exist_ok=True)

        file_path = os.path.join(upload_path, filename)

        # Save file
        with open(file_path, "wb+") as dest:
            for chunk in image_file.chunks():
                dest.write(chunk)

        # Preprocess image
        img = image.load_img(file_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        # Predict
        preds = model.predict(img_array)
        pred_index = np.argmax(preds)
        confidence = float(np.max(preds)) * 100
        # pred_class = class_names[pred_index]
        # disease_info = DISEASE_DATA.get(pred_class, {})
        raw_pred_class = class_names[pred_index]
        pred_class = DISPLAY_NAME_MAP.get(raw_pred_class, raw_pred_class)
        disease_info = DISEASE_DATA.get(pred_class, {})
        # ✉️ Clean email body (NO triple quotes)
        email_body = (
            f"Dear {request.user.username},\n\n"
            "Thank you for using SkinCure.\n\n"

            "🔍 Predicted Skin Condition:\n"
            f"{pred_class}\n\n"

            "📊 Confidence Level:\n"
            f"{confidence:.2f}%\n\n"

            "🧬 Causes:\n"
            f"{format_as_bullets(disease_info.get('causes'))}\n\n"

            "⚠️ Symptoms:\n"
            f"{format_as_bullets(disease_info.get('symptoms'))}\n\n"

            "🛡️ Precautions:\n"
            f"{format_as_bullets(disease_info.get('precautions'))}\n\n"

            "💊 Treatment Options:\n"
            f"{format_as_bullets(disease_info.get('treatment'))}\n\n"

            "🏃 Recommended Care / Exercises:\n"
            f"{format_as_bullets(disease_info.get('exercises'))}\n\n"

            "⚠️ Disclaimer:\n"
            "This prediction is generated using AI and is NOT a medical diagnosis.\n"
            "Please consult a certified dermatologist for confirmation and treatment.\n\n"

            "Regards,\n"
            "SkinCure Team\n"
            "AI-powered Skin Health Platform"
        )

        send_mail(
            subject="SkinCure | Your Skin Disease Prediction Report",
            message=email_body,
            from_email="SkinCure <dermascan.service@gmail.com>",
            recipient_list=[request.user.email],
        )

        # Save confidence for result page
        request.session["confidence"] = round(confidence, 2)

        return redirect("result_page", disease=pred_class)

    return redirect("prediction")

@login_required
def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, "doctor_list.html", {"doctors": doctors})
@login_required
def result_page(request, disease):

    data = DISEASE_DATA.get(disease, {
        "causes": "No data found",
        "precautions": "No data found",
        "treatment": "No data found",
    })
    confidence = request.session.get("confidence", None)
    return render(request, "result_page.html", {
        "disease": disease,
        "info": data,
        "confidence": confidence,
    })
@login_required
def book_appointment(request, doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)

    if request.method == "POST":
        problem = request.POST.get("problem")
        date = request.POST.get("date")
        time = request.POST.get("time")

        Appointment.objects.create(
            patient=request.user,
            doctor=doctor,
            problem=problem,
            date=date,
            time=time
        )

        return redirect("appointment_success")

    return render(request, "book_appointment.html", {"doctor": doctor})
@login_required
def appointment_success(request):
    return render(request, "appointment_success.html")

@login_required
def profile_page(request):
    return render(request, "profile.html")
