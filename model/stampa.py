import pdfkit # installare


def printF( cf, target, listP, qty, revenue, mixx, qbep, rbep, mds, ro, nameFile):
    p = listP
    r=revenue
    mixIdeale = mixx
    q = qty
    l1 = ''
    l2 = ''

    l1 += f'<h7> (the fix cost=$ {cf}, the target=$ {target} and the quantity is specified in the table) </h7>'
    if target == 0:
        l1 += f'<dl><dt>the SALES is $ {sum(r):1.2f}</dt>'
        l1 += f'<dl><dt>the OPERATING INCOME is {ro:1.2f} in sales </dt>'
        if ro>0:
            l1 += f'<dt> the MARGIN OF SAFETY is {mds:1.2f} in sales </dt>'
            l1 += f'<dt> -------------------------------------------------'

        l1 += f'<dt> SALES $ {rbep:1.2f} are required to BREAK EVEN </dt>'

    else:
        l1 += f'<dt> SALES $ {rbep:1.2f} are required to make a PROFIT of $ {target} </dt>'
    l1 += f'<dt>The SALES of EACH TOYS must be:</dt></dl>'

    for i in range(len(p)):
        l2 += f'<tr align="center"><td>{p[i]}</td>&nbsp<td>{q[i]} unit </td>&nbsp<td>$ {r[i]:1.2f}</td>&nbsp<td>$ {mixIdeale[i]:1.2f}</td></tr>'

    with open("result.html", 'w') as f:
        f.write(f'''
            <html>
            <head>
                <title><center> RESULT SIMULATION </center></title>
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css" integrity="sha384-xOolHFLEh07PJGoPkLv1IbcEPTNtaed2xpHsD9ESMhqIYd0nLMwNLD69Npy4HI+N" crossorigin="anonymous">
            </head>
            <body>
                <div class="container" style="text-align:center; ">
                <h1> CVP ANALYSIS RESULT </h1>
                {l1}

                <table class="table table-striped" align="center">
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
            </body>
            </html>
            ''')

    options = {
        'page-size': "Letter",
        'margin-top': '0.70in',
        'margin-left': '0.70in',
        'margin-bottom': '0.70in',
        'margin-right': '0.70in',
        'encoding': 'UTF-8',
        'no-outline': None
    }

    pdfkit.from_file("result.html", f'{nameFile}.pdf', options=options)


# nel caso internet non è accesso la pagina non può richiamare un link e apparira un msg di errore e la stampa non avrà il formato indicato nel link

