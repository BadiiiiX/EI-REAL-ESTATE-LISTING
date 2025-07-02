from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CenterPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(side="left", fill="both", expand=True)

        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)


    def clear_graph(self, title):
        self.ax.clear()
        self.ax.set_title(f"Aucune prédiction pour : {title}")
        self.ax.set_xlabel("Date")
        self.ax.set_ylabel("Prix (€)")
        self.ax.grid(True)
        self.fig.tight_layout()
        self.canvas.draw()

    def update_graph(self, df_real, df_interp, ad_price, ad_date, predictions, title, force_xlim=None):
        self.ax.clear()

        colors = {
            "Naive": "orange",
            "Mean": "green",
            "Seasonal": "purple",
            "Rolling": "crimson"
        }

        self.ax.scatter(
            df_real.index, df_real["price"],
            label="Ventes", color="black", marker='o', s=30
        )
        for date, price in zip(df_real.index, df_real["price"]):
            try:
                p = float(str(price).replace('€', '').replace(',', '').strip())
                self.ax.text(date, p, f"{p:.0f}€", fontsize=8, color="black", ha='center', va='bottom')
            except:
                continue

        # 2. Ligne interpolée
        self.ax.plot(
            df_interp.index, df_interp["price"],
            label="Historique (interpolé)", linestyle='-', color='blue', alpha=0.3
        )

        # 3. Prédictions (courbes + point final + texte)
        for label in predictions.columns:
            y_vals = predictions[label].astype(float)

            self.ax.plot(
                predictions.index, y_vals,
                label=label, linestyle='--', color=colors.get(label, "gray")
            )

            self.ax.scatter(
                predictions.index[-1], y_vals.iloc[-1],
                color=colors.get(label, "gray"), marker='s', s=50
            )

            self.ax.text(
                predictions.index[-1], y_vals.iloc[-1],
                f"{float(y_vals.iloc[-1]):.0f}€",
                fontsize=8, color=colors.get(label, "gray"),
                ha='left', va='bottom'
            )

        # 4. Prix de l’annonce
        try:
            ad_val = float(str(ad_price).replace('€', '').replace(',', '').strip())
        except:
            ad_val = ad_price

        self.ax.scatter(
            ad_date, ad_val,
            label="Annonce", color="red", marker='x', s=100
        )
        self.ax.text(
            ad_date, ad_val,
            f"{float(ad_val):.0f}€",
            fontsize=9, color="red",
            ha='center', va='top'
        )

        self.ax.set_title(f"Prix et prédictions : {title}")
        self.ax.set_xlabel("Date")
        self.ax.set_ylabel("Prix (€)")
        self.ax.legend()
        self.ax.grid(True)

        if force_xlim:
            self.ax.set_xlim(df_real.index.min(), force_xlim)

        self.fig.tight_layout()
        self.canvas.draw()
