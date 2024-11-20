# Esteganografía con el algoritmo F5

## Instalación

1.  Crear un ambiente virtual en python.
2.  Instalar los paquetes indicados en el archivo requirements.txt en el entorno vitual de python.

 ~~~
  pip3 install -r requirements.txt
~~~

3.  Copiar al ambiente virtual el archivo .py que contiene el código de la aplicación.

***
## Ejecución

1. Ejecutar el siguiente comando en el ambiente virtual de python:

  ~~~
  streamlit run <archivo.py>
~~~

2. Aparecerá el siguiente mensaje:

 ~~~
 You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://<ipv4>:8501
~~~
Donde IPv4 es la dirección de red de su host.

3. En un web browser digitar http://localhost:8501

   

4.  Para cargar una imagen se debe dar click en el botón **Browse files**, luego aparecerá un selector de archivos que le permitirá escoger una imagen de formato .jpg o .jpeg.

5.   Después aparecerá un cuadro de texto para ingresar el mensaje que se va a incrustar en la imagen. El mensaje debe tener máximo 5 caracteres, si ingresa un mayor número de caracteres aparecerá un mensaje de error.

6.   Luego de ingresar el mensaje de 5 caracteres, debe pulsar Enter y aparecerá un botón **Incrustar mensaje y mostrar resultados**
7.   Luego de dar click en el botón **Incrustar mensaje y mostrar resultados** aparecerán la imagen original, la imagen procesada con el texto incrustado, el mensaje extraído y los valores de PSNR, MSE y SSIM.
8.   Si se desea realizar el proceso con otra imagen, se debe dar click en la X que se encuentra a la derecha del nombre del archivo cargado.

