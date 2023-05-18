from cliente.models import Cliente as ClienteModel
class Cliente: 
    def __init__(self, data) -> None:
        self.data = data
        self.nombre = data.get("nombreCliente").get("nombre")
        self.apellido = data.get("nombreCliente").get("apellido")
        self.telefono = data.get("telefono")
        self.edad = data.get("edad")


    def insert_db(self):
        try:
            cliente = ClienteModel.objects.create(
                nombre = self.nombre,
                apellido = self.apellido,
                telefono = self.telefono,
                edad = self.edad
            )
            cliente.save()
        except Exception as e:
            print(e)
            return None
        
        return cliente


