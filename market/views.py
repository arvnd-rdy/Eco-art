from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.views import View
from .forms import SignUpForm, ProductUploadForm, ProfileForm, ReviewForm, CheckoutForm
from django.views.generic import TemplateView, ListView, CreateView, DetailView
from .models import Product, ContactMessage, Profile, Review, Order, OrderItem, Notification, Wishlist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
import datetime
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from decimal import Decimal

# Create your views here.

def create_notification(user, notification_type, title, message, related_product=None, related_user=None, related_order=None):
    """Utility function to create notifications"""
    Notification.objects.create(
        user=user,
        notification_type=notification_type,
        title=title,
        message=message,
        related_product=related_product,
        related_user=related_user,
        related_order=related_order
    )

class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            # Create welcome notification
            create_notification(
                user=user,
                notification_type='welcome',
                title='Welcome to EcoArt Market!',
                message='Thank you for joining our community of eco-conscious artists and art lovers. Start exploring sustainable artwork today!'
            )
            
            return redirect('home')
        return render(request, 'registration/signup.html', {'form': form})

class IndexView(TemplateView):
    template_name = 'market/index.html'

class ProductListView(ListView):
    model = Product
    template_name = 'market/index.html'
    context_object_name = 'products'
    ordering = ['-created_at']
    paginate_by = 9

    def get(self, request, *args, **kwargs):
        today = datetime.date.today().isoformat()
        session = request.session
        visit_key = f'visits_{today}'
        if visit_key in session:
            session[visit_key] += 1
        else:
            session[visit_key] = 1
        session.modified = True
        self.visit_count = session[visit_key]
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-created_at')
        q = self.request.GET.get('q', '').strip()
        category = self.request.GET.get('category', '').strip()
        location = self.request.GET.get('location', '').strip()
        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))
        if category:
            queryset = queryset.filter(category=category)
        if location:
            queryset = queryset.filter(location__icontains=location)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['category'] = self.request.GET.get('category', '')
        context['location'] = self.request.GET.get('location', '')
        context['categories'] = Product.CATEGORY_CHOICES
        context['locations'] = Product.objects.values_list('location', flat=True).distinct()
        context['visit_count'] = getattr(self, 'visit_count', 1)
        cart = self.request.session.get('cart', [])
        
        # Get wishlist items for current user
        wishlist_items = []
        if self.request.user.is_authenticated:
            wishlist_items = Wishlist.objects.filter(user=self.request.user).values_list('product_id', flat=True)
        
        for product in context['products']:
            product.in_cart = product.pk in cart
            product.in_wishlist = product.pk in wishlist_items
        return context

class ProductUploadView(CreateView):
    model = Product
    template_name = 'market/upload.html'
    form_class = ProductUploadForm
    success_url = '/'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        
        # Create notification for new product upload
        create_notification(
            user=self.request.user,
            notification_type='system',
            title='Product Uploaded Successfully!',
            message=f'Your artwork "{form.instance.title}" has been uploaded and is now live on the marketplace.',
            related_product=form.instance
        )
        
        return response

class ProductDetailView(DetailView):
    model = Product
    template_name = 'market/product_detail.html'
    context_object_name = 'product'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        product_id = self.get_object().id
        session = request.session
        recently_viewed = session.get('recently_viewed', [])
        if product_id in recently_viewed:
            recently_viewed.remove(product_id)
        recently_viewed.insert(0, product_id)
        session['recently_viewed'] = recently_viewed[:8]
        session.modified = True
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        
        # Get reviews for this product
        reviews = product.reviews.all()
        context['reviews'] = reviews
        
        # Check if current user has already reviewed this product
        if self.request.user.is_authenticated:
            user_review = reviews.filter(user=self.request.user).first()
            context['user_review'] = user_review
            
            # Pre-populate form with existing review data if user has already reviewed
            if user_review:
                context['review_form'] = ReviewForm(instance=user_review)
            else:
                context['review_form'] = ReviewForm()
            
            # Check if product is in cart and wishlist
            cart = self.request.session.get('cart', [])
            context['in_cart'] = product.pk in cart
            context['in_wishlist'] = Wishlist.objects.filter(user=self.request.user, product=product).exists()
        
        similar_products = (
            product.__class__.objects
            .filter(category=product.category)
            .exclude(pk=product.pk)
            .order_by('-created_at')[:3]
        )
        cart = self.request.session.get('cart', [])
        wishlist_items = []
        if self.request.user.is_authenticated:
            wishlist_items = Wishlist.objects.filter(user=self.request.user).values_list('product_id', flat=True)
        
        for sp in similar_products:
            sp.in_cart = sp.pk in cart
            sp.in_wishlist = sp.pk in wishlist_items
        context['similar_products'] = similar_products
        return context

class ReviewView(LoginRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = ReviewForm(request.POST)
        
        if form.is_valid():
            # Check if user already reviewed this product
            existing_review = Review.objects.filter(product=product, user=request.user).first()
            
            if existing_review:
                # Update existing review
                existing_review.rating = form.cleaned_data['rating']
                existing_review.comment = form.cleaned_data['comment']
                existing_review.save()
                messages.success(request, 'Your review has been updated!')
                
                # Create notification for review update
                create_notification(
                    user=product.owner,
                    notification_type='review_received',
                    title='Review Updated',
                    message=f'{request.user.username} updated their review for "{product.title}"',
                    related_product=product,
                    related_user=request.user
                )
            else:
                # Create new review
                review = form.save(commit=False)
                review.product = product
                review.user = request.user
                review.save()
                messages.success(request, 'Thank you for your review!')
                
                # Create notification for new review
                create_notification(
                    user=product.owner,
                    notification_type='review_received',
                    title='New Review Received!',
                    message=f'{request.user.username} left a {form.cleaned_data["rating"]}-star review for "{product.title}"',
                    related_product=product,
                    related_user=request.user
                )
        else:
            messages.error(request, 'Please correct the errors in your review.')
        
        return redirect('product_detail', pk=pk)

class DeleteReviewView(LoginRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        review = get_object_or_404(Review, product=product, user=request.user)
        
        # Store review info for notification
        review_comment = review.comment[:50] + "..." if len(review.comment) > 50 else review.comment
        
        # Delete the review
        review.delete()
        messages.success(request, 'Your review has been deleted successfully.')
        
        # Create notification for review deletion
        create_notification(
            user=product.owner,
            notification_type='review_deleted',
            title='Review Deleted',
            message=f'{request.user.username} deleted their review for "{product.title}"',
            related_product=product,
            related_user=request.user
        )
        
        return redirect('product_detail', pk=pk)

class CheckoutView(LoginRequiredMixin, View):
    def get(self, request):
        cart = request.session.get('cart', [])
        if not cart:
            messages.warning(request, 'Your cart is empty.')
            return redirect('cart')
        
        # Get cart items
        cart_items = Product.objects.filter(pk__in=cart)
        
        # Calculate totals
        subtotal = sum(item.price for item in cart_items)
        shipping_cost = Decimal('15.00')  # Fixed shipping cost
        tax = subtotal * Decimal('0.08')  # 8% tax
        total = subtotal + shipping_cost + tax
        
        form = CheckoutForm()
        
        context = {
            'cart_items': cart_items,
            'subtotal': subtotal,
            'shipping_cost': shipping_cost,
            'tax': tax,
            'total': total,
            'form': form,
        }
        
        return render(request, 'market/checkout.html', context)
    
    def post(self, request):
        cart = request.session.get('cart', [])
        if not cart:
            messages.warning(request, 'Your cart is empty.')
            return redirect('cart')
        
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Get cart items
            cart_items = Product.objects.filter(pk__in=cart)
            
            # Calculate totals
            subtotal = sum(item.price for item in cart_items)
            shipping_cost = Decimal('15.00')
            tax = subtotal * Decimal('0.08')
            total = subtotal + shipping_cost + tax
            
            # Create order
            order = form.save(commit=False)
            order.user = request.user
            order.subtotal = subtotal
            order.shipping_cost = shipping_cost
            order.tax = tax
            order.total = total
            order.save()
            
            # Create order items
            for product in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=1,
                    price=product.price
                )
            
            # Clear cart
            request.session['cart'] = []
            request.session.modified = True
            
            # Create notification for order placed
            create_notification(
                user=request.user,
                notification_type='order_placed',
                title='Order Placed Successfully!',
                message=f'Your order #{order.order_number} has been placed. Total: ${order.total}',
                related_order=order
            )
            
            # Create notifications for product owners
            for product in cart_items:
                create_notification(
                    user=product.owner,
                    notification_type='order_placed',
                    title='New Order for Your Artwork!',
                    message=f'{request.user.username} purchased "{product.title}" in order #{order.order_number}',
                    related_product=product,
                    related_user=request.user,
                    related_order=order
                )
            
            # Redirect to order confirmation
            messages.success(request, f'Order {order.order_number} has been placed successfully!')
            return redirect('order_confirmation', order_id=order.id)
        else:
            # Recalculate totals for form errors
            cart_items = Product.objects.filter(pk__in=cart)
            subtotal = sum(item.price for item in cart_items)
            shipping_cost = Decimal('15.00')
            tax = subtotal * Decimal('0.08')
            total = subtotal + shipping_cost + tax
            
            context = {
                'cart_items': cart_items,
                'subtotal': subtotal,
                'shipping_cost': shipping_cost,
                'tax': tax,
                'total': total,
                'form': form,
            }
            
            return render(request, 'market/checkout.html', context)

class OrderConfirmationView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        return render(request, 'market/order_confirmation.html', {'order': order})

class OrderHistoryView(LoginRequiredMixin, View):
    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        return render(request, 'market/order_history.html', {'orders': orders})

class OrderDetailView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        return render(request, 'market/order_detail.html', {'order': order})

class WishlistView(LoginRequiredMixin, View):
    def get(self, request):
        wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
        products = [item.product for item in wishlist_items]
        
        # Calculate totals for wishlist items
        subtotal = sum(product.price for product in products)
        shipping_cost = Decimal('15.00') if products else Decimal('0.00')
        tax = subtotal * Decimal('0.08')
        total = subtotal + shipping_cost + tax
        
        context = {
            'wishlist_products': products,
            'subtotal': subtotal,
            'shipping_cost': shipping_cost,
            'tax': tax,
            'total': total,
        }
        return render(request, 'market/wishlist.html', context)

class NotificationsView(LoginRequiredMixin, View):
    def get(self, request):
        notifications = Notification.objects.filter(user=request.user)
        unread_count = notifications.filter(is_read=False).count()
        
        context = {
            'notifications': notifications,
            'unread_count': unread_count,
        }
        return render(request, 'market/notifications.html', context)
    
    def post(self, request):
        # Mark notifications as read
        notification_ids = request.POST.getlist('notification_ids')
        if notification_ids:
            Notification.objects.filter(
                id__in=notification_ids,
                user=request.user
            ).update(is_read=True)
        
        return redirect('notifications')

class MarkNotificationReadView(LoginRequiredMixin, View):
    def post(self, request, notification_id):
        notification = get_object_or_404(Notification, id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        return JsonResponse({'success': True})

class ProductDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if request.user == product.owner:
            product_title = product.title
            product.delete()
            messages.success(request, f'"{product_title}" has been deleted successfully.')
        else:
            messages.error(request, 'You do not have permission to delete this product.')
        return redirect('profile')

class ContactSellerView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        return render(request, 'market/contact_seller.html', {'product': product})

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        message = request.POST.get('message')
        ContactMessage.objects.create(product=product, sender=request.user, message=message)
        send_mail(
            subject=f'New message for {product.title}',
            message=f'Message from {request.user.username}: {message}',
            from_email=request.user.email,
            recipient_list=[product.owner.email],
            fail_silently=False,
        )
        return redirect('product_detail', pk=pk)

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        profile, created = Profile.objects.get_or_create(user=user)
        products = user.products.all()
        edit_mode = request.GET.get('edit') == '1'
        form = ProfileForm(instance=profile) if edit_mode else None
        return render(request, 'market/profile.html', {
            'user': user,
            'profile': profile,
            'products': products,
            'edit_mode': edit_mode,
            'form': form,
        })

    def post(self, request):
        user = request.user
        profile, created = Profile.objects.get_or_create(user=user)
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        products = user.products.all()
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        return render(request, 'market/profile.html', {
            'user': user,
            'profile': profile,
            'products': products,
            'edit_mode': True,
            'form': form,
        })

class AboutView(TemplateView):
    template_name = 'market/about.html'

class ContactView(TemplateView):
    template_name = 'market/contact.html'

class TeamView(TemplateView):
    template_name = 'market/team.html'

class SellerProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        seller = get_object_or_404(User, id=user_id)
        profile, _ = Profile.objects.get_or_create(user=seller)
        products = seller.products.all().order_by('-created_at')
        return render(request, 'market/seller_profile.html', {
            'seller': seller,
            'profile': profile,
            'products': products,
        })

class HomeView(View):
    def get(self, request):
        # Visit stats
        today = timezone.now().date().isoformat()
        session = request.session
        visit_key = f'visits_{today}'
        if visit_key in session:
            session[visit_key] += 1
        else:
            session[visit_key] = 1
        session.modified = True
        visit_count = session[visit_key]
        total_visits = sum(v for k, v in session.items() if k.startswith('visits_'))
        last_visit = session.get('last_visit', None)
        session['last_visit'] = timezone.now().isoformat()
        # Recently viewed products
        recently_viewed_ids = session.get('recently_viewed', [])
        from market.models import Product
        recently_viewed = Product.objects.filter(id__in=recently_viewed_ids)
        featured_products = Product.objects.order_by('-created_at')[:4]
        return render(request, 'market/home.html', {
            'visit_count': visit_count,
            'total_visits': total_visits,
            'last_visit': last_visit,
            'recently_viewed': recently_viewed,
            'featured_products': featured_products,
        })

class MarketplaceView(ProductListView):
    template_name = 'market/marketplace.html'

class CartView(View):
    def get(self, request):
        cart = request.session.get('cart', [])
        from market.models import Product
        products = Product.objects.filter(id__in=cart)
        
        # Calculate totals
        subtotal = sum(product.price for product in products)
        shipping_cost = Decimal('15.00') if products.exists() else Decimal('0.00')
        tax = subtotal * Decimal('0.08')
        total = subtotal + shipping_cost + tax
        
        context = {
            'cart_products': products,
            'subtotal': subtotal,
            'shipping_cost': shipping_cost,
            'tax': tax,
            'total': total,
        }
        return render(request, 'market/cart.html', context)

def add_to_cart(request, pk):
    cart = request.session.get('cart', [])
    if pk not in cart:
        cart.append(pk)
        request.session['cart'] = cart
        request.session.modified = True
        
        # Create notification for adding to cart
        if request.user.is_authenticated:
            product = Product.objects.get(pk=pk)
            create_notification(
                user=request.user,
                notification_type='product_added_to_cart',
                title='Added to Cart',
                message=f'"{product.title}" has been added to your cart',
                related_product=product
            )
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('marketplace')))

def remove_from_cart(request, pk):
    cart = request.session.get('cart', [])
    if pk in cart:
        cart.remove(pk)
        request.session['cart'] = cart
        request.session.modified = True
        
        # Create notification for removing from cart
        if request.user.is_authenticated:
            product = Product.objects.get(pk=pk)
            create_notification(
                user=request.user,
                notification_type='product_removed_from_cart',
                title='Removed from Cart',
                message=f'"{product.title}" has been removed from your cart',
                related_product=product
            )
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('cart')))

def add_to_wishlist(request, pk):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=pk)
        wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
        
        if created:
            # Create notification for adding to wishlist
            create_notification(
                user=request.user,
                notification_type='product_added_to_wishlist',
                title='Added to Wishlist',
                message=f'"{product.title}" has been added to your wishlist',
                related_product=product
            )
            messages.success(request, f'"{product.title}" added to wishlist!')
        else:
            messages.info(request, f'"{product.title}" is already in your wishlist!')
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('marketplace')))

def remove_from_wishlist(request, pk):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=pk)
        wishlist_item = Wishlist.objects.filter(user=request.user, product=product).first()
        
        if wishlist_item:
            wishlist_item.delete()
            
            # Create notification for removing from wishlist
            create_notification(
                user=request.user,
                notification_type='product_removed_from_wishlist',
                title='Removed from Wishlist',
                message=f'"{product.title}" has been removed from your wishlist',
                related_product=product
            )
            messages.success(request, f'"{product.title}" removed from wishlist!')
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('wishlist')))

def move_to_cart(request, pk):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=pk)
        
        # Add to cart
        cart = request.session.get('cart', [])
        if pk not in cart:
            cart.append(pk)
            request.session['cart'] = cart
            request.session.modified = True
        
        # Remove from wishlist
        wishlist_item = Wishlist.objects.filter(user=request.user, product=product).first()
        if wishlist_item:
            wishlist_item.delete()
        
        messages.success(request, f'"{product.title}" moved to cart!')
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('wishlist')))

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You have been successfully logged out!')
        return redirect('home')
