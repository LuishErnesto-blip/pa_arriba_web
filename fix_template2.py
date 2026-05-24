with open('blog/templates/blog/detalle_post.html', 'rb') as f:
    content = f.read()
old = b'<img src="{% static \'core/gallery_images/\' %}{{ post.image.name|cut:\'blog_images/\' }}" alt="{{ post.image_alt_text|default:post.title }}" class="w-full h-auto object-cover rounded-lg mb-8 shadow-md">'
new_val = b'<img src="{{ post.image.url }}" alt="{{ post.image_alt_text|default:post.title }}" class="w-full h-auto object-cover rounded-lg mb-8 shadow-md">'
result = content.replace(old, new_val)
print('Cambio aplicado:', old in content and old not in result)
with open('blog/templates/blog/detalle_post.html', 'wb') as f:
    f.write(result)
