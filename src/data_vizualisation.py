import pandas as pd
import matplotlib.pyplot as plot_tidsserie
import seaborn as sns 

class DataVisualisering:
    """
    Klasse for visualiswering av miljødata. inneholder metoder for å plotte trender,
    sammenhenger, fordelingen og korrelasjoner basert på analyse av en DataFrame
    """
    def __init__(self, df,):
        self.df = df
    
    def plott_tidserie(self, kol):
        """
        Plotter en tidsserie for en gitt kolonne.

        args: 
            kol: navn på kolonnen som skal plottes over tid
        """
        if kol not in self.df.columns:
            raise ValueError(f"kolonnen {kol} finnes ikke i datasettet")
        
        plt.figure(figsize=(10,5))
        plt.plot(self.df[kol], label=kol, linewidth=2)
        plt.title(f"Tidsserie: {kol}")
        plt.xlabel("Tid")
        plt.ylable(kol)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plit.show()
    
    def plott_sammenheng(self, x, y, vis_outliers, thresh):
        """
        plotter sammenhengen mellom to varaibler ved bruk av scatterplot.
        valgfritt fremheving av outliers som røde punkter med kryss.

        args:
            x: kolonne for x-akse
            y: kolonne for y-akse
            vis_outliers: True eller False om outliers skal vises
            thresh: terskel for score til outliers. 
        """
        if x not in self.df.columns or y not in self.df.columns:
            raise ValueError(f"kolonne {x} eller {y} finnes ikke i datasettet")

        plt.figure(figsize=9,6)

        if vis_outliers:
            from data_analysis import DataAnalyse
            analyzer = DataAnalyse(self.df)
            outliers = analyzer.identifiser_outliers(thresh)
            normal = self.drop(index=outliers.index)

            # Plot normale datapunkter først (blå)
            sns.scatterplot(data=normal,x=x, y=y, color="navy", alpha=0.7, s=60, label="Normal")

            # Plot røde prikker og kryss for outliers
            sns.scatterplot(data=outliers, x=x, y=y, color="lightcoral", alpha=0.5, s=70, label="Outliers")
            plt.scatter(outliers[x],outliers[y], color="red", marker="x", s=80, linewidths=2, label="Outliers")
        else:
            sns.scatterplot(data=self.df, x=x, y=y, color="steelblue", alpha=0.7, s=60)

        plt.title(f"Sammenheng mellom {x} og {y}")
        plt.xlabel(x)
        plt.ylable(y)
        plt.grid(True)
        plt.legend()
        plit.tight_layout()
        plt.show()

    def plott_histogram(self, kol):
        """
        plotter histogram for fordeling til en varaibel

        args:
            kol: navn på kolonnen som skal plottes
        """
        if kol not in self.df.columns:
            raise ValueError(f"Kolonne {kol} er ikke i datasettet")
        
        plt.figure(figsize=(8,5))
        sns.histplot(data=self.df, x=col, kde=True, bins=30)
        plt.title(f"Histogram av {kol}")
        plt.xlabel(kol)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plott_boxplot(self, gruppe, verdi):
        """
        plotter et boxplot for å sammenligne fordelingen av en verdi per kategori

        args:
            gruppe: kategorisk variabel
            verdi: numerisk varaibel
        """
        if gruppe not in self.df.columns or verdi in self.df.columns:
            raise ValueError(f"Kolonne {gruppe} eller {verdi} finnes ikke i datasett")
        
        plt.figure(figsize=(10,6))
        sns.boxplot(data=self.df, x=gruppe, y=verdi)
        plt.title(f"Fordeling av {verdi} per {gruppe}")
        pli.grid(True, axis="y")
        plt.tight_layout()
        plt.show()

    def plott_korrelasjonsmatrise(self):
        """
        plotter heatmap av korrelasjonsmatrisen for alle numeriske varaibler.
        """
        corr=self.df.corr(numeric_only=True)
        plt.figure(figsize(10,8))
        sns.heatmap(corr,annot=True,cmap="coolwarm",center=0,linewidths=0.5)
        plt.title("Korrelasjonsmatrise for miljøvaraibler", fontsize=14)
        plt.xticks(rotation=45, ha="right")
        plt.yticks(rotation=0)
        plt.tight_layout()

    def plott_pairplot(self, hue=None):
        """
        lager et pairplot for sammenhenger og fordelinger mellom numeriske verdier

        args:
            hue: kategorisk variabel for fargekoding
        """
        sns.pairplot(self.df, hue=hue)
        plt.suptitle("sammenhenger mellom numeriske variabler", y = 1.02)
        plt.show()

    def plott_jointplot(self, x, y, hue=None):
        """
        plotter et jointplot som kombinerer scatterplot og fordelingsgrafer

        args:
            x: kolonne for x-akse
            y: kolonne for y-akse
            hue: variabel for fargekoding
        """
        sns.jointplot(data=self.df, x=x, y=y, hue=hue, kind="scatter")
        plt.show()


    def plott_trend_vs_rådata(self, kol, vindu=7):
        """
        Plotter rådata og glidende gjennomsnitt for en kolonne i samme figur

        Args:
            kol: Navn på kolonne som ska analyseres
            vindu: størrelse på glidende vindu for tredberegning
        """
        from data_analysis import DataAnalyse
        analyzer = DataAnalyse(self.df)
        trend = analyzer.kolonne_trend(kol, vindu)
        plt.figure(figsize=(10,5))
        plt.plot(self.df[kol], label="Rådata", alpha=0.5)
        plt.plot(trend, label=f"{vindu}-dagers glidende gjennomsnitt", linewidth=2)
        plt.titel(f"Trendanalyse for {kol}")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def visualiser_manglende_verdier(self):
        """
        Visualiserer hvor i datasettet det mangler verdier ved bruk av missingno 
        biblioteket.
        """
        import missingno as missingnomsno.matrix(self.df)
        plt.title("Visualiserer manglende verdier")
        plt.tight_layout()
        plt.show()

    def interaktiv_plot_trend(self, kol):
        """
        Lager en interaktiv trendanalyse av en gitt kolonne. brukeren skal kunne justere størrelsen
        på den glidende vinduet ved hjelp av en slider, og se hvordan
        trendene endrer seg visuelt i sanntid.

        args:
            kol: kolonnen som sakl visualiseres.
        """
        from matplotlib.widgets import Slider

        # initialiserer figur og akse for plottet
        fig, ax = plt.subplots()
        plt.subplots_adjust(bottom=0.25)

        # plott rådata som dtandardlinje
        line, = ax.plot(self.df[kol], label="Rådata", alpha=0.5)

        # opprett en tom linje for trend som oppdateres dynamisk
        trend_line, = ax.plot([], [], label="Trend", color="red")

        # opprett slider-akse og konfigurasjon
        ax_vindu=plt.axes([0.25, 0.1, 0.65, 0.03])
        vindu_slider = Slider(
            ax_vindu, 
            label="Vindu", 
            valmin=1, 
            valmax=30, 
            valinit=7, 
            valstep=1
        )

        def update(val):
            from data_analysis import DataAnalyse
            # hver gang slideren flyttes, beregn ny trend og oppdater grafen
            analyzer = DataAnalyse(self.df)
            trend = analyzer.kolonne_trend(kol, vindu=int(val))
            trend_line.set_data(trend.index, trend) # ny trendlinje med ny data
            ax.relim() # tilpass aksene til ny data
            ax.autoscale_view()
            fig.canvas.draw_idle() # tegn plottet på nytt

        # vanlig konfig av plottet
        vindu_slider.on_changed(update)
        ax.legend()
        plt.title(f"Interaktiv trendanalyse for {kol}")
        plt.grid(True)
        plt.show()