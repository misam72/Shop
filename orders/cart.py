from home.models import Product

CART_SESSION_ID = 'cart'

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart
    
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product_name'] = product
        
        for item in cart.values():
            item['total_price'] = float(item['price']) * item['quantity']
            yield item
    
    def add(self, product, quantity):
        pid = str(product.id)
        if pid not in self.cart:
            self.cart[pid] = {'quantity':0, 'price': str(product.price)}
        self.cart[pid]['quantity'] += quantity
        self.save()
    
    def remove(self, product):
        pid = str(product.id)
        if pid in self.cart:
            del self.cart[pid]
            self.save()
    
    # for counting number of items in CART
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def save(self):
        self.session.modified = True
    
    def get_total_price(self):
        print(self.cart)
        return sum(float(item['price']) * item['quantity'] for item in self.cart.values())