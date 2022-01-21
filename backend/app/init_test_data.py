#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from email_validator import EmailNotValidError, validate_email
from faker import Faker


from backend.app.datebase.session import db_session
from backend.app.model import User
from backend.app.common.log import log
from backend.app.api.jwt_security import get_hash_password

db = db_session()


class InitData:
    """ 初始化数据 """

    def __init__(self):
        self.fake = Faker('zh_CN')

    @staticmethod
    def create_superuser_by_yourself():
        """ 手动创建管理员账户 """
        print('请输入用户名:')
        username = input()
        print('请输入密码:')
        password = input()
        print('请输入邮箱:')
        while True:
            email = input()
            try:
                success_email = validate_email(email)
            except EmailNotValidError:
                print('邮箱不符合规范，请重新输入：')
                continue
            new_email = success_email.email
            break
        user_obj = User(
            username=username,
            password=get_hash_password(password),
            email=new_email,
            is_superuser=True,
        )
        db.add(user_obj)
        db.commit()
        db.refresh(user_obj)
        print(f'管理员用户创建成功，账号：{username}，密码：{password}')

    def fake_user(self):
        """ 自动创建普通用户 """
        username = self.fake.user_name()
        password = self.fake.password()
        email = self.fake.email()
        user_obj = User(
            username=username,
            password=get_hash_password(password),
            email=email,
            is_superuser=False,
        )
        db.add(user_obj)
        db.commit()
        db.refresh(user_obj)
        log.info(f"普通用户创建成功，账号：{username}，密码：{password}")

    def fake_no_active_user(self):
        """ 自动创建锁定普通用户 """
        username = self.fake.user_name()
        password = self.fake.password()
        email = self.fake.email()
        user_obj = User(
            username=username,
            password=get_hash_password(password),
            email=email,
            is_active=False,
            is_superuser=False,
        )
        db.add(user_obj)
        db.commit()
        db.refresh(user_obj)
        log.info(f"普通锁定用户创建成功，账号：{username}，密码：{password}")

    def fake_superuser(self):
        """ 自动创建管理员用户 """
        username = self.fake.user_name()
        password = self.fake.password()
        email = self.fake.email()
        user_obj = User(
            username=username,
            password=get_hash_password(password),
            email=email,
            is_superuser=True,
        )
        db.add(user_obj)
        db.commit()
        db.refresh(user_obj)
        log.info(f"管理员用户创建成功，账号：{username}，密码：{password}")

    def fake_no_active_superuser(self):
        """ 自动创建锁定管理员用户 """
        username = self.fake.user_name()
        password = self.fake.password()
        email = self.fake.email()
        user_obj = User(
            username=username,
            password=get_hash_password(password),
            email=email,
            is_active=False,
            is_superuser=True,
        )
        db.add(user_obj)
        db.commit()
        db.refresh(user_obj)
        log.info(f"管理员锁定用户创建成功，账号：{username}，密码：{password}")

    def init_data(self):
        """ 自动创建数据 """
        log.info('----------------开始初始化数据----------------')
        self.create_superuser_by_yourself()
        self.fake_user()
        self.fake_no_active_user()
        self.fake_superuser()
        self.fake_no_active_superuser()
        log.info('----------------数据初始化完成----------------')


if __name__ == '__main__':
    init = InitData()
    init.init_data()
