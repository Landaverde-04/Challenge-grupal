import numpy as np
import os


class AnalyticsService:

    def __init__(self):
        self.path_transacciones = os.path.join("data", "transacciones.csv")
        self._cargar_datos()

    # -------------------------------------------------
    # CARGA DE DATOS
    # -------------------------------------------------
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

    # -------------------------------------------------
    # 2.1 ESTADÍSTICAS POR CUENTA
    # -------------------------------------------------
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

            # ---- Agrupación diaria (solo ingresos) ----
            dias_cuenta = self.dias[mask_cuenta & mask_ingresos]
            montos_cuenta = ingresos

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

    # -------------------------------------------------
    # 2.2 DASHBOARD ADMINISTRADOR
    # -------------------------------------------------
    def dashboard_admin(self):

        if self.transacciones.size == 0:
            print("No hay transacciones para analizar.")
            return

        print("\n=== DASHBOARD ADMINISTRADOR ===")

        # 1. Transacciones por día
        dias_unicos, indices = np.unique(self.dias, return_inverse=True)
        transacciones_por_dia = np.bincount(indices)

        print("\nTransacciones por día:")
        for d, total in zip(dias_unicos, transacciones_por_dia):
            print(f"{d}: {total}")

        # Top 5 días pico
        top5_indices = np.argsort(transacciones_por_dia)[-5:][::-1]

        print("\nTop 5 días pico:")
        for idx in top5_indices:
            print(f"{dias_unicos[idx]} -> {transacciones_por_dia[idx]} transacciones")

        # 2. Totales diarios del banco
        mask_ingresos = (self.tipo == "DEPOSITO") | (self.tipo == "TRANSFER_IN")
        mask_gastos = (self.tipo == "RETIRO") | (self.tipo == "TRANSFER_OUT")

        total_ingresos_dia = np.bincount(indices, weights=self.monto * mask_ingresos)
        total_gastos_dia = np.bincount(indices, weights=self.monto * mask_gastos)

        print("\nTotales diarios del banco:")
        for i, d in enumerate(dias_unicos):
            neto = total_ingresos_dia[i] - total_gastos_dia[i]
            print(f"{d} | Ingresos: {total_ingresos_dia[i]} | Gastos: {total_gastos_dia[i]} | Neto: {neto}")

        # 3. Top cuentas por depósitos
        cuentas_unicas = np.unique(self.id_cuenta)
        totales_dep = []

        for cuenta in cuentas_unicas:
            mask_cuenta = (self.id_cuenta == cuenta)
            total_dep = self.monto[mask_cuenta & mask_ingresos].sum()
            totales_dep.append((cuenta, total_dep))

        totales_dep.sort(key=lambda x: x[1], reverse=True)

        print("\nTop cuentas por depósitos:")
        for cuenta, total in totales_dep[:10]:
            print(f"Cuenta {cuenta}: {total}")

        # 4. Top cuentas por gastos
        totales_gastos = []

        for cuenta in cuentas_unicas:
            mask_cuenta = (self.id_cuenta == cuenta)
            total_g = self.monto[mask_cuenta & mask_gastos].sum()
            totales_gastos.append((cuenta, total_g))

        totales_gastos.sort(key=lambda x: x[1], reverse=True)

        print("\nTop cuentas por gastos:")
        for cuenta, total in totales_gastos[:10]:
            print(f"Cuenta {cuenta}: {total}")