from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def buscar_productos(palabra_clave):
    
    options = Options()
    options.headless = True

  
    driver = webdriver.Chrome(options=options)

    try:
        url = f"https://listado.mercadolibre.com.co/{palabra_clave}"
        driver.get(url)
        
        # Espera que cargue el contenido 
        time.sleep(5)

        productos = driver.find_elements(By.CSS_SELECTOR, "li.ui-search-layout__item")[:5]

        if not productos:
            print("No se encontraron productos.")
            return

        print(f"\nResultados para: {palabra_clave.upper().replace('-', ' ')}\n")

        for i, producto in enumerate(productos, 1):
            try:
                titulo = producto.find_element(By.CSS_SELECTOR, "h2.ui-search-item__title").text
                precio_entero = producto.find_element(By.CSS_SELECTOR, "span.price-tag-fraction").text
                try:
                    precio_decimales = producto.find_element(By.CSS_SELECTOR, "span.price-tag-cents").text
                except:
                    precio_decimales = "00"

                precio = f"{precio_entero},{precio_decimales}"
                print(f"{i}. {titulo}")
                print(f"   Precio: ${precio}\n")
            except Exception:
                print(f"{i}. No se pudo obtener título o precio.")
    finally:
        driver.quit()

# Cambia aquí la palabra clave fácilmente:y te redirige a los productos por ver
palabra = "celular"
buscar_productos(palabra)
