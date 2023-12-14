import tkinter as tk
from tkinter import ttk, filedialog
from back import getLabelsOnDirectory
from PIL import Image, ImageTk


def open_image(path):
    # Функция для открытия изображения с использованием PIL
    image = Image.open(path)
    image.show()


class ImageApp:
    def __init__(self, root, images):
        self.root = root
        # Создание списка для хранения объектов PhotoImage
        self.image_objects = []
        i = 0
        self.list_frame = []
        self.list_frame.append(tk.Frame(self.root, height=95))
        self.list_frame[-1].pack(fill=tk.BOTH, side=tk.TOP)
        # Загрузка изображений и создание миниатюр
        for img in images:
            if i % 5 == 0:
                self.list_frame.append(tk.Frame(self.root, height=95))
                self.list_frame[-1].pack(fill=tk.BOTH, side=tk.TOP)
            image = Image.open(img.image_path)
            thumbnail = image.resize((90, 90))
            photo = ImageTk.PhotoImage(thumbnail)
            self.image_objects.append(photo)

            # Создание метки с изображением
            label = ttk.Label(self.list_frame[-2], image=photo)
            label.photo = photo  # Сохранение ссылки на PhotoImage, чтобы избежать GC
            label.pack(side=tk.LEFT, pady=5)

            # Привязка события щелчка к функции открытия изображения
            label.bind("<Button-1>", lambda event, path=img.image_path: open_image(path))
            i += 1


def create_selected_labels_section():
    selected_labels_label.pack(side=tk.LEFT)
    clear_labels_button.pack(side=tk.RIGHT, pady=10, padx=10)


def clear_selected_labels():
    global listSelectedLabel
    listSelectedLabel = []
    print_selected_items()


def select_directory():
    directory_path = filedialog.askdirectory()
    update_label_list(directory_path)
    create_selected_labels_section()
    print_selected_items()


def update_label_list(directory_path):
    global listImages
    global labels
    labels, listImages = getLabelsOnDirectory(directory_path)
    combobox['values'] = labels


def draw_images():
    for child in frame4.winfo_children():
        child.destroy()
    global listImages
    listToOut = listImages.copy()

    for label in listSelectedLabel:
        listOut = []
        for imgData in listToOut:
            if label in imgData:
                listOut.append(imgData)
        listToOut = listOut

    ImageApp(frame4, listToOut)


def print_selected_items():
    # Получаем список выбранных элементов и выводим в консоль
    selected_items = listSelectedLabel
    selected_labels_label.config(text=f"Выбранные метки: {[index for index in selected_items]}")
    print("Выбранные метки::", [index for index in selected_items])
    draw_images()


def on_combobox_key_release(event):
    search_term = combobox.get().lower()

    # Фильтрация и добавление подсказок, которые начинаются с введенного значения
    suggestions = [option for option in labels if search_term in option.lower()]
    combobox['values'] = suggestions

    delay = 500
    combobox.after(delay, lambda: combobox.event_generate('<Button-1>'))


def on_combobox_select(event):
    selected_item = combobox.get()
    print(f"Selected item: {selected_item}")
    combobox.set("")
    listSelectedLabel.append(selected_item)
    print_selected_items()
    on_combobox_key_release(None)


listImages = []
labels = []
listSelectedLabel = []

# Создание главного окна
root = tk.Tk()
root.title("imaSearcher")
root.geometry("800x600")  # Установка размеров окна

frame = tk.Frame(master=root, width=30)
frame.pack(fill=tk.BOTH, side=tk.LEFT)

frame2 = tk.Frame(master=root)
frame2.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

frame3 = tk.Frame(master=frame2, height=70)
frame3.pack(fill=tk.X)

frame4 = tk.Frame(master=frame2)
frame4.pack(fill=tk.BOTH, expand=True)

# Кнопка для выбора директории
select_button = ttk.Button(frame, text="Выбрать директорию", command=select_directory)
select_button.pack(side=tk.TOP, padx=10, pady=10, anchor="w")

# Список (Listbox) для отображения меток
combobox = ttk.Combobox(frame, height=30, values=listImages)
combobox.pack(side=tk.TOP, anchor="w", padx=10, pady=10)

# Метка "Выбранные метки"
selected_labels_label = ttk.Label(frame3, text="Выбранные метки: ")
selected_labels_label.pack(side=tk.LEFT)

selected_labels_label.pack_forget()

# Кнопка "Очистить метки"
clear_labels_button = ttk.Button(frame3, text="Очистить метки", command=clear_selected_labels)
clear_labels_button.pack(side=tk.RIGHT, pady=10, padx=10)

combobox.bind("<<ComboboxSelected>>", on_combobox_select)
combobox.bind("<KeyRelease>", on_combobox_key_release)
clear_labels_button.pack_forget()

# Запуск главного цикла
root.mainloop()
