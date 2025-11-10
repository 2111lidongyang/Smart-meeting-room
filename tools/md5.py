import hashlib


def pass_md5(password):
    """
    # 对用户密码进行md5加密
    :param password: 加密前的密码
    :return: 加密后的密码
    """
    h = hashlib.md5()
    h.update(password.encode())
    new_password = h.hexdigest()
    return new_password
