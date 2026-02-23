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

        for cuenta in cuentas:  # solo impresión final

            mask_cuenta = (self.id_cuenta == cuenta)

            ingresos = self.monto[mask_cuenta & mask_ingresos]
            gastos = self.monto[mask_cuenta & mask_gastos]

            total_depositos = ingresos.sum()
            total_gastos = gastos.sum()

            dias_cuenta = self.dias[mask_cuenta & mask_ingresos]

            if ingresos.size > 0:

                dias_unicos, indices = np.unique(dias_cuenta, return_inverse=True)
                totales_diarios = np.bincount(indices, weights=ingresos)

                promedio = totales_diarios.mean()
                std = totales_diarios.std()

                p50 = np.percentile(totales_diarios, 50)
                p90 = np.percentile(totales_diarios, 90)
                p99 = np.percentile(totales_diarios, 99)

            else:
                promedio = std = p50 = p90 = p99 = 0

            ratio = total_depositos / total_gastos if total_gastos != 0 else 0

            print(f"\nCuenta {cuenta}")
            print(f"Total depósitos: {total_depositos}")
            print(f"Total gastos: {total_gastos}")
            print(f"Ratio depósitos/gastos: {ratio}")
            print(f"Promedio diario: {promedio}")
            print(f"Desviación estándar diaria: {std}")
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

        dias_unicos, indices = np.unique(self.dias, return_inverse=True)
        transacciones_por_dia = np.bincount(indices)

        print("\nTransacciones por día:")
        for d, total in zip(dias_unicos, transacciones_por_dia):
            print(f"{d}: {total}")

        top5 = np.argsort(transacciones_por_dia)[-5:][::-1]

        print("\nTop 5 días pico:")
        for idx in top5:
            print(f"{dias_unicos[idx]} -> {transacciones_por_dia[idx]} transacciones")

        mask_ingresos = (self.tipo == "DEPOSITO") | (self.tipo == "TRANSFER_IN")
        mask_gastos = (self.tipo == "RETIRO") | (self.tipo == "TRANSFER_OUT")

        ingresos_dia = np.bincount(indices, weights=self.monto * mask_ingresos)
        gastos_dia = np.bincount(indices, weights=self.monto * mask_gastos)

        print("\nTotales diarios del banco:")
        for i, d in enumerate(dias_unicos):
            neto = ingresos_dia[i] - gastos_dia[i]
            print(f"{d} | Ingresos: {ingresos_dia[i]} | Gastos: {gastos_dia[i]} | Neto: {neto}")

    # -------------------------------------------------
    # 2.3 ANOMALÍAS
    # -------------------------------------------------
    def detectar_anomalias(self):

        if self.transacciones.size == 0:
            print("No hay transacciones para analizar.")
            return

        print("\n=== ANOMALÍAS DETECTADAS ===")

        mask_ingresos = (self.tipo == "DEPOSITO") | (self.tipo == "TRANSFER_IN")
        cuentas = np.unique(self.id_cuenta)

        # 1️⃣ Z-SCORE
        print("\n-- Z-Score sobre depósitos diarios (|z| > 3) --")

        for cuenta in cuentas:

            mask_cuenta = (self.id_cuenta == cuenta)

            dias_cuenta = self.dias[mask_cuenta & mask_ingresos]
            montos_cuenta = self.monto[mask_cuenta & mask_ingresos]

            if montos_cuenta.size < 2:
                continue

            dias_unicos, indices = np.unique(dias_cuenta, return_inverse=True)
            totales = np.bincount(indices, weights=montos_cuenta)

            media = totales.mean()
            std = totales.std()

            if std == 0:
                continue

            z = (totales - media) / std
            anomalos = np.where(np.abs(z) > 3)[0]

            for idx in anomalos:
                print(f"Cuenta {cuenta} - Día {dias_unicos[idx]} - Z={z[idx]:.2f}")

        # 2️⃣ STRUCTURING
        print("\n-- Structuring (≥4 depósitos ≤ 50 en un día) --")

        mask_depositos = (self.tipo == "DEPOSITO")

        for cuenta in cuentas:

            mask_cuenta = (self.id_cuenta == cuenta) & mask_depositos

            dias_cuenta = self.dias[mask_cuenta]
            montos_cuenta = self.monto[mask_cuenta]

            if montos_cuenta.size == 0:
                continue

            dias_unicos, indices = np.unique(dias_cuenta, return_inverse=True)

            for i, dia in enumerate(dias_unicos):
                montos_dia = montos_cuenta[indices == i]

                if montos_dia.size >= 4 and np.all(montos_dia <= 50):
                    print(f"Cuenta {cuenta} - Día {dia} - Structuring detectado")

        # 3️⃣ ACTIVIDAD NOCTURNA
        print("\n-- Actividad nocturna inusual (21:00 - 04:00) --")

        horas = self.fechas.astype('datetime64[h]').astype(int) % 24
        mask_nocturno = (horas >= 21) | (horas < 4)

        for cuenta in cuentas:

            mask_cuenta = (self.id_cuenta == cuenta)

            total_trans = mask_cuenta.sum()
            total_nocturnas = (mask_cuenta & mask_nocturno).sum()

            if total_trans == 0:
                continue

            ratio = total_nocturnas / total_trans

            if ratio > 0.6 and total_nocturnas >= 3:
                print(f"Cuenta {cuenta} - Alta actividad nocturna ({total_nocturnas} transacciones)")
           # -------------------------------------------------
    # 2.4 VISUALIZACIÓN 1 - SERIE TEMPORAL NETO DIARIO
    # -------------------------------------------------
    def plot_serie_temporal_neto(self):

        if self.transacciones.size == 0:
            print("No hay transacciones para graficar.")
            return

        import matplotlib.pyplot as plt

        os.makedirs("outputs/plots", exist_ok=True)

        mask_ingresos = (self.tipo == "DEPOSITO") | (self.tipo == "TRANSFER_IN")
        mask_gastos = (self.tipo == "RETIRO") | (self.tipo == "TRANSFER_OUT")

        dias_unicos, indices = np.unique(self.dias, return_inverse=True)

        ingresos_dia = np.bincount(indices, weights=self.monto * mask_ingresos)
        gastos_dia = np.bincount(indices, weights=self.monto * mask_gastos)

        neto_dia = ingresos_dia - gastos_dia

        plt.figure()
        plt.plot(dias_unicos.astype(str), neto_dia)
        plt.title("Serie Temporal - Neto Diario del Banco")
        plt.xlabel("Fecha")
        plt.ylabel("Monto Neto")
        plt.xticks(rotation=45)
        plt.tight_layout()

        ruta = "outputs/plots/serie_temporal_neto.png"
        plt.savefig(ruta)
        plt.close()

        print(f"Gráfico guardado en: {ruta}")

    # -------------------------------------------------
    # 2.4 VISUALIZACIÓN 2 - HEATMAP ACTIVIDAD
    # -------------------------------------------------
    def plot_heatmap_actividad(self):

        if self.transacciones.size == 0:
            print("No hay transacciones para graficar.")
            return

        import matplotlib.pyplot as plt
        import seaborn as sns

        os.makedirs("outputs/plots", exist_ok=True)

        cuentas = np.unique(self.id_cuenta)
        dias_unicos = np.unique(self.dias)

        matriz = np.zeros((cuentas.size, dias_unicos.size))

        for i, cuenta in enumerate(cuentas):
            for j, dia in enumerate(dias_unicos):
                mask = (self.id_cuenta == cuenta) & (self.dias == dia)
                matriz[i, j] = mask.sum()

        plt.figure()
        sns.heatmap(
            matriz,
            xticklabels=dias_unicos.astype(str),
            yticklabels=cuentas,
            annot=True
        )

        plt.title("Heatmap de Actividad por Cuenta y Día")
        plt.xlabel("Día")
        plt.ylabel("Cuenta")
        plt.xticks(rotation=45)
        plt.tight_layout()

        ruta = "outputs/plots/heatmap_actividad.png"
        plt.savefig(ruta)
        plt.close()

        print(f"Gráfico guardado en: {ruta}")