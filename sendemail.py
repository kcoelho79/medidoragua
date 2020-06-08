from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
import keys

def send_message(level):
    print('... sending email ...')
    message = Mail(
                from_email='kleber@kafework.com.br',
                to_emails='kleber@kafework.com.br',
                subject='### Alerta Nivel da Caixa com - %s da capacidade máxima ###' %level,
                html_content='''
                    <strong>E-mail enviado Robo Watermeter </strong>
                    <br>
                    <a href="http://157.245.133.18"> Clique aqui para ver a meidção da caixa de água</a>

                ''')
    try:
        #sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        sg = SendGridAPIClient(keys.SENDGRID_API_KEY)

        response = sg.send(message)
        print("... status_code << %s >> ..." %response.status_code)
        #print(response.body)
        # print(response.headers)
    except Exception as e:
        print("ERRO  => ", str(e))