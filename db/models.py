# coding: utf-8
from sqlalchemy import Column, Date, DateTime, Integer, SmallInteger, Text, UniqueConstraint, text,DECIMAL,Numeric, String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.mysql import TIMESTAMP
from decimal import Decimal
from uuid import uuid1
from datetime import datetime, date
from . import Base
metadata = Base.metadata


class DoctorScheduling(Base):
    __tablename__ = 'doctor_scheduling'
    __table_args__ = {'comment': '医生排班信息表'}

    id: Mapped[str] = mapped_column(Integer, primary_key=True, comment='主键Id', autoincrement=True)
    dno: Mapped[str] = mapped_column(Text, nullable=False, index=True, server_default=text("''::text"), comment='所属医生编号')
    nsnum: Mapped[int] = mapped_column(Integer, comment='号源总数')
    nsnumstock: Mapped[int] = mapped_column(Integer, comment='号源库存数')
    nsindex: Mapped[str] = mapped_column(Text, unique=True, server_default=text("''::text"), comment='号源编号')
    dnotime: Mapped[date] = mapped_column(Date, comment='排班日期，年-月-日')
    tiemampmstr: Mapped[str] = mapped_column(Text, server_default=text("''::text"), comment='号源时段字符串显示')
    ampm: Mapped[str] = mapped_column(Text, server_default=text("''::text"), comment='医生工作日：上午 还是 下午')
    create_time: Mapped[datetime] = mapped_column(TIMESTAMP(precision=0), server_default=text("now()"), comment='创建时间')
    enable: Mapped[int] = mapped_column(Integer, comment='是否可用（1：是 0 否）')
    tiempm: Mapped[datetime] = mapped_column(TIMESTAMP(precision=6), comment='医生工作日：号源时段(年-月-日 时：分)')

class DoctorSubscribeinfo(Base):
    __tablename__ = 'doctor_subscribeinfo'
    __table_args__ = {'comment': '预约信息详情表'}

    id: Mapped[datetime] = mapped_column(Integer, primary_key=True, comment='主键Id', autoincrement=True)
    dno: Mapped[datetime] = mapped_column(Text, nullable=False, index=True, server_default=text("''::text"), comment='所属医生编号')
    orderid: Mapped[datetime] = mapped_column(Text, index=True, server_default=text("''::text"), comment='订单编号')
    nsindex: Mapped[datetime] = mapped_column(Text, server_default=text("''::text"), comment='订单编号')
    statue: Mapped[datetime] = mapped_column(Integer, server_default=text("1"), comment='订单状态（1:订单就绪，还没支付 2：已支付成功 3：取消订单')
    visitday: Mapped[datetime] = mapped_column(Text, server_default=text("''::text"), comment='就诊日期')
    visittime: Mapped[datetime] = mapped_column(Text, server_default=text("''::text"), comment='就诊时段')
    payfee: Mapped[datetime] = mapped_column(Text, server_default=text("''::text"), comment='支付诊费')
    visit_uopenid: Mapped[datetime] = mapped_column(Text, server_default=text("''::text"), comment='就诊人微信ID')
    visit_uname: Mapped[datetime] = mapped_column(Text, server_default=text("''::text"), comment='就诊人姓名')
    visit_uphone: Mapped[datetime] = mapped_column(Text, server_default=text("''::text"), comment='就诊人联系电话')
    visit_usex: Mapped[datetime] = mapped_column(Text, server_default=text("''::text"), comment='就诊人性别')
    visit_uage: Mapped[datetime] = mapped_column(Text, server_default=text("''::text"), comment='就诊人年龄')
    visit_statue: Mapped[datetime] = mapped_column(Integer, server_default=text("1"), comment='订单所属-就诊状态（1：待就诊 2：已就诊）')
    create_time: Mapped[datetime] = mapped_column(TIMESTAMP(precision=0), server_default=text("now()"), comment='创建时间')
    notify_callback_time: Mapped[datetime] = mapped_column(TIMESTAMP(precision=0), comment='支付回调时间')


class Doctorinfo(Base):
    __tablename__ = 'doctorinfo'
    __table_args__ = {'comment': '医生信息表'}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment='主键Id', autoincrement=True)
    dno: Mapped[str] = mapped_column(Text, nullable=False, unique=True, server_default=text("''::text"), comment='医生编号')
    dnname: Mapped[str] = mapped_column(Text, server_default=text("''::text"), comment='医生名称')
    dnmobile: Mapped[str] = mapped_column(Text, server_default=text("''::text"), comment='医生号码')
    sex: Mapped[int] = mapped_column(Integer, comment='医生性别：1： 男 2: 女 3：保密')
    enable: Mapped[int] = mapped_column(Integer, comment='是否可用（1：是 0 否）')
    rank: Mapped[str] = mapped_column(Text, server_default=text("''::text"), comment='职称')
    fee: Mapped[Decimal] = mapped_column(Numeric, comment='医生诊费')
    grade: Mapped[str] = mapped_column(Text, server_default=text("''::text"), comment='等级')
    destag: Mapped[str] = mapped_column(Text, server_default=text("''::text"), comment='专业擅长标签')
    addr: Mapped[str] = mapped_column(Text, server_default=text("''::text"), comment='开诊地点')
    pic: Mapped[str] = mapped_column(Text, server_default=text("''::text"), comment='医生图片')
    create_time: Mapped[datetime] = mapped_column(TIMESTAMP(precision=0), server_default=text("now()"), comment='创建时间')
    describe: Mapped[str] = mapped_column(Text, comment='说明信息')

class Hospitalinfo(Base):
    __tablename__ = 'hospitalinfo'
    __table_args__ = {'comment': '医院信息表'}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment='主键Id', autoincrement=True)
    name: Mapped[str] = mapped_column(Text, server_default=text("''::text"), comment='医院名称')
    describe: Mapped[str] = mapped_column(Text, server_default=text("''::text"), comment='医院描述')
    describeimages: Mapped[str] = mapped_column(Text, server_default=text("''::text"), comment='describeimages')
    create_time: Mapped[datetime] = mapped_column(TIMESTAMP(precision=0), server_default=text("now()"), comment='创建时间')



