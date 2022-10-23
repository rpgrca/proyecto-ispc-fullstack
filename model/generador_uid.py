import uuid

class GeneradorUid:
    def generar(self) -> uuid.UUID:
        return uuid.uuid4()


class FakeGeneradorUid(GeneradorUid):
    def __init__(self, uid: uuid.UUID):
        self.__uid = uid

    def generar(self) -> uuid.UUID:
        return self.__uid