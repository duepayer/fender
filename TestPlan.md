# Fender Product Page Test Plan

----

**TEST URL:** [http://shop.fender.com/en-US/electric-guitars/stratocaster/american-elite-stratocaster-hss-shawbucker/0114110723.html](http://shop.fender.com/en-US/electric-guitars/stratocaster/american-elite-stratocaster-hss-shawbucker/0114110723.html)

**TEST ENG:** Shawn Bacot

----

## Test Cases


**Verify Product Metadata is present and consistent across the page**
> Expected Result: 
> 
> - Title, Model #, Description and Features are consistent with expected product.
> - Specs contain reference to body shape and configuration listed in product title
> - Highlights mention product and images are consistent with expected product
> - Support contains links to matching product manual and matching product class/category warranty and manuals

**Test Product breadcrumb**
> Expected Result: 
> 
> - Home, category, sub-category, and product page links are displayed in that order
> - Home, category and sub-category links open correct pages when clicked
> - Product is referrenced within category and sub-category pages
> - Product page text is bolded and unclickable

**Test Product Image Zoom**
> Expected Result: 
> 
> - Image zooms in to display larger, more detailed image based on where the mouse is placed within the active main image on hover. Image returns to normal size on mouseout. 
> - "Hover to zoom" instructional text is present below main image.

**Test Product Image Gallery**
> Expected Result: 
> 
> - When user clicks on thumbnail it becomes the main image. 
> - Thumbnail border changes to red to indicate active image. 
> - Right/Left arrows toggle between additional and initially viewable images.

**Test color change option**
> Expected Result: 
> 
> - Clicking new color changes main image to reflect change
> - Active color thumbnail contained in black border
> - Color text is updated to reflect change
> - Main image is activated in image gallery
> - Image contains the correct active fingerboard material as well

**Test fingerboard material change option**
> Expected Result: 
> 
> - Clicking new fingerboard material changes main image to reflect change
> - Active fingerboard material thumbnail contained in black border
> - Color text is updated to reflect change
> - Main image is activated in image gallery
> - Image contains the correct active fingerboard material as well

**Test color and fingerboard combinations**
> Expected Result: 
> 
> - All sets of color and fingerboard combinations are properly reflected in image, color name and fingerboard material name

**Test adding to cart**
> Expected Result: 
> 
> - Clicking add to cart button adds product to mini cart
> - Page scrolls up to display mini cart content
> - Mini cart content section is displayed containing product
> - Product details in mini cart match product
> - Multiple products can be added and are appended to the content link
> - When more than 3 products are added to cart, only first 3 are displayed, the rest can be viewed by scrolling within mini cart content section


**Test price and payment options follow when scrolling below fold**
> Expected Result: 
> 
> - Price, "Add To Cart" and "Play One" buttons and Add To Wishlist link follow on right rail when scrolling below the fold

**Test Facebook share button**
> Expected Result: 
> 
> - Clicking on Facebook share button opens a new window displaying appropriate product image, title and description 
> - Comment section, sharing group and Post to Facebook button are present and functional

**Test Share button**
> Expected Result: 
> 
> - Fullscreen share modal window is displayed when clicked
> - Title and link to product is displayed
> - 10 Top Services are displayed by default
> - Each Service icon links to the correct share option for that service. 
> - Clicking Load More button displays all remaining items
> - Search field filters and displays updated sharing options for each key entry

