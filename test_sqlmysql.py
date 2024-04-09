from sqlalchemy import create_engine, text
engine = create_engine("mysql+pymysql://root:123456@10.185.5.86:3306/test", echo=True)


with engine.connect() as conn:
    result = conn.execute(text("select 'hello world'"))
    print(result.all())