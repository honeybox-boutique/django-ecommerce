import random
import string

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_sale_id_generator(instance):
    """
    This is for a Django project with a saleID field
    """
    sale_new_id = random_string_generator().upper()

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(saleStringID=sale_new_id).exists()
    if qs_exists:
        return unique_sale_id_generator(instance)
    return sale_new_id