#!/usr/bin/env python3

from faker import Faker
import argparse
import random
import os
import sys
import signal
from colorama import Style, init

init(autoreset=True)  # Colorama'yı başlat ve her satırdan sonra stilleri sıfırla

def signal_handler(sig, frame):
    print("\nExiting...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def generate_fake_identity(fake, lang):
    # Sahte kimlik bilgileri
    name = fake.name()
    address = fake.address()
    phone_number = fake.phone_number()
    email = fake.email()
    ip_address = fake.ipv4()
    job = fake.job()
    age = random.randint(18, 80)
    marital_status = random.choice([True, False])
    num_children = random.randint(0, 3)
    has_sibling = random.choice([True, False])
    birth_date = fake.date_of_birth(minimum_age=18, maximum_age=80)
    country, city = get_country_city(lang)

    # Çocuk bilgileri
    if num_children > 0:
        children = []
        for _ in range(num_children):
            child_gender = random.choice(["Male", "Female"]) if lang == 'en' else random.choice(["Erkek", "Kız"]) if lang == 'tr' else random.choice(["Мужчина", "Женщина"])
            children.append(child_gender)
        children_info = f"{translations[lang]['children']}: {', '.join(children)}"
    else:
        children_info = f"{translations[lang]['children']}: {translations[lang]['not_available']}"

    # Kardeş bilgileri
    if has_sibling:
        sibling_gender = random.choice(["Male", "Female"]) if lang == 'en' else random.choice(["Erkek", "Kız"]) if lang == 'tr' else random.choice(["Мужчина", "Женщина"])
        sibling_info = f"{translations[lang]['sibling']}: {sibling_gender}"
    else:
        sibling_info = f"{translations[lang]['sibling']}: {translations[lang]['not_available']}"

    marital_status_str = translations[lang]['married'] if marital_status else translations[lang]['not_married']

    identity_info = (
        f"{Style.BRIGHT}{translations[lang]['name']}:{Style.NORMAL} {name}\n"
        f"{Style.BRIGHT}{translations[lang]['address']}:{Style.NORMAL} {address}\n"
        f"{Style.BRIGHT}{translations[lang]['phone_number']}:{Style.NORMAL} {phone_number}\n"
        f"{Style.BRIGHT}{translations[lang]['email']}:{Style.NORMAL} {email}\n"
        f"{Style.BRIGHT}{translations[lang]['ip_address']}:{Style.NORMAL} {ip_address}\n"
        f"{Style.BRIGHT}{translations[lang]['job']}:{Style.NORMAL} {job}\n"
        f"{Style.BRIGHT}{translations[lang]['age']}:{Style.NORMAL} {age}\n"
        f"{Style.BRIGHT}{translations[lang]['marital_status']}:{Style.NORMAL} {marital_status_str}\n"
        f"{Style.BRIGHT}{translations[lang]['birth_date']}:{Style.NORMAL} {birth_date.strftime('%d-%m-%Y')}\n"
        f"{Style.BRIGHT}{translations[lang]['country']}:{Style.NORMAL} {country}\n"
        f"{Style.BRIGHT}{translations[lang]['city']}:{Style.NORMAL} {city}\n"
        f"{Style.BRIGHT}{children_info}\n"
        f"{Style.BRIGHT}{sibling_info}\n"
        "\n-------------------------------\n"
    )
    
    print(identity_info)
    
    return identity_info

def get_country_city(lang):
    if lang == 'en':
        countries = ['United States', 'United Kingdom', 'Canada']
        cities = {
            'United States': ['New York', 'Los Angeles', 'Chicago'],
            'United Kingdom': ['London', 'Manchester', 'Birmingham'],
            'Canada': ['Toronto', 'Vancouver', 'Montreal']
        }
    elif lang == 'tr':
        countries = ['Turkey']
        cities = {
            'Turkey': ['Istanbul', 'Ankara', 'Izmir']
        }
    elif lang == 'ru':
        countries = ['Russia']
        cities = {
            'Russia': ['Moscow', 'Saint Petersburg', 'Novosibirsk']
        }
    else:
        return 'Unknown', 'Unknown'

    country = random.choice(countries)
    city = random.choice(cities[country])
    return country, city

def save_identity(info, lang, file_path):
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(info)
    
    print(f"{Style.BRIGHT}{translations[lang]['saved_to']}:{Style.NORMAL} {file_path}")

def main():
    parser = argparse.ArgumentParser(description="Generate fake identities.")
    parser.add_argument('-m', type=int, help="Number of fake identities to generate.")
    parser.add_argument('-l', type=str, choices=['en', 'tr', 'ru'], default='en', help="Language for fake data (en for English, tr for Turkish, ru for Russian).")
    parser.add_argument('-y', action='store_true', help="Automatically save the generated identities.")
    parser.add_argument('-n', action='store_true', help="Do not save the generated identities.")
    
    args = parser.parse_args()

    if args.m is None:
        parser.print_help()
        sys.exit(1)

    if args.y and args.n:
        print("Error: You cannot use both -y and -n options at the same time.")
        sys.exit(1)

    if args.l == 'tr':
        fake = Faker('tr_TR')
    elif args.l == 'ru':
        fake = Faker('ru_RU')
    else:
        fake = Faker('en_US')

    save_directory = os.path.expanduser("~/FakeUser")
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    
    existing_files = [f for f in os.listdir(save_directory) if f.startswith("info") and f.endswith(".txt")]
    next_file_number = len(existing_files) + 1
    file_path = os.path.join(save_directory, f"info{next_file_number}.txt")
    
    all_identity_info = ""
    
    for _ in range(args.m):
        identity_info = generate_fake_identity(fake, args.l)
        all_identity_info += identity_info

    if args.y:
        save_identity(all_identity_info, args.l, file_path)
    elif args.n:
        pass
    else:
        save_prompt = input(f"{translations[args.l]['save_prompt']} [Y/n]: ").strip().lower()
        if save_prompt == '-y' or save_prompt == 'y':
            save_identity(all_identity_info, args.l, file_path)
        elif save_prompt == '-n' or save_prompt == 'n':
            print(f"{translations[args.l]['not_saved']}\n")

translations = {
    'en': {
        'name': 'Name',
        'address': 'Address',
        'phone_number': 'Phone Number',
        'email': 'Email',
        'ip_address': 'IP Address',
        'job': 'Job',
        'age': 'Age',
        'marital_status': 'Marital Status',
        'married': 'Married',
        'not_married': 'Not married',
        'children': 'Children',
        'sibling': 'Sibling',
        'not_available': 'Not available',
        'save_prompt': 'Save this identity',
        'saved_to': 'Saved to',
        'not_saved': 'Not saved',
        'birth_date': 'Birth Date',
        'country': 'Country',
        'city': 'City'
    },
    'tr': {
        'name': 'İsim',
        'address': 'Adres',
        'phone_number': 'Telefon Numarası',
        'email': 'E-posta',
        'ip_address': 'IP Adresi',
        'job': 'Meslek',
        'age': 'Yaş',
        'marital_status': 'Medeni Durum',
        'married': 'Evli',
        'not_married': 'Evli değil',
        'children': 'Çocuklar',
        'sibling': 'Kardeş',
        'not_available': 'Sahip değil',
        'save_prompt': 'Bu kimliği kaydet',
        'saved_to': 'Kaydedildi',
        'not_saved': 'Kaydedilmedi',
        'birth_date': 'Doğum Tarihi',
        'country': 'Ülke',
        'city': 'Şehir'
    },
    'ru': {
        'name': 'Имя',
        'address': 'Адрес',
        'phone_number': 'Номер телефона',
        'email': 'Эл. почта',
        'ip_address': 'IP-адрес',
        'job': 'Работа',
        'age': 'Возраст',
        'marital_status': 'Семейное положение',
        'married': 'Женат/Замужем',
        'not_married': 'Не женат/Не замужем',
        'children': 'Дети',
        'sibling': 'Брат/Сестра',
        'not_available': 'Нет в наличии',
        'save_prompt': 'Сохранить этот профиль',
        'saved_to': 'Сохранено в',
        'not_saved': 'Не сохранено',
        'birth_date': 'Дата Рождения',
        'country': 'Страна',
        'city': 'Город'
    }
}

if __name__ == "__main__":
    main()
