"""
🌹 Rosa Beauty Platform - Validators
اعتبارسنجی داده‌های ورودی برای پلتفرم Rosa
"""

import re
from typing import Tuple, Optional
from datetime import datetime, timedelta

def validate_phone(phone: str) -> Tuple[bool, str]:
    """Validate Iranian phone number"""
    if not phone:
        return True, ""  # Optional field
    
    # Remove spaces and special characters
    clean_phone = re.sub(r'[\s\-\(\)]', '', phone)
    
    # Iranian mobile patterns
    patterns = [
        r'^09[0-9]{9}$',           # 09XXXXXXXXX
        r'^(\+98|0098)9[0-9]{9}$', # +989XXXXXXXXX or 00989XXXXXXXXX
        r'^9[0-9]{9}$'             # 9XXXXXXXXX
    ]
    
    for pattern in patterns:
        if re.match(pattern, clean_phone):
            return True, "شماره تلفن معتبر است"
    
    return False, "شماره تلفن نامعتبر است - فرمت صحیح: 09XXXXXXXXX"

def validate_instagram(instagram: str) -> Tuple[bool, str]:
    """Validate Instagram username"""
    if not instagram:
        return True, ""  # Optional field
    
    # Remove @ and instagram.com/ if present
    clean_instagram = instagram.lstrip('@')
    clean_instagram = re.sub(r'.*instagram\.com/', '', clean_instagram)
    clean_instagram = clean_instagram.rstrip('/')
    
    # Instagram username rules
    if not re.match(r'^[a-zA-Z0-9._]{1,30}$', clean_instagram):
        return False, "نام کاربری اینستاگرام نامعتبر است"
    
    if clean_instagram.startswith('.') or clean_instagram.endswith('.'):
        return False, "نام کاربری نمی‌تواند با نقطه شروع یا تمام شود"
    
    if '..' in clean_instagram:
        return False, "نام کاربری نمی‌تواند دو نقطه متوالی داشته باشد"
    
    return True, "نام کاربری اینستاگرام معتبر است"

def validate_password_strength(password: str) -> Tuple[bool, str]:
    """Validate password strength"""
    if len(password) < 6:
        return False, "رمز عبور باید حداقل 6 کاراکتر باشد"
    
    if len(password) > 128:
        return False, "رمز عبور نمی‌تواند بیش از 128 کاراکتر باشد"
    
    # Check for common weak passwords
    weak_passwords = ['123456', 'password', '123456789', 'qwerty', 'abc123']
    if password.lower() in weak_passwords:
        return False, "رمز عبور انتخابی بسیار ضعیف است"
    
    strength_score = 0
    feedback = []
    
    if any(c.islower() for c in password):
        strength_score += 1
    else:
        feedback.append("حروف کوچک")
    
    if any(c.isupper() for c in password):
        strength_score += 1
    else:
        feedback.append("حروف بزرگ")
    
    if any(c.isdigit() for c in password):
        strength_score += 1
    else:
        feedback.append("اعداد")
    
    if any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password):
        strength_score += 1
    else:
        feedback.append("کاراکترهای خاص")
    
    if len(password) >= 8:
        strength_score += 1
    
    if strength_score >= 4:
        return True, "رمز عبور قوی است"
    elif strength_score >= 2:
        return True, f"رمز عبور متوسط است - پیشنهاد: {', '.join(feedback[:2])}"
    else:
        return False, f"رمز عبور ضعیف است - لطفاً اضافه کنید: {', '.join(feedback[:3])}"

def validate_username(username: str) -> Tuple[bool, str]:
    """Validate username format"""
    if not username:
        return False, "نام کاربری الزامی است"
    
    if len(username) < 3:
        return False, "نام کاربری باید حداقل 3 کاراکتر باشد"
    
    if len(username) > 50:
        return False, "نام کاربری نمی‌تواند بیش از 50 کاراکتر باشد"
    
    # Only allow alphanumeric and underscore
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "نام کاربری فقط می‌تواند شامل حروف، اعداد و _ باشد"
    
    # Cannot start with underscore or number
    if username.startswith('_') or username[0].isdigit():
        return False, "نام کاربری نمی‌تواند با _ یا عدد شروع شود"
    
    # Reserved usernames
    reserved = ['admin', 'root', 'api', 'www', 'mail', 'test', 'user', 'guest']
    if username.lower() in reserved:
        return False, "این نام کاربری رزرو شده است"
    
    return True, "نام کاربری معتبر است"

def validate_email(email: str) -> Tuple[bool, str]:
    """Validate email address"""
    if not email:
        return True, ""  # Optional field
    
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(email_pattern, email):
        return False, "آدرس ایمیل نامعتبر است"
    
    if len(email) > 254:
        return False, "آدرس ایمیل بیش از حد طولانی است"
    
    return True, "آدرس ایمیل معتبر است"

def validate_salon_name(name: str) -> Tuple[bool, str]:
    """Validate salon name"""
    if not name:
        return False, "نام سالن الزامی است"
    
    if len(name) < 2:
        return False, "نام سالن باید حداقل 2 کاراکتر باشد"
    
    if len(name) > 100:
        return False, "نام سالن نمی‌تواند بیش از 100 کاراکتر باشد"
    
    # Remove extra spaces
    clean_name = ' '.join(name.split())
    
    if clean_name != name:
        return True, f"نام پیشنهادی: {clean_name}"
    
    return True, "نام سالن معتبر است"

def validate_address(address: str) -> Tuple[bool, str]:
    """Validate address"""
    if not address:
        return True, ""  # Optional field
    
    if len(address) < 10:
        return False, "آدرس باید حداقل 10 کاراکتر باشد"
    
    if len(address) > 500:
        return False, "آدرس نمی‌تواند بیش از 500 کاراکتر باشد"
    
    return True, "آدرس معتبر است"

def validate_price(price: float) -> Tuple[bool, str]:
    """Validate service price"""
    if price is None:
        return False, "قیمت الزامی است"
    
    if price < 0:
        return False, "قیمت نمی‌تواند منفی باشد"
    
    if price > 100000000:  # 100 million
        return False, "قیمت بیش از حد مجاز است"
    
    if price == 0:
        return True, "خدمت رایگان"
    
    return True, "قیمت معتبر است"

def validate_duration(duration_minutes: int) -> Tuple[bool, str]:
    """Validate service duration"""
    if duration_minutes is None:
        return False, "مدت زمان الزامی است"
    
    if duration_minutes < 5:
        return False, "مدت زمان باید حداقل 5 دقیقه باشد"
    
    if duration_minutes > 480:  # 8 hours
        return False, "مدت زمان نمی‌تواند بیش از 8 ساعت باشد"
    
    return True, "مدت زمان معتبر است"

def validate_booking_date(booking_date: datetime) -> Tuple[bool, str]:
    """Validate booking date"""
    if not booking_date:
        return False, "تاریخ رزرو الزامی است"
    
    now = datetime.now()
    
    # Cannot book in the past
    if booking_date < now:
        return False, "نمی‌توان برای گذشته رزرو کرد"
    
    # Cannot book more than 3 months in advance
    max_advance = now + timedelta(days=90)
    if booking_date > max_advance:
        return False, "حداکثر 3 ماه پیش‌تر می‌توان رزرو کرد"
    
    # Check business hours (9 AM to 9 PM)
    if booking_date.hour < 9 or booking_date.hour >= 21:
        return False, "ساعت کاری: 9:00 تا 21:00"
    
    return True, "تاریخ رزرو معتبر است"

def validate_rating(rating: float) -> Tuple[bool, str]:
    """Validate rating value"""
    if rating is None:
        return False, "امتیاز الزامی است"
    
    if rating < 1 or rating > 5:
        return False, "امتیاز باید بین 1 تا 5 باشد"
    
    # Allow half stars
    if rating * 2 != int(rating * 2):
        return False, "امتیاز باید مضرب 0.5 باشد"
    
    return True, "امتیاز معتبر است"

def validate_comment(comment: str) -> Tuple[bool, str]:
    """Validate comment text"""
    if not comment:
        return True, ""  # Optional field
    
    if len(comment) < 3:
        return False, "نظر باید حداقل 3 کاراکتر باشد"
    
    if len(comment) > 1000:
        return False, "نظر نمی‌تواند بیش از 1000 کاراکتر باشد"
    
    # Check for spam patterns
    spam_patterns = [
        r'(.)\1{10,}',  # Repeated characters
        r'[A-Z]{10,}',  # Too many caps
        r'www\.',       # URLs
        r'http',        # URLs
        r'@[a-zA-Z0-9_]+',  # Mentions
    ]
    
    for pattern in spam_patterns:
        if re.search(pattern, comment):
            return False, "نظر شما ممکن است اسپم تشخیص داده شود"
    
    return True, "نظر معتبر است"

def validate_discount_percentage(discount: float) -> Tuple[bool, str]:
    """Validate discount percentage"""
    if discount is None:
        return True, ""  # Optional field
    
    if discount < 0:
        return False, "درصد تخفیف نمی‌تواند منفی باشد"
    
    if discount > 100:
        return False, "درصد تخفیف نمی‌تواند بیش از 100 باشد"
    
    return True, "درصد تخفیف معتبر است"

def validate_experience_years(years: int) -> Tuple[bool, str]:
    """Validate stylist experience years"""
    if years is None:
        return True, ""  # Optional field
    
    if years < 0:
        return False, "سال تجربه نمی‌تواند منفی باشد"
    
    if years > 50:
        return False, "سال تجربه بیش از حد است"
    
    return True, "سال تجربه معتبر است"

def validate_age(age: int) -> Tuple[bool, str]:
    """Validate age"""
    if age is None:
        return True, ""  # Optional field
    
    if age < 16:
        return False, "سن باید حداقل 16 سال باشد"
    
    if age > 100:
        return False, "سن بیش از حد است"
    
    return True, "سن معتبر است"

def validate_city_name(city: str) -> Tuple[bool, str]:
    """Validate city name"""
    if not city:
        return True, ""  # Optional field
    
    if len(city) < 2:
        return False, "نام شهر باید حداقل 2 کاراکتر باشد"
    
    if len(city) > 50:
        return False, "نام شهر نمی‌تواند بیش از 50 کاراکتر باشد"
    
    # Only allow letters, spaces and Persian characters
    if not re.match(r'^[\u0600-\u06FFa-zA-Z\s]+$', city):
        return False, "نام شهر فقط می‌تواند شامل حروف باشد"
    
    return True, "نام شهر معتبر است"

def validate_coordinates(latitude: float, longitude: float) -> Tuple[bool, str]:
    """Validate GPS coordinates"""
    if latitude is None or longitude is None:
        return True, ""  # Optional fields
    
    # Validate latitude
    if not -90 <= latitude <= 90:
        return False, "عرض جغرافیایی باید بین -90 تا 90 باشد"
    
    # Validate longitude
    if not -180 <= longitude <= 180:
        return False, "طول جغرافیایی باید بین -180 تا 180 باشد"
    
    # Check if coordinates are in Iran (approximately)
    if not (25 <= latitude <= 40 and 44 <= longitude <= 64):
        return False, "مختصات خارج از محدوده ایران است"
    
    return True, "مختصات معتبر است"

def validate_file_upload(file_data: bytes, allowed_types: list = None) -> Tuple[bool, str]:
    """Validate uploaded file"""
    if not file_data:
        return False, "فایل انتخاب نشده است"
    
    # Check file size (max 5MB)
    max_size = 5 * 1024 * 1024  # 5MB
    if len(file_data) > max_size:
        return False, "حجم فایل نمی‌تواند بیش از 5 مگابایت باشد"
    
    # Check file type by header
    image_headers = {
        b'\xFF\xD8\xFF': 'jpg',
        b'\x89PNG\r\n\x1a\n': 'png',
        b'GIF87a': 'gif',
        b'GIF89a': 'gif',
    }
    
    file_type = None
    for header, ftype in image_headers.items():
        if file_data.startswith(header):
            file_type = ftype
            break
    
    if not file_type:
        return False, "فرمت فایل پشتیبانی نمی‌شود"
    
    if allowed_types and file_type not in allowed_types:
        return False, f"فرمت مجاز: {', '.join(allowed_types)}"
    
    return True, f"فایل معتبر است ({file_type})"

def sanitize_input(text: str) -> str:
    """Sanitize text input to prevent injection attacks"""
    if not text:
        return ""
    
    # Remove HTML tags
    clean_text = re.sub(r'<[^>]+>', '', text)
    
    # Remove SQL injection patterns
    sql_patterns = [
        r'(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|UNION)\b)',
        r'(--|/\*|\*/)',
        r'(\b(OR|AND)\s+\d+\s*=\s*\d+)',
    ]
    
    for pattern in sql_patterns:
        clean_text = re.sub(pattern, '', clean_text, flags=re.IGNORECASE)
    
    # Remove script tags and javascript
    clean_text = re.sub(r'<script[^>]*>.*?</script>', '', clean_text, flags=re.IGNORECASE | re.DOTALL)
    clean_text = re.sub(r'javascript:', '', clean_text, flags=re.IGNORECASE)
    
    # Trim whitespace
    clean_text = clean_text.strip()
    
    return clean_text

def validate_payment_amount(amount: float, expected_amount: float, tolerance: float = 0.01) -> Tuple[bool, str]:
    """Validate payment amount"""
    if amount is None:
        return False, "مبلغ پرداخت الزامی است"
    
    if amount < 0:
        return False, "مبلغ پرداخت نمی‌تواند منفی باشد"
    
    if abs(amount - expected_amount) > tolerance:
        return False, f"مبلغ پرداخت ({amount:,.0f}) با مبلغ مورد انتظار ({expected_amount:,.0f}) مطابقت ندارد"
    
    return True, "مبلغ پرداخت معتبر است"

# Helper function to validate all salon data at once
def validate_salon_data(salon_data: dict) -> Tuple[bool, dict]:
    """Validate all salon registration data"""
    errors = {}
    
    # Validate username
    is_valid, message = validate_username(salon_data.get('username', ''))
    if not is_valid:
        errors['username'] = message
    
    # Validate password
    is_valid, message = validate_password_strength(salon_data.get('password', ''))
    if not is_valid:
        errors['password'] = message
    
    # Validate salon name
    is_valid, message = validate_salon_name(salon_data.get('name', ''))
    if not is_valid:
        errors['name'] = message
    
    # Validate phone
    is_valid, message = validate_phone(salon_data.get('phone', ''))
    if not is_valid:
        errors['phone'] = message
    
    # Validate Instagram
    is_valid, message = validate_instagram(salon_data.get('instagram', ''))
    if not is_valid:
        errors['instagram'] = message
    
    # Validate address
    is_valid, message = validate_address(salon_data.get('address', ''))
    if not is_valid:
        errors['address'] = message
    
    return len(errors) == 0, errors