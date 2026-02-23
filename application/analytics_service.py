import numpy as np
import os

class AnalyticsService:

    def __init__(self):
        self.path_transacciones = os.path.join("data", "transacciones.csv")
        self._cargar_datos()

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

            print("Datos cargados correctamente para análisis.")
        else:
            print("No hay transacciones registradas.")

    def estadisticas_por_cuenta(self):

        if self.transacciones.size == 0:
            print("No hay transacciones para analizar.")
            return

        mask_ingresos = (self.tipo == "DEPOSITO") | (self.tipo == "TRANSFER_IN")
        mask_gastos = (self.tipo == "RETIRO") | (self.tipo == "TRANSFER_OUT")

        cuentas = np.unique(self.id_cuenta)

        print("\n=== ESTADÍSTICAS POR CUENTA ===")

        for cuenta in cuentas:

            mask_cuenta = (self.id_cuenta == cuenta)

            ingresos = self.monto[mask_cuenta & mask_ingresos]
            gastos = self.monto[mask_cuenta & mask_gastos]

            total_depositos = ingresos.sum()
            total_gastos = gastos.sum()
            # ---- Agrupación diaria (solo ingresos en las cuentas) ----
            dias_cuenta = self.dias[mask_cuenta & mask_ingresos]
            montos_cuenta = self.monto[mask_cuenta & mask_ingresos]

            if montos_cuenta.size > 0:

                dias_unicos, indices = np.unique(dias_cuenta, return_inverse=True)

                totales_diarios = np.bincount(indices, weights=montos_cuenta)

                promedio_diario = totales_diarios.mean()
                std_diaria = totales_diarios.std()

                p50 = np.percentile(totales_diarios, 50)
                p90 = np.percentile(totales_diarios, 90)
                p99 = np.percentile(totales_diarios, 99)

            else:
                promedio_diario = 0
                std_diaria = 0
                p50 = p90 = p99 = 0
            ratio = total_depositos / total_gastos if total_gastos != 0 else 0



            print(f"\nCuenta {cuenta}")
            print(f"Total depósitos: {total_depositos}")
            print(f"Total gastos: {total_gastos}")
            print(f"Ratio depósitos/gastos: {ratio}")
            print(f"Promedio diario: {promedio_diario}")
            print(f"Desviación estándar diaria: {std_diaria}")
            print(f"P50: {p50}")
            print(f"P90: {p90}")
            print(f"P99: {p99}")