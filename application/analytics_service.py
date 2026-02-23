import numpy as np
import os

class AnalyticsService:

    def __init__(self):
        self.path_transacciones = os.path.join("data", "transacciones.csv")
        self._cargar_datos()
        print("Datos cargados correctamente para análisis.")

    def _cargar_datos(self):

        if not os.path.exists(self.path_transacciones):
            print("No existe archivo de transacciones.")
            self.transacciones = np.array([])
            return

        self.transacciones = np.genfromtxt(
            self.path_transacciones,
            delimiter=",",
            skip_header=1,
            dtype=None,
            encoding="utf-8"
        )

        if self.transacciones.size > 0:
            self.id_cuenta = self.transacciones['f1']
            self.tipo = self.transacciones['f2']
            self.monto = self.transacciones['f3']
            self.fecha_str = self.transacciones['f4']

            self.fechas = self.fecha_str.astype('datetime64[s]')
            self.dias = self.fechas.astype('datetime64[D]')
        else:
            print("No hay transacciones registradas.")