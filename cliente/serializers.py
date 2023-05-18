from rest_framework import serializers


class NombreClienteSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=100)
    apellido = serializers.CharField(max_length=100)


class ClienteSerializer(serializers.Serializer):
    nombreCliente = NombreClienteSerializer()
    telefono = serializers.CharField(max_length=100)
    edad = serializers.IntegerField()


class GetClienteSerializer(serializers.Serializer):
    telefono = serializers.CharField(max_length=100)


