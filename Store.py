# Author: Michael Morriss
# Date: 1/12/2021
# Description: Store application that creates Product, Customer, and Store objects and allows for the
#               accumulation of products into customer carts to create a subtotal of available products
#               and has multiple features regarding memberships, shipping, product availability, etc.

class Product:
    """
    Represents a Product object with the parameters being ID, title, description, price, and quantity_available.
    """
    def __init__(self, product_id, title, description, price, quantity_available):
        """
        Creates a Product object and initializes the following variables ID, title, description, price,
        and quantity available.
        """
        self._product_id = product_id
        self._title = title
        self._description = description
        self._price = price
        self._quantity_available = quantity_available

    def get_product_id(self):
        """Returns the ID of the Product"""
        return self._product_id

    def get_title(self):
        """Returns the title of the Product"""
        return self._title

    def get_description(self):
        """Returns the description of the Product"""
        return self._description

    def get_price(self):
        """Returns the price of the Product"""
        return self._price

    def get_quantity_available(self):
        """Returns the available quantity of the Product"""
        return self._quantity_available

    def decrease_quantity(self):
        """Function that decreases available quantity of respective Product by one"""
        self._quantity_available -= 1


class Customer:
    """Represents a Customer object with the parameters being name, account ID, membership status"""
    def __init__(self, name, account_id, premium):
        """Initializes Customer object variables name, account ID, and membership status"""
        self._name = name
        self._account_id = account_id
        self._premium = premium
        self._cart = []

    def get_name(self):
        """Returns the name of the Customer"""
        return self._name

    def get_account_id(self):
        """Returns the account ID of the Customer"""
        return self._account_id

    def get_cart(self):
        """Returns the cart of the Customer"""
        return self._cart

    def is_premium_member(self):
        """Returns boolean value regarding Customer membership, True means Customer is a Premium Member """
        return self._premium

    def add_product_to_cart(self, product_id):
        """Adds a product to the Customer's cart dictionary"""
        self._cart.append(product_id)

    def empty_cart(self):
        """Empties the Customer's cart, clears all items"""
        self._cart = []


class InvalidCheckoutError(Exception):
    """Creates exception for an invalid checkout"""
    pass


class Store:
    """Represents Store object containing Product quantities and Customer membership information"""
    def __init__(self):
        """Initializes list of Products and Customers"""
        self._product_list = []
        self._customer_list = []

    def add_product(self, new_product):
        """Adds a product object to the inventory list"""
        self._product_list.append(new_product)

    def add_member(self, new_member):
        """Adds a new member object to the customer list"""
        self._customer_list.append(new_member)

    def get_product_from_id(self, search_id):
        """Searches product list for given ID and returns respective product """
        for product in self._product_list:
            if search_id == product.get_product_id():
                return product
        return None

    def get_member_from_id(self, customer_id):
        """Searches customer list for given ID and returns respective member"""
        for customer in self._customer_list:
            if customer_id == customer.get_account_id():
                return customer
        return None

    def product_search(self, search_string):
        """Searches inventory for all products containing search words in title or description"""
        products_found = []
        for product in self._product_list:
            if (search_string.lower() in (product.get_title.lower() or product.get_description.lower()))\
                    and (product.get_product_id() not in products_found):
                products_found.append(product.get_product_id)
        if products_found is not []:
            return products_found.sort()
        else:
            return products_found

    def add_product_to_member_cart(self, product_id, customer_id):
        """Takes product id and adds it to the respective customer's cart"""
        buy_customer = self.get_member_from_id(customer_id)
        available = self.get_product_from_id(product_id)
        if available is None:
            return "product ID not found"
        elif buy_customer is None:
            return "member ID not found"
        else:
            stock = available.get_quantity_available()
            if stock >= 1:
                buy_customer.add_product_to_cart(product_id)
                return "product added to cart"
            else:
                return "product out of stock"

    def check_out_member(self, customer_id):
        """Takes customer ID and returns the total of the price of items in the customer's cart"""

        cart_id = self.get_member_from_id(customer_id)
        cart_total = 0

        if cart_id is None:
            raise InvalidCheckoutError
        else:
            cart = cart_id.get_cart()
            for product in cart:
                one_product = self.get_product_from_id(product)
                if one_product.get_quantity_available == 0:
                    continue
                the_price = one_product.get_price()
                cart_total += the_price                 # Adds price to total
                one_product.decrease_quantity()         # Decreases quantity by 1

            if not cart_id.is_premium_member():    # Determining shipping costs
                cart_total += (0.07 * cart_total)
            else:
                cart_total += 0                         # Free shipping if premium member

            cart_id.empty_cart()                        # Empties the customer's cart
            return cart_total


def main():
    """Main function that runs file is ran as script and checks out a member"""
    p1 = Product("889", "Rodent of unusual size", "when a rodent of the usual size just won't do", 33.45, 8)
    p2 = Product("881", "Toothbrush", "Used for brushing teeth", 3.50, 2)
    c1 = Customer("Yinsheng", "QWF", False)

    myStore = Store()

    myStore.add_product(p1)
    myStore.add_product(p2)
    myStore.add_member(c1)

    myStore.add_product_to_member_cart(p1.get_product_id(), c1.get_account_id())
    myStore.add_product_to_member_cart(p2.get_product_id(), c1.get_account_id())

    try:
        myStore.check_out_member(c1.get_account_id())
    except InvalidCheckoutError:
        print("The customer ID does not match any current customer's in the database, please try again")


if __name__ == '__main__':
    main()
