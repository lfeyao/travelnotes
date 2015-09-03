from bucketlist.models import Category, Page, Place

def encode_url(str):
    return str.replace(' ', '_')

def decode_url(str):
    return str.replace('_', ' ')


all_categories = Category.objects.order_by(Lower('name').desc())
all_pages = Page.objects.order_by(Lower('name').desc())

for category in all_categories:
    category.name_url = encode_url(category.name)
    category.save()

for page in all_pages:
    page.name_url = encode_url(page.name)
    page.category_url = encode_url(page.category)
    page.save()


