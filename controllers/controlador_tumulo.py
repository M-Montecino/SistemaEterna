

from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from controllers.controlador_geral import (
        ControladorGeral
    )

class ControladorTumulo:
    def __init__(
        self,
        controlador_geral: "ControladorGeral"):
        self.___tumulo = []
        self.__controlador_geral = (controlador_geral)