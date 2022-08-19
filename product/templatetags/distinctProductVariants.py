from django import template
# from admn import models as AMODEL

register = template.Library()

# Check the product is on cart or not.Base of this, add or remove button set

@register.simple_tag
def distinctProductVariants(productvariant):
	distinctProductVariants=productvariant.values('variant_title').distinct()
	# print('Custom title=> ', distinctProductVariants)
	return distinctProductVariants
