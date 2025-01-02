from rest_framework import serializers
from .models import User, Category, Product, Order, OrderItem, Prescription, CartItem, Address
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 
                 'phone_number', 'address', 'is_admin')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    inStock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'stock', 'inStock', 'category', 
                 'category_name', 'image', 'requires_prescription', 'created_at', 
                 'updated_at')

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'user', 'street_address', 'city', 'state', 'zip_code', 'country', 'is_default', 'created_at', 'updated_at')
        read_only_fields = ('user', 'created_at', 'updated_at')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Ensure all string fields have default values
        for field in ['street_address', 'city', 'state', 'zip_code', 'country']:
            if representation.get(field) is None:
                representation[field] = ''
        return representation

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'product_name', 'quantity', 'price')

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    shipping_address = AddressSerializer()

    class Meta:
        model = Order
        fields = ('id', 'user', 'user_email', 'status', 'total_amount', 'items',
                 'created_at', 'updated_at', 'shipping_address', 'prescription')
        read_only_fields = ('user',)

    def create(self, validated_data):
        items_data = self.context.get('request').data.get('items', [])
        if not items_data:
            raise serializers.ValidationError("No items provided")

        shipping_address_data = validated_data.pop('shipping_address')
        
        # Calculate total amount before creating order
        total_amount = 0
        for item_data in items_data:
            try:
                product = Product.objects.get(id=item_data['product'])
                quantity = item_data['quantity']
                
                # Validate stock
                if product.stock < quantity:
                    raise serializers.ValidationError(f"Not enough stock for {product.name}")
                
                # Add to total
                total_amount += product.price * quantity
            except Product.DoesNotExist:
                raise serializers.ValidationError(f"Product with id {item_data['product']} does not exist")
            except KeyError:
                raise serializers.ValidationError("Invalid item data format")

        # Create or get shipping address
        shipping_address = Address.objects.create(
            user=validated_data['user'],
            **shipping_address_data
        )
        
        # Create order with shipping address and total amount
        validated_data['total_amount'] = total_amount
        order = Order.objects.create(shipping_address=shipping_address, **validated_data)
        
        # Create order items and update stock
        for item_data in items_data:
            product = Product.objects.get(id=item_data['product'])
            quantity = item_data['quantity']
            
            # Create order item
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price * quantity
            )
            
            # Update product stock
            product.stock -= quantity
            product.save()
        
        return order

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )
    quantity = serializers.IntegerField(min_value=1)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        cart_item = CartItem.objects.create(user=user, **validated_data)
        return cart_item

class PrescriptionSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Prescription
        fields = ('id', 'user', 'user_name', 'image', 'uploaded_at', 'status', 'notes')
        read_only_fields = ('user',)
