import json
class RunScript:
    def pullPayeeData(cust):
        print("PayeeMethod")
        #print(cust.get('Payee').get('Name'))
    def pullPaymentData(cust):
        print(" ")
        #print(cust.get('Payment'))
    def pullRemittanceData(cust):
        remitList = cust.get('Remittance')
        for payor in remitList:
            print(payor.get('Description'))

    with open("sample.json",'r') as jsonFile:
        data = json.load(jsonFile)
        for customer in data:
            pullPayeeData(customer)
            pullPaymentData(customer)
            pullRemittanceData(customer)