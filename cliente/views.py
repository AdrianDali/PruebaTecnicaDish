from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from cliente.serializers import ClienteSerializer, GetClienteSerializer
from cliente.classes import Cliente
from cliente.models import Cliente as ClienteModel
from rest_framework.exceptions import APIException
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.


class TestView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        return Response(data={"hello": "world"}, status=status.HTTP_200_OK)


class CreateCliente(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_description="Creacion de un cliente",
        responses={
            200: openapi.Response(
                description="Respuesta exitosa",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'nombreCliente': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'nombre': openapi.Schema(type=openapi.TYPE_STRING),
                                'apellido': openapi.Schema(type=openapi.TYPE_STRING),
                            },
                            required=['nombre', 'apellido'],
                        ),
                        'telefono': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'edad': openapi.Schema(type=openapi.TYPE_INTEGER),
                    },
                    required=['nombreCliente', 'telefono', 'edad'],
                ),
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = ClienteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # convercion de datos
        data = serializer.validated_data
        cliente = Cliente(data)

        if cliente.edad < 18:
            raise APIException('El cliente debe ser mayor de edad')

        if len(cliente.telefono) < 10:
            raise APIException('El telefono debe tener 10 digitos')

        if ClienteModel.objects.filter(telefono=cliente.telefono).exists():
            raise APIException('Ya existe un cliente con ese telefono')
        try:
            cliente.insert_db()
        except Exception as e:
            return Response(data={"message": "Error al crear el cliente"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data={"message": "Cliente creado"}, status=status.HTTP_201_CREATED)


class EditCliente(APIView):
    permission_classes = (AllowAny,)
    @swagger_auto_schema(
        operation_description="Edicion de un cliente",
        responses={
            200: openapi.Response(
                description="Respuesta exitosa, el cliente se edito correctamente",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'cliente': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'nombreCliente': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'nombre': openapi.Schema(type=openapi.TYPE_STRING),
                                        'apellido': openapi.Schema(type=openapi.TYPE_STRING),
                                    },
                                    required=['nombre', 'apellido'],
                                ),
                                'telefono': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'edad': openapi.Schema(type=openapi.TYPE_INTEGER),
                            },
                            required=['nombreCliente', 'telefono', 'edad'],
                        ),
                        'nuevo_cliente': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'nombreCliente': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'nombre': openapi.Schema(type=openapi.TYPE_STRING),
                                        'apellido': openapi.Schema(type=openapi.TYPE_STRING),
                                    },
                                    required=['nombre', 'apellido'],
                                ),
                                'telefono': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'edad': openapi.Schema(type=openapi.TYPE_INTEGER),
                            },
                            required=['nombreCliente', 'telefono', 'edad'],
                        ),
                    },
                    required=['cliente', 'nuevo_cliente'],
                ),
            ),
        },
    )

    def post(self, request, *args, **kwargs):
        serializer = ClienteSerializer(data=request.data.get('cliente'))
        serializer.is_valid(raise_exception=True)
        # convercion de datos
        data = serializer.validated_data

        cliente = Cliente(data)

        serializer = ClienteSerializer(data=request.data.get('nuevo_cliente'))
        serializer.is_valid(raise_exception=True)
        # convercion de datos
        data = serializer.validated_data
        
        cliente_nuevo = Cliente(data)

        if ClienteModel.objects.filter(telefono=cliente_nuevo.telefono).exists():
            raise APIException(
                'No se puede actualizar con este telefono porque ya esta relacionado a otro cliente')
        
        if cliente_nuevo.edad < 18:
            raise APIException('El cliente debe ser mayor de edad')
        
        if len(cliente_nuevo.telefono) < 10:
            raise APIException('El telefono debe tener 10 digitos')

        if not ClienteModel.objects.filter(telefono=cliente.telefono).exists():
            raise APIException(
                'No existe un cliente registrado con este telefono')

        cliente_actualizado =ClienteModel.objects.get(telefono=cliente.telefono)

        print(cliente_actualizado.nombre)


        cliente_actualizado.nombre = cliente_nuevo.nombre
        cliente_actualizado.apellido = cliente_nuevo.apellido
        cliente_actualizado.edad = cliente_nuevo.edad
        cliente_actualizado.telefono = cliente_nuevo.telefono
    
        cliente_actualizado.save()
        
        
        

        return Response(data={"message": "Cliente actualizado"}, status=status.HTTP_200_OK)


class DeleteCliente(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_description="Eliminar un cliente",
        responses={
            200: openapi.Response(
                description="Respuesta exitosa, cliente eliminado",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'nombreCliente': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'nombre': openapi.Schema(type=openapi.TYPE_STRING),
                                'apellido': openapi.Schema(type=openapi.TYPE_STRING),
                            },
                            required=['nombre', 'apellido'],
                        ),
                        'telefono': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'edad': openapi.Schema(type=openapi.TYPE_INTEGER),
                    },
                    required=['nombreCliente', 'telefono', 'edad'],
                ),
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = ClienteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        cliente = Cliente(data)

        if not ClienteModel.objects.filter(telefono=cliente.telefono).exists():
            raise APIException(
                'No existe un cliente registrado con este telefono')

        try:
            cliente = ClienteModel.objects.get(telefono=cliente.telefono)
            cliente.delete()

        except Exception as e:
            return Response(data={"message": "Error al eliminar el cliente"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data={"message": "Cliente eliminado"}, status=status.HTTP_200_OK)


class GetCliente(APIView):

    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_description="Obtener un cliente",
        responses={
            200: openapi.Response(
                description="Respuesta exitosa",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'telefono': openapi.Schema(type=openapi.TYPE_INTEGER),
                    },
                    required=['telefono'],
                ),
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        serializer = GetClienteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        if not ClienteModel.objects.filter(telefono=data.get("telefono")).exists():
            raise APIException(
                'No existe un cliente registrado con este telefono')

        cliente = ClienteModel.objects.get(telefono=data.get("telefono"))

        return Response(data={"nombre": cliente.nombre, "apellido": cliente.apellido, "edad": cliente.edad, "telefono": cliente.telefono}, status=status.HTTP_200_OK)
