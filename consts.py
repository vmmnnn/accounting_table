import ctypes

MIN_ROOT_HEIGHT = 150
MIN_ROOT_WIDTH = 250

TASKBAR_HEIGHT = 75      # 75 - высота панели задач внизу. Получено экспериментально. По возможности, заменить
RIGHT_SHIFT = 15    # Иначе улезает направо. Получено экспериментально. По возможности, заменить


user32 = ctypes.windll.user32
SCREEN = (user32.GetSystemMetrics(0) - RIGHT_SHIFT, user32.GetSystemMetrics(1) - TASKBAR_HEIGHT)

                # widths of columns in the main table
SHIPPING_COLUMN = 80
LINK_COLUMN = 200
FIO_COLUMN = 245
PRODUCT_COLUMN = 180
PAYMENT_COLUMN = 80
NET_COLUMN = 80
ORDER_DATE_COLUMN = 120
SHIPPING_DATE_COLUMN = 120
SHIPPING_WAY_COLUMN = 130

TABLE_WIDTH = SHIPPING_COLUMN + LINK_COLUMN + FIO_COLUMN + PRODUCT_COLUMN + PAYMENT_COLUMN + NET_COLUMN + ORDER_DATE_COLUMN + SHIPPING_DATE_COLUMN + SHIPPING_WAY_COLUMN
TABLE_HEIGHT = 25

SCROLLBAR_COORDINATES = (TABLE_WIDTH - 15, 23)     # координаты scrollbar основной таблицы
SCROLLBAR_HEIGHT = TABLE_HEIGHT * 20
