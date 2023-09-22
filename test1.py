import requests
import hashlib

def get_password_suffix(password):
    sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    return sha1_hash[5:]

def check_password(password, suffix):
    prefix = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()[:5]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"

    try:
        with requests.get(url) as resp:
            if resp.status_code == 200:
                hashes = resp.text.splitlines()
                for h in hashes:
                    if suffix in h:
                        return True
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")

    return False

def main():
    filename = input("Введите имя файла: ")
  
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                username, password = line.split(',')
                password = password.strip()
                suffix = get_password_suffix(password)
                if check_password(password, suffix):
                    print(f"Утечка данных для пользователя {username} пароля {password}")
                else:
                    print(f"Пароль пользователя {username} пароля {password} безопасен")
    except FileNotFoundError:
        print("Файл не найден")
    except ValueError:
        print("Ошибка в формате файла")

if __name__ == "__main__":
    main()