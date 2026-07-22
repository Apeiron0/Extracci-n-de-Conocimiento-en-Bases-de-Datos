import os
import cv2
from matplotlib import pyplot as plt

# Obtener la ruta del directorio donde está guardado este script
script_dir = os.path.dirname(os.path.abspath(__file__))

def plot_histogram(img, title, color='gray', equalize=False):
    """
    Función para calcular y graficar el histograma de una imagen.
    """
    if equalize:
        img = cv2.equalizeHist(img) # Ecualizar el histograma

    if len(img.shape) == 2: # Si la imagen es en escala de grises
        hist = cv2.calcHist([img], [0], None, [256], [0, 256])
        plt.plot(hist, color=color)
    else: # Si la imagen es en color
        for i, c in enumerate(color):
            hist = cv2.calcHist([img], [i], None, [256], [0, 256])
            plt.plot(hist, color=c)
            plt.xlim([0, 256])

    plt.title(title)
    plt.xlabel('Intensidad de iluminación')
    plt.ylabel('Cantidad de píxeles')
    plt.show()


def main():
    # Cargar las imágenes usando rutas relativas al archivo del script
    img1 = cv2.imread(os.path.join(script_dir, 'Lena1.jpg'), cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(os.path.join(script_dir, 'Lena2.jpg'))
    img3 = cv2.imread(os.path.join(script_dir, 'Lena3.jpg'), cv2.IMREAD_GRAYSCALE)

    # Verificar si las imágenes se cargaron correctamente
    if img1 is None or img2 is None or img3 is None:
        print("Error: No se pudo cargar una o más imágenes.")
        return

    # Mostrar las imágenes originales
    cv2.imshow('Lena1 - Escala de Grises', img1)
    cv2.imshow('Lena2 - Color', img2)
    cv2.imshow('Lena3 - Escala de Grises (Ecualizada)', img3)

    # Graficar histogramas
    plot_histogram(img1, 'Histograma de Lena1 (Escala de Grises)')
    plot_histogram(img2, 'Histograma de Lena2 (Color)', color=('b', 'g', 'r'))
    plot_histogram(img3, 'Histograma de Lena3 (Ecualizado)', equalize=True)

    # Esperar a que el usuario cierre las ventanas
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()