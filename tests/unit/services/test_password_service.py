from src.auth.service.password import PasswordService


def test_hashing_consistency():
    """Verify verification works on hashed passwords."""
    password = "super_secret"
    hashed = PasswordService.get_password_hash(password)

    assert hashed != password
    assert PasswordService.verify_password(password, hashed) is True
    assert PasswordService.verify_password("wrong_password", hashed) is False


def test_hashing_randomness():
    """
    Verify that hashing the same password twice results in different strings
    (due to salting).
    """
    pwd = "test"
    hash1 = PasswordService.get_password_hash(pwd)
    hash2 = PasswordService.get_password_hash(pwd)

    assert hash1 != hash2