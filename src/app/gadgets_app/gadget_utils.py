import locale
from PIL import Image
from datetime import datetime

from src.utils.common.logger import CustomLogger
from src.utils.common.paths import ProjectPaths

logger = CustomLogger()
paths = ProjectPaths()

def search_image(image_name: str) -> Image.Image:
    """
    Search and load an image from the images directory.
    
    Args:
        image_name (str): Image filename with extension
        
    Returns:
        Image.Image: Loaded PIL Image object
        
    Raises:
        FileNotFoundError: If image file doesn't exist
        PIL.UnidentifiedImageError: If file is not a valid image
    """
    try:
        image_path = paths.images_dir.joinpath("logo_images/png_images", image_name)
        return Image.open(image_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Image {image_name} not found in {image_path}")
    except Exception as e:
        raise Exception(f"Error loading image {image_name}: {e}")
    

def current_time() -> str:
    """
    Get the current date formatted in Catalan.
    
    Returns:
        str: Current date formatted as 'DD de Month de YYYY' in Catalan
             Example: '15 de març de 2024'
    
    Raises:
        locale.Error: If Catalan locale cannot be set
        ValueError: If date formatting fails
    """
    try:
        # Intentar configurar locale catalán
        try:
            locale.setlocale(locale.LC_TIME, 'ca_ES.UTF-8')
        except locale.Error:
            # Alternativa si el primer intento falla
            try:
                locale.setlocale(locale.LC_TIME, 'cat_ES.UTF-8')
            except locale.Error:
                logger.warning("No es pot establir el locale en català. Using default.")
                # Usar locale por defecto si ambos intentos fallan
                locale.setlocale(locale.LC_TIME, '')
        
        # Formatear fecha actual
        formatted_date: str = datetime.now().strftime("%d de %B de %Y")
        return formatted_date
        
    except Exception as e:
        logger.error(f"Error getting formatted date: {str(e)}")
        # Retornar formato básico si hay error
        return datetime.now().strftime("%d/%m/%Y")