from .models import Order

def notifications_processor(request):
    if request.user.is_authenticated:
        incoming_orders = Order.objects.filter(product__farmer=request.user).order_by('-created_at')[:10]
        pending_count = Order.objects.filter(product__farmer=request.user, status='PENDING').count()
        return {
            'incoming_orders': incoming_orders,
            'pending_orders_count': pending_count,
        }
    return {}
