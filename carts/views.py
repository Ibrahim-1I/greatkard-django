from django.shortcuts import redirect, render, get_object_or_404

from accounts.views import _cart_id
from carts.models import Cart, CartItem
from store.models import Product, Variation  # Assuming you have a product model in store app
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required  # Import login_required decorator
# Create your views here.




def add_cart(request, product_id):
    current_user = request.user  # Get the current user
    try:
        product = Product.objects.get(id=product_id)  # Get the product by id
    except Product.DoesNotExist:
        return redirect('product_not_found')  # Handle product not found

    # Get or create the cart
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))  # Get the cart by session key
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))  # Create a new cart if it doesn't exist
        cart.save()  # Save the cart

    product_variation = []  # Initialize product_variation list

    if current_user.is_authenticated:  # Check if the user is authenticated
        if request.method == 'POST':
            for item in request.POST:  # Loop through POST data
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)  # Get the variation
                    product_variation.append(variation)  # Append the variation to the list
                except Variation.DoesNotExist:
                    pass

            is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()  
            if is_cart_item_exists:  # If the item exists in the cart
                cart_item = CartItem.objects.filter(product=product, user=current_user)  # Get the cart item
                ex_var_list = []  # List to hold existing variation IDs
                id_list = []  # List to hold existing item IDs

                for item in cart_item:  # Loop through existing cart items
                    existing_variations = item.variations.all()  # Get existing variations
                    ex_var_list.append(list(existing_variations))  # Append existing variations to the list
                    id_list.append(item.id)  # Append item ID to the list

                if product_variation in ex_var_list:  # Check if the current variation exists in the existing variations
                    index = ex_var_list.index(product_variation)
                    item_id = id_list[index]  # Get the item ID for the existing variation
                    item = CartItem.objects.get(product=product, id=item_id)  # Get the cart item
                    item.quantity += 1
                    item.save()
                else:
                    item = CartItem.objects.create(product=product, quantity=1, user=current_user)  # Create a new cart item
                    if product_variation:  # Check if there are variations
                        item.variations.clear()  # Clear existing variations
                        item.variations.add(*product_variation)  # Add new variations
                        item.save()  # Save the cart item
            else:
                cart_item = CartItem.objects.create(
                    product=product, 
                    quantity=1, 
                    user=current_user  # Create a new cart item for the authenticated user
                ) 
                if product_variation:
                    cart_item.variations.clear()
                    cart_item.variations.add(*product_variation)
                    cart_item.save()    

            return redirect('cart')  # Redirect to cart page
    else:
        # Handle case for unauthenticated users
        return redirect('login')  # Redirect to login page or appropriate action

    return redirect('cart')  # Fallback to redirect to cart





def remove_cart(request, product_id, cart_item_id):
    # Logic to remove a product from the cart
    
    product = get_object_or_404(Product, id=product_id)  # Get the product by id
    try: 
        if request.user.is_authenticated:   
           cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id )  # Get the cart item
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
          cart_item.quantity -= 1
          cart_item.save()
        else:
           cart_item.delete()
    except:
        pass  # If the item does not exist, we simply pass 

    return redirect('cart')  # Redirect to the cart view


def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)  # Get the product by id
    if request.user.is_authenticated:
        cart_item= CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
       cart = Cart.objects.get(cart_id=_cart_id(request))
       cart_item = CartItem.objects.filter(product=product, cart=cart, id= cart_item_id )  # Get the cart item
    cart_item.delete()  # Delete the cart item
    return redirect('cart')  # Redirect to the cart view

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)  # Get the cart item
        if cart_item.quantity > 1:
            cart_item.quantity -= 1  # Decrement the quantity
            cart_item.save()  # Save the updated cart item
        else:
            cart_item.delete()  # Remove the item if quantity is 1
    except CartItem.DoesNotExist:
        pass  # If the item does not exist, we simply pass

    return redirect('cart')  # Redirect to the cart view


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax =  0
        grand_total = 0
        if request.user.is_authenticated:  # Check if the user is authenticated
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)  # Get active cart items for the user
        else:    
           cart = Cart.objects.get(cart_id=_cart_id(request))  # Get the cart by session key
           cart_items = CartItem.objects.filter(cart=cart, is_active=True)  # Get active cart items
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)  # Calculate total price
            quantity += cart_item.quantity

        tax = (2 * total)/ 100
        grand_total = total + tax  # Calculate grand total

    except ObjectDoesNotExist: # type: ignore
        pass  # If no cart exists, we simply pass


    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)  # Render the cart template with context


@login_required(login_url='login')  
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax =  0
        grand_total = 0
        if request.user.is_authenticated:  # Check if the user is authenticated
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)  # Get active cart items for the user
        else:    
           cart = Cart.objects.get(cart_id=_cart_id(request))  # Get the cart by session key
           cart_items = CartItem.objects.filter(cart=cart, is_active=True)  # Get active cart items
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)  # Calculate total price
            quantity += cart_item.quantity

        tax = (2 * total)/ 100
        grand_total = total + tax  # Calculate grand total

    except ObjectDoesNotExist: # type: ignore
        pass  # If no cart exists, we simply pass

    
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/checkout.html', context)  # Render the checkout template



