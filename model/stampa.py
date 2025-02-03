import pdfkit


class print_file:
    def __init__(self, cf, target, name_file):
        """ Inizializza un istanza della classe printF"""
        self._cf = cf
        self._target = target
        self._nameFile = name_file

    def create_table_row(self, valori):
        """ crea una riga di tabella in formato HTML """
        return f'<tr align="center"><td>{"</td><td>".join(map(str, valori))}</td></tr>'

    def add_text(self, testo):
        """ aggiunge un paragrafo in formato HTML """
        return f'<p>{testo}</p>'

    def generazione_pdf(self, listP, qty, revenue, mixx, qbep, rbep, mds, ro, var):
        """  Genera un report in formato HTML e PDF basato sull'analisi cvp"""

        # Inizializzazione del contenuti HTNL per la sezione di intestazione
        l1 = f'<h5>(FIX COST= ${self._cf},  TARGET= ${self._target},  QUANTITY= specified in the "QTY" column of the table)<br><br></h5>'

        # Controllo se l'obiettivo di profitto è zero
        if self._target == 0:
            l1 += self.add_text(f'the SALES is ${sum(revenue):1.2f} <br> the OPERATING INCOME is ${ro:1.2f} <br>')

            # Se il reddito operativo è positivo, aggiungi il margine di sicurezza
            if ro > 0:
                l1 += self.add_text(f'the MARGIN OF SAFETY is {mds:1.2f} in sales')

            # Indica il punto di pareggio
            l1 += self.add_text(f'SALES ${rbep:1.2f} are required to BREAK EVEN<br>The SALES of EACH TOYS must be:')
        else:
            # Indica il profitto desiderato
            l1 += self.add_text(f'SALES $ {rbep:1.2f} are required to make a PROFIT of ${self._target}<br>The SALES of EACH TOYS must be:')

        # Creazione della tabella dei proditti
        l2 = ''.join([self.create_table_row([listP[i], f"{qty[i]} unit", f"${revenue[i]:1.2f}", f"${mixx[i]:1.2f}"]) for i in range(len(listP))])

        # Inizializzazione della sezione per le variazioni
        l3 = ''
        if len(var.keys()) > 0:
            l3 += self.add_text(f'<span class="large-text"> The following analysis examines the variation in operating income <br>resulting from specific modifications to variables such as units sold, price and fixed costs</span>')

            # Creazione della tabella delle variazioni
            l3 += f'''<table class="table table-striped">
                        <thead>
                            <th>VarQty</th><th>VarPrice</th><th>VarCF</th><th>VarRO</th> 
                        </thead>
                        <tbody> 
                    '''
            l3 += ''.join([self.create_table_row([f"{int(t[0])}%", f"{int(t[1])}%", t[2], f"${i:1.2f}"]) for t, i in var.items()])
            l3 += f'</tbody></table>'

        # Scrittura del file HTML
        with open("result.html", 'w') as f:
            f.write(f'''
                    <html>
                    <head>
                        <title> RESULT SIMULATION </title>
                        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css" integrity="sha384-xOolHFLEh07PJGoPkLv1IbcEPTNtaed2xpHsD9ESMhqIYd0nLMwNLD69Npy4HI+N" crossorigin="anonymous">
                        <style>
                            body{{text-align:center;}}
                            .container2{{margin-top:100px; page-break-before: always; }}
                            .table{{width:80%, margin:auto;}}
                            .large-text {{font-size:14pt;}} 
                    
                        </style>
                    </head>
                    <body>
                        <h1> CVP ANALYSIS RESULT </h1>
                        {l1}
                        <table class="table table-striped">
                        <thead>
                            <th>PRODUCT</th>
                            <th>QTY</th>
                            <th>REVENUE</th>
                            <th>IDEAL REVENUE</th>
                        </thead>

                        <tbody>
                        {l2}
                        </tbody>
                        </table>
                        </div>
                        <div class="container2">
                        {l3}
                        </div>

                    </body>
                    </html>
                    ''')

        # Opzioni per la generazione del PDF
        options = {
            'page-size': "Letter",
            'margin-top': '0.70in',
            'margin-left': '0.70in',
            'margin-bottom': '0.70in',
            'margin-right': '0.70in',
            'encoding': 'UTF-8',
            'no-outline': None
        }

        # Generazione del PDF dal file HTML
        pdfkit.from_file("result.html", f'{self._nameFile}.pdf', options=options)

# NB. nel caso internet non è accesso la pagina non può richiamare il link di stile delle tabelle.
