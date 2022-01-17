# -*- codeing = utf-8 -*-
# @Time : 2021/6/17 21:41
# @Author : guanghao zhou
# @File : sql.py
# Software : PyCharm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import Integer, VARCHAR, DateTime, Text
from sqlalchemy import ForeignKey

BaseModel = declarative_base()


class Manager(BaseModel):
    __tablename__ = "manager"
    m_id = Column(Integer, primary_key=True)
    username = Column(VARCHAR(10))
    password = Column(VARCHAR(20))


class District(BaseModel):
    __tablename__ = "district"
    d_id = Column(Integer, primary_key=True)
    m_id = Column(Integer, ForeignKey('manager.m_id'))
    address = Column(Text)


class Record(BaseModel):
    __tablename__ = "record"
    time_r = Column(DateTime, primary_key=True)
    d_id = Column(Integer, ForeignKey('district.d_id'))
    cars_per_minute = Column(Integer)
    pedestrian_per_minute = Column(Integer)


class Sql:
    def __init__(self):
        DB_CONNECT = 'mysql+mysqldb://root:2209@localhost/traffic_flow?charset=utf8'
        self.engine = create_engine(DB_CONNECT)
        self.DB_Session = sessionmaker(bind=self.engine)
        self.session = self.DB_Session()

    def select_manager(self, username, password):
        """
        查询管理员，返回管理员对象
        :param username: 待查寻管理员账号
        :param password: 待查寻管理员密码
        :return: Manager -> 管理员数据表对象
        """
        return self.session.query(Manager).filter(Manager.username == username).first()

    def select_distinct(self, d_id):
        """
        返回d_id所属的地名
        :param d_id: 查询地名的d_id
        :return:string -> 查询到的地名
        """
        return self.session.query(District).filter(District.d_id == d_id).first().address

    def select_distinct_all(self):
        """
        返回地名表的d_id及所属地名
        :return: {int: string} -> 返回字典，key: d_id, value: 地名
        """
        distinct = self.session.query(District).all()
        dic = {}
        for dis in distinct:
            dic[dis.d_id] = dis.address
        return dic

    def select_record(self, d_id):
        """
        查询Record中d_id所有数据
        :param d_id: 待查寻的d_id
        :return: [[str1, str2, str3], ] -> str1: 当前记录的时间，str2: 车流辆, str3: 人流量
        """
        rQuery = self.session.query(Record).filter(Record.d_id == d_id).all()
        record = []
        for r in rQuery:
            unit = [r.time_r.strftime('%Y-%m-%d %H:%M:%S'), r.cars_per_minute, r.pedestrian_per_minute]
            record.append(unit)
        return record

    def find_len_district(self):
        """
        返回当前数据表有多少数据
        :return: size -> int, 数据条数
        """
        size = self.session.execute("select count(*) from district")
        return size.fetchone()[0]

    def add_record(self, time_r, d_id, cars_per_minute, pedestrian_per_minute):
        """
        对Record表添加数据
        :param time_r:
        :param d_id:
        :param cars_per_minute:
        :param pedestrian_per_minute:
        :return: None
        """
        record = Record(time_r=time_r, d_id=d_id, cars_per_minute=cars_per_minute, pedestrian_per_minute=pedestrian_per_minute)
        self.session.add(record)
        self.session.commit()

    def add_manager(self, username, password):
        """
        添加管理员
        :param username: 管理员名
        :param password: 管理员密码
        :return: None
        """
        manager = Manager(username=username, password=password)
        self.session.add(manager)
        self.session.commit()

    def update_manager(self, username, m_id):
        # mQuery.filter(Manager.m_id == 1).first().username = "张三"
        # mQuery.filter(Manager.username == "lisi", Manager.m_id > 5).update({Manager.username: 'jojo'})
        # self.session.commit()
        pass

    def delete_manager(self, manager):
        # mQuery.filter(Manager.username == "dio", Manager.m_id > 9).delete()
        # self.session.commit()
        pass

    def add_district(self, d_id, m_id, address):
        """
        添加摄像头
        :param d_id: 地区编号
        :param m_id: 管理员编号
        :param address: 地区
        :return: None
        """
        district = District(d_id=d_id, m_id=m_id, address=address)
        self.session.add(district)
        self.session.commit()
