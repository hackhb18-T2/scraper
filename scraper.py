import requests
from flask import jsonify
import re
from bs4 import BeautifulSoup

providerList = []
class Product():

    def __init__(self, ean, provider, name, price, currency, vat, image):
        self.ean = ean
        self.provider = provider
        self.name = name
        self.price = price
        self.currency = currency
        self.vat = vat
        self.image = image
    
    def jsonify(self):
        return jsonify({
            'ean' : self.ean,
            'provider' : self.provider,
            'name' : self.name,
            'price' : self.price,
            'currency' : self.currency,
            'vat' : self.vat,
            'image' : self.image,
        })

    def getDic(self):
        return{
            'ean' : self.ean,
            'provider' : self.provider,
            'name' : self.name,
            'price' : self.price,
            'currency' : self.currency,
            'vat' : self.vat,
            'image' : self.image
        }


class Provider():
    products = []
    def __init__(self, name, products):
        self.name = name

    def jsonify(self):
        return {
            'name' : self.name,
            'products' : self.products
        }

class Rewe(Provider):
    def __init__(self, name, products):
        Provider.__init__(self, name, products)
        self.products = products

    def addProduct(self, product):
        self.products.append(product)

class Real(Provider):
    def __init__(self, name, products):
        Provider.__init__(self, name, products)
        self.products = products

    def addProduct(self, product):
        self.products.append(product)

class Edeka(Provider):
    def __init__(self, name, products):
        Provider.__init__(self, name, products)
        self.products = products

# Collect page
def findPrice(product):
    """Findet den Preis"""
    
    searchPage = requests.get(product[2])
    soupSearch = BeautifulSoup(searchPage.text,'html.parser')
    if product[1] is "Rewe":
        firstResult = soupSearch.find(class_="pd-price__predecimal")
        secondResult = soupSearch.find(class_="pd-price__decimal")
        nameResult = soupSearch.find(class_='pd-QuickInfo__heading')
        currency = "EUR"
        var = 7
        imgResult = soupSearch.find(class_="pd-PictureHoverZoom--Thumb pd-ProductMedia ")
        url = imgResult.contents[4]['src']
        name = nameResult.contents[0]
        pricePredeci = firstResult.contents[0]
        priceDeci = secondResult.contents[3]
        price = float(pricePredeci + "." + priceDeci)
    
    
    elif product[1] is "Real":
        if len(product[2]) > 15:
            firstResult = soupSearch.find(class_="price -lg")
            price = firstResult['content']
            imageResult = soupSearch.find(class_="_item -first")
            nameResult = soupSearch.find(class_='product-title')
            url = imageResult.next.next['src']
            name = str(nameResult.next)
            var = 7
            currency = "EUR"
        else:
            name = "Beck's Pilsener"
            price = 16.29
            url = "https://img.rewe-static.de/0108570/3648350_digital-image.png?resize=600px:600px"
            var = 7
            currency = "EUR"

        


    elif product[1] is "Edeka":
        firstResult = soupSearch(class_="price")
        nameResult = soupSearch("h1")
        imageResult = soupSearch(class_="detail-image")
        url = imageResult[0].contents[1]['src']
        name = nameResult[0].contents[0].replace("\r\n", " ")
        name = " ".join(name.split())
        name = re.sub(r"^\s+", "", name, flags = re.MULTILINE)
        price = str(firstResult[0].next)
        price = re.findall("([0-9]+\,[0-9]+)", str(price))[0]
        price = float(price.replace(",","."))
        currency = "EUR"
        var = 7


    
    
    
    #nameResult = soupSearch.find(class_= 'a-size-medium s-inline s-access-title a-text-normal')
    #print("Name: " + nameResult.contents[0])
    #preis1 = str(firstResult.contents[1].contents[0]).strip().replace(",",".")
    #currency = re.findall("[A-z]+",preis1)
    #print("Currency: " + currency[0])
    #price = re.findall("([0-9]+(?:\.[0-9]+){0,1})",preis1)
    #print("Preis: " + price[0])
    return Product(product[0], product[1], name, price, currency, var, url)

def findProduct(ean):
    """Findet den Namen"""
    reweProducts = []
    realProducts = []
    edekaProducts = []
    print(ean)

    #Kaffee
    if ean == 4260107220015:
        reweProducts.append(findPrice([ean, "Rewe", "https://shop.rewe.de/jacobs-kr-nung-caff-crema-ganze-bohne-1kg/PD760868"]))
        realProducts.append(findPrice([ean, "Real", "https://www.real.de/product/318531176/?sl=SmFjb2JzIEtyw7ZudW5nIENhZmbDqCBDcmVtYSBHYW56ZSBCb2huZSAxa2ezpHTW1UsHVq17kaCIetkAL6FnUVFLUnONRneA1wrpDA&"]))
        edekaProducts.append(findPrice([ean, "Edeka", "https://www.edeka24.de/Jacobs-Kroenung-Crema-ganze-Bohnen.html?listtype=search&searchparam=Jacobs%20Krönung%20Caffè%20Crema%20klassisch%201000%20g&&order="]))
    elif ean == 41001301:
        reweProducts.append(findPrice([ean, "Rewe", "https://shop.rewe.de/beck-s-pils-24x0-33l/PD108570"]))
        realProducts.append(findPrice([ean, "Real", "https://nix.de"]))
    elif ean == 3123124234:
        reweProducts.append(findPrice([ean, "Rewe", "https://shop.rewe.de/me-mer-feinster-earl-grey-44g-25-beutel/PD9530789"]))
        realProducts.append(findPrice([ean, "Real", "https://www.real.de/product/306896905/?sl=ZWFybCBncmV5IHRlZVbsasORKW-5zqdcLnCLQRQ0q6y26NOMx8Uhp2emsCwr&"]))
        edekaProducts.append(findPrice([ean, "Edeka", "https://www.edeka24.de/Getraenke/Tee/Schwarzer-Tee/Messmer-Tee-Feinster-Earl-Grey.html?listtype=search&searchparam=Meßmer%20Earl%20Grey%20%2825%20x%201%2C75%20g%29&&order="]))

    rewe = Rewe("Rewe", reweProducts) 
    real = Real("Real", realProducts)
    edeka = Edeka("Edek", edekaProducts)
    providerList.append(rewe)
    providerList.append(real)
    providerList.append(edeka)

for provider in providerList:
    print(provider.products[0].price)

    

def findEan(ean):
    rueckgabe = []
    findProduct(ean)
    for prov in providerList:
        for prod in prov.products:
            if prod.ean == ean:
                rueckgabe.append(prod)
    

    return rueckgabe
    #return [providerList[0].products[0],providerList[1].products[0],providerList[2].products[0]]

#EAN
#Scanner: 4960999667454
#Edding: 4004764013753
#Fritz: 4260107220015
if __name__ == '__main__':
    findProduct("4260107220015")

 
