import streamlit as st
import cv2
import numpy as np
from scipy.fftpack import dct, idct
from skimage.metrics import peak_signal_noise_ratio as psnr, mean_squared_error as mse, structural_similarity as ssim
from PIL import Image
from io import BytesIO


# Función para dividir la imagen en bloques 8x8 y aplicar DCT

def apply_dct(image):
    h, w = image.shape
    dct_blocks = np.zeros((h, w), dtype=np.float32)
    for i in range(0, h, 8):
        for j in range(0, w, 8):
            block = image[i:i+8, j:j+8] - 128
            dct_blocks[i:i+8, j:j+8] = dct(dct(block.T).T)
    return dct_blocks


# Función para invertir el proceso de DCT (IDCT)

def apply_idct(dct_blocks):
    h, w = dct_blocks.shape
    img_blocks = np.zeros((h, w), dtype=np.float32)
    for i in range(0, h, 8):
        for j in range(0, w, 8):
            block = idct(idct(dct_blocks[i:i+8, j:j+8].T).T) + 128
            img_blocks[i:i+8, j:j+8] = block
    return np.clip(img_blocks, 0, 255)

# Función para incrustar el mensaje

def embed_message(dct_blocks, message):
    bin_message = ''.join([format(ord(char), '08b') for char in message])
    idx = 0
    for i in range(dct_blocks.shape[0]):
        for j in range(dct_blocks.shape[1]):
            if idx < len(bin_message):
                coef = int(dct_blocks[i, j])
                if coef != 0:
                    coef = (coef & ~1) | int(bin_message[idx])
                    dct_blocks[i, j] = coef
                    idx += 1
                if idx >= len(bin_message):
                    break
    return dct_blocks

# Función para extraer el mensaje

def extract_message(dct_blocks, message_length):
    bin_message = ''
    idx = 0
    for i in range(dct_blocks.shape[0]):
        for j in range(dct_blocks.shape[1]):
            if idx < message_length * 8:
                coef = int(dct_blocks[i, j])
                if coef != 0:
                    bin_message += str(coef & 1)
                    idx += 1
    message = ''.join([chr(int(bin_message[i:i+8], 2)) for i in range(0, len(bin_message), 8)])
    return message

# Función para calcular las métricas

def calculate_metrics(original, modified):
    psnr_value = psnr(original, modified)
    mse_value = mse(original, modified)
    ssim_value = ssim(original, modified, multichannel=False)
    return psnr_value, mse_value, ssim_value

# Función principal para esteganografía

def f5_steganography(image, message):
    dct_blocks = apply_dct(image)
    dct_modified = embed_message(dct_blocks, message)
    stego_image = apply_idct(dct_modified).astype(np.uint8)
    extracted_message = extract_message(dct_modified, len(message))
    psnr_value, mse_value, ssim_value = calculate_metrics(image, stego_image)
    return stego_image, extracted_message, psnr_value, mse_value, ssim_value



# Inicializar las variables de sesión si no existen

if "uploaded_file" not in st.session_state:
    st.session_state["uploaded_file"] = None
if "message" not in st.session_state:
    st.session_state["message"] = ""


# Streamlit Interface
st.title("Esteganografía F5 en Imágenes")
st.markdown("---")



# Selector de archivo con filtro de formato
st.session_state["uploaded_file"] = st.file_uploader("Selecciona una imagen .JPG o .JPEG", type=["jpg", "jpeg"])

if st.session_state["uploaded_file"]:
    
     # Cargar la imagen original
     
    original_image = Image.open(st.session_state["uploaded_file"])

    # Redimensionar a 512x512 para un formato uniforme
    
    original_image = original_image.resize((512, 512))
    
    grayscale_image = original_image.convert('L') # Convertir a escala de grises y redimensionar
    
    original_array = np.array(grayscale_image)

    # Entrada del mensaje
    
    st.session_state["message"] = st.text_input("Ingresa un mensaje de hasta 5 caracteres")
    
    if len(st.session_state["message"]) > 5:
        st.error("El mensaje debe contener hasta 5 caracteres")
        st.session_state["message"] = ""  # Vaciar el campo si el mensaje es demasiado largo
        
    
    if st.session_state["message"] and st.button("Incrustar mensaje y mostrar resultados"):
        
        # Procesar esteganografía F5
        
        stego_image, extracted_message, psnr_value, mse_value, ssim_value = f5_steganography(original_array, st.session_state["message"])# Mostrar las imágenes en columnas
    
        # Imagen Transformada
        
        stego_pil_image = Image.fromarray(stego_image)
    
        # Mostrar las imágenes en columnas
    
        col1, col2 = st.columns(2)

        with col1:
            st.image(original_image, caption="Imagen Original", use_column_width=True)

        with col2:
            st.image(stego_pil_image, caption="Imagen procesada con mensaje incrustado", use_column_width=True)
            
        # Mostrar resultados
        
        st.text(f"Mensaje extraído: {extracted_message}")
        st.text(f"PSNR: {psnr_value:.2f}")
        st.text(f"MSE: {mse_value:.2f}")
        st.text(f"SSIM: {ssim_value:.2f}") 


