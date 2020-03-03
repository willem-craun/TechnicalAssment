import json

from django.views.generic import TemplateView
from django.contrib.staticfiles import finders

def pull_payee_data(cust):
    name = cust['Payee']['Name']
    fax = cust['Payee']['Fax']
    phone = cust['Payee']['Phone']
    address = cust['Payee']['Address']['Address1']
    if cust['Payee']['Address']['Address2'] is not "":
        address= address+'\n\t '+cust['Payee']['Address']['Address2']
    city = cust['Payee']['Address']['City']
    statorprov = cust['Payee']['Address']['StateOrProvince']
    country = cust['Payee']['Address']['Country']
    post = cust['Payee']['Address']['PostalCode']
    atten = cust['Payee']['Attention']
    subdate = cust['Payee']['SubmissionDate']

    return f'Name: {name} \nFax: {fax} \nPhone: {phone} \nAddress: {address},\n\t {city} {statorprov}, {country} {post}\nAttention: {atten}\nSubmission Date: {subdate}'  


def pull_payment_data(cust):
    customer_payment = cust.get('Payment')
    pan, cvv, exp = customer_payment['PAN'], customer_payment['CVV'], customer_payment['Exp']

    return f'PAN: {pan} \nCVV: {cvv} \nExp: {exp}'


def pull_remittance_data(cust):
    return_rem =  []
    for rem in cust.get('Remittance'):
        return_rem.append('Payor Name: '+rem['PayorName']+' \n\tPayor ID#: '+str(rem['PayorId'])+' \n\tInvoice #: '+str(rem['InvoiceNo'])+' \n\tDescription: '+rem['Description']+' \n\tAmount: '+str(rem['Amount']))

    return return_rem

class JSONParserView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        result = finders.find('sample.json')

        names_list    = []
        payment_list  = []
        remitt_list   = []

        with open(result,'r') as jason:

            data = json.load(jason)
            for customer in data:
                names_list.append(pull_payee_data(customer))
                payment_list.append(pull_payment_data(customer))
                remitt_list.append(pull_remittance_data(customer))

        context['names']                           = names_list
        context['payments']                        = payment_list
        context['remitts']                         = remitt_list
        context['names_payments_and_remitts_list'] = zip(names_list, payment_list, remitt_list)

        return context

