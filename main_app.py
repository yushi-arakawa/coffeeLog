import os
import customtkinter as ctk
from PIL import Image, ImageTk
from sqlalchemy.orm import sessionmaker
from setup_db import init_db, Bean
from datetime import date
import random

# フォント
FONT_TITLE = ("Montserrat", 30)
FONT_HEADER = ("Montserrat", 18)
FONT_NORMAL = ("Montserrat", 12)
FONT_BUTTON = ("Montserrat", 12, "bold")

# DB接続
engine = init_db()
Session = sessionmaker(bind=engine)
session = Session()

# GUI設定       
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class BeanApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("coffeelog")
        self.geometry("1150x700")
        self.selected_bean_id = None  # 編集・削除対象ID

        # パスの設定
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(BASE_DIR, "icon.png")

        # アイコンの設定（Dockやウィンドウに反映）
        icon_image = ImageTk.PhotoImage(Image.open(icon_path))
        self.iconphoto(True, icon_image)

        # ナビゲーションバー
        self.nav_frame = ctk.CTkFrame(self,width=200)
        self.nav_frame.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="ns")

        # 上部のスペース
        self.nav_frame.grid_rowconfigure(0, weight=1) 

        # ボタン（フォントサイズ調整付き）
        button_font = ctk.CTkFont(size=15)  # 文字サイズ共通 

        self.bean_button = ctk.CTkButton(self.nav_frame, text="Beans", width=100, height=85, command=self.show_bean_page,font=button_font)
        self.bean_button.grid(row=1, column=0, pady=10)

        self.water_button = ctk.CTkButton(self.nav_frame, text="Water", width=100, height=85, command=self.show_water_page,font=button_font)
        self.water_button.grid(row=2, column=0, pady=10)

        self.grinder_button = ctk.CTkButton(self.nav_frame, text="Grinder", width=100, height=85, command=self.show_grinder_page,font=button_font)
        self.grinder_button.grid(row=3, column=0, pady=10)

        self.dripper_button = ctk.CTkButton(self.nav_frame, text="Dripper", width=100, height=85, command=self.show_dripper_page,font=button_font)
        self.dripper_button.grid(row=4, column=0, pady=10)

        self.recipe_button = ctk.CTkButton(self.nav_frame, text="Recipe", width=100, height=85, command=self.show_recipe_page,font=button_font)
        self.recipe_button.grid(row=5, column=0, pady=10)

        self.recipe_button = ctk.CTkButton(self.nav_frame, text="analysis", width=100, height=85, command=self.show_analysis_page,font=button_font)
        self.recipe_button.grid(row=6, column=0, pady=10)

        # ★ 下部のスペース
        self.nav_frame.grid_rowconfigure(7, weight=1)

        # コンテンツフレーム
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.show_bean_page()  # 初期表示

    # ----------------- Beanページ ---------------------
    def show_bean_page(self):
        self.clear_content_frame()

        title_label = ctk.CTkLabel(self.content_frame, text="Beans", font=FONT_TITLE)
        title_label.grid(row=0, column=0, columnspan=2,pady=(10, 20))

        # テーブル (スクロール対応)
        self.table_frame = ctk.CTkScrollableFrame(self.content_frame, height=400)
        self.table_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        # content_frameの列設定 (右に伸びるように)
        self.content_frame.grid_rowconfigure(1, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)  
        self.content_frame.grid_columnconfigure(1, weight=0)

        # フォーム
        self.form_frame = ctk.CTkFrame(self.content_frame)
        self.form_frame.grid(row=2, column=0, sticky="w", padx=10, pady=10)

        # フォームの幅を狭めるためにcolumnconfigureで左寄せを設定
        self.form_frame.grid_columnconfigure(0, weight=0)
        self.form_frame.grid_columnconfigure(1, weight=1)

        # 右側にtips用のフレーム
        self.tips_frame = ctk.CTkFrame(self.content_frame)
        self.tips_frame.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)

        # tips内の内容
        tips_label = ctk.CTkLabel(self.tips_frame, text="ああああ")
        tips_label.grid(row=0, column=0, padx=10, pady=10)

        # content_frame の列幅調整
        self.content_frame.grid_columnconfigure(0, weight=1)  # フォーム
        self.content_frame.grid_columnconfigure(1, weight=30)  # チップス（広げる）

        self.create_form()
        self.show_bean_list()
        #self.create_tips()

    def show_bean_list(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        headers = ["name", "origin", "roast level", "roast date", "note", "", "","",""]
        for col, header in enumerate(headers):
            label = ctk.CTkLabel(self.table_frame, text=header, font=FONT_HEADER)
            label.grid(row=0, column=col, padx=5, pady=5, sticky="ew")

        beans = session.query(Bean).all()
        for row_idx, bean in enumerate(beans, start=1):
            values = [
                bean.name, bean.origin, bean.roast_level,
                bean.roast_date.strftime("%Y-%m-%d") if bean.roast_date else "", bean.note or "",""
            ]
            for col_idx, value in enumerate(values):
                label = ctk.CTkLabel(self.table_frame, text=value, width=120)
                label.grid(row=row_idx, column=col_idx, padx=5, pady=2, sticky="ew")

            # 編集・削除ボタン
            edit_button = ctk.CTkButton(self.table_frame, text="edit", width=70, command=lambda b=bean: self.edit_bean(b))
            edit_button.grid(row=row_idx, column=6, padx=5)
            delete_button = ctk.CTkButton(self.table_frame, text="delete", width=70, command=lambda b=bean: self.delete_bean(b.id))
            delete_button.grid(row=row_idx, column=7, padx=5)

    def create_form(self):
        labels = ["name", "origin", "roast level", "roast date (YYYY-MM-DD)", "note"]
        self.entries = {}

        for i, label_text in enumerate(labels):
            label = ctk.CTkLabel(self.form_frame, text=label_text, width=200)
            label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry = ctk.CTkEntry(self.form_frame, width=400)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[label_text] = entry

        save_button = ctk.CTkButton(self.form_frame, text="ok", command=self.save_bean)
        save_button.grid(row=len(labels), column=0, columnspan=2, pady=10, sticky="n")

    def clear_form(self):
        self.selected_bean_id = None
        for entry in self.entries.values():
            entry.delete(0, ctk.END)

    def edit_bean(self, bean):
        self.selected_bean_id = bean.id
        self.entries["name"].delete(0, ctk.END)
        self.entries["name"].insert(0, bean.name)
        self.entries["origin"].delete(0, ctk.END)
        self.entries["origin"].insert(0, bean.origin)
        self.entries["roast level"].delete(0, ctk.END)
        self.entries["roast level"].insert(0, bean.roast_level)
        self.entries["roast date (YYYY-MM-DD)"].delete(0, ctk.END)
        self.entries["roast date (YYYY-MM-DD)"].insert(0, bean.roast_date.strftime("%Y-%m-%d") if bean.roast_date else "")
        self.entries["note"].delete(0, ctk.END)
        self.entries["note"].insert(0, bean.note or "")

    def save_bean(self):
        data = {key: entry.get() for key, entry in self.entries.items()}
        roast_date = date.fromisoformat(data["roast date (YYYY-MM-DD)"]) if data["roast date (YYYY-MM-DD)"] else None

        if self.selected_bean_id:
            bean = session.query(Bean).get(self.selected_bean_id)
            bean.name = data["name"]
            bean.origin = data["origin"]
            bean.roast_level = data["roast level"]
            bean.roast_date = roast_date
            bean.note = data["note"]
        else:
            bean = Bean(name=data["name"], origin=data["origin"], roast_level=data["roast level"], roast_date=roast_date, note=data["note"])
            session.add(bean)

        session.commit()
        session.refresh(bean)
        self.clear_form()
        self.show_bean_list()

    def delete_bean(self, bean_id):
        bean = session.query(Bean).get(bean_id)
        if bean:
            session.delete(bean)
            session.commit()
        self.show_bean_list()

    # ----------------- 共通機能 ---------------------
    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    # ----------------- 他ページ ---------------------
    def show_water_page(self):
        self.clear_content_frame()
        ctk.CTkLabel(self.content_frame, text="Water", font=FONT_TITLE).pack(pady=20)
        self.clear_content_frame()

        title_label = ctk.CTkLabel(self.content_frame, text="Water", font=FONT_TITLE)
        title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

        # テーブル (スクロール対応)
        self.water_table_frame = ctk.CTkScrollableFrame(self.content_frame, height=400)
        self.water_table_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        self.content_frame.grid_rowconfigure(1, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=0)

        # フォーム
        self.water_form_frame = ctk.CTkFrame(self.content_frame)
        self.water_form_frame.grid(row=2, column=0, sticky="w", padx=10, pady=10)

        self.water_form_frame.grid_columnconfigure(0, weight=0)
        self.water_form_frame.grid_columnconfigure(1, weight=1)

        # Tipsフレーム
        self.water_tips_frame = ctk.CTkFrame(self.content_frame)
        self.water_tips_frame.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)

        tips_label = ctk.CTkLabel(self.water_tips_frame, text="水の性質や硬度などの説明")
        tips_label.grid(row=0, column=0, padx=10, pady=10)

        # content_frame の列幅調整
        self.content_frame.grid_columnconfigure(0, weight=1)  # フォーム
        self.content_frame.grid_columnconfigure(1, weight=30)  # チップス（広げる）

        self.create_water_form()
        self.show_water_list()

    def show_water_list(self):
        for widget in self.water_table_frame.winfo_children():
            widget.destroy()

        headers = ["name", "hardness", "pH", "note", "", "", "",""]
        for col, header in enumerate(headers):
            label = ctk.CTkLabel(self.water_table_frame, text=header, font=FONT_HEADER)
            label.grid(row=0, column=col, padx=5, pady=5, sticky="ew")

        from setup_db import Water  # Waterモデルのインポート
        waters = session.query(Water).all()

        for row_idx, water in enumerate(waters, start=1):
            values = [
                water.name or "",
                str(water.hardness) if water.hardness is not None else "",
                str(water.ph) if water.ph is not None else "",
                water.note or "",
                "",
                ""
            ]
            for col_idx, value in enumerate(values):
                label = ctk.CTkLabel(self.water_table_frame, text=value, width=120)
                label.grid(row=row_idx, column=col_idx, padx=5, pady=2, sticky="ew")

            # 編集・削除ボタン
            edit_button = ctk.CTkButton(self.water_table_frame, text="edit", width=70, command=lambda w=water: self.edit_water(w))
            edit_button.grid(row=row_idx, column=6, padx=5)
            delete_button = ctk.CTkButton(self.water_table_frame, text="delete", width=70, command=lambda w=water: self.delete_water(w.id))
            delete_button.grid(row=row_idx, column=7, padx=5)

    def create_water_form(self):
        labels = ["name", "hardness", "pH", "note"]
        self.water_entries = {}

        for i, label_text in enumerate(labels):
            label = ctk.CTkLabel(self.water_form_frame, text=label_text, width=200)
            label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry = ctk.CTkEntry(self.water_form_frame, width=400)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.water_entries[label_text] = entry

            save_button = ctk.CTkButton(self.water_form_frame, text="ok", command=self.save_water)
            save_button.grid(row=len(labels), column=0, columnspan=2, pady=10, sticky="n")

            self.selected_water_id = None

    def clear_water_form(self):
        self.selected_water_id = None
        for entry in self.water_entries.values():
            entry.delete(0, ctk.END)

    def edit_water(self, water):
        self.selected_water_id = water.id
        self.water_entries["name"].delete(0, ctk.END)
        self.water_entries["name"].insert(0, water.name)
        self.water_entries["hardness"].delete(0, ctk.END)
        self.water_entries["hardness"].insert(0, str(water.hardness or ""))
        self.water_entries["pH"].delete(0, ctk.END)
        self.water_entries["pH"].insert(0, str(water.ph or ""))
        self.water_entries["note"].delete(0, ctk.END)
        self.water_entries["note"].insert(0, water.note or "")

    def save_water(self):
        data = {key: entry.get() for key, entry in self.water_entries.items()}
        hardness = float(data["hardness"]) if data["hardness"] else None
        ph = float(data["pH"]) if data["pH"] else None

        from setup_db import Water  # Waterモデルのインポート

        if self.selected_water_id:
            water = session.query(Water).get(self.selected_water_id)
            water.name = data["name"]
            water.hardness = hardness
            water.ph = ph
            water.note = data["note"]
        else:
            water = Water(
                name=data["name"], hardness=hardness, ph=ph, note=data["note"]
            )
            session.add(water)

        session.commit()
        session.refresh(water)
        self.clear_water_form()
        self.show_water_list()

    def delete_water(self, water_id):
        from setup_db import Water  # Waterモデルのインポート
        water = session.query(Water).get(water_id)
        if water:
            session.delete(water)
            session.commit()
        self.show_water_list()

    def show_grinder_page(self):
        self.clear_content_frame()
        ctk.CTkLabel(self.content_frame, text="Grinder Page", font=FONT_TITLE).pack(pady=20)
        self.clear_content_frame()

        title_label = ctk.CTkLabel(self.content_frame, text="Grinder", font=FONT_TITLE)
        title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

        # テーブル (スクロール対応)
        self.grinder_table_frame = ctk.CTkScrollableFrame(self.content_frame, height=400)
        self.grinder_table_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        self.content_frame.grid_rowconfigure(1, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=0)

        # フォーム
        self.grinder_form_frame = ctk.CTkFrame(self.content_frame)
        self.grinder_form_frame.grid(row=2, column=0, sticky="w", padx=10, pady=10)

        self.grinder_form_frame.grid_columnconfigure(0, weight=0)
        self.grinder_form_frame.grid_columnconfigure(1, weight=1)

        # Tipsフレーム
        self.grinder_tips_frame = ctk.CTkFrame(self.content_frame)
        self.grinder_tips_frame.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)

        tips_label = ctk.CTkLabel(self.grinder_tips_frame, text="グラインダーの情報や性能を登録・管理できます")
        tips_label.grid(row=0, column=0, padx=10, pady=10)

        # content_frame の列幅調整
        self.content_frame.grid_columnconfigure(0, weight=1)  # フォーム
        self.content_frame.grid_columnconfigure(1, weight=30)  # チップス（広げる）

        self.create_grinder_form()
        self.show_grinder_list()

    def show_grinder_list(self):
        for widget in self.grinder_table_frame.winfo_children():
            widget.destroy()

        headers = ["name", "model", "note","","","",""]
        for col, header in enumerate(headers):
            label = ctk.CTkLabel(self.grinder_table_frame, text=header, font=FONT_HEADER)
            label.grid(row=0, column=col, padx=5, pady=5, sticky="ew")

        from setup_db import Grinder  # Grinderモデルのインポート
        grinders = session.query(Grinder).all()

        for row_idx, grinder in enumerate(grinders, start=1):
            values = [
                grinder.name or "",
                str(grinder.model) if grinder.model is not None else "",
                str(grinder.note) if grinder.note is not None else "",
                "",
                "",
                ""
            ]
            for col_idx, value in enumerate(values):
                label = ctk.CTkLabel(self.grinder_table_frame, text=value, width=120)
                label.grid(row=row_idx, column=col_idx, padx=5, pady=2, sticky="ew")

            # 編集・削除ボタン
            edit_button = ctk.CTkButton(self.grinder_table_frame, text="edit", width=70, command=lambda g=grinder: self.edit_grinder(g))
            edit_button.grid(row=row_idx, column=6, padx=5)
            delete_button = ctk.CTkButton(self.grinder_table_frame, text="delete", width=70, command=lambda g=grinder: self.delete_grinder(g.id))
            delete_button.grid(row=row_idx, column=7, padx=5)

    def create_grinder_form(self):
        labels = ["name", "model", "note"]
        self.grinder_entries = {}

        for i, label_text in enumerate(labels):
            label = ctk.CTkLabel(self.grinder_form_frame, text=label_text, width=200)
            label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry = ctk.CTkEntry(self.grinder_form_frame, width=400)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.grinder_entries[label_text] = entry

        save_button = ctk.CTkButton(self.grinder_form_frame, text="ok", command=self.save_grinder)
        save_button.grid(row=len(labels), column=0, columnspan=2, pady=10, sticky="n")

        self.selected_grinder_id = None

    def clear_grinder_form(self):
        self.selected_grinder_id = None
        for entry in self.grinder_entries.values():
            entry.delete(0, ctk.END)

    def edit_grinder(self, grinder):
        self.selected_grinder_id = grinder.id
        self.grinder_entries["name"].delete(0, ctk.END)
        self.grinder_entries["name"].insert(0, grinder.name)
        self.grinder_entries["model"].delete(0, ctk.END)
        self.grinder_entries["model"].insert(0, grinder.model)
        self.grinder_entries["note"].delete(0, ctk.END)
        self.grinder_entries["note"].insert(0, grinder.note)

    def save_grinder(self):
        data = {key: entry.get() for key, entry in self.grinder_entries.items()}

        from setup_db import Grinder  # Grinderモデルのインポート

        if self.selected_grinder_id:
            grinder = session.query(Grinder).get(self.selected_grinder_id)
            grinder.name = data["name"]
            grinder.model = data["model"]
            grinder.note = data["note"]
        else:
            grinder = Grinder(
                name=data["name"],
                model=data["model"],
                note=data["note"]
            )
            session.add(grinder)

        session.commit()
        session.refresh(grinder)
        self.clear_grinder_form()
        self.show_grinder_list()

    def delete_grinder(self, grinder_id):
        from setup_db import Grinder  # Grinderモデルのインポート
        grinder = session.query(Grinder).get(grinder_id)
        if grinder:
            session.delete(grinder)
            session.commit()
        self.show_grinder_list()

    def show_dripper_page(self):
        self.clear_content_frame()
        ctk.CTkLabel(self.content_frame, text="Dripper", font=FONT_TITLE).pack(pady=20)
        self.clear_content_frame()

        title_label = ctk.CTkLabel(self.content_frame, text="Dripper", font=FONT_TITLE)
        title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

        # テーブル (スクロール対応)
        self.dripper_table_frame = ctk.CTkScrollableFrame(self.content_frame, height=400)
        self.dripper_table_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        self.content_frame.grid_rowconfigure(1, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=0)

        # フォーム
        self.dripper_form_frame = ctk.CTkFrame(self.content_frame)
        self.dripper_form_frame.grid(row=2, column=0, sticky="w", padx=10, pady=10)

        self.dripper_form_frame.grid_columnconfigure(0, weight=0)
        self.dripper_form_frame.grid_columnconfigure(1, weight=1)

        # Tipsフレーム
        self.dripper_tips_frame = ctk.CTkFrame(self.content_frame)
        self.dripper_tips_frame.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)

        tips_label = ctk.CTkLabel(self.dripper_tips_frame, text="ドリッパーの情報や性能を登録・管理できます")
        tips_label.grid(row=0, column=0, padx=10, pady=10)

        # content_frame の列幅調整
        self.content_frame.grid_columnconfigure(0, weight=1)  # フォーム
        self.content_frame.grid_columnconfigure(1, weight=30)  # チップス（広げる）

        self.create_dripper_form()
        self.show_dripper_list()

    def show_dripper_list(self):
            for widget in self.dripper_table_frame.winfo_children():
                widget.destroy()

            headers = ["name", "model", "note","filter type","note","",""]
            for col, header in enumerate(headers):
                label = ctk.CTkLabel(self.dripper_table_frame, text=header, font=FONT_HEADER)
                label.grid(row=0, column=col, padx=5, pady=5, sticky="ew")

            from setup_db import Dripper
            drippers = session.query(Dripper).all()

            for row_idx, dripper in enumerate(drippers, start=1):
                values = [
                    dripper.name or "",
                    str(dripper.model) if dripper.model is not None else "",
                    str(dripper.filter_type) if dripper.filter_type is not None else "",
                    str(dripper.note) if dripper.note is not None else "",
                    "",
                    ""
                ]
                for col_idx, value in enumerate(values):
                    label = ctk.CTkLabel(self.dripper_table_frame, text=value, width=120)
                    label.grid(row=row_idx, column=col_idx, padx=5, pady=2, sticky="ew")

                # 編集・削除ボタン
                edit_button = ctk.CTkButton(self.dripper_table_frame, text="edit", width=70, command=lambda d=dripper: self.edit_dripper(d))
                edit_button.grid(row=row_idx, column=6, padx=5)
                delete_button = ctk.CTkButton(self.dripper_table_frame, text="delete", width=70, command=lambda d=dripper: self.delete_dripper(d.id))
                delete_button.grid(row=row_idx, column=7, padx=5)

    def create_dripper_form(self):
        labels = ["name", "model", "filter type","note"]
        self.dripper_entries = {}

        for i, label_text in enumerate(labels):
            label = ctk.CTkLabel(self.dripper_form_frame, text=label_text, width=200)
            label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry = ctk.CTkEntry(self.dripper_form_frame, width=400)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.dripper_entries[label_text] = entry

        save_button = ctk.CTkButton(self.dripper_form_frame, text="ok", command=self.save_dripper)
        save_button.grid(row=len(labels), column=0, columnspan=2, pady=10, sticky="n")

        self.selected_dripper_id = None

    def clear_dripper_form(self):
        self.selected_dripper_id = None
        for entry in self.dripper_entries.values():
            entry.delete(0, ctk.END)

    def edit_dripper(self, dripper):
        self.selected_dripper_id = dripper.id
        self.dripper_entries["name"].delete(0, ctk.END)
        self.dripper_entries["name"].insert(0, dripper.name)
        self.dripper_entries["model"].delete(0, ctk.END)
        self.dripper_entries["model"].insert(0, dripper.model)
        self.dripper_entries["filter type"].delete(0, ctk.END)
        self.dripper_entries["filtertype"].insert(0, dripper.note)
        self.dripper_entries["note"].delete(0, ctk.END)
        self.dripper_entries["note"].insert(0, dripper.note)

    def save_dripper(self):
        data = {key: entry.get() for key, entry in self.dripper_entries.items()}

        from setup_db import Dripper 

        if self.selected_grinder_id:
            dripper = session.query(Dripper).get(self.selected_dripper_id)
            dripper.name = data["name"]
            dripper.model = data["model"]
            dripper.filter_type = data["filter type"]
            dripper.note = data["note"]
        else:
            dripper = Dripper(
                name=data["name"],
                model=data["model"],
                filter_type=data["filter type"],
                note=data["note"]
            )
            session.add(dripper)

        session.commit()
        session.refresh(dripper)
        self.clear_dripper_form()
        self.show_dripper_list()

    def delete_dripper(self, dripper_id):
        from setup_db import Dripper
        dripper = session.query(Dripper).get(dripper_id)
        if dripper:
            session.delete(dripper)
            session.commit()
        self.show_dripper_list()

    def show_recipe_page(self):
        self.clear_content_frame()
        ctk.CTkLabel(self.content_frame, text="Recipe Page", font=FONT_TITLE).pack(pady=20)

    def show_analysis_page(self):
        self.clear_content_frame()
        ctk.CTkLabel(self.content_frame, text="analysis Page", font=FONT_TITLE).pack(pady=20)


if __name__ == "__main__":
    app = BeanApp()
    app.mainloop()