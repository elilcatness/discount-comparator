from data.parsers.magnit import MagnitParser
from data.models.product import Product


def main():
    product = Product(name='Шоколадка', price=65, img='http://vk.com/elilcat/photo3219_2313')
    print(product.to_dict())


if __name__ == '__main__':
    main()