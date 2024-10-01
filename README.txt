Para instalar no meu pc tive que instalar uma versao manual do python no c:/pyhon301 e depois passar no terminal a versao especifica:

para instalar os componentes:
C:/Python310/python.exe -m pip install pyzbar
usar --user caso nao deixe instalar

para rodar o script, passar o caminho do python:
C:/Python310/python.exe qrcode.py



LEITURA DE ZAPCODES

2 metodos, 
Metodo1 em 2 passos, gerando imagens pelo pdfextract.py e depois rodando o opencv_img.py pra procurar nessas imagens
Metodo2 ler diretamente os pdfs pelo opencv_pdf.py