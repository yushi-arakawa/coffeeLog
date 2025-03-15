import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import date
from sqlalchemy.ext.declarative import declarative_base

# データベースの設定
DATABASE_URL = "sqlite:///coffee.db"  # SQLiteファイルとして保存される

# ORMベース
Base = declarative_base()

# ---- 各テーブル定義 ----

class Bean(Base):
    __tablename__ = 'beans'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    origin = Column(String)  # 産地
    roast_level = Column(String)  # 浅煎り/中煎り/深煎り
    roast_date = Column(Date)
    note = Column(String)

class Water(Base):
    __tablename__ = 'waters'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)  # 水の名前
    hardness = Column(Float)  # 硬度
    ph = Column(Float)  # pH値
    note = Column(String)  # メモ

class Grinder(Base):
    __tablename__ = 'grinders'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    model = Column(String)
    note = Column(String)  # メモ

class Dripper(Base):
    __tablename__ = 'drippers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    model = Column(String)
    filter_type = Column(String)  # ペーパー/金属 etc.
    note = Column(String)  # メモ

class BrewRecord(Base):
    __tablename__ = 'brew_records'
    id = Column(Integer, primary_key=True)
    bean_id = Column(Integer, ForeignKey('beans.id'))
    water_id = Column(Integer, ForeignKey('waters.id'))
    grinder_id = Column(Integer, ForeignKey('grinders.id'))
    dripper_id = Column(Integer, ForeignKey('drippers.id'))

    room_temp = Column(Float)
    humidity = Column(Float)

    bean_amount = Column(Float)  # g
    grind_size = Column(String)  # 粒度
    bloom_water = Column(Float)  # g
    bloom_time = Column(Integer)  # 秒

    total_water = Column(Float)  # g
    target_yield = Column(Float)  # g
    actual_yield = Column(Float)  # g
    brew_time = Column(Integer)  # 秒
    water_temp = Column(Float)  # 湯温

    pour_speed = Column(Float)  # ml/sec
    pour_count = Column(Integer)  # 回数

    drink_temp = Column(Float)  # 飲用温度

    tds = Column(Float)
    taste_acidity = Column(Integer)  # 1-5
    taste_sweetness = Column(Integer)
    taste_bitterness = Column(Integer)
    aroma = Column(Integer)
    total_score = Column(Integer)
    flavor_note = Column(String)

    bean = relationship('Bean')
    water = relationship('Water')
    grinder = relationship('Grinder')
    dripper = relationship('Dripper')


class ExtractionLog(Base):
    __tablename__ = "extraction_logs"
    id = Column(Integer, primary_key=True)
    bean_id = Column(Integer, ForeignKey('beans.id'))
    method = Column(String)
    water_temp = Column(Float)
    grind_size = Column(String)
    extraction_time = Column(Float)
    rating = Column(Float)
    note = Column(String)
    date = Column(Date)

    bean = relationship("Bean", back_populates="extractions")

# Bean側の関係も追加
Bean.extractions = relationship("ExtractionLog", back_populates="bean", cascade="all, delete-orphan")


# ---- DBセットアップ ----

def init_db():

    base_path = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_path, 'coffee_brew.db')
    engine = create_engine(f'sqlite:///{db_path}', echo=True)
    Base.metadata.create_all(engine)
    print("DBを読み込みました。")
    return engine

if __name__ == "__main__":
    init_db()