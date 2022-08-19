from multiprocessing import context
from django.shortcuts import render
from django.views import generic
from product.models import Variant, Product, ProductImage, ProductVariant, ProductVariantPrice

# start by me 
from product.serializers import ProductSerializers
from rest_framework.views import APIView
from rest_framework import status, permissions
# from rest_framework import permissions
from rest_framework.response import Response
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# end by me 


class CreateProductView(generic.TemplateView):
	template_name = 'products/create.html'

	def get_context_data(self, **kwargs):
		context = super(CreateProductView, self).get_context_data(**kwargs)
		variants = Variant.objects.filter(active=True).values('id', 'title')
		print('variants are: ', variants) # by me 
		context['product'] = True
		context['variants'] = list(variants.all())
		return context


# List product and search 
def ListingProductView(request):
	products = Product.objects.all()
	# search part 
	if request.method=='GET':
		title = request.GET.get('title', None)
		dropdown = request.GET.get('dropdown', None)
		price_from = request.GET.get('price_from', None)
		price_to = request.GET.get('price_to', None)
		date = request.GET.get('date', None)
		print('Title ', title, dropdown, price_from, price_to, date)
		if title:
			products=products.filter(title__icontains=title)
		if dropdown:
			# products=products.filter(productvariant__id = dropdown)
			products=products.filter(productvariant__variant_title__icontains = dropdown)
			print('Products as variant: ', products)
		if price_from and price_to:
			products=products.filter(productvariantprice__price__range=(price_from, price_to))
		if date:
			products=products.filter(created_at__date=date)
		# distinct products 
		products=products.distinct()

	variant=Variant.objects.filter(active=True)
	print('Variants are=> ', variant)
	total_products = products.count()
	# for Paginator 
	page = request.GET.get('page', 1)
	paginator = Paginator(products, 3)  # 3 objects in each page.
	try:
		products = paginator.page(page)
	except PageNotAnInteger:
		products = paginator.page(1)
	except EmptyPage:
		products = paginator.page(paginator.num_pages)
	context={
		'products' : products,
		'total_products': total_products,
		'variant': variant,
	}
	return render(request, 'products/list.html', context)



# API for Product creation 
class ProductCreateAPIView(APIView):
	def post(self, request): 
		data=request.data
		print('All data: ', data)

		# product create
		title = data.get('title')
		sku = data.get('sku')
		description = data.get('description')
		product = Product.objects.create(title=title, sku=sku, description=description)

		# Create image 
		file_path = data.get('file_path') 
		product_image = ProductImage.objects.create(product=product, file_path=file_path)
		
		# create product variants
		productVariants = data.get('productVariants')
		productVariants_len=len(productVariants)
		productVariants_id=[[] for i in range(productVariants_len)] 
		for i in range(productVariants_len):
			lst=productVariants[i].get('tags')
			for tag in lst:
				# print('tags: ', tag)
				product_variant=ProductVariant.objects.create(variant_title=tag, 
												variant_id=productVariants[i].get('option'),
												product=product)
				print('product_variant: ', product_variant)
				productVariants_id[i].append(product_variant.id)

		# store product variant id sequently 
		temp_productVariants_id=[]
		if productVariants_len == 1:
			for i in productVariants_id[0]:
				temp_productVariants_id.append(i)
		elif productVariants_len == 2:
			for i in productVariants_id[0]:
				for j in productVariants_id[1]:
					temp_productVariants_id.append(i)
					temp_productVariants_id.append(j)
		elif productVariants_len == 3:
			for i in productVariants_id[0]:
				for j in productVariants_id[1]:
					for k in productVariants_id[2]:
						temp_productVariants_id.append(i)
						temp_productVariants_id.append(j)
						temp_productVariants_id.append(k)

		print('productVariants_id: ', productVariants_id)
		# create productVariantPrices
		productVariantPrices=data.get('productVariantPrices')
		for productVariantPrice in productVariantPrices:
			product_variant_one = None
			product_variant_two = None
			product_variant_three = None
			if temp_productVariants_id and productVariants_len==1:
				product_variant_one=temp_productVariants_id.pop(0)
			elif temp_productVariants_id and productVariants_len==2:
				product_variant_one=temp_productVariants_id.pop(0)
				product_variant_two=temp_productVariants_id.pop(0)
			elif temp_productVariants_id and productVariants_len==3:
				product_variant_one=temp_productVariants_id.pop(0)
				product_variant_two=temp_productVariants_id.pop(0)
				product_variant_three=temp_productVariants_id.pop(0)
				
			ProductVariantPrice_obj=ProductVariantPrice.objects.create(product_variant_one_id=product_variant_one,
												product_variant_two_id=product_variant_two,
												product_variant_three_id=product_variant_three,
												price=float(productVariantPrice.get('price')),
												stock=float(productVariantPrice.get('stock')),
												product=product
												) 
			print('ProductVariantPrice_obj price & stock: ', ProductVariantPrice_obj.price, ProductVariantPrice_obj.stock)
		return HttpResponse("msg", content_type='text/plain') 




class EditProductView(generic.TemplateView):
	template_name = 'products/edit.html'

	def get_context_data(self, pk=None, **kwargs):
		context = super(EditProductView, self).get_context_data(**kwargs)
		variants = Variant.objects.filter(active=True).values('id', 'title')
		# print('variants are: ', variants) # by me 
		context['product'] = True
		context['variants'] = list(variants.all())
		context['id'] = pk
		return context


# **************************  API *************************************
# get all product or Create new product
class AllProductsAPIView(APIView):
	def get(self, request):
		products = Product.objects.all()
		serializer = ProductSerializers(products, many=True)
		return Response(serializer.data)

	def post(self, request):
		serializer = ProductSerializers(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST) 

# update product  
class EditProductAPIView(APIView):
	def get_object(self, pk):
		try:
			return Product.objects.get(id=pk)
		except Product.DoesNotExist():
			return HttpResponse(status=404)

	def get(self, request, pk):  # see indivisual product
		st = self.get_object(pk)
		serializer = ProductSerializers(st)
		# return JsonResponse(serializer.data)
		print('Edit data=> ', serializer.data)
		print('ID=> ', pk)
		return Response(serializer.data)
		
	def put(self, request, pk):
		product = self.get_object(pk)
		serializer = ProductSerializers(product, data=request.data)
		if serializer.is_valid():
			serializer.save()
			# return JsonResponse(serializer.data)
			return Response(serializer.data)
		return Response(serializer.errors, status=400)

 
