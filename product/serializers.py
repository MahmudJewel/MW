from curses import meta
from dataclasses import fields
from rest_framework import serializers
from .models import Variant, Product, ProductImage, ProductVariant, ProductVariantPrice
from drf_writable_nested.serializers import WritableNestedModelSerializer


class VariantSerializers(serializers.ModelSerializer):
	class Meta:
		model = Variant
		fields = ['id', 'title', 'description', 'active']


class ProductImageSerializers(serializers.ModelSerializer):
	# product = ProductSerializers()
	class Meta:
		model = ProductImage
		fields = '__all__'


class ProductVariantSerializers(serializers.ModelSerializer):
	class Meta:
		model = ProductVariant
		fields = '__all__'


class ProductVariantPriceSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductVariantPrice
		fields = '__all__'
		depth=1


class ProductSerializers(WritableNestedModelSerializer):
	productimage_set = ProductImageSerializers(many=True)
	productvariantprice_set = ProductVariantPriceSerializer(many=True)
	# depth=1
	class Meta:
		model = Product
		fields = ['id', 'title', 'sku', 'description',
				  'productimage_set', 'productvariantprice_set']
		# depth=1
