import itertools

# -------------------- IMAGE URL LIST --------------------
IMAGES = [
    "https://images.immediate.co.uk/production/volatile/sites/30/2023/01/Maqlooba-4cd95c3.jpg?quality=90&resize=708,643",
    "https://pastrieslikeapro.com/wp-content/uploads/2014/09/fresh-as-a-daisy-doughnuts-3.jpg",
    "https://handletheheat.com/wp-content/uploads/2022/06/angel-food-cake-with-berries-SQUARE.jpg",
    "https://www.innovamarketinsights.com/wp-content/uploads/2023/10/soft-drinks--jpg.webp",
    "https://valampuri.foodorders.lk/images/food/phpxpdKKq.jpg",
    "https://img.delicious.com.au/MQnnlDkF/del/2024/05/devilys-food-cake-212625-2.jpg",
    "https://www.thisvivaciouslife.com/wp-content/uploads/2023/06/20-Minute-Gluten-Free-Donuts-Fried-Bakery-Style-square.jpg",
    "https://thai-foodie.com/wp-content/uploads/2025/04/thai-curry-fried-rice-plated.jpg", 
    "https://d2td6mzj4f4e1e.cloudfront.net/wp-content/uploads/sites/9/2019/04/soft-drinks.jpg",
    "https://tuktuknegombo.com/wp-content/uploads/2024/11/Seafood-Kottu-Negombo.webp",
    "https://www.foodandwine.com/thmb/RYsqVqa6snK1_WkmZm7m-h6rwfM=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/FAW-recipes-double-chocolate-pudding-hero-f8cf686f09504feb8b155c4c2c459838.jpg",
    "https://rakskitchen.net/wp-content/uploads/2021/04/vegan-mango-pudding-feature.jpg",
    "https://images.immediate.co.uk/production/volatile/sites/30/2020/12/Noodles-with-chilli-oil-eggs-6ec34e9.jpg?quality=90&resize=708,643",
    "https://japanesecooking101.com/wp-content/uploads/2013/10/IMG_7721.jpg",
    "https://blog.cinnamonhotels.com/wp-content/uploads/2022/03/shutterstock_446312773.jpg",
    "https://images.immediate.co.uk/production/volatile/sites/30/2020/08/chorizo-mozarella-gnocchi-bake-cropped-9ab73a3.jpg",
    "https://static.independent.co.uk/s3fs-public/thumbnails/image/2018/01/12/12/healthy-avo-food.jpg",
    "https://images.immediate.co.uk/production/volatile/sites/30/2022/06/Party-food-recipes-fcfb3af.jpg?quality=90&resize=708,643",
    "https://www.kimscravings.com/wp-content/uploads/2022/04/Better-Than-Sex-Cake-7.jpg",
    "https://images.immediate.co.uk/production/volatile/sites/30/2022/06/Tequila-sunrise-fb8b3ab.jpg",
    "https://blog.travelkhana.com/tkblog/wp-content/uploads/sites/2/2023/02/A-to-Z-Food-1024x683.jpg",
]

# -------------------- ROTATION --------------------
_cycle = itertools.cycle(IMAGES)

def get_next_image_url():
    """
    Returns next image URL in rotation (NO download needed)
    """
    return next(_cycle)