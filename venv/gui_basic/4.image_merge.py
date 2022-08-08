from tkinter import *
import tkinter.ttk as ttk

#### Functional Function ###########################
# File add function
from tkinter import filedialog # Need for adding the file
def add_file():
    # filedialog.askopenfilenames 으로 선택된 파일들의 절대 경로들을 리스트 형태로 저장하여 반환
    files = filedialog.askopenfilenames(title="이미지 파일을 선택하세요", filetypes=(("PNG 파일", "*.png"), ("모든 파일", "*.*")), initialdir=r"C:/")
    for i in files:
        list_box.insert(END, i)

# File list delete function
def del_file():
    # (listcombo_name).curselection() 으로 선택한 목록의 인덱스 값들을 리스트의 형태로 저장하여 반환
    # 리스트는 앞에서부터 삭제를 하게 되면 뒤에서 지울 데이터의 인덱스의 값이 변하기 때문에 인덱스가 큰 순서대로 지운다
    #  ㄴ reversed 해주는 이유
    for index in reversed(list_box.curselection()):
        list_box.delete(index)

# Save path setting function
def browse_dest_path():
    folder_selected = filedialog.askdirectory()
    if folder_selected == '':
        return
    txt_dest_path.delete(0, END)
    txt_dest_path.insert(END, folder_selected)

import tkinter.messagebox as msg
from PIL import Image
import os


# Execute function
def start():
    # cmb_width.get() 가로 설정 값 가져오기 [원본유지 1024 800 640]
    # cmb_space.get() 간격 설정 값 가져오기 [없음 좁게 보통 넓게]
    # cmb_format.get() 포맷형식 값 가져오기 [PNG JPG BMP]
    try:
        # File list isnull check
        if list_box.size() == 0:
            msg.showerror("오류", "이미지 파일을 추가하십시오.")
            return

        # File path isnull check
        if txt_dest_path.get() == "":
            msg.showerror("오류", "저장 경로를 설정해주십시오.")
            return

        # Check merge option settion
        cmb_width_get = cmb_width.get()
        cmb_space_get = cmb_space.get()
        cmb_format_get = cmb_format.get()
        if cmb_width_get == "원본유지":
            cmb_width_get = -1 # -1 일때는 원본 기준
        else:
            cmb_width_get = int(cmb_width_get)
        if cmb_space_get == "좁게":
            cmb_space_get = 20
        elif cmb_space_get == "보통":
            cmb_space_get = 40
        elif cmb_space_get == "넓게":
            cmb_space_get = 80
        else:
            cmb_space_get = 0
        cmb_format_get = cmb_format_get.lower()  # PNG JPG BMP을 가져와서 소문자로 저장

        # file merge function
        file_list = list_box.get(0, END) # 리스트 박스 안에 있는 목록들을 튜플 형태로 저장하여 반환
        imgs = [Image.open(i) for i in file_list]  # 이미지 정보를 저장
        widths, heights = zip(*(i.size for i in imgs))  # unzip 기능으로 이미지 정보에서 x, y값을 뽑아 낸 후 x, y값을 따로 저장

        if cmb_width_get == -1: # 가로 설정이 원본일 때
            pass
        elif cmb_width_get == 1024: # 가로 설정이 1024 일 때
            widths, heights = [1024 for i in widths], [int(v*1024 / i) for i, v in zip(widths, heights)]
            imgs = [z.resize((i, v), Image.Resampling.LANCZOS) for i, v, z in zip(widths, heights, imgs)] # 이미지 파일을 변경된 해상도에 맞게 리사이즈
        elif cmb_width_get == 800: # 가로 설정이 800일 때
            resize_y = [int(v*800 / i) for i, v in zip(widths, heights)]
            widths = [800 for i in widths]
            heights = resize_y
            imgs = [z.resize((i, v), Image.Resampling.LANCZOS) for i, v, z in zip(widths, heights, imgs)] # 이미지 파일을 변경된 해상도에 맞게 리사이즈
        elif cmb_width_get == 640: # 가로 설정이 640일 때
            resize_y = [int(v*640 / i) for i, v in zip(widths, heights)]
            widths = [640 for i in widths]
            heights = resize_y
            imgs = [z.resize((i, v), Image.Resampling.LANCZOS) for i, v, z in zip(widths, heights, imgs)] # 이미지 파일을 변경된 해상도에 맞게 리사이즈
        else:
            pass

        max_width, total_height = max(widths), sum(heights) # 이미지 병합을 위한 가로 길이 세로 길이 설정
        y_offset = cmb_space_get  # y 위치
        list_box_size = list_box.size() # 리스트 박스 안에 있는 항목 갯수 저장
        total_height += (list_box_size+1) * y_offset
        result_img = Image.new("RGB", (max_width, total_height), (255, 255, 255))
        for idx, img in enumerate(imgs):
            result_img.paste(img, (0, y_offset)) # 이미지 삽입
            y_offset += img.size[1] + cmb_space_get # 이미지 삽입 후 다음 이미지가 저장될 y좌표값 설정
            p_var.set( (idx+1) / list_box_size * 100 ) # 진행률 p_var에 반영
            progress_bar.update() # Progress bar 변경점 반영

        dest_path = os.path.join(txt_dest_path.get(), "imageMerge_result."+cmb_format_get)
        result_img.save(dest_path)
        msg.showinfo("알림", "작업이 완료되었습니다.")
    except Exception as err:
        msg.showerror("오류", err)

#####################################################



root = Tk()
#### Create Frame 설정 ###########################################
root.title("JH Image Merge Program")
root.geometry("640x480+800+300") # 해상도 설정 # 프로그램 뜨는 위치도 설정 가능 (3번째 인자는 x좌표 4인자는 y좌표)
root.resizable(False, False) # 창크기 변경(x, y) 허용 가능 여부설정

# File Frame
file_frame = Frame(root)
file_frame.pack(pady=10, fill="x")

btn_add_file = Button(file_frame, padx=5, pady=5, width=12, text="파일추가", command=add_file)
btn_add_file.pack(side="left", padx=10)
btn_del_file = Button(file_frame, padx=5, pady=5, width=12, text="선택삭제", command=del_file)
btn_del_file.pack(side="right", padx=10)

# List Frame
list_frame = Frame(root)
list_frame.pack(fill="both")

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")

list_box = Listbox(list_frame, selectmode="extended", height=15, yscrollcommand=scrollbar.set)
list_box.pack(side="left", fill="both", padx=10, pady=5, expand=True)
scrollbar.config(command=list_box.yview)

# Save path Frame
path_frame = LabelFrame(root, text="저장경로")
path_frame.pack(fill="x")

txt_dest_path = Entry(path_frame) # 한 줄이니까 Text 말고 entry로
txt_dest_path.pack(side="left", fill="x", padx=2, expand=True)

btn_dest_path = Button(path_frame, text="찾아보기", width=10, command=browse_dest_path)
btn_dest_path.pack(side="right", pady=5, padx=5)

# Option Frame
option_frame = LabelFrame(root, text="옵션")
option_frame.pack(fill="x")

# 가로 넓이 옵션 프레임
lbl_width = Label(option_frame, text="가로넓이", width=8)
lbl_width.pack(side="left")

# 가로 넓이 옵션 Combo
opt_width = ["원본유지", "1024", "800", "640"]
cmb_width = ttk.Combobox(option_frame, state="readonly", values=opt_width, width=20)
cmb_width.current(0)
cmb_width.pack(side="left", padx=2, pady=5)

# 간격 옵션 프레임
lbl_space = Label(option_frame, text="간격", width=5)
lbl_space.pack(side="left")

# 간격 옵션 Combo
opt_space = ["없음", "좁게", "보통", "넓게"]
cmb_space = ttk.Combobox(option_frame, state="readonly", values=opt_space, width=20)
cmb_space.current(0)
cmb_space.pack(side="left")

# 파일 포맷 옵션 프레임
lbl_format = Label(option_frame, text="포맷 형식", width=10)
lbl_format.pack(side="left")

# 파일 포맷 옵션 Combo
opt_format = ["PNG", "JPG", "BMP"]
cmb_format = ttk.Combobox(option_frame, state="readonly", values=opt_format, width=20)
cmb_format.current(0)
cmb_format.pack(side="left", padx=(0, 10))

# 진행 상황 (Progress bar)
frame_progress = LabelFrame(root, text="진행상황")
frame_progress.pack(fill="x")

p_var = DoubleVar()
progress_bar = ttk.Progressbar(frame_progress, maximum=100, variable=p_var, mode="determinate")
progress_bar.pack(fill="x")

# 실행 프레임
run_frame = Frame(root)
run_frame.pack(fill="x", padx=2, pady=1)

btn_start = Button(run_frame, padx=5, pady=5, text="시작", width=12, command=start)
btn_start.pack(side="right")

btn_close = Button(run_frame, padx=5, pady=5, text="닫기", width=12, command=root.quit)
btn_close.pack(side="left")

root.mainloop()