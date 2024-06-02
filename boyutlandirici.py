import os
from tkinter import Tk, Label, Button, Entry, filedialog, messagebox
from PIL import Image


def calculate_average_size(folder_path):
    total_width, total_height, count = 0, 0, 0
    file_list = os.listdir(folder_path)
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        if file_name.endswith('.jpg') or file_name.endswith('.jpeg') or file_name.endswith('.png'):
            image = Image.open(file_path)
            width, height = image.size
            total_width += width
            total_height += height
            count += 1
    if count > 0:
        average_width = total_width // count
        average_height = total_height // count
        return average_width, average_height
    else:
        return 0, 0


def select_folder():
    folder_path = filedialog.askdirectory(title="Yeniden boyutlandırılacak klasörü seçin")
    if not folder_path:
        return
    average_width, average_height = calculate_average_size(folder_path)
    folder_path_label.config(text=f"Klasör Yolu: {folder_path}")
    average_size_label.config(text=f"Ortalama Boyut: {average_width} x {average_height}")


def resize_images():
    try:
        width = int(width_entry.get())
        height = int(height_entry.get())
    except ValueError:
        result_label.config(text="Lütfen geçerli bir genişlik ve yükseklik girin.")
        return

    folder_path = folder_path_label.cget("text").replace("Klasör Yolu: ", "")
    if not folder_path:
        result_label.config(text="Lütfen önce bir klasör seçin.")
        return

    output_folder = os.path.join(folder_path, 'boyutlanmis')
    os.makedirs(output_folder, exist_ok=True)

    file_list = os.listdir(folder_path)
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        if file_name.endswith('.jpg') or file_name.endswith('.jpeg') or file_name.endswith('.png'):
            try:
                image = Image.open(file_path)
                image = image.convert("RGB")  # Görüntüyü RGB moduna dönüştür
                resized_image = image.resize((width, height), Image.ANTIALIAS)
                output_path = os.path.join(output_folder, file_name)
                resized_image.save(output_path, "JPEG")
            except Exception as e:
                print(f"Error processing image {file_path}: {e}")

    messagebox.showinfo("Başarılı", "Tüm görüntüler yeniden boyutlandırıldı ve kaydedildi.")
    result_label.config(text="Tüm görüntüler yeniden boyutlandırıldı ve kaydedildi.")
    width_entry.delete(0, 'end')
    height_entry.delete(0, 'end')
    folder_path_label.config(text="")
    average_size_label.config(text="")


root = Tk()
root.title("Görüntü Yeniden Boyutlandırma")
root.geometry("400x350")

label = Label(root, text="Görüntüleri Yeniden Boyutlandır")
label.pack(pady=10)

select_button = Button(root, text="Klasör Seç", command=select_folder)
select_button.pack(pady=10)

folder_path_label = Label(root, text="")
folder_path_label.pack(pady=5)

average_size_label = Label(root, text="")
average_size_label.pack(pady=5)

width_label = Label(root, text="Genişlik:")
width_label.pack(pady=5)
width_entry = Entry(root)
width_entry.pack(pady=5)

height_label = Label(root, text="Yükseklik:")
height_label.pack(pady=5)
height_entry = Entry(root)
height_entry.pack(pady=5)

start_button = Button(root, text="İşlemi Başlat", command=resize_images)
start_button.pack(pady=10)

result_label = Label(root, text="")
result_label.pack(pady=20)

root.mainloop()
