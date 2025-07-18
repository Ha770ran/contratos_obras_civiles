# AUTOMATIZACIÒN CONTRATO DE OBRA CIVIL
#importar necesarias para el programa
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer
import pandas as pd
import os



#Datos SQL
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contractsoc.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#Datos declarados SQL
class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contract_number = db.Column(db.String(20), nullable=False)
    contract_date = db.Column(db.String(10), nullable=False)
    employer_name = db.Column(db.String(100), nullable=False)
    employer_nit = db.Column(db.String(20), nullable=False)
    legal_representative = db.Column(db.String(100), nullable=False)
    legal_representative_id = db.Column(db.String(20), nullable=False)
    employer_address = db.Column(db.String(200), nullable=False)
    contractor_name = db.Column(db.String(100), nullable=False)
    contractor_id = db.Column(db.String(20), nullable=False)
    legal_representative_contractor = db.Column(db.String(100), nullable=False)
    legal_representative_contractor_id = db.Column(db.String(20), nullable=False)
    contractor_address = db.Column(db.String(200), nullable=False)
    contractor_phone = db.Column(db.String(20), nullable=False)
    contractor_email = db.Column(db.String(100), nullable=False)
    contract_object = db.Column(db.String(200), nullable=False)
    project_name = db.Column(db.String(100), nullable=False)
    project_city = db.Column(db.String(100), nullable=False)
    value = db.Column(db.String(20), nullable=False)
    payment_frequency = db.Column(db.String(20), nullable=False)
    contract_time = db.Column(db.String(100), nullable=False)
    warranties_cum = db.Column(db.String(300), nullable=False)
    warranties_ant= db.Column(db.String(300), nullable=False)
    warranties_amp_sal = db.Column(db.String(300), nullable=False)
    warranties_rce = db.Column(db.String(300), nullable=False)
    warranties_cal = db.Column(db.String(300), nullable=False)
    warranties_other = db.Column(db.String(300), nullable=False)
    advance_value = db.Column(db.String(20), nullable=False)
    offer = db.Column(db.String(100), nullable=False)
    special_observations = db.Column(db.String(100), nullable=False)

#from app import app, db  # Asegúrate de importar tu aplicación y la instancia de SQLAlchemy#(no tener en cuenta)
with app.app_context():
    db.create_all()

#Ingreso tabla excel de contratos

EXCEL_FILE = "contracts.xlsx"

def update_excel():
    # Obtener todos los contratos desde la base de datos
    with app.app_context():
        contracts = Contract.query.all()

    # Crear lista de datos para el DataFrame
    data = [
        {
            "Número de Contrato:": contract.contract_number,
            "Fecha del Contrato:": contract.contract_date, 
            "Nombre del Contratante:": contract.employer_name,
            "Contratante NIT:": contract.employer_nit,
            "Nombre Rep. Legal Contratante:": contract.legal_representative, 
            "Rep. Legal Contratante No. C.C.:": contract.legal_representative_id,
            "Dirección del Contratante:": contract.employer_address,
            "Nombre del Contratista:": contract.contractor_name, 
            "NIT del Contratista:": contract.contractor_id, 
            "Rep. Legal del Contratista:": contract.legal_representative_contractor, 
            "Rep. Legal Contratista No. C.C.:":contract.legal_representative_contractor_id,
            "Dirección del Contratista:": contract.contractor_address,
            "Teléfono del Contratista:": contract.contractor_phone,
            "Email del Contratista:": contract.contractor_email, 
            "Objeto del Contrato:": contract.contract_object,
            "Nombre del Proyecto:": contract.project_name,
            "Ciudad del Proyecto:": contract.project_city, 
            "Valor del Contrato:": contract.value, 
            "Frecuencia de Pago:": contract.payment_frequency,
            "Duración del Contrato:": contract.contract_time, 
            "Poliza Cumplimiento:": contract.warranties_cum, 
            "Poliza Anticipo:": contract.warranties_ant, 
            "Amparo, salario y prestaciones soc.:": contract.warranties_amp_sal, 
            "Poliza RCE:": contract.warranties_rce,
            "Poliza calidad y correcto fun.:": contract.warranties_cal, 
            "Otra Poliza:": contract.warranties_other, 
            "Valor del Anticipo:": contract.advance_value, 
            "Oferta:": contract.offer, 
            "Observaciones Especiales:": contract.special_observations, 
        }
        for contract in contracts
    ]

    # Crear un DataFrame con los datos
    df = pd.DataFrame(data)

    # Guardar en un archivo Excel
    df.to_excel(EXCEL_FILE, index=False, engine='openpyxl')

    print(f"📂 Archivo Excel actualizado: {EXCEL_FILE}")
 
 # FINALIZA TABLA EXCEL ACTUALIZADA.

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create():
    new_contract = Contract(
        contract_number=request.form['contract_number'],
        contract_date=request.form['contract_date'],
        employer_name=request.form['employer_name'],
        employer_nit=request.form['employer_nit'],
        legal_representative=request.form['legal_representative'],
        legal_representative_id=request.form['legal_representative_id'],
        employer_address=request.form['employer_address'],
        contractor_name=request.form['contractor_name'],
        contractor_id=request.form['contractor_id'],
        legal_representative_contractor=request.form['legal_representative_contractor'],
        legal_representative_contractor_id=request.form['legal_representative_contractor_id'],
        contractor_address=request.form['contractor_address'],
        contractor_phone=request.form['contractor_phone'],
        contractor_email=request.form['contractor_email'],
        contract_object=request.form['contract_object'],
        project_name=request.form['project_name'],
        project_city=request.form['project_city'],
        value=request.form['value'],
        payment_frequency=request.form['payment_frequency'],
        contract_time=request.form['contract_time'],
        warranties_cum=request.form['warranties_cum'],
        warranties_ant=request.form['warranties_ant'],
        warranties_amp_sal=request.form['warranties_amp_sal'],
        warranties_rce=request.form['warranties_rce'],
        warranties_cal=request.form['warranties_cal'],
        warranties_other=request.form['warranties_other'],
        advance_value=request.form['advance_value'],
        offer=request.form['offer'],
        special_observations=request.form['special_observations']
    )
    db.session.add(new_contract)
    db.session.commit()

    #Genera PDF
    generate_pdf(new_contract)

    #Actualizar el cuadro excel:
    update_excel()

    return redirect(url_for('index'))

    # Aquí es donde defines los elementos del documento.
    elements = []

#generar el contrato:
def generate_pdf(contract):
    pdf_filename = f"{contract.contract_number}.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)

    page_number = 1

     # Título centrado
    title = "CONTRATO OBRA CIVIL"
    c.setFont("Helvetica-Bold", 16)
    title_y = 720 # Ajuste la coordenada Y para acercar el título
    c.drawCentredString(letter[0] / 2.0, title_y, title.upper())

    # Ajuste de espacio entre el título y el cuadro de variables
    space_between_title_and_table = 8  
    table_start_y = title_y - space_between_title_and_table - 20

    # Crear el estilo para los párrafos
    styles = getSampleStyleSheet()
    cell_style = styles['BodyText']  # Estilo de cuerpo de texto

    # Datos organizados en un array bidimensional
    data = [
        ["Número de Contrato:", Paragraph(contract.contract_number,cell_style)],
        ["Fecha del Contrato:", Paragraph(contract.contract_date, cell_style)],
        ["Nombre del Contratante:", Paragraph(contract.employer_name, cell_style)],
        ["Contratante NIT:", Paragraph(contract.employer_nit, cell_style)],
        ["Nombre Rep. Legal Contratante:", Paragraph(contract.legal_representative, cell_style)],
        ["Rep. Legal Contratante No. C.C.:", Paragraph(contract.legal_representative_id, cell_style)],
        ["Dirección del Contratante:", Paragraph(contract.employer_address, cell_style)],
        ["Nombre del Contratista:", Paragraph(contract.contractor_name, cell_style)],
        ["NIT del Contratista:", Paragraph(contract.contractor_id, cell_style)],
        ["Rep. Legal del Contratista:", Paragraph(contract.legal_representative_contractor, cell_style)],
        ["Rep. Legal Contratista No. C.C.:", Paragraph(contract.legal_representative_contractor_id, cell_style)],
        ["Dirección del Contratista:", Paragraph(contract.contractor_address, cell_style)],
        ["Teléfono del Contratista:", Paragraph(contract.contractor_phone, cell_style)],
        ["Email del Contratista:", Paragraph(contract.contractor_email, cell_style)],
        ["Objeto del Contrato:", Paragraph(contract.contract_object, cell_style)],
        ["Nombre del Proyecto:", Paragraph(contract.project_name, cell_style)],
        ["Ciudad del Proyecto:", Paragraph(contract.project_city, cell_style)],
        ["Valor del Contrato:", Paragraph(contract.value, cell_style)],
        ["Frecuencia de Pago:", Paragraph(contract.payment_frequency, cell_style)],
        ["Duración del Contrato:", Paragraph(contract.contract_time, cell_style)],
        ["Poliza Cumplimiento:", Paragraph(contract.warranties_cum, cell_style)],
        ["Poliza Anticipo:", Paragraph(contract.warranties_ant, cell_style)],
        ["Amparo, salario y prestaciones soc.:", Paragraph(contract.warranties_amp_sal, cell_style)],
        ["Poliza RCE:", Paragraph(contract.warranties_rce, cell_style)],
        ["Poliza calidad y correcto fun.:", Paragraph(contract.warranties_cal, cell_style)],
        ["Otra Poliza:", Paragraph(contract.warranties_other, cell_style)],
        ["Valor del Anticipo:", Paragraph(contract.advance_value, cell_style)],
        ["Oferta:", Paragraph(contract.offer, cell_style)],
        ["Observaciones Especiales:", Paragraph(contract.special_observations, cell_style)],
    
    ]

    # Crear tabla
    table = Table(data, colWidths=[2.5 * inch, 3 * inch])

    # Estilo de la tabla
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.skyblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.floralwhite),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    table.setStyle(style)
    

    # Calcular el ancho y alto de la tabla
    table_width, table_height = table.wrap(0, 0)

    # Calcular las coordenadas x, y para centrar la tabla en la página
    x_position = (letter[0] - table_width) / 2
    y_position = table_start_y - table_height

    # Dibujar la tabla en el PDF centrada
    table.wrapOn(c, letter[0], letter[1])
    table.drawOn(c, x_position, y_position)

    # Añadir espacio entre la tabla y el texto
    additional_spacing = 40  # Espacio adicional (equivalente a 2 líneas)
    paragraph_y_position = y_position - additional_spacing

    new_y_position = y_position - 20  # Ajusta el espaciado según sea necesario

    # Crear el estilo para el párrafo
    styles = getSampleStyleSheet()
    paragraph_style = styles['BodyText']
    paragraph_style.alignment = 4  # Justificación completa

    # Texto del párrafo introduccion
    additional_text = (
    "Las partes identificadas en el presente contrato deciden libre y voluntariamente pactar y cumplir "
    "las siguientes clausulas que se regirán por las normas civiles y comerciales colombianas. "

    )

    # Crear el párrafo introduccion
    paragraph = Paragraph(additional_text, paragraph_style)

    # Ajustar la posición del párrafo en el PDF
    paragraph.wrapOn(c, letter[0] - 100, letter[1])
    paragraph.drawOn(c, 50, paragraph_y_position)

    # Insertar el número de página al pie
    c.setFont("Helvetica", 10)
    c.drawString(letter[0] - 100, 30, f"Página {page_number}")

    # Finalizar la primera página
    c.showPage()

    # Incrementar el número de página
    page_number += 1

    # Determinar la forma y presentación para las clausulas de las páginas adicionales que estan en las paginas 1,2,3
    styles = getSampleStyleSheet()
    paragraph_style = styles['BodyText']
    paragraph_style.alignment = 4  # Justificación completa

    additional_text_1 = (
        "<b>PRIMERA. OBJETO DEL CONTRATO</b>: EL CONTRATISTA se obliga para con EL CONTRATANTE a desarrollar " 
        "de forma correcta, utilizando toda su pericia, siendo diligente y entregando su mayor esfuerzo " 
        "para ejecutar la obra civil y demás actividades relacionadas con el objeto contractual para el "
        "proyecto determinado.\n"

        "<b>PARÁGRAFO PRIMERO</b>: Las actividades y costos extras o adicionales serán autorizadas por el "
        "CONTRATANTE y serán cobradas conforme los precios pactados previamente. En caso contrario el "
        "CONTRATISTA no tendrá derecho a facturarlas o reclamarlas.\n"

        "<b>PARÁGRAFO SEGUNDO</b>: El CONTRATISTA suministrará todos los materiales, herramientas y elementos "
        "necesarios para la ejecución de este contrato.\n "

        "<b>SEGUNDA. DURACIÓN DEL CONTRATO</b>: El plazo de ejecución del contrato es el establecido en la información "
        "general del presente documento, dando inicio en la fecha establecida o mediante orden de inicio emitida por "
        "escrito por el contratante al contratista.\n"
        
        "<b>PARÁGRAFO PRIMERO</b>: En este período el CONTRATISTA se obliga a la ejecución completa del objeto del "
        "contrato a entera satisfacción de EL CONTRATANTE, pudiéndose prorrogar por mutuo acuerdo por escrito entre "
        "las partes, detallando el motivo de dicha prorroga.\n" 

        "<b>PARÁGRAFO SEGUNDO</b>: Podrá suspenderse temporalmente la ejecución del contrato por circunstancias de " 
        "fuerza mayor, caso fortuito de acuerdo a lo estipulado por la ley en estas materias, o por acuerdo de las partes; " 
        "el tiempo de suspensión no se computará en el plazo del contrato. Cuando la obra deba suspenderse, se informará "
        "por parte del contratante al contratista por escrito, indicando la fecha de inicio y su terminación. En caso que "
        "se deba reiniciar labores antes de la fecha de terminación de la suspensión, el contratante debe informarle al "
        "contratista por escrito con 2 días hábiles de anticipación. El CONTRATISTA se compromete a mantener vigentes las "
        "pólizas durante el tiempo que dure la suspensión del contrato, de no hacerlo, incurre en incumplimiento grave.\n"

        "<b>PARÁGRAFO TERCERO</b>: Toda modificación en plazo, precio o demás cambios debe ser informada por el CONTRATISTA " 
         "a la compañía de seguros, respondiendo por las vigencias y actualización de las pólizas del contrato, de no hacerlo, "
         "incurre en incumplimiento grave.\n"

        "<b>PARÁGRAFO CUARTO</b>: Lo establecido en el presente contrato regulara las relaciones de las partes, y primirá sobre "
        "cualquier acuerdo, cotización, o demás.\n"

        "<b>TERCERA. VALOR Y FORMA DE PAGO</b>: El valor estimado del contrato corresponde a la suma de informada en la información "
        "general del presente documento, incluido IVA y demás impuestos que se causen para el desarrollo del presente contrato. La " 
        "forma de pago será efectuada de acuerdo con lo establecido en la información general del presente documento, donde se tendrán "  
        "en cuenta las siguientes condiciones que se presenten. 1): En caso que se halle pactado anticipo, el contratante podrá entregar " 
        "el mismo al contratista máximo hasta el valor del porcentaje pactado, previa presentación de las polizas exigidas en el contrato "
        "y visto bueno del contratante. En caso que en el presente contrato no se pacte entrega de anticipo mencionado en el informe " 
        "general del presente documento, no se aplicara este numeral. 2): En caso que se halle pactado pago o desembolsos periódicos, de "
        "forma quincenal o mensual u otro tiempo, el contratante podrá pagar al contratista previo visto bueno de la factura y presentación "  
        "de polizas exigidas en el contrato. En caso que en el presente contrato se presentara anticipo, el contratante amortizara el "
        "anticipo sobre la factura del contratista de forma completa o porcentualmente hasta completar el 100% del anticipo, según decida " 
        "el contratante. En caso que en el presente contrato no se pacte pagos o desembolsos periódicos mencionado en el informe general " 
        "del presente documento, no se aplicará este numeral. 3): En caso que se halle pactado un único pago o desembolso al finalizar la "
        "obra o contraentrega del trabajo realizado, el contratante pagara al contratista al finalizar la obra previo bueno del "
        "contratante y presentación de pólizas exigidas en el contrato. En caso que en el presente contrato se presentará anticipo, el " 
        "contratante amortizará el anticipo sobre la factura del contratista de forma completa hasta completar el 100% del anticipo. " 
        "En caso que en el presente contrato no se pacte único pago o desembolso al finalizar la obra o contraentrega al trabajo " 
        "realizado mencionado en el informe general del presente documento, no se aplicará este numeral.\n"

        "<b>PARÁGRAFO PRIMERO</b>: Para emitir los pagos anteriores, el contratista debe aportar las facturas o cuentas de cobro de dichas "  
        "actividades y valores al área contable de la compañía, de acuerdo con las siguientes condiciones: 1.: Identificar el número de " 
        "contrato en la factura o cuenta de cobro. 2.: Concepto de la actividad realizada. 3.: Fecha de la factura o cuenta de cobro."
        "4.: Cumplir con los artículos 621 del Código de Comercio y los artículos 617, 618 del Estatuto Tributario. 5.: La factura o cuenta " 
        "de cobro debe contar con visto bueno por escrito del contratante. 6.: Al momento de presentar la factura o cuenta de cobro, el "
        "contrato debe estar firmado, con pólizas emitidas de forma correcta, en caso de haberse requerido, y habiendo cumplido las " 
        "exigencias de documentación del contrato. 7.: El contratista debe anexar junto a la factura o cuenta de cobro copia constancia " 
        "de paz y salvo de sus trabajadores respecto al pago de salarios y demás prestaciones sociales, incluyendo, salud, pensión y arl.\n "

        "<b>PARÁGRAFO SEGUNDO</b>: El contratante de acuerdo al contrato y los términos de ley tiene la facultad de rechazar o no aceptar "
        "la factura o cuenta de cobro, cuando se presenten inconsistencias a las condiciones exigidas, sin que ello represente sobre el " 
        "contratista mayores intereses, valores o conflictos.\n"

        "<b>CUARTA. OBLIGACIONES DEL CONTRATISTA</b>: Serán obligaciones especiales a cargo del contratista: 1. Ejecutar el objeto del presente " 
        "contrato de acuerdo con su conocimiento, pericia, diligencia, idoneidad, eficacia, responsabilidad y plazos previamente convenidos. "
        "2. Ejecutar bajo su responsabilidad técnica y administrativa el objeto de este contrato. 3. La entrega de la obra civil " 
        "completamente ejecutada cuando finalice el tiempo pactado. 4. Contratar por su cuenta el personal idóneo que se requiera, en número y condiciones que garanticen la oportuna "

    )

    # Crear el párrafo con estilo
    paragraph = Paragraph(additional_text_1, paragraph_style)
    
    # Colocar el párrafo en el PDF
    paragraph.wrapOn(c, letter[0] - 100, letter[1])
    paragraph.drawOn(c, 50, letter[1] - 730) 

    # Insertar el número de página al pie (pag 1)
    c.setFont("Helvetica", 10)
    c.drawString(letter[0] - 100, 30, f"Página {page_number}")

    #mostrar pagina 1 de texto.
    c.showPage()

    # Incrementar el número de página
    page_number += 1

    # Crear una nueva página para el párrafo adicional 2
 
    additional_text_2 = (
        "y correcta ejecución de los trabajos. 5.: Ejercer personalmente la vigilancia administrativa " 
        "del servicio objeto del contrato, así como del personal empleado o subcontratado para la ejecución de los trabajos objeto del " 
        "presente contrato. 6.: El CONTRATISTA mantendrá indemne al CONTRATANTE de cualquier reclamación que presente un trabajador suyo, y " 
        "autoriza al CONTRATANTE a descontar de los saldos o de sus valores retenidos, cualquier pago que deba hacer en consideración a las " 
        "reclamaciones laborales que hagan sus trabajadores. 7.: Pagar a su costa todos los salarios, prestaciones sociales, aportes al ISS, " 
        "ICBF, SENA, Caja de Compensación Familiar, FIC, indemnizaciones que se causen a favor de los trabajadores a su cargo. 8.: En caso que " 
        "se soliciten, entregar a satisfacción del CONTRATANTE las pólizas exigidas en el contrato, las que deben ser aceptadas por el " 
        "CONTRATANTE previo inicio de la labor. 9.: A responder ante terceros por los daños comprobados que ocasione el personal a su cargo."
        "10.: A cumplir con todas las obligaciones de carácter tributario que se desprenden de la naturaleza del contrato. 11.: A informar " 
        "pronta y oportunamente a EL CONTRATANTE de cualquier hecho o circunstancia anormal que observe, con el fin de evitar perjuicios, para" 
        "lo cual deberá presentar un informe detallado por escrito. 12.: Entregar los manuales de funcionamiento o mantenimiento para el usuario " 
        "de la propiedad, fichas técnicas de los elementos, partes, equipos que hacen parte del desarrollo de la obra civil ejecutada. "
        "13.: Otorgar garantía de calidad, idoneidad y buen funcionamiento de los bienes o productos utilizados en la obra y garantía de " 
        "estabilidad de la misma, si corresponde conforme a la naturaleza del contrato, en los términos indicados y prescritos en el artículo" 
        "2060 del Código Civil. 14.: En caso que se presente, invertir correctamente y/o garantizar el buen manejo del anticipo. 15. A atender " 
        "las reclamaciones que le haga EL CONTRATANTE en un termino mayor de 2 dias habiles respecto al presente contrato 16.: A cumplir con " 
        "todas las obligaciones laborales, y parafiscales de sus propios trabajadores."
        "17.: En cumplir con toda la normatividad colombiana relacionada con la seguridad y salud en el trabajo, y en atender los requerimientos "  
        "y recomendaciones que le brinde el contratante respecto a este tema. 18.: A liquidar el Contrato en el tiempo debido. 19.: Dar " 
        "cumplimiento a todas las normas legales, convencionales y reglamentarias, teniendo en cuenta que sus relaciones laborales se rigen por " 
        "lo dispuesto en el código sustantivo de trabajo y en las demás disposiciones concordantes y complementarias, siendo a cargo exclusivo " 
        "del CONTRATISTA todos los gastos, costos, salarios, prestaciones sociales, indemnización derivados de la contratación de personal " 
        "requerido para el objeto del presente contrato. Para la totalidad del personal idóneo requerido, el CONTRATISTA debe asumir, para todo " 
        "efecto legal la calidad jurídica de patrono o empleador de dicho personal. 20.: Cumplir con todas las obligaciones que se desprenden de " 
        "la naturaleza del presente contrato, así como todas las normas y disposiciones de las leyes o reglamentos vigentes, respecto de la " 
        "ejecución del proyecto. 21.: Garantizar la calidad de la mano de obra contratada, haciéndose responsable de los daños que se presenten, " 
        "en todos aquellos casos en que la causa de los deterioros se determine como consecuencia de mala elaboración de los procesos de " 
        "instalación. 22.: El CONTRATISTA será responsable de su equipo y material que tenga en la obra; el CONTRATISTA debe tener las pólizas " 
        "necesarias para asegurar contra todo riesgo, por lo tanto, el CONTRATANTE no será responsable por las pérdidas o deterioros de los " 
        "equipos y materiales del contratante, salvo dolo o culpa grave del contratante. 23. Actuar siempre en buena fe. 24. Las demás " 
        "obligaciones determinadas por la ley.\n"

        "<b>QUINTA. OBLIGACIONES DEL CONTRATANTE</b>: Son obligaciones especiales del CONTRATANTE:"
        " a): Suministrar a tiempo toda la información que EL CONTRATISTA requiera para el normal desarrollo de su trabajo. b): Definir y resolver todos "  
        "los problemas que se presenten dentro de la obra en relación al objeto del contrato. c): Cumplir con todas las obligaciones que le impone el " 
        "presente contrato, en especial atender el pago oportuno por concepto de obra ejecutada. d): Las demás obligaciones determinadas por la ley.\n"

        "<b>SEXTA. RETENCIONES</b>: El CONTRATISTA autoriza al CONTRATANTE a retener el 10% del valor del contrato que será aplicado en las facturas " 
        "o cuentas de cobro presentadas por el CONTRATISTA. El CONTRATANTE podrá disponer del retenido por la ocurrencia de uno de los siguientes " 
        "eventos: 1) Cuando EL CONTRATISTA no cumpla con su objeto contractual y condiciones del contrato, por hechos imputables al contratista. " 
        "2) Cuando EL CONTRATISTA o sus dependientes hayan causado un daño o perjuicio al CONTRATANTE por hechos imputable al contratista. 3) Cuando "  
        "EL CONTRATISTA no haya suscrito las pólizas requeridas en el presente contrato. 4). Cuando por Ley deba hacerse Retención.\n" 

        "<b>PARÁGRAFO PRIMERO</b>: Igualmente las autorizaciones de retención serán hasta por las sumas que llegue a adeudar EL CONTRATISTA a sus dependientes, " 
        "cuantía de las pólizas, monto de los perjuicios graves causados, valor de las herramientas o retención en la fuente según el caso. "
        "PARÁGRAFO SEGUNDO: El contratante devolverá el dinero retenido al contratista cuando, el contrato termine, se reciba a satisfacción del " 
        "contratante por escrito la labor ejecutada y se haya liquidado sin problema alguno. La devolución del retenido no causa intereses.\n"

        "<b>SEPTIMA. TERMINACIÓN DEL CONTRATO</b>: El presente contrato terminará, además, por cualquiera de las siguientes causas:\n"
        "1.: Por las causales legales. "
        "2.: Por mutuo acuerdo de las partes, el cual deberá constar por escrito. "
        "3.: Por resolución o terminación, según el caso, sin perjuicio de la responsabilidad e indemnización de perjuicios a que haya lugar, según " 
        "las reglas generales y las especiales. "
        "4.: Por decisión unilateral del contratante, previa notificación al contratista por escrito con 3 días hábiles de anticipación, donde se " 
        "pagará lo realmente ejecutado hasta la fecha."
        "5.: Por el vencimiento del plazo, que es la preclusión de la oportunidad expresa o tácita para su respectiva ejecución a menos que las " 
        "partes acuerden continuar con la ejecución. "

    )

    # Crear el párrafo con estilo
    paragraph = Paragraph(additional_text_2, paragraph_style)

    # Colocar el párrafo en el PDF
    paragraph.wrapOn(c, letter[0] - 100, letter[1])
    paragraph.drawOn(c, 50, letter[1] - 730) 

     # Insertar el número de página al pie (pag 2)
    c.setFont("Helvetica", 10)
    c.drawString(letter[0] - 100, 30, f"Página {page_number}")

    #mostrar pagina 2 de texto
    c.showPage()

     # Incrementar el número de página
    page_number += 1

    # Crear una nueva página para el párrafo adicional 3
 
    additional_text_3 = (
    "6.: Por la inejecución, ejecución tardía, defectuosa o por el incumplimiento por cualquiera de las partes de las obligaciones contraídas " 
    "en el presente contrato, sin perjuicio de la responsabilidad e indemnización de perjuicios a que haya lugar, según las reglas generales y " 
    "las especiales. "
    "7.: Por la cesación de pagos, concurso de acreedores, insolvencia o embargos judiciales de cualquiera de las partes que afecten el cumplimiento " 
    "de las obligaciones adquiridas en los términos del presente contrato, sin perjuicio de la responsabilidad e indemnización de perjuicios a que " 
    "haya lugar, según las reglas generales y las especiales.\n"    
    "8.: Cuando el CONTRATISTA, sea incluido en listas restrictivas, tales como lista OFAC, lista Clinton, SANGRILAFT o de similar naturaleza. "
    "9.: Por la cesión del presente contrato que hiciere EL CONTRATISTA a cualquier otra persona sin la autorización escrita de EL CONTRATANTE. "
    "10.: Cuando EL CONTRATISTA rehúse a suscribir las garantías o polizas exigidas. "
    "11.: Por fuerza mayor o caso fortuito que impida el cumplimiento del contrato. "
    "12.: Por la evasión por parte de EL CONTRATISTA, durante la ejecución del contrato, del pago total o parcial de los aportes a los Sistemas " 
    "de Seguridad Social en Salud, Pensiones y FIC. "
    "13.: Las demás que determine la Ley.\n"

    "<b>OCTAVA. SUPERVISIÓN DEL CONTRATO</b>: EL CONTRATANTE, sus representantes o delegados para el efecto, supervisarán la ejecución del servicio " 
    "encargado, y podrá formular las observaciones del caso con el fin de ser analizadas conjuntamente con EL CONTRATISTA y efectuar por parte de " 
    "éste las modificaciones o correcciones a que hubiera lugar.\n"

    "<b>NOVENA. CALIDAD Y ESTATUTO DEL CONSUMIDOR</b>: El CONTRATISTA se compromete, en virtud del presente contrato, a dar cumplimiento al presente " 
    "contrato con estricta observancia de las disposiciones de la ley 1480 de 2011 – Estatuto del Consumidor a favor del consumidor final y/o " 
    "propiedad horizontal, a garantizar las condiciones de estabilidad, calidad e idoneidad del suministro e instalación y los materiales que se " 
    "adquieran para incorporarlos en el proyecto, contar con una política de garantías y asumir cualquier responsabilidad ante la autoridad competente, " 
    "como consecuencia de incumplimiento, requerimiento o reclamo.\n"

    "<b>DÉCIMA. ENTREGA Y RECIBO DE LAS OBRAS</b>: A más tardar los últimos cinco día del plazo de ejecución estipulado en el presente contrato, EL " 
    "CONTRATISTA deberá tener debidamente terminada y aprobada a satisfacción de EL CONTRATANTE, la totalidad del objeto contratado, completamente " 
    "listo para iniciar su servicio u operación, limpia de escombros, materiales sobrantes, formaletas, etc.; en caso que no se cumpla, se ordenara " 
    "al contratista atender los daños y perjuicios que se generen. Los recibos parciales o pagos que EL CONTRATANTE haga de parte del objeto del " 
    "presente contrato, no implican aceptación final por parte de ella de la obra contratada, ya que la obligación de EL CONTRATISTA es la de entregar " 
    "dicha obra en su totalidad. A pesar de la entrega, la responsabilidad de EL CONTRATISTA subsistirá por el tiempo que señala la cláusula sobre " 
    "garantías y pólizas.\n" 

    "<b>DÉCIMA PRIMERA. DEVOLUCIONES</b>: El CONTRATANTE y/o la interventoría, en el caso que aplique, podrán rechazar los recibos parciales y final " 
    " de la obra ejecutada y no autorizar el correspondiente pago, si las obras no se ajustan a las especificaciones suministradas. En tales eventos, " 
    "deberá el CONTRATISTA efectuar las correcciones pertinentes, dentro de los diez (10) días siguientes a la observación.\n"

    "<b>DÉCIMA SEGUNDA. INDEPENDENCIA LABORAL</b>: El presente contrato no genera dependencia laboral entre EL CONTRATISTA y EL CONTRATANTE, " 
    " situación que exime a EL CONTRATANTE de cualquier responsabilidad presente y futura con relación al pago de salarios, prestaciones, " 
    " indemnizaciones y demás que puedan generar relación laboral entre EL CONTRATISTA y el personal que él contrate para realizar todas las obras. " 
    " De presentarse alguna reclamación de carácter laboral, EL CONTRATISTA saldrá al saneamiento y responderá por la totalidad de la reclamación.\n"

    "<b>PARÁGRAFO PRIMERO</b>: EL CONTRATISTA se obliga a tener a su personal debidamente afiliado a alguna E.P.S., y fondo de pensiones y cesantías. " 
    "Será por su cuenta el cumplimiento de todas las obligaciones por concepto de salarios y prestaciones sociales con fundamento en las normas legales "
    "vigentes, así como las prestaciones extra legales que tenga establecidas o establezca con sus trabajadores en pactos o convenciones colectivas.\n"

    "<b>PARÁGRAFO SEGUNDO</b>: EL CONTRATISTA suministrará a sus trabajadores los equipos de protección personal e implementos necesarios para la ejecución "  
    "de las labores y tomará las medidas para mantener en la obra la higiene y la seguridad en el trabajo, de conformidad a las normas legales que regulan " 
    "la materia, incluyendo el orden y el aseo de los sitios de trabajo. De igual forma debe asegurar que sus trabajadores usen correctamente los elementos " 
    "de protección personal y demás dispositivos para la prevención y control de los riesgos laborales.\n"

    "<b>PARÁGRAFO TERCERO</b>: EL CONTRATISTA tomará las precauciones necesarias para la seguridad del personal a su cargo o servicio y los transeúntes, de " 
    "acuerdo con las reglamentaciones vigentes en el país. De encontrar que no se da cumplimiento en la obra a lo aquí establecido y a las normas sobre la " 
    "seguridad y la salud en el trabajo y demás normas relacionadas, se suspenderá la prestación del servicio.\n"

    "<b>PARÁGRAFO CUARTO</b>: EL CONTRATANTE podrá impedir el acceso a la obra del personal de EL CONTRATISTA en un momento dado hasta tanto este último haya " 
    "demostrado el cumplimiento de las obligaciones aquí previstas en materia de seguridad social, según los términos establecidos por la ley, sin que " 
    "esto pueda ser utilizado por EL CONTRATISTA como justificación para ampliar el plazo del contrato o el incumplimiento del mismo, ni para reclamar " 
    "perjuicios.\n"

    "<b>PARÁGRAFO QUINTO</b>: No existe vínculo o relación laboral alguna entre EL CONTRATISTA y EL CONTRATANTE, esta salvedad se extiende al personal o " 
    "dependientes de EL CONTRATISTA que utilice en la ejecución del objeto del presente contrato.\n"

    "<b>DÉCIMA TERCERA. CONDICIONES</b>: Expresamente las partes establecen que no se reconocerá por parte de EL CONTRATANTE al CONTRATISTA recargos por horas extras, " 
    "nocturnas o trabajo en dominical o festivo, ni por alimentación de los trabajadores de EL CONTRATISTA, tanto en horarios extendidos o normales.\n"

    )

    
    # Crear el párrafo con estilo
    paragraph = Paragraph(additional_text_3, paragraph_style)

    # Colocar el párrafo en el PDF
    paragraph.wrapOn(c, letter[0] - 100, letter[1])
    paragraph.drawOn(c, 50, letter[1] - 730) 

     # Insertar el número de página al pie (pag 3)
    c.setFont("Helvetica", 10)
    c.drawString(letter[0] - 100, 30, f"Página {page_number}")

    #mostrar pagina 3 de texto
    c.showPage()

     # Incrementar el número de página
    page_number += 1

    # Crear una nueva página para el párrafo adicional 4

    additional_text_4 = (
    "<b>DÉCIMA CUARTA. INDEMNIDAD</b>: EL CONTRATISTA actuará por su propia cuenta, con absoluta autonomía e independencia, y no estará sometido a " 
    "subordinación laboral con EL CONTRATANTE y sus derechos se limitarán, de acuerdo con la naturaleza del contrato, a exigir el cumplimiento de las " 
    "obligaciones en el contrato y al pago de los honorarios estipulados, de igual forma sus obligaciones se circunscriben a la prestación del servicio " 
    "para el cual fue contratado. En consecuencia, EL CONTRATISTA mantendrá indemne al CONTRATANTE de los requerimientos judiciales y extrajudiciales que "  
    "invoquen los trabajadores y el personal a cargo del CONTRATISTA como resultado del incumplimiento de sus obligaciones. Cualquier costo en que incurra " 
    "EL CONTRATANTE para la defensa de sus intereses o suma que deba cancelar como consecuencia de las situaciones planteadas en este contrato o por " 
    "cualquier otra derivada del incumplimiento de las obligaciones del CONTRATISTA, deberá ser reintegrado en su totalidad al CONTRATANTE debidamente " 
    "actualizado, sin requerimiento judicial o extrajudicial al cual renuncia EL CONTRATISTA con la firma de este contrato.\n"

    "<b>DÉCIMA QUINTA. CALIDAD DE LOS SERVICIOS</b>: EL CONTRATISTA asume toda responsabilidad ante el CONTRATANTE por la calidad, cantidad y oportunidad de"  
    "los trabajos ejecutados objeto del presente Contrato, cuya calidad mínimo será la establecida en el Estatuto del Consumidor para estos casos.\n"

    "<b>DÉCIMA SEXTA. CESIÓN Y SUBCONTRATACIÓN</b>: EL CONTRATISTA no podrá ceder la ejecución del objeto del presente contrato sin autorización previa y escrita " 
    "del CONTRATANTE. El incumplimiento de esta obligación facultará al CONTRATANTE para dar por terminado el presente contrato, sin que por este hecho se genere " 
    "alguna indemnización por parte del CONTRATANTE a favor del CONTRATISTA.\n"

    "<b>PARÁGRAFO PRIMERO</b>: El CONTRATISTA sólo podrá subcontratar todo aquello que no implique la ejecución de todo el objeto del presente contrato. En caso "  
    "que el CONTRATANTE permitiera por escrito celebrar subcontratos, quedará entendido que ninguno de los subcontratistas ni del personal empleado por éstos " 
    "podrá considerarse como empleados de EL CONTRATANTE y no tendrá nexos ni responsabilidad laboral alguna con ellos.\n"

    "<b>PARÁGRAFO SEGUNDO</b>: El CONTRATISTA se obliga a exigirle al subcontratista el cumplimiento de todas las mismas obligaciones a cargo del CONTRATISTA " 
    "expresadas a lo largo de todo este contrato y lo que haga parte del mismo.\n"

    "<b>DÉCIMA SEPTIMA. INCUMPLIMIENTO DEL CONTRATO</b>: Para efectos del presente contrato se tendrá el siguiente procedimiento para la declaratoria de " 
    "incumplimientos: 1. Cuando se presenten retardos superiores a tres días (3) en el cumplimiento de entregas parciales, o se presenten incumplimientos " 
    "sobre especificaciones técnicas o de calidad pactadas en el contrato, o incumplimientos en cualquier otra obligación establecida en el mismo, el "
    "CONTRATANTE procederá a requerirlo para que dentro de los tres (3) días siguientes al recibo del requerimiento a la dirección suministrada en el contrato, " 
    "proceda a cumplir con las obligaciones que le corresponden. 2. Cuando no sea satisfecho el requerimiento del numeral anterior o se presenten por segunda vez "
    "retardos o incumplimientos en las obligaciones y/o especificaciones del contrato por parte del CONTRATISTA, se configurará un incumplimiento grave del contrato "  
    "que facultará al CONTRATANTE, una vez se informe por escrito al CONTRATISTA, a nombrar un tercero que ejecute parcial o totalmente las obligaciones contraídas, " 
    "cuyo costo será asumido por el CONTRATISTA incumplido, y la aseguradora será garante. 3. Una vez configurado el incumplimiento grave, el CONTRATANTE estará " 
    "facultado para declarar la terminación anticipada y unilateral mediante escrito remitido al correo electrónico del CONTRATISTA o por otro medio, enviándole la " 
    "liquidación unilateral del mismo y sin que se genere indemnización de ningún tipo a favor del CONTRATISTA. 4. Durante la liquidación unilateral del contrato por " 
    "parte del CONTRATANTE, este último, podrá aplicar los descuentos, deudas, daños y compensaciones correspondientes de las sumas que adeude al CONTRATISTA.\n"

    "<b>PARÁGRAFO PRIMERO</b>: El incumplimiento del contrato, aunque no dé lugar a la terminación, obligará al CONTRATISTA, en todo caso, al resarcimiento de los " 
    "perjuicios que generen al CONTRATANTE, quien podrá hacer efectivas las garantías existentes. La efectividad de las garantías no impedirá ni limitará, de ningún " 
    "modo, el derecho del CONTRATANTE a exigir el pago de los daños y perjuicios que se le causen y excedan de los importes de aquellas.\n"

    "<b>DÉCIMA OCTAVA. MULTAS</b>: El CONTRATANTE, aplicará multas diarias hasta del uno por ciento (1%) del valor total del contrato hasta llegar a un monto máximo " 
    "del diez 10% del valor del contrato, en los siguientes eventos: 1. Incumplimiento de las obligaciones estipuladas en el contrato o en sus anexos y de las "
    "obligaciones laborales a su cargo, conforme lo establece el numeral primero de la cláusula anterior. 2. Incumplimiento en el término para liquidar el contrato o "  
    "por no allegar los documentos requeridos para tal fin. 3. El incumplimiento de las normas de seguridad y salud en el trabajo, riesgos laborales, salud ocupacional "  
    "y normas medioambientales frente a sus trabajadores.\n"

    "<b>PARÁGRAFO PRIMERO</b>: Las multas se causarán sin que sea necesario reconvenirlo para constituirlo en mora. Se aplicará una multa diaria hasta que el CONTRATISTA " 
    "cese la conducta que dio origen a la multa. El CONTRATISTA acepta que el CONTRATANTE descuente el valor de las multas consagradas en la presente cláusula de las " 
    "sumas que le adeude al CONTRATISTA, en virtud del presente contrato o de cualquier otro que se haya suscrito entre las partes. El pago de las multas aquí pactadas " 
    "no indemniza los perjuicios sufridos por EL CONTRATANTE ni limita en nada las posibilidades de reclamación de esta última por los daños padecidos.\n"

       )

    # Crear el párrafo con estilo
    paragraph = Paragraph(additional_text_4, paragraph_style)

    # Colocar el párrafo en el PDF
    paragraph.wrapOn(c, letter[0] - 100, letter[1])
    paragraph.drawOn(c, 50, letter[1] - 730) 

     # Insertar el número de página al pie (pag 4)
    c.setFont("Helvetica", 10)
    c.drawString(letter[0] - 100, 30, f"Página {page_number}")

    #mostrar pagina 4 de texto
    c.showPage()

     # Incrementar el número de página
    page_number += 1

    # Crear una nueva página para el párrafo adicional 4
 
    additional_text_5 = (
    "<b>DÉCIMA NOVENA. GARANTIA</b>: En caso que en el informe general del presente contrato, se solicite al CONTRATISTA constituir pólizas a favor del CONTRATANTE, el " 
    "CONTRATISTA se compromete a: 1. Constituir las pólizas exigidas en la información general del presente contrato con una compañía de seguros legalmente autorizada para " 
    "funcionar en Colombia bajo la matriz de Grandes Beneficiarios y aceptada por EL CONTRATANTE con su respectivo recibo de paz y salvo, las pólizas se deberán diligenciarse " 
    "y emitirse con la Agencia Blin Seguros Ltda. 2. Para la Garantía de Responsabilidad Civil deberá tener subamparos como: RC cruzada, Patronal, Vehículos propios y no "
    "propios, Contratistas y subcontratistas, Daño emergente y lucro cesante. 3. Para la emisión de las pólizas, el CONTRATISTA deberá diligenciar las pólizas a través de la "
    "agencia Seguros BLIN SEGUROS LTDA, y expedirá las mismas bajo la mitigación de riesgos del CONTRATANTE de Grandes Beneficiarios. 4. Para la emisión de las pólizas, el " 
    "CONTRATISTA deberá diligenciar las pólizas a través de la agencia Seguros BLIN SEGUROS LTDA , y expedirá las mismas bajo la mitigación de riesgos del CONTRATANTE de " 
    "Grandes Beneficiarios.\n"

    "<b>5. Documentos requeridos para la expedición de las pólizas</b>: El CONTRATISTA hará entrega de los siguientes documentos requeridos para la expedición de las pólizas "
    "dentro de los tres (3) días hábiles siguientes contados a partir de la suscripción del contrato: <b>Persona Jurídica</b>:- Formulario de conocimiento del cliente "
    "(Formulario Sarlaft) - Estados financieros actualizados de los dos últimos años contables. - Certificado de cámara de comercio (con vigencia no mayor a 30 días)."
    "- Rut.- Documento de identidad del representante legal. - Record de obras (cuando sea necesario). <b>Persona Natural</b>:- Formulario de conocimiento del cliente "
    "(Formulario Sarlaft). - Declaración de renta del año anterior.- Certificado de cámara de comercio (con vigencia no mayor a 30 días). - Rut - Documento de identidad. "
    "- Record de obras.\n"
    "La persona de contacto es: <b>Ansorena Orjuela Arango</b>: gerenciagenerales@blinseguros.com, Celular: 3108918342, y <b>Claudia Mejía</b>: "
    "gerenciaadministrativa@blinseguros.com, Celular: 301 589 2626, <b>PARÁGRAFO PRIMERO</b>: Las anteriores garantías están sujetas a la aprobación del CONTRATANTE y se "
    "solicitará a la compañía de seguros respectiva que los plazos de vigencia se desplacen, para su inicio, desde la fecha de recibo a satisfacción o desde la culminación " 
    "de los trabajos según lo exigido en esta cláusula.\n"

    "<b>PARÁGRAFO SEGUNDO</b>: Será responsabilidad del CONTRATISTA el ampliar y ajustar las garantías en caso de alguna modificación al contrato y dar el aviso respectivo a la "
    "correspondiente compañía de seguros.\n"

    "<b>VIGÉSIMA. CLÁUSULA PENAL</b>: El CONTRATISTA pagará al CONTRATANTE, sin necesidad de previo requerimiento, una vez se haya configurado un incumplimiento de las " 
    "obligaciones contraídas en virtud del presente contrato, una suma equivalente al veinte por ciento (20%) del valor total del mismo. La presente cláusula penal no tiene el " 
    "carácter de estimación anticipada de perjuicios, ni su pago extinguirá las obligaciones contraídas por el CONTRATISTA en virtud del presente contrato. En consecuencia, la "    
    "estipulación y el pago de la pena dejan a salvo el derecho del CONTRATANTE de exigir acumulativamente con ella el cumplimiento o la resolución del contrato, en ambos casos " 
    "con indemnización de perjuicios.<para>"

    "<b>VIGÉSIMA PRIMERA. NOTIFICACIONES</b>: Tanto el contratante como el contratista serán notificados oficialmente en los datos suministrados en el informe general del " 
    "presente contrato.<para>"

    "<b>PARÁGRAFO PRIMERO</b>: Será responsabilidad de las partes cualquier cambio de dirección que no sea oportunamente notificado al otro contratante.<para>"

    "<b>VIGÉSIMA SEGUNDA. CONFIDENCIALIDAD</b>: EL CONTRATISTA, en virtud de la suscripción del presente contrato, se compromete a llevar a cabo las tareas asignadas de acuerdo " 
    "con los más altos estándares de confidencialidad y competencia ética e integridad profesional. EL CONTRATISTA también se compromete a no revelar directa o indirectamente a "
    "ninguna persona, ni durante la vigencia del contrato, ni después de su terminación, ninguna información que hubiera obtenido durante la ejecución del mismo y que no sea de "     
    "dominio público, excepto con el permiso explícito y por escrito del CONTRATANTE. EL CONTRATISTA deberá tratar los detalles del contrato como privados y confidenciales, " 
    "excepto en la medida que le sea necesario para cumplir sus obligaciones contractuales o para cumplir con las leyes aplicables. EL CONTRATISTA no deberá publicar, ni permitir " 
    "que se publique, ni divulgue ningún detalle de los trabajos, documento técnico, conocimiento del ramo, ni ningún otro detalle sin antes contar con el previo consentimiento " 
    "del CONTRATANTE.<para>"

    "<b>VIGÉSIMA TERCERA. PROPIEDAD INTELECTUAL</b>: Los derechos patrimoniales de autor o propiedad industrial que realice el CONTRATISTA en virtud del presente contrato, se " 
    "ceden en su totalidad al CONTRATANTE, de conformidad con los artículos 20 de la Ley 23 de 1982, modificado por ley 1450 de 2011 en su artículo 28 y el artículo 10 de la " 
    "Decisión Andina 351 de 1993.<para>"

    "<b>VIGÉSIMA CUARTA. ACTA DE LIQUIDACIÓN</b>: De común acuerdo entre las partes y al momento de terminarse la totalidad de la obra o del servicio prestado, se suscribirá " 
    "un acta de liquidación definitiva del contrato, la cual deberá contener la siguiente información:<para>"
    " 1. Valor inicial y final del contrato."
    " 2. Dar cuenta del servicio prestado."
    " 3. Constancia de entrega de las obras o trabajos realizados."
    " 4. Cuando sea aplicable al objeto del contrato, constancia de entrega de los manuales, instrucciones, mantenimiento y fichas técnicas de los elementos, partes o " 
    "equipos que hacen parte del bien suministrado o el servicio prestado."
    " 5. Relación de las garantías y/o pólizas otorgadas con objeto del contrato, y entrega de pólizas poscontractuales (según aplique)."
    " 6. Cualquier otra circunstancia relacionada con la ejecución del contrato que sea relevante para su terminación."
    " 7. Certificación de la interventoría o supervisión respecto del cumplimiento por parte del CONTRATISTA de las obligaciones adquiridas en virtud del presente contrato."
    " 8. Constancia de las multas y sanciones que se hayan impuesto al CONTRATISTA. "
    " 9. Paz y salvo del almacén de la obra por concepto de materiales, herramientas y equipos. (Diligenciado en un memorando)."

    )

    # Crear el párrafo con estilo
    paragraph = Paragraph(additional_text_5, paragraph_style)

    # Colocar el párrafo en el PDF
    paragraph.wrapOn(c, letter[0] - 100, letter[1])
    paragraph.drawOn(c, 50, letter[1] - 730) 

     # Insertar el número de página al pie (pag 5)
    c.setFont("Helvetica", 10)
    c.drawString(letter[0] - 100, 30, f"Página {page_number}")

    #mostrar pagina 5 de texto
    c.showPage()

     # Incrementar el número de página
    page_number += 1

     #Crear pagina 5. 


    additional_text_6 = (
    "<b>PARÁGRAFO PRIMERO</b>: En el evento en que el CONTRATISTA no comparezca a la liquidación del contrato, o no desee firmarla, el CONTRATANTE estará facultado para " 
    "liquidarla unilateralmente y se compartirá al contratista a su correo electrónico u otro medio de notificación."

    "<b>VIGÉSIMA QUINTA. ANEXOS</b>: Forman parte integral del presente contrato como ANEXOS los siguientes documentos:<para>"
    " 1. Fotocopia de la cédula del Representante Legal de EL CONTRATISTA.<para>"
    " 2. Fotocopia del Certificado de Existencia y Representación Legal de EL CONTRATISTA.<para>"
    " 3. Copia de RUT de EL CONTRATISTA.<para>"
    " 4. Propuesta económica o cotización.<para>"
    " 5. Las garantías y pólizas exigidas.<para>"

    "<b>VIGÉSIMA SEXTA. REFORMAS AL CONTRATO</b>: Toda adición o modificación al presente contrato deberá hacerse por escrito, firmado por EL CONTRATISTA y EL CONTRATANTE, "
    "requisito sin el cual no producirá ningún efecto. La adición o modificación se agregará al contrato original y formará parte integral del mismo.<para>"

    "<b>VIGÉSIMA SEPTIMA. NEGOCIOS LICITOS</b>: Las partes y sus representantes legales dejan expresa constancia que se dedican a negocios lícitos, y que, a la fecha, ni sus nombres ni el de "
    "ninguno de sus socios o administradores, figuran en la Orden Ejecutiva No. 12.978, SDNT, mejor conocida como la Lista Clinton, publicada por el Departamento de Estado de" 
    "los Estados Unidos, comprometiéndose las partes a mantener esta misma condición durante toda la vigencia del presente contrato y de sus prórrogas. Será causal de " 
    "terminación inmediata de este contrato el hecho que alguna de las partes, sus socios o representantes, dejen de cumplir con el compromiso aquí referido, en todo o en " 
    "parte. La parte que incumpla lo establecido en esta cláusula no tendrá derecho a que se le reconozca indemnización alguna por la terminación del contrato. EL CONTRATISTA" 
    "se obliga a responder frente al CONTRATANTE por todos los perjuicios que se llegaren a causar como consecuencia de esta afirmación.<para>"

   "<b>PARÁGRAFO PRIMERO</b>: Para todos los efectos, el “lavado de dinero” es el conjunto de procedimientos usados para cambiar la identidad del dinero obtenido " 
     "ilegalmente, a fin de aparentar haber sido obtenido de fuentes legítimas. Estos procedimientos incluyen disimular la procedencia y propiedad verdadera de los fondos.<para>"

    "<b>VIGÉSIMA OCTAVA. MÉRITO EJECUTIVO</b>: El presente contrato prestará mérito ejecutivo para cualquiera de las partes, por contener obligaciones claras, expresas y " 
    "exigibles, sin que sea necesario para su exigibilidad el requerimiento previo o constitución en mora.<para>"

    "<b>VIGÉSIMA NOVENA. INVALIDEZ DE ACUERDOS ANTERIORES</b>: Las partes manifiestan que no reconocerán validez a estipulaciones anteriores, verbales o escritas, relacionadas " 
    "con el presente contrato, por cuanto aquí se consigna el acuerdo completo y total. De ahí que acuerdan dejar sin efecto alguno cualquier otro contrato verbal o escrito " 
    "celebrado con anterioridad entre EL CONTRATANTE y EL CONTRATISTA.<para>"

    "<b>TRIGÉSIMA. LEGISLACIÓN APLICABLE Y DOMICILIO</b>: Este contrato se regirá y será interpretado de conformidad con las leyes de la República de Colombia, y tendrá como "
    "domicilio contractual el municipio de Rionegro.<para>"

    "Para constancia, se firma en el municipio de Rionegro - Antioquia, en dos ejemplares del mismo tenor literal, destinados para las partes.<para>"

    )

    # Crear el párrafo con estilo
    paragraph = Paragraph(additional_text_6, paragraph_style)

    # Colocar el párrafo en el PDF
    paragraph.wrapOn(c, letter[0] - 100, letter[1])
    paragraph.drawOn(c, 50, letter[1] - 400) 

    # Añadir espacio antes de la sección de firmas
    c.drawString(50, letter[1] - 700, "")  # Solo para establecer la coordenada, ajusta si es necesario.
    c.drawString(50, letter[1] - 680, "FIRMA DEL CONTRATANTE                    FIRMA DEL CONTRATISTA")

    # Añadir espacio después del texto
    c.drawString(50, letter[1] - 720, "_____________________                    ____________________________")

     # Insertar el número de página al pie (pag 6)
    c.setFont("Helvetica", 10)
    c.drawString(letter[0] - 100, 30, f"Página {page_number}")

    #mostrar pagina 3 de texto
    c.showPage()

     # Incrementar el número de página
    page_number += 1

    #guardad PDF
    c.save()
   
if __name__ == '__main__':
    app.run(debug=True)