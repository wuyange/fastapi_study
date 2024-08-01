# coding: utf-8
from sqlalchemy import Column, Date, DateTime, Integer, SmallInteger, Text, UniqueConstraint, text,DECIMAL,Numeric, String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.mysql import TIMESTAMP
from uuid import uuid1
from . import Base
metadata = Base.metadata


class DoctorScheduling(Base):
    __tablename__ = 'doctor_scheduling'
    __table_args__ = {'comment': '医生排班信息表'}

    id: Mapped[str] = mapped_column(String(36), primary_key=True, server_default=lambda: str(uuid1()), comment='主键Id')
    dno = mapped_column(Text, nullable=False, index=True, server_default=text("''::text"), comment='所属医生编号')
    nsnum = mapped_column(Integer, comment='号源总数')
    nsnumstock = mapped_column(Integer, comment='号源库存数')
    nsindex = mapped_column(Text, unique=True, server_default=text("''::text"), comment='号源编号')
    dnotime = mapped_column(Date, comment='排班日期，年-月-日')
    tiemampmstr = mapped_column(Text, server_default=text("''::text"), comment='号源时段字符串显示')
    ampm = mapped_column(Text, server_default=text("''::text"), comment='医生工作日：上午 还是 下午')
    create_time = mapped_column(TIMESTAMP(precision=0), server_default=text("now()"), comment='创建时间')
    enable = mapped_column(Integer, comment='是否可用（1：是 0 否）')
    tiempm = mapped_column(TIMESTAMP(precision=6), comment='医生工作日：号源时段(年-月-日 时：分)')

class DoctorSubscribeinfo(Base):
    __tablename__ = 'doctor_subscribeinfo'
    __table_args__ = {'comment': '预约信息详情表'}

    id = mapped_column(Integer, primary_key=True, server_default=text("nextval('doctor_subscribeinfo_id_seq'::regclass)"), comment='主键Id')
    dno = mapped_column(Text, nullable=False, index=True, server_default=text("''::text"), comment='所属医生编号')
    orderid = mapped_column(Text, index=True, server_default=text("''::text"), comment='订单编号')
    nsindex = mapped_column(Text, server_default=text("''::text"), comment='订单编号')
    statue = mapped_column(Integer, server_default=text("1"), comment='订单状态（1:订单就绪，还没支付 2：已支付成功 3：取消订单')
    visitday = mapped_column(Text, server_default=text("''::text"), comment='就诊日期')
    visittime = mapped_column(Text, server_default=text("''::text"), comment='就诊时段')
    payfee = mapped_column(Text, server_default=text("''::text"), comment='支付诊费')
    visit_uopenid = mapped_column(Text, server_default=text("''::text"), comment='就诊人微信ID')
    visit_uname = mapped_column(Text, server_default=text("''::text"), comment='就诊人姓名')
    visit_uphone = mapped_column(Text, server_default=text("''::text"), comment='就诊人联系电话')
    visit_usex = mapped_column(Text, server_default=text("''::text"), comment='就诊人性别')
    visit_uage = mapped_column(Text, server_default=text("''::text"), comment='就诊人年龄')
    visit_statue = mapped_column(Integer, server_default=text("1"), comment='订单所属-就诊状态（1：待就诊 2：已就诊）')
    create_time = mapped_column(TIMESTAMP(precision=0), server_default=text("now()"), comment='创建时间')
    notify_callback_time = mapped_column(TIMESTAMP(precision=0), comment='支付回调时间')


class Doctorinfo(Base):
    __tablename__ = 'doctorinfo'
    __table_args__ = {'comment': '医生信息表'}

    id = mapped_column(Integer, primary_key=True, server_default=text("nextval('doctorinfo_id_seq'::regclass)"), comment='主键Id')
    dno = mapped_column(Text, nullable=False, unique=True, server_default=text("''::text"), comment='医生编号')
    dnname = mapped_column(Text, server_default=text("''::text"), comment='医生名称')
    dnmobile = mapped_column(Text, server_default=text("''::text"), comment='医生号码')
    sex = mapped_column(Integer, comment='医生性别：1： 男 2: 女 3：保密')
    enable = mapped_column(Integer, comment='是否可用（1：是 0 否）')
    rank = mapped_column(Text, server_default=text("''::text"), comment='职称')
    fee = mapped_column(Numeric, comment='医生诊费')
    grade = mapped_column(Text, server_default=text("''::text"), comment='等级')
    destag = mapped_column(Text, server_default=text("''::text"), comment='专业擅长标签')
    addr = mapped_column(Text, server_default=text("''::text"), comment='开诊地点')
    pic = mapped_column(Text, server_default=text("''::text"), comment='医生图片')
    create_time = mapped_column(TIMESTAMP(precision=0), server_default=text("now()"), comment='创建时间')
    describe = mapped_column(Text, comment='说明信息')

class Hospitalinfo(Base):
    __tablename__ = 'hospitalinfo'
    __table_args__ = {'comment': '医院信息表'}

    id = mapped_column(Integer, primary_key=True, server_default=text("nextval('hospitalinfo_id_seq'::regclass)"), comment='主键Id')
    name = mapped_column(Text, server_default=text("''::text"), comment='医院名称')
    describe = mapped_column(Text, server_default=text("''::text"), comment='医院描述')
    describeimages = mapped_column(Text, server_default=text("''::text"), comment='describeimages')
    create_time = mapped_column(TIMESTAMP(precision=0), server_default=text("now()"), comment='创建时间')



