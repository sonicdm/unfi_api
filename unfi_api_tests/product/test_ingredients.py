from unittest import TestCase
from unfi_api.product.ingredients import Ingredients
from unfi_api_tests.assets import ProductsFiles
from datetime import date


class TestIngredient(TestCase):

    """
    ingredients_json = {
  "Ingredients": "Annie's durum semolina pasta, original white Vermont cheddar cheese (milk, salt, cheese cultures, enzymes), whey, sweet cream buttermilk.",
  "ModifiedDate": "5/22/2020"
}
    """

    def setUp(self) -> None:
        self.product_file = ProductsFiles()
        self.ingredients_json = self.product_file.ingredients_json

    def test_ingredient_init(self):
        ingredients = Ingredients(
            ingredients="Test Ingredients",
            modified_date="5/22/2020"
        )

        self.assertEqual(ingredients.ingredients,
                         "Test Ingredients")

    def test_ingredient_to_dict(self):
        ingredients = Ingredients(
            ingredients="Test Ingredients",
            modified_date="5/22/2020"
        )

        self.assertEqual(
            ingredients.dict(),
            dict(
                ingredients="Test Ingredients",
                modified_date=date(2020, 5, 22)
            )
        )

    def test_ingredient_from_dict(self):
        print(self.ingredients_json)
        ingredients = Ingredients(**self.ingredients_json)

        self.assertEqual(ingredients.ingredients,
                         self.ingredients_json["Ingredients"])
