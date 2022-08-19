from django.urls import path
from django.views.generic import TemplateView

# from product.views.product import CreateProductView, EditProductView
from product.views.variant import VariantView, VariantCreateView, VariantEditView


from product.views.product import CreateProductView, EditProductView, ProductCreateAPIView, ListingProductView, AllProductsAPIView, EditProductAPIView


app_name = "product"

urlpatterns = [
    # Variants URLs
    path('variants/', VariantView.as_view(), name='variants'),
    path('variant/create', VariantCreateView.as_view(), name='create.variant'),
    path('variant/<int:id>/edit', VariantEditView.as_view(), name='update.variant'),

    # Products URLs
    path('create/', CreateProductView.as_view(), name='create.product'), # product creation
    # path('list/', TemplateView.as_view(template_name='products/list.html', extra_context={
    #     'product': True
    # }), name='list.product'), # listing product


    # edit product 
    path('edit/<int:pk>', EditProductView.as_view(), name='edit.product'),
    # api by me
    path('list/', ListingProductView, name='list.product'),

    # api url  
    path('api/createproduct/', ProductCreateAPIView.as_view(), name='ProductCreateAPIView'),
    path('api/all-products/', AllProductsAPIView.as_view(), name='AllProductsAPIView'),
    path('api/edit/<int:pk>/', EditProductAPIView.as_view(), name='EditProductAPIView'),

]
