#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.app.api import jwt_security
from backend.app.model import User
from backend.app.schemas.sm_user import CreateUser, DeleteUser, ResetPassword


def get_user_by_id(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> User:
    return db.query(User).filter(User.username == username).first()


def update_user_login_time(db: Session, username: str):
    db.query(User).filter(User.username == username).update({'last_login': func.now()})
    db.commit()


def get_email_by_username(db: Session, username: str) -> str:
    current = db.query(User).filter(User.username == username).first()
    return current.email


def get_username_by_email(db: Session, email: str) -> str:
    return db.query(User).filter(User.email == email).first().username


def get_avatar_by_username(db: Session, username: str) -> str:
    return db.query(User).filter(User.username == username).first().avatar


def create_user(db: Session, create: CreateUser) -> User:
    create.password = jwt_security.get_hash_password(create.password)
    new_user = User(**create.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update_userinfo(db: Session,
                    current_user: User,
                    username: str,
                    email: str,
                    avatar: Optional[str],
                    mobile_number: Optional[int],
                    we_chart: Optional[str],
                    qq: Optional[str],
                    blog_address: Optional[str],
                    introduction: Optional[str]) -> bool:
    userinfo = db.query(User).filter(User.username == current_user.username)
    userinfo.update({
        'username': username,
        'email': email,
        'avatar': avatar,
        'mobile_number': mobile_number,
        'we_chart': we_chart,
        'qq': qq,
        'blog_address': blog_address,
        'introduction': introduction,
    })
    db.commit()
    return userinfo.first()


def delete_user(db: Session, user_id: DeleteUser) -> bool:
    user = db.query(User).filter(User.id == user_id)
    user.delete()
    db.commit()
    return user.first()


def check_email(db: Session, email: str) -> bool:
    return db.query(User).filter(User.email == email).first()


def reset_password(db: Session, username: str, password: str) -> bool:
    current_user = db.query(User).filter(User.username == username)
    current_user.update({'password': jwt_security.get_hash_password(password)})
    db.commit()
    return current_user.first()


def get_users(db: Session) -> list:
    return db.query(User).order_by(User.time_joined.desc()).all()


def get_user_is_super(db: Session, user_id: int) -> bool:
    return db.query(User).filter(User.id == user_id).first().is_superuser


def get_user_is_action(db: Session, user_id: int) -> bool:
    return db.query(User).filter(User.id == user_id).first().is_active


def super_set(db: Session, user_id: int, no_super: bool = False, is_super: bool = True) -> bool:
    user = db.query(User).filter(User.id == user_id)
    super_status = user.first().is_superuser
    if super_status:
        user.update({'is_superuser': no_super})
        db.commit()
        return super_status
    if not super_status:
        user.update({'is_superuser': is_super})
        db.commit()
        return super_status


def active_set(db: Session, user_id: int, no_action: bool = False, is_action: bool = True) -> bool:
    user = db.query(User).filter(User.id == user_id)
    active_status = user.first().is_active
    if active_status:
        user.update({'is_active': no_action})
        db.commit()
        return active_status
    if not active_status:
        user.update({'is_active': is_action})
        db.commit()
        return active_status
