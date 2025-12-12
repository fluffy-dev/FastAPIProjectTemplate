from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordService:
    """
    Utility service for cryptographic password operations.
    """

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verifies a plain-text password against a hashed password.

        Args:
            plain_password (str): The password provided by the user.
            hashed_password (str): The bcrypt hash stored in the database.

        Returns:
            bool: True if the password matches the hash, False otherwise.
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Generates a secure hash for a plain-text password using bcrypt.

        Args:
            password (str): The plain-text password.

        Returns:
            str: The resulting password hash.
        """
        return pwd_context.hash(password)
