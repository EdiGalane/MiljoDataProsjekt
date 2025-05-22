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
    
    def plott_sammenheng(self, x, y):
        """
        plotter sammenhengen mellom to varaibler

        args:
            x: kolonne for x-akse
            y: kolonne for y-akse
        """
        plt.figure(figsize=8,6)
        sns.scatterplot(data=self.df, x=x, y=y)
        plt.title(f"Sammenheng mellom {x} og {y}")
        plt.grid(True)
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