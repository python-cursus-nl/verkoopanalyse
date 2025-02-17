import json
import locale


locale.setlocale(locale.LC_ALL, "")


def laad_verkoopdata():
    with open("verkoopdata.json") as f:
        return json.load(f)


def vind_product_met_get(data, productnaam):
    """
    Zoek een product op naam met de .get() methode.
    Return None als het product niet gevonden wordt.
    """
    producten = data.get("2024", {}).get("q1", {}).get("producten", [])

    for product_categorie in producten:
        items = product_categorie.get("items", [])
        for product in items:
            if product.get("naam") == productnaam:
                return product

    return None


def vind_product_met_try_except(data, productnaam):
    """
    Zoek een product op naam met try-except blokken.
    Return None als het product niet gevonden wordt.
    """
    try:
        for product_categorie in data["2024"]["q1"]["producten"]:
            for product in product_categorie["items"]:
                if product["naam"] == productnaam:
                    return product
    except KeyError as e:
        print(f"Sleutel {e} niet gevonden")
        return None


def omzet_per_categorie(data):
    """Verkrijg totale omzet per categorie"""

    producten = data["2024"]["q1"]["producten"]

    # Maak een lege `dict` om het resultaat in op te slaan
    resultaat = {}

    # Loop over alle productgroepen
    for product_categorie in producten:
        categorie = product_categorie["categorie"]
        totale_omzet = 0

        # Loop over alle items in de productgroepen
        for item in product_categorie["items"]:
            # Loop door de maanden
            for maand in ["jan", "feb", "mrt"]:
                verkopen = item["verkopen"][maand]
                verkoopprijs = item["verkoopprijs"][maand]
                omzet = verkopen * verkoopprijs
                totale_omzet += omzet

        # Sla het resultaat per categorie op
        resultaat[categorie] = totale_omzet

    return resultaat


if __name__ == "__main__":
    # Laad de data
    verkoopdata = laad_verkoopdata()

    # Bekijk eerst de structuur
    print("Structuur van de verkoopdata:")
    print(
        json.dumps(verkoopdata, indent=2)
    )  # indent geeft aan met hoeveel spaties je regels wilt inspringen

    # Voorbeeld: navigeer naar de eerste categorie
    eerste_product = verkoopdata["2024"]["q1"]["producten"][0]
    print(f"\nEerste categorie: {eerste_product['categorie']}")

    # Voorbeeld: haal alle categorieën op
    categorieen = []
    for product_categorie in verkoopdata["2024"]["q1"]["producten"]:
        categorie = product_categorie["categorie"]
        categorieen.append(categorie)
    print(f"\nAlle categorieën: {categorieen}")

    # Toon de klanttevredenheid van een laptop, als het product bestaat
    # laptop_data = vind_product_met_get(verkoopdata, "Laptop")
    laptop_data = vind_product_met_try_except(verkoopdata, "Laptop")
    if laptop_data:
        print(
            f"\nGevonden! Klanttevredenheid: {laptop_data['klanttevredenheid']['score']}\n"
        )
    else:
        print("\nProduct niet gevonden\n")

    # Omzet per cateogrie
    resultaat = omzet_per_categorie(verkoopdata)
    for categorie, omzet in resultaat.items():
        bedrag = locale.format_string("€%.2f", omzet, grouping=True, monetary=True)
        bedrag = bedrag.replace(" ", ".")
        print(f"{categorie}: {bedrag}")
