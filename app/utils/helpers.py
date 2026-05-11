class Helpers:
    
    # email validation fonksiyonu
    def is_valid_email(email):
        import re
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None
    
    # telefon numarası doğrulama fonksiyonu
    def is_valid_phone_number(phone_number):
        import re
        pattern = r'^\+?\d{10,15}$'
        return re.match(pattern, phone_number) is not None