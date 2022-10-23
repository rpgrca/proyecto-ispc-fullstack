import uuid

class GeneradorUid:
    def generar(self) -> uuid:
        return uuid.uuid4()


class FakeGeneradorUid(GeneradorUid):
    def __init__(self, uid: uuid):
        self.__uid = uid

    def generar(self) -> uuid:
        return self.__uid