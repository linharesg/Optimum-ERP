from django.shortcuts import redirect, render, get_object_or_404
from company.models import Company
from .models import Invoice
from sales_order.models import SalesOrder, SalesOrderProduct
from random import randint
from django.contrib.auth.decorators import login_required

@login_required
def open_invoice(request, id):
    """
    Esta função exibe os detalhes de uma fatura específica, incluindo informações sobre a venda associada,
    produtos incluídos na venda, valor total dos produtos, desconto aplicado, valor total da fatura e informações
    do emissor e do destinatário.

    Args:
        request (HttpRequest): Objeto HttpRequest que contém os dados da requisição.

    Returns:
        HttpResponse: Uma resposta HTTP contendo a renderização do template "invoices/invoice.html" com os
        detalhes da fatura.

    Raises:
        Http404: Se a venda associada à fatura não existir.
    """
    companies = Company.objects.all()
    sale_order = get_object_or_404(SalesOrder, pk=id)
    sale_order_products = SalesOrderProduct.objects.filter(sale_order=sale_order)
    total_value_products = 0 
    for product in sale_order_products:
        total_value_products += product.total_value_product
    total_value_products_formatted = f"{total_value_products:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    discount = f"{total_value_products * (sale_order.discount/100):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    invoice = Invoice.objects.get(sale_order=sale_order)
    invoice_total_value = f"{sale_order.total_value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    context = {
        "companies": companies,
        "sale_order": sale_order,
        "sale_order_products": sale_order_products,
        "total_value_products": total_value_products_formatted,
        "invoice_total_value": invoice_total_value,
        "discount": discount,
        "invoice": invoice
        }
    
    return render(request, "invoices/invoice.html", context)

def create_invoice(request, id):
    """
    Esta função cria uma nova fatura para uma venda específica. Se uma fatura já existir para a venda
    especificada, a função redireciona para a visualização da fatura. Caso contrário, uma nova fatura é
    criada com base nas informações da empresa (emissor) e do cliente (destinatário).

    Args:
        request (HttpRequest): Objeto HttpRequest que contém os dados da requisição.
        id (int): O ID da venda para a qual a fatura será criada.

    Returns:
        HttpResponseRedirect: Um redirecionamento para a visualização da fatura criada.

    Raises:
        Http404: Se a venda especificada não existir.
    """
    sale_order = get_object_or_404(SalesOrder, pk=id)
    companies = Company.objects.all()
    client = sale_order.client
    acess_key_list = []
    for i in range(0, 10):
        acess_key_list.append(f"{randint(1000,9999)}")
    acess_key = (' '.join(acess_key_list))
    try:
        invoice = Invoice.objects.get(sale_order=sale_order)
    except:
        sale_order = get_object_or_404(SalesOrder, pk=id)
        access_key = acess_key
        barcode = f"{randint(100000000, 999999999)}"
        for company in companies:
            emitter_name = company.name
            emitter_fantasy_name = company.fantasy_name
            emitter_state_registration = company.state_registration
            emitter_cnpj = company.cnpj
            emitter_email = company.email
            emitter_zipcode = company.zipcode
            emitter_street = company.street
            emitter_number = company.number
            emitter_city = company.city
            emitter_state = company.state
            emitter_phone = company.phone
            receiver_name = client.company_name
            receiver_fantasy_name = client.fantasy_name
            receiver_cnpj = client.cnpj
            receiver_email = client.email
            receiver_zipcode = client.zipcode
            receiver_street = client.street
            receiver_number = client.number
            receiver_city = client.city
            receiver_state = client.state
            receiver_phone = client.phone
            Invoice.objects.create(sale_order=sale_order,
                                    emitter_name=emitter_name,
                                    emitter_fantasy_name=emitter_fantasy_name,
                                    emitter_state_registration=emitter_state_registration,
                                    emitter_cnpj=emitter_cnpj,
                                    emitter_email=emitter_email,
                                    emitter_zipcode=emitter_zipcode,
                                    emitter_street=emitter_street,
                                    emitter_number=emitter_number,
                                    emitter_city=emitter_city,
                                    emitter_state=emitter_state,
                                    emitter_phone=emitter_phone,
                                    receiver_name=receiver_name,
                                    receiver_fantasy_name=receiver_fantasy_name,
                                    receiver_cnpj=receiver_cnpj,
                                    receiver_email=receiver_email,
                                    receiver_zipcode=receiver_zipcode,
                                    receiver_street=receiver_street,
                                    receiver_number=receiver_number,
                                    receiver_city=receiver_city,
                                    receiver_state=receiver_state,
                                    receiver_phone=receiver_phone,
                                    access_key=access_key,
                                    barcode=barcode)
        return redirect("invoices:open_invoice", id=sale_order.id)
    return redirect("invoices:open_invoice", id=sale_order.id)